import logging
from utah.core.authorize import BaseURIAuthorizationService, Group
from utah.core.authorize import URIAccessRight
from utah.core.authorize import BaseGroupService
from utah.impl.bryce.utilities import ConnectionDefinition

logger = logging.getLogger(__name__)

def obj_from_group(group:Group) -> dict:
    return {
        "name" : group.name,
        "description" : group.description
    }


def group_from_obj(obj:dict) -> Group:
    if obj:
        return Group(obj["name"], obj["description"])
    else:
        return None


def uri_access_right_from_obj(env_type:str, obj:dict) -> URIAccessRight:
    ret_right = None
    if obj:
        del obj["_id"]
        if not obj["permitted_environments"] or env_type in obj["permitted_environments"]:
            obj["disabled"] = False
        else:
            obj["disabled"] = True

        ret_right = URIAccessRight(**obj)

    return ret_right

def obj_from_uri_access_right(uri_access_right:URIAccessRight) -> dict:
    return {
        "id": uri_access_right.id, 
        "category": uri_access_right.category, 
        "right_name": uri_access_right.right_name, 
        "uri": uri_access_right.uri, 
        "methods": uri_access_right.methods, 
        "filters": uri_access_right.filters, 
        "authorized_groups": uri_access_right.authorized_groups, 
        "permitted_environments": uri_access_right.permitted_environments 
    }


class GroupService(BaseGroupService):
    def __init__(self, mongo_url:str, enrollments_mongo_url:str, default_anonymous_groups:list, default_logged_in_groups:list):

        self.conn_def:ConnectionDefinition = ConnectionDefinition(mongo_url)
        self.enrollments_conn_def:ConnectionDefinition = ConnectionDefinition(enrollments_mongo_url)

        super(GroupService, self).__init__(default_anonymous_groups, default_logged_in_groups)


    def get_enrollment_coll(self):
        logger.debug("GroupService.get_enrollment_coll()")
        return self.enrollments_conn_def.get_database()["enrollments"]


    def get_group_coll(self):
        return self.conn_def.get_database()["groups"]


    def read_group_names_for_user(self, user_id:str):
        logger.debug("GroupService.read_group_names_for_user()")
        enrollments = self.get_enrollment_coll().find_one({"user_id" : user_id})
        if enrollments:
            return enrollments["group_names"]
        else:
            return []


    def get_groups(self):
        ret_groups = []
        for obj in self.get_group_coll().find():
            ret_groups.append(group_from_obj(obj))

        return ret_groups


    def get_group(self, name:str):
        return group_from_obj(self.get_group_coll().find_one({"name":name}))


    def get_group_members(self, group_name:str):
        logger.debug("GroupService.get_group_members()")
        ret_user_ids = []
        for obj in self.get_enrollment_coll().find({"group_names":group_name}):
            ret_user_ids.append(obj["user_id"])

        return ret_user_ids

    def update_group(self, group:Group):
        self.get_group_coll().update_one({"name":group.name}, {"$set" : obj_from_group(group)})


    def add_group(self, group:Group):
        self.get_group_coll().insert_one(obj_from_group(group))


    def delete_group(self, name:str):
        logger.debug("GroupService.delete_group()")

        self.get_group_coll().delete_one({"name": name})
        self.get_enrollment_coll().update_many(
            {"group_names" : name},
            { "$pull": { "group_names": name } }
        )



    def update_groups_for_user(self, user_id:str, groups:list):
        logger.debug("GroupService.update_groups_for_user()")
        coll = self.get_enrollment_coll()
        if coll.find_one({"user_id" : user_id}):
            coll.update_one({"user_id":user_id}, {"$set": {"user_id": user_id, "group_names" : groups} })
        else:
            coll.insert_one({"user_id": user_id, "group_names" : groups})



class URIAuthorizationService(BaseURIAuthorizationService):
    def __init__(self, mongo_url:str, group_service_name:str, cache_timeout_secs:int, environment_type:str="FULL", available_environment_types:str="FULL"):

        self.conn_def:ConnectionDefinition = ConnectionDefinition(mongo_url)

        super(URIAuthorizationService, self).__init__(group_service_name, cache_timeout_secs, environment_type, available_environment_types)


    def get_right_coll(self):
        logger.debug("URIAuthorizationService.get_right_coll()")
        return self.conn_def.get_database()["rights"]


    def get_all_authorizations(self):
        ret_authorizations = []

        for obj in self.get_right_coll().find():
            ret_authorizations.append(uri_access_right_from_obj(self.environment_type, obj))

        return ret_authorizations


    def get_authorization(self, id:str):
        return uri_access_right_from_obj(self.environment_type, self.get_right_coll().find_one({"id" : id}))


    def find_authorization(self, category, right_name)->URIAccessRight:
        return uri_access_right_from_obj(self.environment_type, self.get_right_coll().find_one({"category" : category, "right_name": right_name}))


    def update_authorization_io(self, uri_access_right:URIAccessRight):
        self.get_right_coll().update_one({"id" : uri_access_right.id }, {"$set" : obj_from_uri_access_right(uri_access_right)})


    def add_authorization_io(self, uri_access_right:URIAccessRight):
        self.get_right_coll().insert_one(obj_from_uri_access_right(uri_access_right))


    def delete_authorization_io(self, id:str):
        self.get_right_coll().delete_one({"id" : id})


    def remove_group_from_authorizations_io(self, group_name):
        coll = self.get_right_coll()
        for obj in coll.find({"group_names":group_name}):
            obj["group_names"].remove(group_name)
            coll.update_one({"_id" : obj["_id"]}, obj)


    def get_access_rights_for_uri_io(self, uri):
        ret_list = None
        for obj in self.get_right_coll().find({ "uri" : uri}):
            if ret_list == None:
                ret_list = []

            ret_list.append(uri_access_right_from_obj(self.environment_type, obj))

        return ret_list


