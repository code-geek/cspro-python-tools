import json
from pprint import pprint

inRecord = False
inItem = False

records = list()

with open('dictionary.dcf') as inspectionfile:
    for line in inspectionfile:
        if line.strip() == '[Record]':
            inRecord = True
            thisrecord = {}
            continue

        if inRecord:
            if line.strip():
                splits = line.split('=')
                try:
                    thisrecord[splits[0].strip()] = splits[1].strip()
                except IndexError:
                    print(splits)

            if not line.strip():
                # inItem = True
                inRecord = False
                records.append(thisrecord)

pprint(records)
