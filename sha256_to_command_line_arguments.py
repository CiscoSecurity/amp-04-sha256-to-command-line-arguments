import sys
import configparser
import requests

# Specify the config file
configFile = 'api.cfg'

# Reading the config file to get settings
config = configparser.RawConfigParser()
config.read(configFile)
client_id = config.get('AMPE', 'client_id')
api_key = config.get('AMPE', 'api_key')

# Validate a command line parameter was provided
if len(sys.argv) < 2:
    sys.exit('Usage:\n %s 8133502266008b77de7921451e1210b0ef3f0ed2db7d8d3ee0c3350d856fa6fa' % sys.argv[0])

# Store the command line parameter
process_sha256 = sys.argv[1]

# Containers for output
computer_guids = {}
parent_to = {}

# Creat session object
# http://docs.python-requests.org/en/master/user/advanced/
# Using a session object gains efficiency when making multiple requests
session = requests.Session()
session.auth = (client_id, api_key)

# Define URL and parameters
activity_url = 'https://api.amp.cisco.com/v1/computers/activity'
payload = {'q': process_sha256}

# Query API
response = session.get(activity_url, params=payload)

# Decode JSON response
response_json = response.json()

# Name data section of JSON
data = response_json['data']

# Store unique connector GUIDs and hostnames
for entry in data:
    connector_guid = entry['connector_guid']
    hostname = entry['hostname']
    computer_guids.setdefault(connector_guid, {'hostname':hostname})

print('Computers found: {}'.format(len(computer_guids)))

# Query trajectory for each GUID
for guid in computer_guids:

    # Print the hostname and GUID that is about to be queried
    print('Querying: {} - {}'.format(computer_guids[guid]['hostname'], guid))

    trajectory_url = 'https://api.amp.cisco.com/v1/computers/{}/trajectory'.format(guid)
    trajectory_response = session.get(trajectory_url, params=payload)

    # # Decode JSON response
    trajectory_response_json = trajectory_response.json()

    # Name events section of JSON
    events = trajectory_response_json['data']['events']

    # Parse trajectory events to find the network events
    for event in events:
        event_type = event['event_type']
        if 'command_line' in event and 'arguments' in event['command_line']:
            arguments = event['command_line']['arguments']
            file_sha256 = event['file']['identity']['sha256']
            parent_sha256 = event['file']['parent']['identity']['sha256']
            if file_sha256 == process_sha256:
                if isinstance(arguments, list):
                    print(' '.join(arguments))
                else:
                    print(arguments)
            if parent_sha256 == process_sha256:
                child_file_name = event['file']['file_name']
                parent_to.setdefault(child_file_name, [])
                parent_to[child_file_name].append(arguments)

print('\nThis was also parent to {} processes'.format(len(parent_to)))
for process in parent_to:
    print(process)
    for arguments in parent_to[process]:
        if isinstance(arguments, list):
            print('  ', ' '.join(arguments))
        else:
            print(arguments)
