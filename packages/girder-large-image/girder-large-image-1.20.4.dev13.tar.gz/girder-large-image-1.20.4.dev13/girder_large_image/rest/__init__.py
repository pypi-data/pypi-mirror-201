import json

import yaml

from girder import logger
from girder.api import access
from girder.api.describe import Description, autoDescribeRoute
from girder.api.rest import boundHandler
from girder.constants import AccessType, SortDir, TokenScope
from girder.models.file import File
from girder.models.folder import Folder
from girder.models.group import Group
from girder.models.item import Item
from girder.models.setting import Setting

from .. import constants


def addSystemEndpoints(apiRoot):
    """
    This adds endpoints to routes that already exist in Girder.

    :param apiRoot: Girder api root class.
    """
    apiRoot.folder.route('GET', (':id', 'yaml_config', ':name'), getYAMLConfigFile)

    origItemFind = apiRoot.item._find
    origFolderFind = apiRoot.folder._find

    @boundHandler(apiRoot.item)
    def altItemFind(self, folderId, text, name, limit, offset, sort, filters=None):
        if sort and sort[0][0][0] == '[':
            sort = json.loads(sort[0][0])
        recurse = False
        if text and text.startswith('_recurse_:'):
            recurse = True
            text = text.split('_recurse_:', 1)[1]
        if filters is None and text and text.startswith('_filter_:'):
            try:
                filters = json.loads(text.split('_filter_:', 1)[1].strip())
                text = None
            except Exception as exc:
                logger.warning('Failed to parse _filter_ from text field: %r', exc)
        if recurse:
            return _itemFindRecursive(
                self, origItemFind, folderId, text, name, limit, offset, sort, filters)
        return origItemFind(folderId, text, name, limit, offset, sort, filters)

    @boundHandler(apiRoot.item)
    def altFolderFind(self, parentType, parentId, text, name, limit, offset, sort, filters=None):
        if sort and sort[0][0][0] == '[':
            sort = json.loads(sort[0][0])
        return origFolderFind(parentType, parentId, text, name, limit, offset, sort, filters)

    if not hasattr(origItemFind, '_origFunc'):
        apiRoot.item._find = altItemFind
        altItemFind._origFunc = origItemFind
        apiRoot.folder._find = altFolderFind
        altFolderFind._origFunc = origFolderFind


def _itemFindRecursive(self, origItemFind, folderId, text, name, limit, offset, sort, filters):
    """
    If a recursive search within a folderId is specified, use an aggregation to
    find all folders that are descendants of the specified folder.  If there
    are any, then perform a search that matches any of those folders rather
    than just the parent.

    :param self: A reference to the Item() resource record.
    :param origItemFind: the original _find method, used as a fallback.

    For the remaining parameters, see girder/api/v1/item._find
    """
    from bson.objectid import ObjectId

    if folderId:
        pipeline = [
            {'$match': {'_id': ObjectId(folderId)}},
            {'$graphLookup': {
                'from': 'folder',
                'connectFromField': '_id',
                'connectToField': 'parentId',
                'depthField': '_depth',
                'as': '_folder',
                'startWith': '$_id'
            }},
            {'$group': {'_id': '$_folder._id'}}
        ]
        children = [ObjectId(folderId)] + next(Folder().collection.aggregate(pipeline))['_id']
        if len(children) > 1:
            filters = (filters.copy() if filters else {})
            if text:
                filters['$text'] = {
                    '$search': text
                }
            if name:
                filters['name'] = name
            filters['folderId'] = {'$in': children}
            user = self.getCurrentUser()
            if isinstance(sort, list):
                sort.append(('parentId', 1))
            return Item().findWithPermissions(filters, offset, limit, sort=sort, user=user)
    return origItemFind(folderId, text, name, limit, offset, sort, filters)


def _mergeDictionaries(a, b):
    """
    Merge two dictionaries recursively.  If the second dictionary (or any
    sub-dictionary) has a special key, value of '__all__': True, the updated
    dictionary only contains values from the second dictionary and excludes
    the __all__ key.

    :param a: the first dictionary.  Modified.
    :param b: the second dictionary that gets added to the first.
    :returns: the modified first dictionary.
    """
    if b.get('__all__') is True:
        a.clear()
    for key in b:
        if isinstance(a.get(key), dict) and isinstance(b[key], dict):
            _mergeDictionaries(a[key], b[key])
        elif key != '__all__' or b[key] is not True:
            a[key] = b[key]
    return a


def adjustConfigForUser(config, user):
    """
    Given the current user, adjust the config so that only relevant and
    combined values are used.  If the root of the config dictionary contains
    "access": {"user": <dict>, "admin": <dict>}, the base values are updated
    based on the user's access level.  If the root of the config contains
    "group": {<group-name>: <dict>, ...}, the base values are updated for
    every group the user is a part of.

    The order of update is groups in C-sort alphabetical order followed by
    access/user and then access/admin as they apply.

    :param config: a config dictionary.
    """
    if not isinstance(config, dict):
        return config
    if isinstance(config.get('groups'), dict):
        groups = config.pop('groups')
        if user:
            for group in Group().find(
                    {'_id': {'$in': user['groups']}}, sort=[('name', SortDir.ASCENDING)]):
                if isinstance(groups.get(group['name']), dict):
                    config = _mergeDictionaries(config, groups[group['name']])
    if isinstance(config.get('access'), dict):
        accessList = config.pop('access')
        if user and isinstance(accessList.get('user'), dict):
            config = _mergeDictionaries(config, accessList['user'])
        if user and user.get('admin') and isinstance(accessList.get('admin'), dict):
            config = _mergeDictionaries(config, accessList['admin'])
    return config


@access.public(scope=TokenScope.DATA_READ)
@autoDescribeRoute(
    Description('Get a config file.')
    .notes(
        'This walks up the chain of parent folders until the file is found.  '
        'If not found, the .config folder in the parent collection or user is '
        'checked.\n\nAny yaml file can be returned.  If the top-level is a '
        'dictionary and contains keys "access" or "groups" where those are '
        'dictionaries, the returned value will be modified based on the '
        'current user.  The "groups" dictionary contains keys that are group '
        'names and values that update the main dictionary.  All groups that '
        'the user is a member of are merged in alphabetical order.  If a key '
        'and value of "\\__all\\__": True exists, the replacement is total; '
        'otherwise it is a merge.  If the "access" dictionary exists, the '
        '"user" and "admin" subdictionaries are merged if a calling user is '
        'present and if the user is an admin, respectively (both get merged '
        'for admins).')
    .modelParam('id', model=Folder, level=AccessType.READ)
    .param('name', 'The name of the file.', paramType='path')
    .errorResponse()
)
@boundHandler()
def getYAMLConfigFile(self, folder, name):
    addConfig = None
    user = self.getCurrentUser()
    last = False
    while folder:
        item = Item().findOne({'folderId': folder['_id'], 'name': name})
        if item:
            for file in Item().childFiles(item):
                if file['size'] > 10 * 1024 ** 2:
                    logger.info('Not loading %s -- too large' % file['name'])
                    continue
                with File().open(file) as fptr:
                    config = yaml.safe_load(fptr)
                    if isinstance(config, list) and len(config) == 1:
                        config = config[0]
                    # combine and adjust config values based on current user
                    if isinstance(config, dict) and 'access' in config or 'group' in config:
                        config = adjustConfigForUser(config, user)
                    if addConfig and isinstance(config, dict):
                        config = _mergeDictionaries(config, addConfig)
                    if not isinstance(config, dict) or config.get('__inherit__') is not True:
                        return config
                    config.pop('__inherit__')
                    addConfig = config
        if last:
            break
        if folder['parentCollection'] != 'folder':
            if folder['name'] != '.config':
                folder = Folder().findOne({
                    'parentId': folder['parentId'],
                    'parentCollection': folder['parentCollection'],
                    'name': '.config'})
            else:
                last = 'setting'
            if not folder or last == 'setting':
                folderId = Setting().get(constants.PluginSettings.LARGE_IMAGE_CONFIG_FOLDER)
                if not folderId:
                    break
                folder = Folder().load(folderId, force=True)
                last = True
        else:
            folder = Folder().load(folder['parentId'], user=user, level=AccessType.READ)
    return addConfig
