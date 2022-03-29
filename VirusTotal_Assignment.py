try:
    import json
except ImportError:
    import simplejson as json
import requests
import pandas
import datetime
import time

# Please enter the file's path of the URLs to be checked
file_path = str(input('Please Enter The File Path: '))
input_CSV = pandas.read_csv(file_path)
Urls = input_CSV['Domain'].tolist()

API_key = '7459dcceaae97bf8fbed29997d9b05003db3e42c92e4de20ddde4e9bf2cb053f'
url = 'https://www.virustotal.com/vtapi/v2/url/report'


# A function that classifies a site as safe or risk
def check_if_url_safe(j_response):
    results = []
    if_risk = "Safe"
    for x in j_response['scans']:
        get_result = j_response['scans'].get(x).get("result")
        results.append(get_result)
    #print(results)
    for y in results:
        if y == 'malicious site' or y == 'phishing site' or y == 'malware site':
            if_risk = "Risk"
    return if_risk


# A function that receives a site and checks whether it has been  queried in the last 30 minutes
def if_checked_in_30_last_minutes(site):
    if_to_check_site = True
    now_time = datetime.datetime.now()
    output_CSV = pandas.read_csv("URLs_Status.csv")
    site_list = output_CSV['URL'].tolist()
    #print(site_list)
    if site in site_list:
        index = site_list.index(site)
        last_sample_time = datetime.datetime.strptime(output_CSV['Sample_Time'][index], '%Y-%m-%d %H:%M:%S.%f')
        last_sample_and_now_diff = (now_time - last_sample_time).total_seconds() / 60
        # If 30 minutes have not passed since the last check, the site will not check
        if last_sample_and_now_diff < 30:
            if_to_check_site = False
        # Otherwise, the test data will be updated in the file
        else:
            if_to_check_site = False
            update_site_info(site, index)
    return if_to_check_site


# If a site has not been queried in the last 30 minutes and already appears in the output file, will update the test fields for it
def update_site_info(site, index):
    up_parameters = {'apikey': API_key, 'resource': site}
    up_response = requests.get(url=url, params=up_parameters)
    up_json_response = json.loads(up_response.text)
    up_sites_risk = check_if_url_safe(up_json_response)
    up_total_voting = up_json_response['total']
    up_sample_time = datetime.datetime.now()
    output_CSV = pandas.read_csv("URLs_Status.csv")
    output_CSV.at[index, 'Sample_Time'] = up_sample_time
    output_CSV.at[index, 'Sites_Risk'] = up_sites_risk
    output_CSV.at[index, 'Total_Voting'] = up_total_voting
    output_CSV.to_csv("URLs_Status.csv", index=False)


# Check the list of the sites obtained from the URLs file
for i in Urls:
    check_site = if_checked_in_30_last_minutes(i)
    # A new site that has not been queried yet
    if check_site:
        parameters = {'apikey': API_key, 'resource': i}
        response = requests.get(url=url, params=parameters)
        json_response = json.loads(response.text)
        sites_risk = check_if_url_safe(json_response)
        total_voting = json_response['total']
        sample_time = datetime.datetime.now()
        row_in = pandas.DataFrame([[i, sample_time, sites_risk, total_voting]],
                                  columns=['URL', 'Sample_Time', 'Sites_Risk', 'Total_Voting'])
        row_in.to_csv('URLs_Status.csv', mode='a', header=False, index=False)
    # we can check up to 4 sites per minute
    time.sleep(15)
