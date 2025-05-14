import csv
from .data_loader import load_data

def parse() -> list:
    data = load_data()
    rrcsm_messages = []
    for line in data:
        reader = csv.reader([line])
        fields = next(reader)
        if fields[0] == "RRCSM":
            # fields[9].strip('"')
            rrcsm_messages.append(fields)
    
    # print(rrcsm_messages)
    return rrcsm_messages