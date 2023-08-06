import sys
import urllib
import json
import os
import pathlib
import glob

#from morph_util.morphclass import RequestsApi
from morphcp.morphclass import RequestsApi
#import morph_util.utils.helpers as morph_util
import morphcp.utils.helpers as morph_util
#import morph_util.logging.loghandler as loghandler
import morphcp.logging.loghandler as loghandler
#from morph_util.vars import * 
from morphcp.vars import *
def inject_groups():
    """
    The inject_groups function is used to create groups in the mo-laptop.
    It takes a directory as an argument and looks for files that match the pattern:
    groups_inject_filter_pattern = &quot;*.json&quot;
    The function then opens each file, loads it into memory, and iterates over each group object.  Each group object is then sent to /api/groups using a POST request.
    
    :param inputdir: Specify the directory containing the payloads to inject
    :return: :
    :doc-author: Trelent
    """
    cl = RequestsApi()
    logger = loghandler.get_logger(__name__)
    cp_groups_dir = os.path.join(contentpack_base_folder,os.environ.get("contentpack"),groups_payload_folder,groups_inject_filter_pattern)
    files = glob.glob(cp_groups_dir)
    logger.debug(cp_groups_dir)
    logger.debug(files)
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
        f.close()
        logger.debug(data)
        for item in data["groups"]:
            logger.debug(item)
            payload = {'group': item}
            payload = json.dumps(payload)
            logger.debug(payload)
            resp = cl.post(f"/api/groups", data = payload)
            resp = resp.json()
            if resp['success'] is False and resp['errors'] == {'name': 'must be unique'}:
                logger.warning(f"Group {item['name']} already exists")
                logger.warning(f"Skipping {item['name']}")
            elif resp['success'] is True:
                logger.info(f"Successfully created group {item['name']}")
            elif resp['success'] is False and resp['errors'] != {'name': 'must be unique'}:
                logger.error(f"Failed to create group {item['name']}")
                logger.error(f"Error: {resp['errors']}")
                sys.exit(1)
                

def inject_roles():
    """
    The inject_roles function injects the roles defined in the content pack into
    the system. It does this by reading a file from disk and parsing it as JSON.
    The JSON is then used to create a role in the system, which is then assigned
    permissions based on what features are enabled for that role.
    
    :return: :
    :doc-author: Trelent
    """
    cl = RequestsApi()
    logger = loghandler.get_logger(__name__)
    def create_role(payload):
        resp = cl.post("/api/roles", data = json.dumps(payload)).json()
        logger.debug(resp)
        role_id = resp['role']['id']
        # TODO add error handling
        #tools.debug_printer(f'Json input from file: {payload}', f'Json output from API: {resp}', f'Role ID: {role_id}')
        return role_id
    cp_roles_dir = os.path.join(contentpack_base_folder,os.environ.get("contentpack"),roles_payload_folder,roles_inject_filter_pattern)
    files = glob.glob(cp_roles_dir)
    for file in files:
        with open(file,'r') as f:
            data = json.load(f)
        f.close()
        roleid = create_role(data[0])
        if "featurePermissions" in data[1]:
            for x in data[1]['featurePermissions']:
                resp = cl.put(f"/api/roles/{roleid}/update-permission", data = json.dumps(x)).json()
                logger.debug(resp)
        if "globalSiteAccess" in data[2]:
            print('global site access')
        if "sites" in data[3]:
            for x in data[3]['sites']:
                try: 
                    group_name = urllib.parse.quote(x['name'])
                    resp = cl.get(f"/api/groups?name={group_name}").json()
                    #logger.debug(resp)
                    x['groupId'] = resp['groups'][0]['id']
                    resp = cl.put(f"/api/roles/{roleid}/update-group", data = json.dumps(x)).json()
                    #logger.debug(resp)
                except IndexError as e:
                    logger.warning(f"Failed to update role {roleid} - group not found")
                    logger.warning(f"Error: {e}")
                    continue
        if "globalZoneAccess" in data[4]:
            print("globalZoneAccess")
        if "zones" in data[5]:
            print("global instance type access")
        if "globalInstanceTypeAccess" in data[6]:
            print("global instance type access")
        if "instanceTypePermissions" in data[7]:
            for x in data[7]['instanceTypePermissions']:
                try:
                    instancetype_name = urllib.parse.quote(x['name'])
                    resp = cl.get(f"/api/library/instance-types?name={instancetype_name}").json()
                    x["instanceTypeId"] = resp['instanceTypes'][0]['id']
                    resp = cl.put(f"/api/roles/{roleid}/update-instance-type", data = json.dumps(x)).json()
                except IndexError as e:
                    logger.warning(f"Failed to update role {roleid} - instance type not found")
                    logger.warning(f"Error: {e}")
                    continue
        if "globalAppTemplateAccess" in data[8]:
            print("global app template access")
        if "globalCatalogItemTypeAccess" in data[9]:
            print("global catalog item type access")
        if "globalPersonaAccess" in data[10]:
            print("global persona access")
        if "personaPermissions" in data[11]:
            for x in data[11]['personaPermissions']:
                resp = cl.put(f"/api/roles/{roleid}/update-persona", data = json.dumps(x)).json()
                logger.debug(resp)
        if "globalVdiPoolAccess" in data[12]:
            print("global vdi pool access")
        if "globalReportTypeAccess" in data[13]:
            print("global report type access")
        if "reportTypePermissions" in data[14]:
            for x in data[14]['reportTypePermissions']:
                try:
                    report_name = urllib.parse.quote(x['name'])
                    resp = cl.get(f"/api/report-types?name={report_name}").json()
                    logger.debug(resp)
                    x["reportTypeId"] = resp['reportTypes'][0]['id']
                    resp = cl.put(f"/api/roles/{roleid}/update-report-type", data = json.dumps(x)).json()
                    logger.debug(resp)
                except IndexError as e:
                    logger.warning(f"Failed to update report - report not found")
                    logger.warning(f"Error: {e}")
                    continue
        if "globalTaskAccess" in data[15]:
            print("global task access")
        if "taskPermissions" in data[16]:
            pass
        if "globalTaskSetAccess" in data[17]:
            print("global task set access")
        if "taskSetPermissions" in data[18]:
            pass
    # for file in files:
    #     with open(file,'r') as f:
    #         data = json.load(f)
    #     f.close()
    #     for s in range(len(data)):
    #         if 'role' in data[s]:
    #             logger.debug(data[s])
    #             payload = json.dumps(data[s])
    #             role_id = create_role(payload)
    #             logger.debug(role_id)
    #             # TODO add a look up role ids if failure occurs
    #     for s in range(len(data)):
    #         if 'featurePermissions' in data[s]:
    #             logger.debug(data[s])
    #             x = data[s]['featurePermissions']
    #             for i in x:
    #                 logger.debug(i)
    #                 i = json.dumps(i)
    #                 resp = cl.put(f"/api/roles/{role_id}/update-permission", data = i)
    #                 resp = resp.json()
    #                 if resp['success'] is False:
    #                     logger.error(f"Failed to update role {role_id}")
    #                     logger.error(f"Error: {resp}")
    #                 #TODO add a failure notiifcation
    #     for s in range(len(data)):
    #         if 'sites' in data[s]:
    #             logger.debug(data[s])
    #             x = data[s]['sites']
    #             for i in x:
    #                 logger.debug(i)
    #                 logger.debug(i['name'])
    #                 group_name = urllib.parse.quote(i['name'])
    #                 logger.debug(group_name)
    #                 resp = cl.get(f"/api/groups?name={group_name}")
    #                 resp = resp.json()
    #                 logger.debug(resp)
    #                 group_id = resp['groups'][0]['id']
    #                 i['name'] = group_id
    #                 i['groupId'] = i.pop('name')
    #                 logger.debug(i)
    #                 payload = json.dumps(i)
    #                 resp = cl.put(f"/api/roles/{role_id}/update-group", data = payload)
    #                 resp = resp.json()
    #                 if resp['success'] is False:
    #                     logger.error(f"Failed to update role {role_id}")
    #                     logger.error(f"Error: {resp}")
    #                 #TODO add a failure notiifcation
def inject_tasks(): 
    """
    The inject_tasks function injects tasks into the content pack.
        
    
    :return: The response of the post request to the tasks endpoint
    :doc-author: Trelent
    """
    logger = loghandler.get_logger(__name__)
    cl = RequestsApi()
    cp_tasks_dir = os.path.join(contentpack_base_folder,os.environ.get("contentpack"),task_payload_folder,task_inject_filter_pattern)
    files = glob.glob(cp_tasks_dir)
    for file in files:
        with open(file,'r') as f:
            data = json.load(f)
        f.close()
        payload = json.dumps(data)
        resp = cl.post("/api/tasks", data = payload)
        logger.debug(resp.json())
        
def inject_optionlist():
    """
    The inject_optionlist function is used to inject optionlist payloads into the Morph API.
        The function takes no arguments and returns nothing.
    
    
    :return: A list of option lists that have been injected
    :doc-author: Trelent
    """
    logger = loghandler.get_logger(__name__)
    cl = RequestsApi()
    cp_dir = os.path.join(contentpack_base_folder,os.environ.get("contentpack"),optionlist_payload_folder,optionlist_inject_filter_pattern)
    files = glob.glob(cp_dir)
    for file in files:
        with open(file,'r') as f:
            data = json.load(f)
        f.close()
        payload = json.dumps(data)
        json_object = json.dumps(data, indent=4)
        logger.debug(json_object)
        resps = cl.post("/api/library/option-type-lists", data = payload)
        logger.debug(resps.json())
        
def inject_inputs():
    """
    The inject_inputs function is used to inject the input payloads into the system. 
    It will look for a folder called 'input_payload' in your content pack and then it will look for files that match the pattern defined by input_inject_filter_pattern.  
    The default value of this variable is *.json, so it will find all json files in that directory and attempt to inject them into the system.
    
    :return: A list of the input types that were injected
    :doc-author: Trelent
    """
    logger = loghandler.get_logger(__name__)
    cl = RequestsApi()
    cp_dir = os.path.join(contentpack_base_folder,os.environ.get("contentpack"),input_payload_folder,input_inject_filter_pattern)
    files = glob.glob(cp_dir)
    # FIXME - need to add a way for it to add a tag on the item that it broke on.  
    for file in files:
        logger.debug(file)
        with open(file,'r') as f:
            data = json.load(f)
        f.close()
        try: 
            if data['optionType']['optionList'] != None:
                option_list_name = urllib.parse.quote(data['optionType']['optionList']['name'])
                logger.debug(option_list_name)
                resp = cl.get(f'/api/library/option-type-lists?name={option_list_name}')
                logger.debug(resp.json())
                resp = resp.json()
                option_list_id = resp['optionTypeLists'][0]['id']
                logger.debug(option_list_id)
                data['optionType']['optionList']['name'] = option_list_id
                data['optionType']['optionList']['id'] = data['optionType']['optionList'].pop('name')
        except IndexError as e:
            logger.warning(f"Failed to find option list for {file}")
            logger.warning('Error: %s', e)
            logger.warning('Data: %s', data)
        payload = json.dumps(data)
        json_object = json.dumps(data, indent=4)
        logger.debug(json_object)
        resp = cl.post("/api/library/option-types", data = payload)
        
def inject_workflow():
    """
    The inject_workflow function injects a workflow into the MoEML API.
    The function takes one argument, which is the path to a directory containing
    a set of JSON files that describe workflows. The function will iterate through 
    the directory and read each file, injecting each workflow into the API.
    
    :param inputdir: Specify the directory that contains the files to be injected into workflows
    :return: The response from the api call
    :doc-author: Trelent
    """
    logger = loghandler.get_logger(__name__)
    cl = RequestsApi()
    cp_dir = os.path.join(contentpack_base_folder,os.environ.get("contentpack"),workflow_payload_folder,workflow_inject_filter_pattern)
    files = glob.glob(cp_dir)
    for file in files:
        logger.debug(file)
        with open(file,'r') as f:
            data = json.load(f)
        f.close()
        for x in data['taskSet']['tasks']:
            task_name = urllib.parse.quote(x['taskId'])
            logger.debug(task_name)
            resp = cl.get(f"/api/tasks?name={task_name}")
            logger.debug(resp.json())
            resp = resp.json()
            task_id = resp['tasks'][0]['id']
            logger.debug(task_id)
            x['taskId'] = task_id
            logger.debug(x)
        option_list_ids = []
        for ot in data['taskSet']['optionTypes']:
            ot_name = urllib.parse.quote(ot)
            logger.debug(ot_name)
            resp = cl.get(f"/api/library/option-types?name={ot_name}")
            logger.debug(resp.json())
            resp = resp.json()
            option_list_ids.append(resp['optionTypes'][0]['id'])  
        data['taskSet']['optionTypes'] = option_list_ids
        logger.debug(option_list_ids)
        payload = json.dumps(data)
        json_object = json.dumps(data, indent=4)
        logger.debug(json_object)
        resps = cl.post("/api/task-sets", data = payload)
        logger.debug(resps.json())
        
        
def inject_whitelabel(): 
    """
    The inject_whitelabel function will inject the whitelabel settings into Graylog.
        The function will look for a folder called 'whitelabel' in the contentpack directory. 
        It will then look for files that match the pattern '*.json'. 
        If it finds any, it will read them and inject them into Graylog using PUT /api/whitelabel-settings.
    
    :return: Nothing
    :doc-author: Trelent
    """
    logger = loghandler.get_logger(__name__)
    cl = RequestsApi()
    cp_dir = os.path.join(contentpack_base_folder,os.environ.get("contentpack"),whitelabel_payload_folder,whitelabel_inject_filter_pattern)
    files = glob.glob(cp_dir)
    for file in files:
        with open(file,'r') as f:
            data = json.load(f)
        f.close()
        payload = json.dumps(data)
        json_object = json.dumps(data, indent=4)
        logger.debug(json_object)
        resps = cl.put("/api/whitelabel-settings", data = payload)
        logger.debug(resps.json())
        #TODO - add if statements to check if pngs are there are not. 
        if data['whitelabelSettings']['headerLogo'] != None:
            header_logo = data['whitelabelSettings']['headerLogo']
            header_logo = header_logo.replace(" ","")
            logger.debug(header_logo)
            file_path = os.path.join(contentpack_base_folder,os.environ.get("contentpack"),whitelabel_payload_folder,header_logo)
            files = {"headerLogo.file": (header_logo, open(file_path, "rb"), "image/png")}
            resps = cl.post("/api/whitelabel-settings/images", files = files)
            logger.debug(resps.json())
        if data['whitelabelSettings']['loginLogo'] != None:
            login_logo = data['whitelabelSettings']['loginLogo']
            login_logo = login_logo.replace(" ","")
            logger.debug(login_logo)
            file_path = os.path.join(contentpack_base_folder,os.environ.get("contentpack"),whitelabel_payload_folder,login_logo)
            files = {"loginLogo.file": (login_logo, open(file_path, "rb"), "image/png")}
            resps = cl.post("/api/whitelabel-settings/images", files = files)
            logger.debug(resps.json())
        if data['whitelabelSettings']['footerLogo'] != None:
            footer_logo = data['whitelabelSettings']['footerLogo']
            footer_logo = footer_logo.replace(" ","")
            logger.debug(login_logo)
            file_path = os.path.join(contentpack_base_folder,os.environ.get("contentpack"),whitelabel_payload_folder,footer_logo)
            files = {"footerLogo.file": (footer_logo.replace(' ',''), open(file_path, "rb"), "image/png")}
            resps = cl.post("/api/whitelabel-settings/images", files = files)
            logger.debug(resps.json())
            
def inject_clouds():
    logger = loghandler.get_logger(__name__)
    cl = RequestsApi()
    def getgroups():
        groups = cl.get("/api/groups").json()
        group_id = groups["groups"][0]["id"]
        return group_id
    cp_dir = os.path.join(contentpack_base_folder,os.environ.get("contentpack"),cloud_payload_folder,cloud_pattern)
    files = glob.glob(cp_dir)
    for file in files:
        with open(file,'r') as f:
            data = json.load(f)
        f.close()
        json_object = json.dumps(data, indent=4)
        data['zone']['groupId'] = getgroups()
        cloudid = cl.post("/api/zones", data = json_object).json()
        cloudid = cloudid["zone"]["id"]
        group_ids = cl.get("/api/groups").json()
        for x in group_ids["groups"]:
            group_id = x['id']
            payload = {
                 "group": {
                        "zones": [
                        {
                            "id": cloudid
                        }
                        ]
                    }
            }
            payload = json.dumps(payload)
            response = cl.put(f"/api/groups/{group_id}/update-zones", data = payload).json()
            logger.debug(response)

def inject_integrations():
    logger = loghandler.get_logger(__name__)
    cl = RequestsApi()
    cp_dir = os.path.join(contentpack_base_folder,os.environ.get("contentpack"),integration_payload_folder,integration_pattern)
    files = glob.glob(cp_dir)
    for file in files:
        with open(file,'r') as f:
            data = json.load(f)
        f.close()
        payload = json.dumps(data)
        resp = cl.post("/api/integrations", data = payload).json()
        logger.debug(resp)
        if resp['success'] is True:
            logger.info("Integration successfully created")
        if resp['success'] is False:
            logger.error("Integration creation failed")
            logger.error(resp)
