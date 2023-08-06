from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender
from lementpro.data.folderjoinbyattributemodel import FolderJoinByAttributeModel
from lementpro.data.folderaddobjectstatefilter import FolderAddObjectStateFilter
from lementpro.data.folderpatchobjectstatusfilter import FolderPatchObjectStatusFilter
from lementpro.data.folderpatchobjectuserfilter import FolderPatchObjectUserFilter
from lementpro.data.folderorderbyattributemodel import FolderOrderByAttributeModel
from lementpro.data.folderaddobjectuserfilter import FolderAddObjectUserFilter
from lementpro.data.folderpatchobjectstatefilter import FolderPatchObjectStateFilter
from lementpro.data.folderaddobjectstatusfilter import FolderAddObjectStatusFilter
from lementpro.data.folderpatchreset import FolderPatchReset


class Folder:
    """Service for working with Folder in UserGate Public API"""  
    def post_folders(self, by_user: User, name: str=None, description: str=None, parentId: int=None, menuObjectTypeId: int=None, exportTemplateFileId: int=None, isAbstract: bool=None, objectTypes: list=None, objectStatus: FolderAddObjectStatusFilter=None, objectState: FolderAddObjectStateFilter=None, objectUser: FolderAddObjectUserFilter=None, orderByAttribute: FolderOrderByAttributeModel=None, joinByAttribute: FolderJoinByAttributeModel=None, groupByAttributes: list=None, filterByAttributes: list=None, viewTypeId: str=None, countObjects: bool=None):
        """Create new folder.
        :return: Created folder identifier
        """
        request_data = Build(url="/api/folders").post(name=name,description=description,parentId=parentId,menuObjectTypeId=menuObjectTypeId,exportTemplateFileId=exportTemplateFileId,isAbstract=isAbstract,objectTypes=objectTypes,objectStatus=objectStatus,objectState=objectState,objectUser=objectUser,orderByAttribute=orderByAttribute,joinByAttribute=joinByAttribute,groupByAttributes=groupByAttributes,filterByAttributes=filterByAttributes,viewTypeId=viewTypeId,countObjects=countObjects,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_folders(self, by_user: User, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, SearchString: str=None, SearchStringExact: bool=None, MenuObjectTypeId: int=None, IsSystem: bool=None, IsTemplate: bool=None, GroupId: int=None):
        """Get folders.
        :return: Object type paging info
        """
        request_data = Build(url="/api/folders").get(By=By,Page=Page,Order=Order,OrderBy=OrderBy,SearchString=SearchString,SearchStringExact=SearchStringExact,MenuObjectTypeId=MenuObjectTypeId,IsSystem=IsSystem,IsTemplate=IsTemplate,GroupId=GroupId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_folderId(self, by_user: User, name: str=None, description: str=None, objectTypes: list=None, exportTemplateFileId: int=None, objectStatus: FolderPatchObjectStatusFilter=None, objectState: FolderPatchObjectStateFilter=None, objectUser: FolderPatchObjectUserFilter=None, orderByAttribute: FolderOrderByAttributeModel=None, joinByAttribute: FolderJoinByAttributeModel=None, groupByAttributes: list=None, filterByAttributes: list=None, isAbstract: bool=None, reset: FolderPatchReset=None, viewTypeId: str=None, countObjects: bool=None):
        """Partial update user's folder by id.
        :return: Empty
        """
        request_data = Build(url="/api/folders/{folderId}").patch(name=name,description=description,objectTypes=objectTypes,exportTemplateFileId=exportTemplateFileId,objectStatus=objectStatus,objectState=objectState,objectUser=objectUser,orderByAttribute=orderByAttribute,joinByAttribute=joinByAttribute,groupByAttributes=groupByAttributes,filterByAttributes=filterByAttributes,isAbstract=isAbstract,reset=reset,viewTypeId=viewTypeId,countObjects=countObjects,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_folderId(self, by_user: User, folderId: int=None):
        """Get user's folder detailed info by id.
        :return: Object type info
        """
        request_data = Build(url="/api/folders/{folderId}").get(folderId=folderId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_folderId(self, by_user: User):
        """Delete folder by id.
        :return: No content
        """
        request_data = Build(url="/api/folders/{folderId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def tree(self, by_user: User, MenuObjectTypeId: int=None, CountObjects: bool=None):
        """Get folders tree.
        :return: User folders tree
        """
        request_data = Build(url="/api/folders/tree").get(MenuObjectTypeId=MenuObjectTypeId,CountObjects=CountObjects,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def virtual_subfolders(self, by_user: User, folderId: int=None, Path: list=None, TimeZone: str=None):
        """Get virtual folders.
        :return: Virtual subtree of user folder
        """
        request_data = Build(url="/api/folders/{folderId}/virtual_subfolders").get(folderId=folderId,Path=Path,TimeZone=TimeZone,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def objects(self, by_user: User, folderId: int=None, By: int=None, Page: int=None, Path: list=None, TimeZone: str=None, SearchPhrase: str=None):
        """Get folder objects.
        :return: Folder objects paging info
        """
        request_data = Build(url="/api/folders/{folderId}/objects").get(folderId=folderId,By=By,Page=Page,Path=Path,TimeZone=TimeZone,SearchPhrase=SearchPhrase,)
        return Sender().send_request(request_data, by_user=by_user)
        