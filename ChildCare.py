import requests
from bs4 import BeautifulSoup
import csv

# Function to fetch and parse HTML
def fetch_and_parse_html(id_value):
    url = f"https://earlylearningprograms.dhs.ri.gov/Provider/ViewProviderInfo?ProviderId={id_value}"
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

# Function to extract data from the parsed HTML
def extract_data(soup):
    data = {}

    # Extract basic details with fallback to 'N/A'
    data['ProviderName'] = soup.find('label', {'for': 'ProviderName'}).text.strip() if soup.find('label', {'for': 'ProviderName'}) else 'N/A'
    data['ProviderFullAddress'] = soup.find('label', {'for': 'ProviderFullAddress'}).text.strip() if soup.find('label', {'for': 'ProviderFullAddress'}) else 'N/A'
    data['ProviderTelephone'] = soup.find('label', {'for': 'ProviderTelephone'}).text.replace('Telephone: ', '').strip() if soup.find('label', {'for': 'ProviderTelephone'}) else 'N/A'
    data['ProviderEmail'] = soup.find('label', {'for': 'ProviderEmail'}).find('a').text.strip() if soup.find('label', {'for': 'ProviderEmail'}) else 'N/A'
    data['ProviderWebsite'] = soup.find('label', {'for': 'ProviderWebsite'}).find('a').text.strip() if soup.find('label', {'for': 'ProviderWebsite'}) else 'N/A'
    data['About Us'] = soup.find('label', {'for': ''}).text.strip() if soup.find('label', {'for': ''}) else 'N/A'
    data['Setting'] = soup.find('label', text='Setting:').find_next_sibling('label').text.strip() if soup.find('label', text='Setting:') else 'N/A'
    data['Accepts CCAP'] = soup.find('label', text='Accepts CCAP:').find_next_sibling('label').text.strip() if soup.find('label', text='Accepts CCAP:') else 'N/A'
    data['License Expires'] = soup.find('label', text='License Expires:').find_next_sibling('label').text.strip() if soup.find('label', text='License Expires:') else 'N/A'
    data['License Capacity'] = soup.find('label', text='License Capacity:').find_next_sibling('label').text.strip() if soup.find('label', text='License Capacity:') else 'N/A'
    data['COVID Capacity'] = soup.find('label', text='COVID Capacity:').find_next_sibling('label').text.strip() if soup.find('label', text='COVID Capacity:') else 'N/A'
    data['Availability'] = soup.find('label', text='Availability:').find_next_sibling('label').text.strip() if soup.find('label', text='Availability:') else 'N/A'
    data['Languages Spoken'] = soup.find('label', text='Languages Spoken:').find_next_sibling('label').text.strip() if soup.find('label', text='Languages Spoken:') else 'N/A'
    data['RIDE CECE Approval'] = soup.find('label', text='RIDE CECE Approval:').find_next_sibling('label').text.strip() if soup.find('label', text='RIDE CECE Approval:') else 'N/A'
    data['Contact Person'] = soup.find('label', text='Contact Person:').find_next_sibling('label').text.strip() if soup.find('label', text='Contact Person:') else 'N/A'
    data['Program Status'] = soup.find('label', text='Program Status:').find_next_sibling('label').text.strip() if soup.find('label', text='Program Status:') else 'N/A'

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours_of_operation = {}
    for day in days:
        hours_label = soup.find('label', text=f'{day} :')
        hours = hours_label.find_next_sibling('label').text.strip() if hours_label else '-'
        hours_of_operation[day] = hours
    data.update(hours_of_operation)

    data['Accreditations'] = soup.find('label', {'for': 'Acrreditatons'}).find_next('span').text.strip()

    reports_section = soup.find('label', {'for': 'Reports'})
    data['Report Count'] = len(reports_section.find_all('a')) if reports_section else 'N/A'

    age_group_details = {}
    age_group_rows = soup.select('table#AgeGroupModelGrid tbody tr')
    for row in age_group_rows:
        columns = row.find_all('td')
        age_group = columns[0].text.strip()
        availability = columns[1].text.strip()
        license_capacity = columns[2].text.strip() if columns[2].text.strip() else "N/A"
        age_group_details[f'Availability : {age_group}'] = f'{availability} - Capacity:{license_capacity}' if availability != "N/A" else "N/A"
    data.update(age_group_details)\

    return data
# CSV Headers
csv_header = ['ProviderName', 'ProviderFullAddress', 'ProviderTelephone', 'ProviderEmail', 'ProviderWebsite',
              'About Us', 'Setting','Accepts CCAP','License Expires','License Capacity','COVID Capacity','Availability','Languages Spoken','RIDE CECE Approval','Contact Person','Program Status','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
              'Accreditations', 'Report Count', 'Availability : Infant', 'Availability : Preschool', 
              'Availability : School Age', 'Availability : Toddler']

with open('daycare_info.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

    # Loop through IDs from 850 to 880
    for id_value in range(850, 870):
        print(f"Processing ID: {id_value}")
        soup = fetch_and_parse_html(id_value)
        data = extract_data(soup)
        data_row = [data.get(field, 'N/A') for field in csv_header]
        writer.writerow(data_row)

