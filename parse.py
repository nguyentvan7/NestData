import json
import csv
import dateutil.parser

historyFile = open('HomeHistory.json')
history = json.load(historyFile)

def getTimestamp(event):
    return event['timestamp']

homeEvents = history['structure_history'][0]['events']
homeEvents.sort(key=getTimestamp)
hvacEvents = []

for event in homeEvents:
    if event['event']['@type'] != 'type.googleapis.com/nestlabs.eventingapi.v1.EventEnvelope':
        continue
    if event['event']['event_data']['@type'] != 'type.nestlabs.com/nest.trait.hvac.HvacControlTrait.HvacStateChangeEvent':
        continue
    if len(hvacEvents) > 1 and bool(event['event']['event_data']['hvac_state']) == bool(hvacEvents[-1]['event']['event_data']['hvac_state']):
        continue
    hvacEvents.append(event)

# for hvacEvent in hvacEvents[0:10]:
#     print(hvacEvent['timestamp'])
#     print(hvacEvent['event']['event_data'])
#     print("--")
#     print()

with open('cycles.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    nextStateTime = hvacEvents[1]['timestamp']
    for index in range(0, len(hvacEvents[:-2])):
        hvacEvent = hvacEvents[index]
        row = []
        row.append(hvacEvent['timestamp'])

        isOn = int(bool(hvacEvent['event']['event_data']['hvac_state']))
        row.append(not(isOn))

        stateLength = dateutil.parser.isoparse(hvacEvents[index + 1]['timestamp']) - dateutil.parser.isoparse(hvacEvent['timestamp'])
        row.append(stateLength)

        writer.writerow(row)


historyFile.close()