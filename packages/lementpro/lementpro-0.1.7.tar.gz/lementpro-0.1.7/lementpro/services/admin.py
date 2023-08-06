from lementpro.builders import Build
from lementpro.data.user import User
from lementpro.sender import Sender
from lementpro.data.folderjoinbyattributemodel import FolderJoinByAttributeModel
from lementpro.data.folderpatchobjectuserfilter import FolderPatchObjectUserFilter
from lementpro.data.objecttypeattributeaddsettingsmodel import ObjectTypeAttributeAddSettingsModel
from lementpro.data.folderaddobjectuserfilter import FolderAddObjectUserFilter
from lementpro.data.folderaddobjectstatusfilter import FolderAddObjectStatusFilter
from lementpro.data.companycontactdetailspatchmodel import CompanyContactDetailsPatchModel
from lementpro.data.companypasswordpolicypatchmodel import CompanyPasswordPolicyPatchModel
from lementpro.data.objecttypeaddextensionmodel import ObjectTypeAddExtensionModel
from lementpro.data.usermodelextension import UserModelExtension
from lementpro.data.folderpatchreset import FolderPatchReset
from lementpro.data.objecttypeattributepatchformulamodel import ObjectTypeAttributePatchFormulaModel
from lementpro.data.usermodelnotification import UserModelNotification
from lementpro.data.folderpatchobjectstatusfilter import FolderPatchObjectStatusFilter
from lementpro.data.objecttypepatchcountermodel import ObjectTypePatchCounterModel
from lementpro.data.objecttypeaddcountermodel import ObjectTypeAddCounterModel
from lementpro.data.groupobjectexpirationpatchmodel import GroupObjectExpirationPatchModel
from lementpro.data.objecttypeattributepatchsettingsmodel import ObjectTypeAttributePatchSettingsModel
from lementpro.data.folderaddobjectstatefilter import FolderAddObjectStateFilter
from lementpro.data.objecttypeattributeaddformulamodel import ObjectTypeAttributeAddFormulaModel
from lementpro.data.objecttypepatchextensionmodel import ObjectTypePatchExtensionModel
from lementpro.data.folderorderbyattributemodel import FolderOrderByAttributeModel
from lementpro.data.folderpatchobjectstatefilter import FolderPatchObjectStateFilter
from lementpro.data.companyextensionmodel import CompanyExtensionModel
from lementpro.data.attributepatchrelationmodel import AttributePatchRelationModel
from lementpro.data.attributeaddrelationmodel import AttributeAddRelationModel


class Admin:
    """Service for working with Admin in UserGate Public API"""  
    def post_attributes(self, by_user: User, name: str=None, description: str=None, knownId: str=None, units: str=None, attributeTypeId: str=None, valueTypeId: str=None, isFilterable: bool=None, isGroupable: bool=None, valueListId: int=None, relation: AttributeAddRelationModel=None, precision: int=None, widthInChars: int=None, notifyAboutChanges: bool=None):
        """Create new attribute.
        :return: Created attribute identifier
        """
        request_data = Build(url="/api/admin/attributes").post(name=name,description=description,knownId=knownId,units=units,attributeTypeId=attributeTypeId,valueTypeId=valueTypeId,isFilterable=isFilterable,isGroupable=isGroupable,valueListId=valueListId,relation=relation,precision=precision,widthInChars=widthInChars,notifyAboutChanges=notifyAboutChanges,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_attributes(self, by_user: User, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, Ids: list=None, KnownIds: list=None, SearchString: str=None, SearchStringExact: bool=None, AttributeTypeId: str=None, ValueTypeId: str=None, ValueListId: int=None, RelationTypeId: str=None, RelatedTypeId: str=None, NotifyAboutExpiration: bool=None, NotifyAboutChanges: bool=None, IsFilterable: bool=None, IsGroupable: bool=None, IsGroupableOrFilterable: bool=None):
        """Get attributes.
        :return: Object type paging info
        """
        request_data = Build(url="/api/admin/attributes").get(By=By,Page=Page,Order=Order,OrderBy=OrderBy,Ids=Ids,KnownIds=KnownIds,SearchString=SearchString,SearchStringExact=SearchStringExact,AttributeTypeId=AttributeTypeId,ValueTypeId=ValueTypeId,ValueListId=ValueListId,RelationTypeId=RelationTypeId,RelatedTypeId=RelatedTypeId,NotifyAboutExpiration=NotifyAboutExpiration,NotifyAboutChanges=NotifyAboutChanges,IsFilterable=IsFilterable,IsGroupable=IsGroupable,IsGroupableOrFilterable=IsGroupableOrFilterable,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_attributeId(self, by_user: User, name: str=None, description: str=None, units: str=None, attributeTypeId: str=None, valueTypeId: str=None, isFilterable: bool=None, isGroupable: bool=None, valueListId: int=None, relation: AttributePatchRelationModel=None, precision: int=None, widthInChars: int=None, notifyAboutChanges: bool=None):
        """Partial update attribute by id.
        :return: Empty
        """
        request_data = Build(url="/api/admin/attributes/{attributeId}").patch(name=name,description=description,units=units,attributeTypeId=attributeTypeId,valueTypeId=valueTypeId,isFilterable=isFilterable,isGroupable=isGroupable,valueListId=valueListId,relation=relation,precision=precision,widthInChars=widthInChars,notifyAboutChanges=notifyAboutChanges,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_attributeId(self, by_user: User, attributeId: int=None):
        """Get attribute detailed info by id.
        :return: Object type info
        """
        request_data = Build(url="/api/admin/attributes/{attributeId}").get(attributeId=attributeId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_attributeId(self, by_user: User):
        """Delete attribute by id.
        :return: No content
        """
        request_data = Build(url="/api/admin/attributes/{attributeId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def object_types_tree(self, by_user: User, attributeId: int=None):
        """Get object-types tree linked to attribute.
        :return: Object-types tree
        """
        request_data = Build(url="/api/admin/attributes/{attributeId}/object_types_tree").get(attributeId=attributeId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def categories(self, by_user: User, name: str=None, knownId: str=None, hasComments: bool=None, menuIsVisible: bool=None, menuUrl: str=None, menuIconClass: str=None, menuPosition: int=None):
        """Create new category.
        :return: Created category identifier
        """
        request_data = Build(url="/api/admin/categories").post(name=name,knownId=knownId,hasComments=hasComments,menuIsVisible=menuIsVisible,menuUrl=menuUrl,menuIconClass=menuIconClass,menuPosition=menuPosition,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_categoryId(self, by_user: User, name: str=None, knownId: str=None, hasComments: bool=None, menuIsVisible: bool=None, menuUrl: str=None, menuIconClass: str=None, menuPosition: int=None):
        """Partial update object type by id.
        :return: Empty
        """
        request_data = Build(url="/api/admin/categories/{categoryId}").patch(name=name,knownId=knownId,hasComments=hasComments,menuIsVisible=menuIsVisible,menuUrl=menuUrl,menuIconClass=menuIconClass,menuPosition=menuPosition,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_categoryId(self, by_user: User):
        """Delete category by id.
        :return: No content
        """
        request_data = Build(url="/api/admin/categories/{categoryId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_companies(self, by_user: User):
        """Get company detailed info.
        :return: Company info
        """
        request_data = Build(url="/api/admin/companies").get()
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_companies(self, by_user: User, name: str=None, description: str=None, maxUploadFileSize: int=None, isReadOnly: bool=None, isDisabled: bool=None, isSchemaReadonly: bool=None, timeZone: str=None, contactDetails: CompanyContactDetailsPatchModel=None, passwordPolicy: CompanyPasswordPolicyPatchModel=None, extension: CompanyExtensionModel=None):
        """Modify company, partially
        :return: No Content
        """
        request_data = Build(url="/api/admin/companies").patch(name=name,description=description,maxUploadFileSize=maxUploadFileSize,isReadOnly=isReadOnly,isDisabled=isDisabled,isSchemaReadonly=isSchemaReadonly,timeZone=timeZone,contactDetails=contactDetails,passwordPolicy=passwordPolicy,extension=extension,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_mailbox(self, by_user: User, login: str=None, password: str=None, smtpHost: str=None, smtpPort: int=None, imapHost: str=None, imapPort: int=None, isDisabled: bool=None):
        """Add company mailbox
        :return: Created company mailbox identifier
        """
        request_data = Build(url="/api/admin/companies/mailbox").post(login=login,password=password,smtpHost=smtpHost,smtpPort=smtpPort,imapHost=imapHost,imapPort=imapPort,isDisabled=isDisabled,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_mailbox(self, by_user: User, login: str=None, password: str=None, smtpHost: str=None, smtpPort: int=None, imapHost: str=None, imapPort: int=None, isDisabled: bool=None):
        """Partial update company mailbox
        :return: Empty
        """
        request_data = Build(url="/api/admin/companies/mailbox").patch(login=login,password=password,smtpHost=smtpHost,smtpPort=smtpPort,imapHost=imapHost,imapPort=imapPort,isDisabled=isDisabled,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_mailbox(self, by_user: User):
        """Get company mailbox
        :return: Mailbox integration info
        """
        request_data = Build(url="/api/admin/companies/mailbox").get()
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_mailbox(self, by_user: User):
        """Delete company mailbox
        :return: No content
        """
        request_data = Build(url="/api/admin/companies/mailbox").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_departments(self, by_user: User, parentId: int=None, name: str=None, description: str=None, code: str=None, isHidden: bool=None, bossUserId: int=None):
        """Create new department.
        :return: Created department identifier
        """
        request_data = Build(url="/api/admin/departments").post(parentId=parentId,name=name,description=description,code=code,isHidden=isHidden,bossUserId=bossUserId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_departments(self, by_user: User, DateCreatedFrom: str=None, DateCreatedTo: str=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, IsSystem: bool=None, NameExact: bool=None, Name: str=None, ParentId: int=None, IsHidden: bool=None, DepartmentIds: list=None):
        """Get departments
        :return: Department paging info
        """
        request_data = Build(url="/api/admin/departments").get(DateCreatedFrom=DateCreatedFrom,DateCreatedTo=DateCreatedTo,By=By,Page=Page,Order=Order,OrderBy=OrderBy,IsSystem=IsSystem,NameExact=NameExact,Name=Name,ParentId=ParentId,IsHidden=IsHidden,DepartmentIds=DepartmentIds,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def put_departmentId(self, by_user: User, parentId: int=None, name: str=None, description: str=None, code: str=None, sortWeight: int=None, isHidden: bool=None, bossUserId: int=None):
        """Update Department by id.
        :return: Empty
        """
        request_data = Build(url="/api/admin/departments/{departmentId}").put(parentId=parentId,name=name,description=description,code=code,sortWeight=sortWeight,isHidden=isHidden,bossUserId=bossUserId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_departmentId(self, by_user: User, departmentId: int=None):
        """Get department detailed info by id.
        :return: Created department info
        """
        request_data = Build(url="/api/admin/departments/{departmentId}").get(departmentId=departmentId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_departmentId(self, by_user: User):
        """Delete department by id.
        :return: No content
        """
        request_data = Build(url="/api/admin/departments/{departmentId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def put_boss(self, by_user: User, userId: int=None):
        """Set department boss.
        :return: Empty
        """
        request_data = Build(url="/api/admin/departments/{departmentId}/boss").put(userId=userId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_boss(self, by_user: User):
        """Delete department boss.
        :return: Empty
        """
        request_data = Build(url="/api/admin/departments/{departmentId}/boss").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def tree(self, by_user: User, departmentId: int=None):
        """Get departments tree.
        :return: Created department info
        """
        request_data = Build(url="/api/admin/departments/{departmentId}/tree").get(departmentId=departmentId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def tree(self, by_user: User):
        """Get departments tree.
        :return: Created department info
        """
        request_data = Build(url="/api/admin/departments/tree").get()
        return Sender().send_request(request_data, by_user=by_user)
          
    def users(self, by_user: User, userId: int=None):
        """Move user to department.
        :return: Empty
        """
        request_data = Build(url="/api/admin/departments/{departmentId}/users").post(userId=userId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def userId(self, by_user: User):
        """Delete user from department.
        :return: Empty
        """
        request_data = Build(url="/api/admin/departments/{departmentId}/users/{userId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def files(self, by_user: User, StorageTypes: list=None, IsTemp: bool=None, IsFinal: bool=None, UserId: int=None, UserIdFrom: int=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, FileIds: list=None, FileGroupId: int=None, SearchString: str=None, SearchStringExact: bool=None):
        """Get files info by filter
        :return: File stream content
        """
        request_data = Build(url="/api/admin/files").get(StorageTypes=StorageTypes,IsTemp=IsTemp,IsFinal=IsFinal,UserId=UserId,UserIdFrom=UserIdFrom,By=By,Page=Page,Order=Order,OrderBy=OrderBy,FileIds=FileIds,FileGroupId=FileGroupId,SearchString=SearchString,SearchStringExact=SearchStringExact,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_folder_templates(self, by_user: User, name: str=None, description: str=None, parentId: int=None, menuObjectTypeId: int=None, exportTemplateFileId: int=None, isAbstract: bool=None, objectTypes: list=None, objectStatus: FolderAddObjectStatusFilter=None, objectState: FolderAddObjectStateFilter=None, objectUser: FolderAddObjectUserFilter=None, orderByAttribute: FolderOrderByAttributeModel=None, joinByAttribute: FolderJoinByAttributeModel=None, groupByAttributes: list=None, filterByAttributes: list=None, userGroups: list=None):
        """Create new folder template.
        :return: Created folder identifier
        """
        request_data = Build(url="/api/admin/folder_templates").post(name=name,description=description,parentId=parentId,menuObjectTypeId=menuObjectTypeId,exportTemplateFileId=exportTemplateFileId,isAbstract=isAbstract,objectTypes=objectTypes,objectStatus=objectStatus,objectState=objectState,objectUser=objectUser,orderByAttribute=orderByAttribute,joinByAttribute=joinByAttribute,groupByAttributes=groupByAttributes,filterByAttributes=filterByAttributes,userGroups=userGroups,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_folder_templates(self, by_user: User, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, SearchString: str=None, SearchStringExact: bool=None, MenuObjectTypeId: int=None, IsSystem: bool=None, GroupId: int=None):
        """Get folders templates.
        :return: Object type paging info
        """
        request_data = Build(url="/api/admin/folder_templates").get(By=By,Page=Page,Order=Order,OrderBy=OrderBy,SearchString=SearchString,SearchStringExact=SearchStringExact,MenuObjectTypeId=MenuObjectTypeId,IsSystem=IsSystem,GroupId=GroupId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_folderId(self, by_user: User, name: str=None, description: str=None, objectTypes: list=None, exportTemplateFileId: int=None, objectStatus: FolderPatchObjectStatusFilter=None, objectState: FolderPatchObjectStateFilter=None, objectUser: FolderPatchObjectUserFilter=None, orderByAttribute: FolderOrderByAttributeModel=None, joinByAttribute: FolderJoinByAttributeModel=None, groupByAttributes: list=None, filterByAttributes: list=None, isAbstract: bool=None, reset: FolderPatchReset=None, userGroups: list=None):
        """Partial update folder template by id.
        :return: Empty
        """
        request_data = Build(url="/api/admin/folder_templates/{folderId}").patch(name=name,description=description,objectTypes=objectTypes,exportTemplateFileId=exportTemplateFileId,objectStatus=objectStatus,objectState=objectState,objectUser=objectUser,orderByAttribute=orderByAttribute,joinByAttribute=joinByAttribute,groupByAttributes=groupByAttributes,filterByAttributes=filterByAttributes,isAbstract=isAbstract,reset=reset,userGroups=userGroups,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_folderId(self, by_user: User, folderId: int=None):
        """Get folder template detailed info by id.
        :return: Object type info
        """
        request_data = Build(url="/api/admin/folder_templates/{folderId}").get(folderId=folderId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_folderId(self, by_user: User):
        """Delete folder template by id.
        :return: No content
        """
        request_data = Build(url="/api/admin/folder_templates/{folderId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def tree(self, by_user: User, GroupId: int=None):
        """Get folder templates tree.
        :return: Object type paging info
        """
        request_data = Build(url="/api/admin/folder_templates/tree").get(GroupId=GroupId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_groups(self, by_user: User, name: str=None, description: str=None, avatarFileId: int=None):
        """Create new group.
        :return: Created group identifier
        """
        request_data = Build(url="/api/admin/groups").post(name=name,description=description,avatarFileId=avatarFileId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_groups(self, by_user: User, DateCreatedFrom: str=None, DateCreatedTo: str=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, IsSystem: bool=None, Name: str=None, NameExact: bool=None):
        """Get groups
        :return: Group paging info
        """
        request_data = Build(url="/api/admin/groups").get(DateCreatedFrom=DateCreatedFrom,DateCreatedTo=DateCreatedTo,By=By,Page=Page,Order=Order,OrderBy=OrderBy,IsSystem=IsSystem,Name=Name,NameExact=NameExact,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def put_groupId(self, by_user: User, name: str=None, description: str=None, avatarFileId: int=None, objectExpiration: GroupObjectExpirationPatchModel=None):
        """Update Group by id.
        :return: Empty
        """
        request_data = Build(url="/api/admin/groups/{groupId}").put(name=name,description=description,avatarFileId=avatarFileId,objectExpiration=objectExpiration,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_groupId(self, by_user: User, groupId: int=None):
        """Get group detailed info by id.
        :return: Created group info
        """
        request_data = Build(url="/api/admin/groups/{groupId}").get(groupId=groupId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_groupId(self, by_user: User):
        """Delete group by id.
        :return: No content
        """
        request_data = Build(url="/api/admin/groups/{groupId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def object_type_rights(self, by_user: User, groupId: int=None):
        """Get group object_type rights by group id.
        :return: Created group info
        """
        request_data = Build(url="/api/admin/groups/{groupId}/object_type_rights").get(groupId=groupId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def rights(self, by_user: User, ObjectTypeIds: list=None, GroupIds: list=None, Rights: str=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None):
        """Get groups rights
        :return: Group objectType paging info
        """
        request_data = Build(url="/api/admin/groups/rights").get(ObjectTypeIds=ObjectTypeIds,GroupIds=GroupIds,Rights=Rights,By=By,Page=Page,Order=Order,OrderBy=OrderBy,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def rights(self, by_user: User, objectTypeId: int=None, rights: str=None):
        """Update or insert group object type right, by groupId.
        :return: Empty
        """
        request_data = Build(url="/api/admin/groups/{groupId}/rights").put(objectTypeId=objectTypeId,rights=rights,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def object_expiration(self, by_user: User, groupId: int=None, expireSoon: int=None, expire: int=None):
        """Add group notification settings
        :return: Created objectType menu identifier
        """
        request_data = Build(url="/api/admin/groups/object_expiration").post(groupId=groupId,expireSoon=expireSoon,expire=expire,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_object_expiration(self, by_user: User, expireSoon: int=None, expire: int=None):
        """Partial update group notification settings
        :return: Empty
        """
        request_data = Build(url="/api/admin/groups/{groupId}/object_expiration").patch(expireSoon=expireSoon,expire=expire,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_object_expiration(self, by_user: User, groupId: int=None):
        """Get group notification settings info by group id
        :return: ObjectType menu info
        """
        request_data = Build(url="/api/admin/groups/{groupId}/object_expiration").get(groupId=groupId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_object_expiration(self, by_user: User):
        """Delete group notification settings by group id
        :return: No content
        """
        request_data = Build(url="/api/admin/groups/{groupId}/object_expiration").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def users(self, by_user: User, userId: int=None):
        """Add user to group.
        :return: Created user-group identifier
        """
        request_data = Build(url="/api/admin/groups/{groupId}/users").post(userId=userId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def pack(self, by_user: User, userIds: list=None):
        """Add users to group.
        :return: Created user-group identifiers
        """
        request_data = Build(url="/api/admin/groups/{groupId}/users/pack").post(userIds=userIds,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def userId(self, by_user: User):
        """Delete user from group.
        :return: Empty
        """
        request_data = Build(url="/api/admin/groups/{groupId}/users/{userId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def start(self, by_user: User):
        """Start route instance.
        :return: Empty result
        """
        request_data = Build(url="/api/admin/route/instances/{routeInstanceId}/start").post()
        return Sender().send_request(request_data, by_user=by_user)
          
    def pause(self, by_user: User):
        """Pause route instance.
        :return: Empty result
        """
        request_data = Build(url="/api/admin/route/instances/{routeInstanceId}/pause").post()
        return Sender().send_request(request_data, by_user=by_user)
          
    def resume(self, by_user: User):
        """Resume route instance.
        :return: Empty result
        """
        request_data = Build(url="/api/admin/route/instances/{routeInstanceId}/resume").post()
        return Sender().send_request(request_data, by_user=by_user)
          
    def instances(self, by_user: User, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, SchemaVersionId: int=None, StatusIds: list=None):
        """Get routes by list.
        :return: List of schemas and versions
        """
        request_data = Build(url="/api/admin/route/instances").get(By=By,Page=Page,Order=Order,OrderBy=OrderBy,SchemaVersionId=SchemaVersionId,StatusIds=StatusIds,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def routeInstanceId(self, by_user: User, routeInstanceId: str=None):
        """Get route detailed info
        :return: List of schemas and versions
        """
        request_data = Build(url="/api/admin/route/instances/{routeInstanceId}").get(routeInstanceId=routeInstanceId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_mailbox_integrations(self, by_user: User, name: str=None, description: str=None, login: str=None, password: str=None, imapHost: str=None, imapPort: int=None, isDisabled: bool=None):
        """Create new mailbox integration.
        :return: Created mailbox integration identifier
        """
        request_data = Build(url="/api/admin/mailbox_integrations").post(name=name,description=description,login=login,password=password,imapHost=imapHost,imapPort=imapPort,isDisabled=isDisabled,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_mailbox_integrations(self, by_user: User, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, SearchString: str=None, SearchStringExact: bool=None, IsDisabled: bool=None):
        """Get mailbox integrations
        :return: Mailbox integration paging info
        """
        request_data = Build(url="/api/admin/mailbox_integrations").get(By=By,Page=Page,Order=Order,OrderBy=OrderBy,SearchString=SearchString,SearchStringExact=SearchStringExact,IsDisabled=IsDisabled,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_integrationId(self, by_user: User, name: str=None, description: str=None, login: str=None, password: str=None, imapHost: str=None, imapPort: int=None, isDisabled: bool=None):
        """Partial update mailbox integration by id.
        :return: Empty
        """
        request_data = Build(url="/api/admin/mailbox_integrations/{integrationId}").patch(name=name,description=description,login=login,password=password,imapHost=imapHost,imapPort=imapPort,isDisabled=isDisabled,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_integrationId(self, by_user: User, integrationId: int=None):
        """Get mailbox integration detailed info by id.
        :return: Mailbox integration info
        """
        request_data = Build(url="/api/admin/mailbox_integrations/{integrationId}").get(integrationId=integrationId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_integrationId(self, by_user: User):
        """Delete mailbox integration by id.
        :return: No content
        """
        request_data = Build(url="/api/admin/mailbox_integrations/{integrationId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def action(self, by_user: User, integrationMailboxId: int=None, objectTypeId: int=None, rules: list=None, executionInterval: int=None, autoReply: bool=None, errorEmail: str=None):
        """Create new mailbox integration action.
        :return: Created mailbox integration action identifier
        """
        request_data = Build(url="/api/admin/mailbox_integrations/action").post(integrationMailboxId=integrationMailboxId,objectTypeId=objectTypeId,rules=rules,executionInterval=executionInterval,autoReply=autoReply,errorEmail=errorEmail,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_action(self, by_user: User, objectTypeId: int=None, rules: list=None, autoReply: bool=None, errorEmail: str=None, executionInterval: int=None):
        """Partial update mailbox integration action by id.
        :return: Empty
        """
        request_data = Build(url="/api/admin/mailbox_integrations/{integrationId}/action").patch(objectTypeId=objectTypeId,rules=rules,autoReply=autoReply,errorEmail=errorEmail,executionInterval=executionInterval,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_action(self, by_user: User, integrationId: int=None):
        """Get mailbox integration action detailed info by id.
        :return: Mailbox integration action info
        """
        request_data = Build(url="/api/admin/mailbox_integrations/{integrationId}/action").get(integrationId=integrationId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_action(self, by_user: User):
        """Delete mailbox integration action by id.
        :return: No content
        """
        request_data = Build(url="/api/admin/mailbox_integrations/{integrationId}/action").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def mxgraph(self, by_user: User, id: int=None, name: str=None, description: str=None, elements: list=None, transitions: list=None, variables: list=None):
        """Create new schema - mxgraph editor.
        :return: Created schema identifier
        """
        request_data = Build(url="/api/admin/route/mxgraph").post(id=id,name=name,description=description,elements=elements,transitions=transitions,variables=variables,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def draft(self, by_user: User, id: int=None, name: str=None, description: str=None, elements: list=None, transitions: list=None, variables: list=None, versionId: int=None):
        """Create new schema draft - mxgraph editor.
        :return: Created schema identifier
        """
        request_data = Build(url="/api/admin/route/mxgraph/draft").post(id=id,name=name,description=description,elements=elements,transitions=transitions,variables=variables,versionId=versionId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def schemaId(self, by_user: User, schemaId: int=None, versionId: int=None):
        """Get detailed schema version info - mxgraph editor.
        :return: List of schemas and versions
        """
        request_data = Build(url="/api/admin/route/mxgraph/{schemaId}").get(schemaId=schemaId,versionId=versionId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_object_types(self, by_user: User, knownId: str=None, name: str=None, description: str=None, isAbstract: bool=None, isDefault: bool=None, isSealed: bool=None, isChunk: bool=None, parentId: int=None, colorHex: str=None, extension: ObjectTypeAddExtensionModel=None, counter: ObjectTypeAddCounterModel=None):
        """Create new object type.
        :return: Created object type identifier
        """
        request_data = Build(url="/api/admin/object_types").post(knownId=knownId,name=name,description=description,isAbstract=isAbstract,isDefault=isDefault,isSealed=isSealed,isChunk=isChunk,parentId=parentId,colorHex=colorHex,extension=extension,counter=counter,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_object_types(self, by_user: User, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, IsSystem: bool=None, Ids: list=None, KnownIds: list=None):
        """Get object types.
        :return: Object type paging info
        """
        request_data = Build(url="/api/admin/object_types").get(By=By,Page=Page,Order=Order,OrderBy=OrderBy,IsSystem=IsSystem,Ids=Ids,KnownIds=KnownIds,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_objectTypeId(self, by_user: User, knownId: str=None, name: str=None, description: str=None, isAbstract: bool=None, isDefault: bool=None, isSealed: bool=None, isChunk: bool=None, colorHex: str=None, extension: ObjectTypePatchExtensionModel=None, counter: ObjectTypePatchCounterModel=None, sortWeight: int=None):
        """Partial update object type by id.
        :return: Empty
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}").patch(knownId=knownId,name=name,description=description,isAbstract=isAbstract,isDefault=isDefault,isSealed=isSealed,isChunk=isChunk,colorHex=colorHex,extension=extension,counter=counter,sortWeight=sortWeight,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_objectTypeId(self, by_user: User, objectTypeId: int=None):
        """Get object type detailed info by id.
        :return: Object type info
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}").get(objectTypeId=objectTypeId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_objectTypeId(self, by_user: User):
        """Delete object type by id.
        :return: No content
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def tree(self, by_user: User, objectTypeId: int=None):
        """Get object type tree.
        :return: Object type info
        """
        request_data = Build(url="/api/admin/object_types/tree").get(objectTypeId=objectTypeId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def sort_weight(self, by_user: User, by: int=None, page: int=None, position: int=None):
        """Set sort weight for object type.
        :return: Empty
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/sort_weight").put(by=by,page=page,position=position,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_files(self, by_user: User, fileIds: list=None):
        """Upsert objectType file.
        :return: Empty
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/files").patch(fileIds=fileIds,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_files(self, by_user: User, objectTypeId: int=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None):
        """Get objectType files.
        :return: ObjectType files paging info
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/files").get(objectTypeId=objectTypeId,By=By,Page=Page,Order=Order,OrderBy=OrderBy,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def objectTypeFileId(self, by_user: User):
        """Delete objectType file by id.
        :return: No content
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/files/{objectTypeFileId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_checkpoints(self, by_user: User, name: str=None, description: str=None, delay: int=None, duration: int=None):
        """Create new objectType checkpoint.
        :return: Created objectType checkpoint identifier
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/checkpoints").post(name=name,description=description,delay=delay,duration=duration,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_checkpoints(self, by_user: User, objectTypeId: int=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None):
        """Get objectType checkpoints.
        :return: ObjectType checkpoints paging info
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/checkpoints").get(objectTypeId=objectTypeId,By=By,Page=Page,Order=Order,OrderBy=OrderBy,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_objectTypeCheckpointId(self, by_user: User, name: str=None, description: str=None, delay: int=None, duration: int=None):
        """Partial update objectType checkpoint by id.
        :return: Empty
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/checkpoints/{objectTypeCheckpointId}").patch(name=name,description=description,delay=delay,duration=duration,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_objectTypeCheckpointId(self, by_user: User, objectTypeId: int=None, objectTypeCheckpointId: int=None):
        """Get objectType checkpoint detailed info by id.
        :return: ObjectType checkpoint info
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/checkpoints/{objectTypeCheckpointId}").get(objectTypeId=objectTypeId,objectTypeCheckpointId=objectTypeCheckpointId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_objectTypeCheckpointId(self, by_user: User):
        """Delete objectType checkpoint by id.
        :return: No content
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/checkpoints/{objectTypeCheckpointId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def bim(self, by_user: User, icon: str=None, hint: str=None, showCreateBtn: bool=None, calcElementState: bool=None):
        """Create new objectType bim.
        :return: Created objectType bim identifier
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/bim").post(icon=icon,hint=hint,showCreateBtn=showCreateBtn,calcElementState=calcElementState,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_objectTypeBimId(self, by_user: User, icon: str=None, hint: str=None, showCreateBtn: bool=None, calcElementState: bool=None):
        """Partial update objectType bim by id.
        :return: Empty
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/bim/{objectTypeBimId}").patch(icon=icon,hint=hint,showCreateBtn=showCreateBtn,calcElementState=calcElementState,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_objectTypeBimId(self, by_user: User, objectTypeId: int=None, objectTypeBimId: int=None):
        """Get objectType bim detailed info by id.
        :return: ObjectType bim info
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/bim/{objectTypeBimId}").get(objectTypeId=objectTypeId,objectTypeBimId=objectTypeBimId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_objectTypeBimId(self, by_user: User):
        """Delete objectType bim by id.
        :return: No content
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/bim/{objectTypeBimId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def menu(self, by_user: User, name: str=None, description: str=None, url: str=None, isVisible: bool=None, iconClass: str=None):
        """Create new objectType menu.
        :return: Created objectType menu identifier
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/menu").post(name=name,description=description,url=url,isVisible=isVisible,iconClass=iconClass,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_objectTypeMenuId(self, by_user: User, name: str=None, description: str=None, url: str=None, sortWeight: int=None, iconClass: str=None, isVisible: bool=None):
        """Partial update objectType menu by id.
        :return: Empty
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/menu/{objectTypeMenuId}").patch(name=name,description=description,url=url,sortWeight=sortWeight,iconClass=iconClass,isVisible=isVisible,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_objectTypeMenuId(self, by_user: User, objectTypeId: int=None, objectTypeMenuId: int=None):
        """Get objectType menu detailed info by id.
        :return: ObjectType menu info
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/menu/{objectTypeMenuId}").get(objectTypeId=objectTypeId,objectTypeMenuId=objectTypeMenuId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_objectTypeMenuId(self, by_user: User):
        """Delete objectType menu by id.
        :return: No content
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/menu/{objectTypeMenuId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_attributes(self, by_user: User, attributeId: int=None, defaultValue: str=None, valueFormat: str=None, settings: ObjectTypeAttributeAddSettingsModel=None, formula: ObjectTypeAttributeAddFormulaModel=None):
        """Create new objectType attribute.
        :return: Created objectType attribute identifier
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/attributes").post(attributeId=attributeId,defaultValue=defaultValue,valueFormat=valueFormat,settings=settings,formula=formula,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_attributes(self, by_user: User, objectTypeId: int=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, AttributeIds: list=None, RelatedObjectTypeId: int=None, SearchSubstring: str=None, SearchSubstringExact: bool=None):
        """Get objectType attributes.
        :return: ObjectType attributes paging info
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/attributes").get(objectTypeId=objectTypeId,By=By,Page=Page,Order=Order,OrderBy=OrderBy,AttributeIds=AttributeIds,RelatedObjectTypeId=RelatedObjectTypeId,SearchSubstring=SearchSubstring,SearchSubstringExact=SearchSubstringExact,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_objectTypeAttributeId(self, by_user: User, defaultValue: str=None, valueFormat: str=None, settings: ObjectTypeAttributePatchSettingsModel=None, formula: ObjectTypeAttributePatchFormulaModel=None):
        """Partial update objectType attribute by id.
        :return: Empty
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/attributes/{objectTypeAttributeId}").patch(defaultValue=defaultValue,valueFormat=valueFormat,settings=settings,formula=formula,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_objectTypeAttributeId(self, by_user: User, objectTypeId: int=None, objectTypeAttributeId: int=None):
        """Get objectType attribute detailed info by id.
        :return: ObjectType attribute info
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/attributes/{objectTypeAttributeId}").get(objectTypeId=objectTypeId,objectTypeAttributeId=objectTypeAttributeId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_objectTypeAttributeId(self, by_user: User):
        """Delete objectType attribute by id.
        :return: No content
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/attributes/{objectTypeAttributeId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def route_schema(self, by_user: User, objectTypeId: int=None):
        """Get route schema info by object type id.
        :return: Object type info
        """
        request_data = Build(url="/api/admin/object_types/{objectTypeId}/route_schema").get(objectTypeId=objectTypeId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def schemas(self, by_user: User, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, SearchString: str=None, SearchStringExact: bool=None, IsDeleted: bool=None, ObjectTypeId: int=None, Versions_Id: int=None, Versions_Ids: list=None, Versions_IsDraft: bool=None, Versions_IsActive: bool=None):
        """Get schemas by list.
        :return: List of schemas and versions
        """
        request_data = Build(url="/api/admin/route/schemas").get(By=By,Page=Page,Order=Order,OrderBy=OrderBy,SearchString=SearchString,SearchStringExact=SearchStringExact,IsDeleted=IsDeleted,ObjectTypeId=ObjectTypeId,Versions_Id=Versions_Id,Versions_Ids=Versions_Ids,Versions_IsDraft=Versions_IsDraft,Versions_IsActive=Versions_IsActive,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def activate(self, by_user: User):
        """Activate schema version.
        :return: Empty result
        """
        request_data = Build(url="/api/admin/route/schemas/{schemaId}/version/{versionId}/activate").post()
        return Sender().send_request(request_data, by_user=by_user)
          
    def schemaId(self, by_user: User):
        """Delete schema.
        :return: Empty result
        """
        request_data = Build(url="/api/admin/route/schemas/{schemaId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_object_type(self, by_user: User, objectTypeId: int=None, needStartAfterCreateObject: bool=None):
        """Set ObjectType.
        :return: Empty result
        """
        request_data = Build(url="/api/admin/route/schemas/{schemaId}/object_type").post(objectTypeId=objectTypeId,needStartAfterCreateObject=needStartAfterCreateObject,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_object_type(self, by_user: User):
        """Delete ObjectType.
        :return: Empty result
        """
        request_data = Build(url="/api/admin/route/schemas/{schemaId}/object_type").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_service_integrations(self, by_user: User, name: str=None, description: str=None, url: str=None, contentTypeId: str=None, methodId: str=None):
        """Add service integration
        :return: Created service integration identifier
        """
        request_data = Build(url="/api/admin/service_integrations").post(name=name,description=description,url=url,contentTypeId=contentTypeId,methodId=methodId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_service_integrations(self, by_user: User, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None):
        """Get service integrations
        :return: ServiceIntegration paging info
        """
        request_data = Build(url="/api/admin/service_integrations").get(By=By,Page=Page,Order=Order,OrderBy=OrderBy,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_serviceIntegrationId(self, by_user: User, name: str=None, description: str=None, url: str=None, contentTypeId: str=None, methodId: str=None):
        """Partial update service integration
        :return: Empty
        """
        request_data = Build(url="/api/admin/service_integrations/{serviceIntegrationId}").patch(name=name,description=description,url=url,contentTypeId=contentTypeId,methodId=methodId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_serviceIntegrationId(self, by_user: User, serviceIntegrationId: int=None):
        """Get service integration info by id
        :return: Service integration info
        """
        request_data = Build(url="/api/admin/service_integrations/{serviceIntegrationId}").get(serviceIntegrationId=serviceIntegrationId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_serviceIntegrationId(self, by_user: User):
        """Delete service integration by id
        :return: No content
        """
        request_data = Build(url="/api/admin/service_integrations/{serviceIntegrationId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_object_type(self, by_user: User, serviceIntegrationId: int=None, objectTypeId: int=None):
        """Add service integration objectType
        :return: Created service integration objectType identifier
        """
        request_data = Build(url="/api/admin/service_integrations/object_type").post(serviceIntegrationId=serviceIntegrationId,objectTypeId=objectTypeId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_object_type(self, by_user: User, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, ServiceIntegrationId: int=None, ObjectTypeId: int=None):
        """Get service integrations objectType
        :return: ServiceIntegrationObjectType paging info
        """
        request_data = Build(url="/api/admin/service_integrations/object_type").get(By=By,Page=Page,Order=Order,OrderBy=OrderBy,ServiceIntegrationId=ServiceIntegrationId,ObjectTypeId=ObjectTypeId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_serviceIntegrationObjectTypeId(self, by_user: User, objectTypeId: int=None):
        """Partial update service integration objectType
        :return: Empty
        """
        request_data = Build(url="/api/admin/service_integrations/object_type/{serviceIntegrationObjectTypeId}").patch(objectTypeId=objectTypeId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_serviceIntegrationObjectTypeId(self, by_user: User, serviceIntegrationObjectTypeId: int=None):
        """Get service integration objectType info by id
        :return: Service integration objectType info
        """
        request_data = Build(url="/api/admin/service_integrations/object_type/{serviceIntegrationObjectTypeId}").get(serviceIntegrationObjectTypeId=serviceIntegrationObjectTypeId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_serviceIntegrationObjectTypeId(self, by_user: User):
        """Delete service integration objectType by id
        :return: No content
        """
        request_data = Build(url="/api/admin/service_integrations/object_type/{serviceIntegrationObjectTypeId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_param(self, by_user: User, serviceIntegrationId: int=None, paramTypeId: str=None, key: str=None, value: str=None):
        """Add service integration param
        :return: Created service integration param identifier
        """
        request_data = Build(url="/api/admin/service_integrations/param").post(serviceIntegrationId=serviceIntegrationId,paramTypeId=paramTypeId,key=key,value=value,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_param(self, by_user: User, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, ServiceIntegrationId: int=None, ParamTypeId: str=None):
        """Get service integrations param
        :return: ServiceIntegrationParam paging info
        """
        request_data = Build(url="/api/admin/service_integrations/param").get(By=By,Page=Page,Order=Order,OrderBy=OrderBy,ServiceIntegrationId=ServiceIntegrationId,ParamTypeId=ParamTypeId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_serviceIntegrationParamId(self, by_user: User, paramTypeId: str=None, key: str=None, value: str=None):
        """Partial update service integration param
        :return: Empty
        """
        request_data = Build(url="/api/admin/service_integrations/param/{serviceIntegrationParamId}").patch(paramTypeId=paramTypeId,key=key,value=value,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_serviceIntegrationParamId(self, by_user: User, serviceIntegrationParamId: int=None):
        """Get service integration param info by id
        :return: Service integration param info
        """
        request_data = Build(url="/api/admin/service_integrations/param/{serviceIntegrationParamId}").get(serviceIntegrationParamId=serviceIntegrationParamId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_serviceIntegrationParamId(self, by_user: User):
        """Delete service integration param by id
        :return: No content
        """
        request_data = Build(url="/api/admin/service_integrations/param/{serviceIntegrationParamId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def function(self, by_user: User, function: str=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, DateFrom: str=None, DateTo: str=None, SchemaId: int=None, SchemaVersionId: int=None, RouteInstanceId: str=None, ExecutorId: int=None, ElementTypeId: str=None, Percentile: str=None):
        """Get statistics
        :return: Statistics
        """
        request_data = Build(url="/api/admin/route/statistics/{function}").get(function=function,By=By,Page=Page,Order=Order,OrderBy=OrderBy,DateFrom=DateFrom,DateTo=DateTo,SchemaId=SchemaId,SchemaVersionId=SchemaVersionId,RouteInstanceId=RouteInstanceId,ExecutorId=ExecutorId,ElementTypeId=ElementTypeId,Percentile=Percentile,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_users(self, by_user: User, password: str=None, userName: str=None, email: str=None, firstName: str=None, middleName: str=None, lastName: str=None, phoneNumber: str=None, preferredLocale: str=None, isDismissed: bool=None, isDisabled: bool=None, position: str=None, extension: UserModelExtension=None, role: str=None, notification: UserModelNotification=None):
        """Create new user.
        :return: Created User identifier
        """
        request_data = Build(url="/api/admin/users").post(password=password,userName=userName,email=email,firstName=firstName,middleName=middleName,lastName=lastName,phoneNumber=phoneNumber,preferredLocale=preferredLocale,isDismissed=isDismissed,isDisabled=isDisabled,position=position,extension=extension,role=role,notification=notification,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_users(self, by_user: User, DateCreatedFrom: str=None, DateCreatedTo: str=None, IsSystem: bool=None, Roles: list=None, IsDismissed: bool=None, IsDisabled: bool=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, SearchString: str=None, SearchStringExact: bool=None, DepartmentIds: list=None, RootDepartment: bool=None, UserIds: list=None, GroupId: int=None, GroupIntersect: bool=None, UserName: str=None, Emails: list=None, CanBeNotifiedInScopeOfVacation: bool=None, ReceiveNotificationByEmail: bool=None, ReceiveNotificationOnNewObject: bool=None, ReceiveNotificationOnChangedObject: bool=None, ReceiveNotificationOnlyOnChangeInFavoriteObjects: bool=None, ReceiveNotificationOnMentioned: bool=None):
        """Get users with detailed info by system admin
        :return: User paging extended info
        """
        request_data = Build(url="/api/admin/users").get(DateCreatedFrom=DateCreatedFrom,DateCreatedTo=DateCreatedTo,IsSystem=IsSystem,Roles=Roles,IsDismissed=IsDismissed,IsDisabled=IsDisabled,By=By,Page=Page,Order=Order,OrderBy=OrderBy,SearchString=SearchString,SearchStringExact=SearchStringExact,DepartmentIds=DepartmentIds,RootDepartment=RootDepartment,UserIds=UserIds,GroupId=GroupId,GroupIntersect=GroupIntersect,UserName=UserName,Emails=Emails,CanBeNotifiedInScopeOfVacation=CanBeNotifiedInScopeOfVacation,ReceiveNotificationByEmail=ReceiveNotificationByEmail,ReceiveNotificationOnNewObject=ReceiveNotificationOnNewObject,ReceiveNotificationOnChangedObject=ReceiveNotificationOnChangedObject,ReceiveNotificationOnlyOnChangeInFavoriteObjects=ReceiveNotificationOnlyOnChangeInFavoriteObjects,ReceiveNotificationOnMentioned=ReceiveNotificationOnMentioned,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_userId(self, by_user: User, userId: int=None):
        """Get user by id.
        :return: User detailed info
        """
        request_data = Build(url="/api/admin/users/{userId}").get(userId=userId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_userId(self, by_user: User, userName: str=None, password: str=None, email: str=None, firstName: str=None, middleName: str=None, lastName: str=None, phoneNumber: str=None, preferredLocale: str=None, isDismissed: bool=None, isDisabled: bool=None, position: str=None, extension: UserModelExtension=None, role: str=None, notification: UserModelNotification=None):
        """Modify user by id, partially
        :return: No Content
        """
        request_data = Build(url="/api/admin/users/{userId}").patch(userName=userName,password=password,email=email,firstName=firstName,middleName=middleName,lastName=lastName,phoneNumber=phoneNumber,preferredLocale=preferredLocale,isDismissed=isDismissed,isDisabled=isDisabled,position=position,extension=extension,role=role,notification=notification,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def disable(self, by_user: User):
        """Disable user.
        :return: No Content
        """
        request_data = Build(url="/api/admin/users/{userId}/disable").post()
        return Sender().send_request(request_data, by_user=by_user)
          
    def enable(self, by_user: User):
        """Enable user.
        :return: No Content
        """
        request_data = Build(url="/api/admin/users/{userId}/enable").post()
        return Sender().send_request(request_data, by_user=by_user)
          
    def dismiss(self, by_user: User):
        """Dismiss user.
        :return: No Content
        """
        request_data = Build(url="/api/admin/users/{userId}/dismiss").post()
        return Sender().send_request(request_data, by_user=by_user)
          
    def employ(self, by_user: User):
        """Employ user.
        :return: No Content
        """
        request_data = Build(url="/api/admin/users/{userId}/employ").post()
        return Sender().send_request(request_data, by_user=by_user)
          
    def password(self, by_user: User, userId: int=None, newPassword: str=None):
        """Change user password (by administrator)
        :return: No Content
        """
        request_data = Build(url="/api/admin/users/password").post(userId=userId,newPassword=newPassword,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_mailbox(self, by_user: User, login: str=None, password: str=None, smtpHost: str=None, smtpPort: int=None, imapHost: str=None, imapPort: int=None, isDisabled: bool=None, signature: str=None):
        """Create new mailbox by userId.
        :return: Created mailbox identifier
        """
        request_data = Build(url="/api/admin/users/{userId}/mailbox").post(login=login,password=password,smtpHost=smtpHost,smtpPort=smtpPort,imapHost=imapHost,imapPort=imapPort,isDisabled=isDisabled,signature=signature,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_mailbox(self, by_user: User, login: str=None, password: str=None, smtpHost: str=None, smtpPort: int=None, imapHost: str=None, imapPort: int=None, isDisabled: bool=None, signature: str=None):
        """Partial update mailbox by userId.
        :return: Empty
        """
        request_data = Build(url="/api/admin/users/{userId}/mailbox").patch(login=login,password=password,smtpHost=smtpHost,smtpPort=smtpPort,imapHost=imapHost,imapPort=imapPort,isDisabled=isDisabled,signature=signature,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_mailbox(self, by_user: User, userId: int=None):
        """Get mailbox detailed info by userId.
        :return: Mailbox info
        """
        request_data = Build(url="/api/admin/users/{userId}/mailbox").get(userId=userId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_mailbox(self, by_user: User):
        """Delete mailbox by userId.
        :return: No content
        """
        request_data = Build(url="/api/admin/users/{userId}/mailbox").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_value_lists(self, by_user: User, name: str=None, description: str=None, valueTypeId: str=None, values: list=None):
        """Create new value list.
        :return: Created value_list identifier
        """
        request_data = Build(url="/api/admin/value_lists").post(name=name,description=description,valueTypeId=valueTypeId,values=values,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_value_lists(self, by_user: User, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, SearchString: str=None, SearchStringExact: bool=None, ValueTypeId: str=None):
        """Get value_lists.
        :return: Object type paging info
        """
        request_data = Build(url="/api/admin/value_lists").get(By=By,Page=Page,Order=Order,OrderBy=OrderBy,SearchString=SearchString,SearchStringExact=SearchStringExact,ValueTypeId=ValueTypeId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_valueListId(self, by_user: User, name: str=None, description: str=None):
        """Partial update value_list by id.
        :return: Empty
        """
        request_data = Build(url="/api/admin/value_lists/{valueListId}").patch(name=name,description=description,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_valueListId(self, by_user: User, valueListId: int=None):
        """Get value_list detailed info by id.
        :return: Object type info
        """
        request_data = Build(url="/api/admin/value_lists/{valueListId}").get(valueListId=valueListId,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_valueListId(self, by_user: User):
        """Delete value_list by id.
        :return: No content
        """
        request_data = Build(url="/api/admin/value_lists/{valueListId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
          
    def post_entries(self, by_user: User, name: str=None, value: str=None):
        """Create new valueList entry.
        :return: Created valueList entry identifier
        """
        request_data = Build(url="/api/admin/value_lists/{valueListId}/entries").post(name=name,value=value,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def get_entries(self, by_user: User, valueListId: int=None, By: int=None, Page: int=None, Order: str=None, OrderBy: str=None, SearchString: str=None, SearchStringExact: bool=None):
        """Get valueList entrys.
        :return: ObjectType entries paging info
        """
        request_data = Build(url="/api/admin/value_lists/{valueListId}/entries").get(valueListId=valueListId,By=By,Page=Page,Order=Order,OrderBy=OrderBy,SearchString=SearchString,SearchStringExact=SearchStringExact,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def patch_valueListEntryId(self, by_user: User, name: str=None):
        """Partial update valueList entry by id.
        :return: Empty
        """
        request_data = Build(url="/api/admin/value_lists/{valueListId}/entries/{valueListEntryId}").patch(name=name,)
        return Sender().send_request(request_data, by_user=by_user)
          
    def delete_valueListEntryId(self, by_user: User):
        """Delete valueList entry by id.
        :return: No content
        """
        request_data = Build(url="/api/admin/value_lists/{valueListId}/entries/{valueListEntryId}").delete()
        return Sender().send_request(request_data, by_user=by_user)
        