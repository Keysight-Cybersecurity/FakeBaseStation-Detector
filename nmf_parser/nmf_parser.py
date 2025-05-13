from .data_loader import load_data

def parser():
    data = load_data()
    rrcsm_messages = []
    for line in data:
        fields = line.split(",")
        if fields[0] == "RRCSM":
            rrcsm_messages.append(fields)
    
    print(rrcsm_messages)