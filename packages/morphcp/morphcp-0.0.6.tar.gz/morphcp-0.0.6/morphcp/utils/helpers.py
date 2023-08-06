#import morph_util.logging.loghandler as loghandler
import morphcp.logging.loghandler as loghandler
import sys
import os
#from morph_util.morphclass import RequestsApi
from morphcp.morphclass import RequestsApi

def result_pass_or_fail_id(element, json, ):
    """
    The result_pass_or_fail_id function is used to determine if the API call was successful or not.
    If it was successful, then the function returns a True boolean value and an id number for that object.
    If it failed, then the function returns a False boolean value and prints out all of the errors returned by
    the API call.
    
    :param element: Define the element in the json that contains
    :param json: Pass the json data to the function
    :param : Determine if the json response is successful or not
    :return: The id of the element that is passed to it
    :doc-author: Trelent
    """
    logger = loghandler.get_logger(__name__)
    if json["success"] is True:
        logger.info("Successful")
        logger.debug(json)
        id = json[element]['id']
        logger.debug(id)
    elif json["success"] is False:
        logger.error("Failed")
        logger.error(json['errors'])
        logger.error("Exiting")
        sys.exit(1)
        
def debug_printer(*args):
    """
    The debug_printer function prints the arguments passed to it.
    
    :param *args: Pass a non-keyworded, variable-length argument list
    :return: A tuple of the arguments passed to it
    :doc-author: Trelent
    """
    logger = loghandler.get_logger(__name__)
    logger.debug("###### DEBUG PRINTER ######")
    logger.debug("")
    for arg in args:
        logger.debug(arg)
    logger.debug("")
    logger.debug("###### DEBUG PRINTER ######")

def get_bearer(uname, upass):
    """
    The get_bearer function takes in a username and password, then returns the bearer token for that user.
    The function is called by other functions to get the bearer token of a user.
    
    :param uname: Specify the username of the user that is requesting a bearer token
    :param upass: Pass the password of the user to get_bearer
    :return: A bearer token for the user
    :doc-author: Trelent
    """
    if os.path.exists("../../*.dat"):
        print('its here')
    cl = RequestsApi()
    # TODO - update this to be the morpheus variable instead of the hardcoded value
    tenant_name = os.environ.get('instancename')
    tenant_name = tenant_name.replace(' ','')
    payload={'username': f"{tenant_name}\{uname}",'password': upass}
    bearer = cl.post("/oauth/token?grant_type=password&scope=write&client_id=morph-api", data = payload)
    bearer = bearer.json()
    return bearer['access_token']


def clear_session():
    """
    The clear_session function is used to clear the bearer token and delete all .dat files in the current directory.
    
    :return: None
    :doc-author: Trelent
    """
    logger = loghandler.get_logger(__name__)
    logger.info('Clearing bearer token and deleting .dat files.')
    for fname in os.listdir('.'):
        if fname.endswith('.dat') and fname.startswith(os.environ.get('instancename')):
            logger.info(f'File: {fname} is being deleted.')
            os.remove(fname)