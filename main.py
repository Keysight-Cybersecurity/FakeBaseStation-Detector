from nmf_parser import nmf_parser as nmf
from pprint import pprint
from asn1_decoder import *
from binascii import unhexlify
import json
from pycrate_mobile.NAS5G import *

def main():
    rrcsm_packets = nmf.parse()
    rrc_dec_messages = []
    for message in rrcsm_packets:
        rrc_dec_message = decode(message[9])
        # print(f"Decoded message: {rrc_dec_message}")
        # pprint(f"Type of rrc_dec_message: {type(rrc_dec_message)}")
        # pprint(f"Main paths: {rrc_dec_message}")
        rrc_dec_dict = json.loads(rrc_dec_message)
        rrc_dec_messages.append(rrc_dec_dict)

    NASMessages = []
    for entry in rrc_dec_messages:
        dlInformationTransfer = entry.get("criticalExtensions").get("dlInformationTransfer")
        # print(f"DLInformationTransfer: {dlInformationTransfer}")
        if dlInformationTransfer is not None:
            dedicatedNASMessage = dlInformationTransfer.get("dedicatedNAS-Message")
            if dedicatedNASMessage is not None and len(dedicatedNASMessage) > 0:
                NASMessages.append(dedicatedNASMessage)
    
    print(NASMessages[0])
    # print(decode_nas5g(unhexlify(NASMessages[0])))
    # nas_hex = bytes.fromhex(NASMessages[0])
    # pprint(dir(NAS5G))
    # nas_msg = parse_NAS5G(nas_hex)
    # print(nas_msg)

    def is_security_protected(nas_bytes):
        if len(nas_bytes) < 1:
            return False, None
        first_byte = nas_bytes[0]
        sec_hdr_type = (first_byte >> 4) & 0x0F
        return sec_hdr_type != 0, sec_hdr_type

    # Example:
    nas_bytes = bytes.fromhex(NASMessages[0])

    protected, hdr_type = is_security_protected(nas_bytes)
    if protected:
        print(f"Security protected NAS message (Security Header Type = {hdr_type})")
    else:
        print("Plain NAS message (not security protected)")
           
    

if __name__ == "__main__":
    main()
