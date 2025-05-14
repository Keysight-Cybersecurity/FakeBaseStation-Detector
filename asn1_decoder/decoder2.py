from binascii import unhexlify
from pycrate_asn1dir import RRCNR

def decode(rrc_message):
    possible_pdus = RRCNR.NR_RRC_Definitions._obj_ # The PDU definitions should be in there... not all of them are PDUs, and there are over 2000. I don't know which one you might want.
    pdu = RRCNR.NR_RRC_Definitions.DLInformationTransfer
    pdu.from_aper(unhexlify(rrc_message)) #Parse from ASN1 PER encoding to structured PDU.
    # bytes = pdu.to_aper() # Serialize from PDU to ASN1 PER encoding.

    # print(pdu.get_val_paths())
    return pdu.to_json() #.get_val_paths() # Returns all paths to all items in your pdu structure
    # elt.set_val(value) # Sets the ._val attribute of the element object (which is within the pdu) to value
    # elt.get_val_at(path), elt.set_val_at(path), elt.get_obj_at(path) return the value, set the value, and return the object respectively of the element at path.
    # \> path elements are lists of strings, where the strings are the names of elements. i.e. ["path","to","element"]

