'''MACKS will enumerate configuration data about your Meraki environment, as well as collect data including network events.
'''

import argparse
import csv
import meraki
import os
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--apikey', type=str, help='API key for your org')
parser.add_argument('-e', '--enum', action='store_true', help='only enumerate orgs info and not collect network events')
parser.add_argument('-d', '--dir', type=str, help='folder to store output reports to')
args = parser.parse_args()

#Initializes the Meraki Dashboard API client
dashboard = meraki.DashboardAPI( 
        api_key = args.apikey,
        base_url = 'https://api.meraki.com/api/v1/',
        output_log=False,
        log_file_prefix=os.path.basename(__file__)[:-3],
        log_path='logs',
        print_console=True
        )

#Writes column headers for .csv files
def csv_write_headers(headers, outfile):
    with open(outfile, 'w', newline='') as out:
        hwriter = csv.writer(out)
        hwriter.writerow(headers)

#Writes data for .csv files
def csv_write_data(results, outfile):
    with open(outfile, 'a', newline='') as out:
        hwriter = csv.writer(out)
        hwriter.writerow(results)

#This function enumerates configuration information about the Meraki environment
def enum_orgs():

    orgs = dashboard.organizations.getOrganizations()
    for org in orgs:
        epath = args.dir + '\\' + org['name'] + '\\enum'
        if not os.path.exists(epath):
            os.makedirs(epath)
        org_df = pd.DataFrame(orgs)
        org_df.to_csv(epath + '\\orgs.csv', index=False)

        try:
            licenses = dashboard.organizations.getOrganizationLicenses(org['id'])
            licenses_df = pd.DataFrame(licenses)
            licenses_df.to_csv(epath + '\\licenses.csv', index=False)

        except meraki.APIError as e:
            print(str(e))

        products = dashboard.organizations.getOrganizationInventoryDevices(org['id'])
        products_df = pd.DataFrame(products)
        products_df.to_csv(epath + '\\device inventory.csv', index=False)
    
        networks = dashboard.organizations.getOrganizationNetworks(org['id'])
        for network in networks:
            net_df = pd.DataFrame(networks)
            net_df.to_csv(epath + '\\networks.csv', index=False)
                
            clients = dashboard.networks.getNetworkClients(network['id'])
            client_df = pd.DataFrame(clients)
            client_df.to_csv(epath + '\\network clients.csv', index=False)
            
            traffic_settings = dashboard.networks.getNetworkTrafficAnalysis(network['id'])
            print(traffic_settings)
            traffic_set_df = pd.DataFrame(traffic_settings)
            traffic_set_df.to_csv(epath + '\\traffic settings.csv', index=False)
            return(orgs, networks)
            
#This function collects network events from all networks in each org and write all events to one .csv file per network.
def get_net_events():
    orgs = dashboard.organizations.getOrganizations()
    for org in orgs:
        
        networks = dashboard.organizations.getOrganizationNetworks(org['id'])
        products = dashboard.organizations.getOrganizationInventoryDevices(org['id'])
        print(products)                         
        devices = ['appliance', 'secureConnect', 'switch', 'systemsManager', 'cellularGateway', 'wirelessController', 'camera']
        

        for device in devices:
            try:
                
                for network in networks:
                    net_events = dashboard.networks.getNetworkEvents(network['id'], productType=device, total_pages='all', perPage=1000)

                    headers = ['occurredAt', 'networkId', 'type', 'description', 'clientId', 'clientDescription', 'clientMac', 'category',	'deviceSerial',	'deviceName', 'eventData']
                    
                    net_path = args.dir + '\\' + org['name'] + '\\data' + '\\' + network['name']
                    if not os.path.exists(net_path):
                        os.makedirs(net_path)
                    csv_write_headers(headers, net_path + '\\' + network['name'] + '_network events.csv')

                    events = net_events['events']
                    for item in events:
                        k1 = item.keys()   
                        k2 = item.values()
                        event_data = item.items()
                    
                        csv_write_data(k2, net_path + '\\' + network['name'] + '_network events.csv')

                    
            except meraki.APIError as e:
                if '400 Bad Reuest' in str(e):
                    print(e)
                    print(e.status, e.reason)
                    continue
    
                       
def main():

    if args.enum:
        enum_orgs()
        exit

    else:
        enum_orgs()
        get_net_events()
    

if __name__ == '__main__':
    main()
    


