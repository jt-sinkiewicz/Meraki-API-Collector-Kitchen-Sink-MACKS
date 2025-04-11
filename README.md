# Meraki-API-Collector-Kitchen-Sink-MACKS
MACKS is a python script that uses the Meraki Dashboard API client to enumerate configuration data about your Meraki environment, as well as collect data including network events.

MACKS is a python script that uses the Meraki Dashboard API client to enumerate configuration data about your Meraki environment, as well as collect data including network events. 

MACKS requires the following packages:

meraki
pandas

usage: macks_0.10.py [-h] [-a APIKEY] [-e] [-d DIR]

options:
  -h, --help            show this help message and exit
  -a APIKEY, --apikey APIKEY
                        API key for your org
  -e, --enum            only enumerate orgs info and not collect network events
  -d DIR, --dir DIR     folder to store output reports to
MACKS is read-only, it does not change or alter any data or configurations in any organization or networks. Only GET requests are used.

The following information will be collected for all organizations and networks that the API key being used has access to:

Org/Environment Enumeration:
	-Device Inventory
	-Network Clients
	-Information for all networks in each organization
	-Information for all organizations the API key being used has access to
	-Traffic Analysis Settings (Disabled, Basic, or Detailed)

Data Collection:
	-Network Events

The script will create the following file/folder structure:

\<output directory specified at command line>\<org1 name>\data\<network1 name>\<network1 name>_network events.csv
								    <network2 name>\<network2 name>_network events.csv
							      \enum\device inventory.csv
						              	   \network clients.csv
								   \networks.csv
								   \orgs.csv
								   \traffic settings.csv

