from pycrate_mobile.NAS5G import *
import pycrate_core.elt
from typing import Iterator
from binascii import unhexlify

# Logging
import logging
logger = logging.getLogger(__name__)


def getPathsFromNAS5G(element:pycrate_core.elt.Envelope)->list[str]:
    """
    Traverse the envelopes recursively and return all paths from all endpoints.
    Paths are of the format (path, value) where path is a list of strings.

    Args:
        element: the root element of all envelopes to explore. Usually this is the output of the parse_NAS5G function.
    
    Returns:
        paths: list of all elements found in calls to this function on leafs of current envelope node.
    
    """
    paths:list = []
    try:
        if element.CLASS in ["Envelope","Alt"]:
            for next_item in element._content:
                next_item:pycrate_core.elt.Element
                if next_item.CLASS == 'Atom':
                    if next_item._val == None and next_item._trans:
                        logger.info(f"getPathsFromNAS5G > Element {next_item._name} is transparent and has no value. It will not be added to paths.")
                    else:
                        paths.append((next_item.fullname().split("."), next_item._val))
                    #paths.append((next_item.fullname().split("."), next_item._val))
                elif next_item.CLASS == 'Alt':
                    paths+=getPathsFromNAS5G(next_item)
                elif next_item.CLASS == 'Envelope':
                    # Dirty workaround for placeholders (i.e. some items which have a L value of None), not 100% sure this works as intended.
                    # "Placeholders" that are either ont in the PDU, or are only evaluated at serialization time.
                    ignore_flag = False
                    for tlv_value in next_item._content:
                        if tlv_value._name == 'L' and tlv_value._val == None:
                            ignore_flag = True
                    if ignore_flag:
                        continue
                    else:
                        paths+=getPathsFromNAS5G(next_item)
                else:
                    logger.warning(f"functions.py > getPathsFromNAS5G : Class {next_item.CLASS} not considered.")
        else:
            logger.warning(f"Class {element.CLASS} is not managed in getPathsFromNAS5G.")
    except AttributeError as e:
        logger.warning(f"Element does not have CLASS attribute : {e}")
        #raise e

    return paths


# Returns absolute paths so that we can then use "set_val_at()" function to change the value we wanted.
# In case multiple paths match, all of them will be returned.
# This is NOT EFFICIENT (O(n*m)), but this is the only way I have found to have a general function that can find this.
def returnPathsFromEndpoint(paths: Iterator, endpoint:str) -> list:
    """
    Returns the list of all paths to a given ressource, where the ressource "endpoint" is given by its name.
    
    Flaw:
        Do note that one endpoint can have multiple paths.
        eg. path1 = [a, b, c, d] and path2 = [e, d, f, g] both have d as endpoint, and so both the paths will be returned.
    
    Args:
        paths: Iterator of paths, where paths are of the form (path, value), and path is a non-empty list of values.
        endpoint: name of the element we are getting the path of.

    Returns:
        valid_paths: list of all paths that contain the endpoint name. Can be empty.
    """
    valid_paths:list[list] = []
    for path in paths:
        if endpoint in path[0]: # Actual path, path[1] is endpoint value. We could think about getting path[1] too if we wanted the value.
            valid_paths.append(path[0])
    
    return valid_paths



def getObjectAt_NAS5G(pdu, path):
    """
    5GMM (NAS) equivalent of the ASN1 (NGAP) function get_obj_at. Returns first ATOM encountered on the path, or the endpoint of the path.

    Args:
        pdu: NAS-5G PDU using the pycrate 5GMM structure (Envelopes, Atoms, Elements...)
        path: list of strings describing the path to the element

    returns:
        First ATOM encountered on the path, or the endpoint of the path

    raises:
        AssertionError: if the first element on the path is not the first element of the PDU.
        Exception: if one of the elements in the path does not match an actual element in the PDU.
    
    """
    current_element = pdu
    path_depth = 1
    assert current_element._name == path[0]," getObjAt5GMM: First element of path is not root, aborting."
    while path_depth < len(path) and current_element.CLASS!="ATOM":
        i=0
        while current_element._by_name[i] != path[path_depth] and i < len(current_element._by_name):
            i+=1
        if i >= len(current_element._by_name):
            logger.name(f"Path {path} does not match actual item. Aborting.")
            raise Exception(f"Path {path} doesn't match actual item. Aborting")
        current_element = current_element._content[i]
        path_depth+=1
    return current_element

def flatten(nas5g_element):
    for elt in nas5g_element:
        if not elt.get_trans():
            print(elt)
        try:
            elt._content
            flatten(elt)
        except Exception:
            continue

def decode(nas5g_message):
    nas5G_pdu, err = parse_NAS5G(nas5g_message)
    if err != 0:
        logger.error(f"Error while parsing NAS5G message, code {err}")
        return err
    
    flatten(nas5G_pdu)
    for path in getPathsFromNAS5G(nas5G_pdu):
        print(path)

    print(getObjectAt_NAS5G(nas5G_pdu, ["5GMMRegistrationRequest", "PayloadContainerType"]))

