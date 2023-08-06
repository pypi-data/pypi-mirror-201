from utah.core.bootstrap import set_app_home
set_app_home(".")

import pymongo
import os
import sys
import argparse
import base64
import urllib.parse

from utah.core import bootstrap
import os

log_path = "%s/logs" % bootstrap.get_var_data_loc()
if not os.path.exists(log_path):
    os.mkdir(log_path)

from utah.core.setup import BaseUtahInititializer
from utah.core.setup import create_directory
from utah.core.setup import InitializationException
from utah.core.utilities import get_stash
from utah.core.authentication import generate_password
from utah.core.utilities import date_to_string
from datetime import datetime

from utah.core.setup import DEPLOY_MODEL_NONE
from utah.core.setup import DEPLOY_MODEL_DEV_PROD
from utah.core.setup import DEPLOY_MODEL_DEV_UAT_PROD

import logging
_logger = logging.getLogger(__name__)



def mongo_url(username:str, password:str, host:str, port:int, tls:bool, database:str=""):
    return "mongodb://%s:%s@%s:%s/%s?authMechanism=DEFAULT&tls=%s" % (username, urllib.parse.quote(password, safe=""), host, port, database, str(tls).lower())

class UtahInitializer(BaseUtahInititializer):
    def __init__(self, src_repo_loc:str, mongo_admin_username:str, mongo_admin_password:str, mongo_admin_host:str, mongo_admin_port:int, mongo_admin_tls:bool, db_purpose:str, deploy_model:int):
        super().__init__(src_repo_loc, deploy_model)

        self.mongo_admin_url = mongo_url(mongo_admin_username, mongo_admin_password, mongo_admin_host, mongo_admin_port, mongo_admin_tls)

        self.mongo_admin_host = mongo_admin_host
        self.mongo_admin_port = mongo_admin_port
        self.mongo_admin_tls = mongo_admin_tls
        self.db_purpose = db_purpose

    def create_database(self):
        self.mongo_client = pymongo.MongoClient(self.mongo_admin_url)
        db_name = "%s_arches_app_db" % self.db_purpose
        pwd = generate_password(pwd_min_length=25)

        _logger.info(self.mongo_client.list_database_names())
        if db_name in self.mongo_client.list_database_names():
            raise InitializationException("Database %s already exists" % db_name)

        mydb = self.mongo_client[db_name]
        coll = mydb["setup_info"]
        coll.insert_one({
            "database_type" : self.db_purpose,
            "setup_date" : date_to_string(datetime.utcnow())
        })
        
        username = "%s_read_write" % db_name

        mydb.command("createUser", username, pwd=pwd, roles=[{'role':'readWrite', 'db':db_name}])

        ret_url = mongo_url(username, pwd, self.mongo_admin_host, self.mongo_admin_port, self.mongo_admin_tls, db_name)
        #coll.drop()
        return ret_url


    def prepare(self):
        stash = get_stash()

        ret_url = self.create_database()

        stash.write_value("MONGO_COMMON_APP_DB_URL", ret_url, True)
        stash.write_value("MONGO_DOWNSTREAM_APP_DB_URL", ret_url, True)
        stash.write_value("MONGO_LOCAL_APP_DB_URL", ret_url, True)



if __name__ == "__main__":
    #mongodb://mongoadmin:secret@docker_bridge:27018/?authMechanism=DEFAULT&tls=false

    parser = argparse.ArgumentParser(description='Setup a new arches based workspace')
    parser.add_argument('--mongo_admin_username', dest='mongo_admin_username', action='store', required=True, help='Mongo admin username')
    parser.add_argument('--mongo_admin_password', dest='mongo_admin_password', action='store', required=True, help='Mongo admin password')
    parser.add_argument('--mongo_admin_host', dest='mongo_admin_host', action='store', required=True, help='Mongo admin host')
    parser.add_argument('--mongo_admin_port', dest='mongo_admin_port', action='store', required=True, help='Mongo admin port')
    parser.add_argument('--mongo_admin_tls', dest='mongo_admin_tls', action='store_true', required=False, default=False, help='Mongo admin tls true/false')
    parser.add_argument('--db_purpose', dest='db_purpose', action='store', required=True, choices=["cmn", "sta", "dev", "uat", "prd"], help='Purpose for the database being populated')
    parser.add_argument('--deploy_model', dest='deploy_model', action='store', required=True, choices=["none", "dev_prod", "dev_uat_prod"], help='Deployment pattern for the database infrastructure')
    args = parser.parse_args()


    config_path = bootstrap.get_app_home() + "/config/utah_service_config.pp_json"
    f = open(config_path)
    cfg = f.read()
    f.close()

    if cfg.find(".bryce.") == -1:
        raise Exception("System is not currently in bryce configuration. Confirm the correct utah_service_config file is in place")

    source_repo_path = bootstrap.get_app_home() + "/sample_content"

    if args.deploy_model == "none":
        deploy_model = DEPLOY_MODEL_NONE
    elif args.deploy_model == "dev_prod":
        deploy_model = DEPLOY_MODEL_DEV_PROD
    elif args.deploy_model == "dev_uat_prod":
        deploy_model = DEPLOY_MODEL_DEV_UAT_PROD


    initializer = UtahInitializer(source_repo_path, args.mongo_admin_username, args.mongo_admin_password, args.mongo_admin_host, args.mongo_admin_port, args.mongo_admin_tls, args.db_purpose, deploy_model)

    _logger.info("Call initialize")

    initializer.initialize()

    _logger.info("finish")
