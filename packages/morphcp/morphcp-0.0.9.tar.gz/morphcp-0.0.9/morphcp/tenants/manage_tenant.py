import urllib
import json
import os

#from morph_util.morphclass import RequestsApi
from morphcp.morphclass import RequestsApi
#import morph_util.utils.helpers as morph_util
import morphcp.utils.helpers as morph_util
#from morph_util.vars import * 
from morphcp.vars import *
#import morph_util.logging.loghandler as loghandler
import morphcp.logging.loghandler as loghandler

def create_tenant():
    """
    The create_tenant function creates a new tenant in the Morpheus UI.
    It returns the id of the newly created tenant.
    
    :return: The id of the newly created tenant
    :doc-author: Trelent
    """
    cl = RequestsApi()
    logger = loghandler.get_logger(__name__)
    logger.info('Creating Tenant')
    base_tenant_role_id = cl.get(f'/api/roles?name={urllib.parse.quote(base_tenant_role_name)}')
    base_tenant_role_id = base_tenant_role_id.json()
    base_tenant_role_id = base_tenant_role_id["roles"][0]["id"]
    tenant_name = os.environ.get('instancename')
    subtenant = tenant_name.replace(' ','')
    payload = json.dumps({
        "account":{
        "name": tenant_name,
        "description": f'Morpheus Data HotShots Tenant: {tenant_name}',
        "subdomain": subtenant,
        "role": { "id": base_tenant_role_id},
        "active": True
        }
    })
    created_tenant_id = cl.post(f'/api/accounts', data = payload)
    created_tenant_id =created_tenant_id.json()
    morph_util.result_pass_or_fail_id('account',created_tenant_id)
    tenant_id = created_tenant_id['account']['id']
    logger.debug("Debug_Printer")
    morph_util.debug_printer(base_tenant_role_id,tenant_name,payload)
    logger.info("Created Tenant")
    return tenant_id
        


def create_tenant_admin(tenant_id):
    """
    The create_tenant_admin function creates a tenant admin user for the given tenant.
    The function accepts one argument, which is the id of the tenant to create a user for.

    
    :param tenant_id: Specify the tenant id for which the user will be created
    :return: The id of the newly created tenant admin user
    :doc-author: Trelent
    """
    cl = RequestsApi()
    logger = loghandler.get_logger(__name__)
    logger.info('Creating Tenant Admin')
    multi_tenant_role_id = cl.get(f'/api/users/available-roles?accountId={tenant_id}&name={urllib.parse.quote(multi_tenant_role_name)}')
    multi_tenant_role_id = multi_tenant_role_id.json()
    multi_tenant_role_id = multi_tenant_role_id['roles'][0]['id']
    payload = json.dumps({
        "user":{
            "username": tenant_admin_user_name,
            "email": 'Morpheus@local.local',
            "password": tenant_admin_password,
            "roles": [{"id": multi_tenant_role_id}],
            "receiveNotifications": False
            }
        })
    # hotshotUser_payload = json.dumps({
    #             "user":{
    #             "username": os.environ.get("hotshotusername"),
    #             "email": 'Morpheus@local.local',
    #             "password": hotshot_user_password,
    #             "roles": [{"id": multi_tenant_role_id}],
    #             "receiveNotifications": False
    #         }
    #     })
    create_admin_user = cl.post(f'/api/accounts/{tenant_id}/users', data = payload)
    #create_hotshotuser = cl.post(f'/api/accounts/{tenant_id}/users', data = hotshotUser_payload)
    create_admin_user = create_admin_user.json()
#    create_hotshotuser = create_hotshotuser.json()
    morph_util.debug_printer(f'User {create_admin_user}',f'Multitennat Role ID {multi_tenant_role_id}',f'Payload {payload}',f'Tenant Admin User{tenant_admin_user_name}')
    morph_util.result_pass_or_fail_id('user',create_admin_user)
    logger.info("Created Tenant Admin amd Hotshot User")