import requests
from bs4 import BeautifulSoup
import csv

# Function to fetch and parse HTML
def fetch_and_parse_html(id_value):
    url = f"https://earlylearningprograms.dhs.ri.gov/Provider/ViewProviderInfo?ProviderId={id_value}"
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser'), url

# Function to extract data from the parsed HTML
def extract_data(soup, url):
    data = {}

    # Add URL to the data
    data['URL'] = url

    # Extract basic details with fallback to 'N/A'
    data['ProviderName'] = soup.find('label', {'for': 'ProviderName'}).text.strip() if soup.find('label', {'for': 'ProviderName'}) and soup.find('label', {'for': 'ProviderName'}).text.strip() else 'N/A'
    data['ProviderFullAddress'] = soup.find('label', {'for': 'ProviderFullAddress'}).text.strip() if soup.find('label', {'for': 'ProviderFullAddress'}) and soup.find('label', {'for': 'ProviderFullAddress'}).text.strip() else 'N/A'
    data['ProviderTelephone'] = soup.find('label', {'for': 'ProviderTelephone'}).text.replace('Telephone: ', '').strip() if soup.find('label', {'for': 'ProviderTelephone'}) and soup.find('label', {'for': 'ProviderTelephone'}).text.strip() else 'N/A'
    data['ProviderEmail'] = soup.find('label', {'for': 'ProviderEmail'}).find('a').text.strip() if soup.find('label', {'for': 'ProviderEmail'}) and soup.find('label', {'for': 'ProviderEmail'}).find('a') else 'N/A'
    data['ProviderWebsite'] = soup.find('label', {'for': 'ProviderWebsite'}).find('a').text.strip() if soup.find('label', {'for': 'ProviderWebsite'}) and soup.find('label', {'for': 'ProviderWebsite'}).find('a') else 'N/A'
    data['About Us'] = soup.find('label', {'for': ''}).text.strip() if soup.find('label', {'for': ''}) and soup.find('label', {'for': ''}).text.strip() else 'N/A'
    data['Setting'] = soup.find('label', string='Setting:').find_next_sibling('label').text.strip() if soup.find('label', string='Setting:') and soup.find('label', string='Setting:').find_next_sibling('label') else 'N/A'
    data['Accepts CCAP'] = soup.find('label', string='Accepts CCAP:').find_next_sibling('label').text.strip() if soup.find('label', string='Accepts CCAP:') and soup.find('label', string='Accepts CCAP:').find_next_sibling('label') else 'N/A'
    data['License Expires'] = soup.find('label', string='License Expires:').find_next_sibling('label').text.strip() if soup.find('label', string='License Expires:') and soup.find('label', string='License Expires:').find_next_sibling('label') else 'N/A'
    data['License Capacity'] = soup.find('label', string='License Capacity:').find_next_sibling('label').text.strip() if soup.find('label', string='License Capacity:') and soup.find('label', string='License Capacity:').find_next_sibling('label') else 'N/A'
    data['COVID Capacity'] = soup.find('label', string='COVID Capacity:').find_next_sibling('label').text.strip() if soup.find('label', string='COVID Capacity:') and soup.find('label', string='COVID Capacity:').find_next_sibling('label') else 'N/A'
    data['Availability'] = soup.find('label', string='Availability:').find_next_sibling('label').text.strip() if soup.find('label', string='Availability:') and soup.find('label', string='Availability:').find_next_sibling('label') else 'N/A'
    data['Languages Spoken'] = soup.find('label', string='Languages Spoken:').find_next_sibling('label').text.strip() if soup.find('label', string='Languages Spoken:') and soup.find('label', string='Languages Spoken:').find_next_sibling('label') else 'N/A'
    data['RIDE CECE Approval'] = soup.find('label', string='RIDE CECE Approval:').find_next_sibling('label').text.strip() if soup.find('label', string='RIDE CECE Approval:') and soup.find('label', string='RIDE CECE Approval:').find_next_sibling('label') else 'N/A'
    data['Contact Person'] = soup.find('label', string='Contact Person:').find_next_sibling('label').text.strip() if soup.find('label', string='Contact Person:') and soup.find('label', string='Contact Person:').find_next_sibling('label') else 'N/A'
    data['Program Status'] = soup.find('label', string='Program Status:').find_next_sibling('label').text.strip() if soup.find('label', string='Program Status:') and soup.find('label', string='Program Status:').find_next_sibling('label') else 'N/A'

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours_of_operation = {}
    for day in days:
        hours_label = soup.find('label', string=f'{day} :')
        hours = hours_label.find_next_sibling('label').text.strip() if hours_label and hours_label.find_next_sibling('label') else '-'
        hours_of_operation[day] = hours
    data.update(hours_of_operation)

    data['Accreditations'] = soup.find('label', {'for': 'Acrreditatons'}).find_next('span').text.strip() if soup.find('label', {'for': 'Acrreditatons'}) and soup.find('label', {'for': 'Acrreditatons'}).find_next('span') else 'N/A'

    # Selecting the reports section
    reports_section = soup.find('div', class_='panel panel-primary')

    # Finding all <a> tags within the reports section
    if reports_section:
        report_links = reports_section.find_all('a', class_='dontSpin')
        data['Report Count'] = len(report_links) if report_links else 'N/A'
    else:
        data['Report Count'] = 'N/A'

    age_group_details = {}
    age_group_rows = soup.select('table#AgeGroupModelGrid tbody tr')
    for row in age_group_rows:
        columns = row.find_all('td')
        if columns:
            age_group = columns[0].text.strip() if columns[0].text.strip() else '-'
            availability = columns[1].text.strip() if columns[1].text.strip() else '-'
            license_capacity = columns[2].text.strip() if columns[2].text.strip() else "-"
            age_group_details[f'Availability : {age_group}'] = f'{availability} - Capacity:{license_capacity}'
        else:
            age_group_details[f'Availability : {age_group}'] = '-'
    data.update(age_group_details)

    return data

# CSV Headers
csv_header = ['URL', 'ProviderName', 'ProviderFullAddress', 'ProviderTelephone', 'ProviderEmail', 'ProviderWebsite',
              'About Us', 'Setting','Accepts CCAP','License Expires','License Capacity','COVID Capacity','Availability','Languages Spoken','RIDE CECE Approval','Contact Person','Program Status','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
              'Accreditations', 'Report Count', 'Availability : Infant', 'Availability : Preschool', 
              'Availability : School Age', 'Availability : Toddler']

with open('daycare_info.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

    # Loop through IDs from 850 to 870
    for id_value in range(850, 870):
        print(f"Processing ID: {id_value}")
        soup, url = fetch_and_parse_html(id_value)
        data = extract_data(soup, url)
        data_row = [data.get(field, '-') for field in csv_header]
        writer.writerow(data_row)
