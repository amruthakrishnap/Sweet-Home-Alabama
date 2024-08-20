import requests
from bs4 import BeautifulSoup
import csv
import re

# Function to fetch and parse HTML
def fetch_and_parse_html(id_value):
    url = f"https://earlylearningprograms.dhs.ri.gov/Provider/ViewProviderInfo?ProviderId={id_value}"
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser'), url



def extract_data(soup, url):
    data = {}

    # Add URL to the data
    data['URL'] = url

    # Extract basic details with fallback to '-'
    data['ProviderName'] = soup.find('label', {'for': 'ProviderName'}).text.strip() if soup.find('label', {'for': 'ProviderName'}) and soup.find('label', {'for': 'ProviderName'}).text.strip() else '-'
    data['ProviderFullAddress'] = soup.find('label', {'for': 'ProviderFullAddress'}).text.strip() if soup.find('label', {'for': 'ProviderFullAddress'}) and soup.find('label', {'for': 'ProviderFullAddress'}).text.strip() else '-'
    zipcode_match = re.search(r'\b\d{5}\b', data['ProviderFullAddress'])
    data['Zipcode'] = zipcode_match.group(0) if zipcode_match else '-'
    label = soup.find('label', {'for': 'ProviderTelephone'})
    if label:
      phone_text = label.text.replace('Telephone:', '').strip()
      data['ProviderTelephone'] = phone_text if phone_text else '-'
    else:
        data['ProviderTelephone'] = '-'

    # data['ProviderEmail'] = soup.find('label', {'for': 'ProviderEmail'}).find('a').text.strip() if soup.find('label', {'for': 'ProviderEmail'}) and soup.find('label', {'for': 'ProviderEmail'}).find('a') else '-'

    maillabel = soup.find('label', {'for': 'ProviderEmail'})
    if maillabel:
        email_link = maillabel.find('a')
        if(email_link.text.strip() ==''):
            data['ProviderEmail'] = '-'
        else:
            email_text = email_link.text.strip()
            data['ProviderEmail'] = email_text
    else:
        data['ProviderEmail'] = '-'


    # data['ProviderWebsite'] = soup.find('label', {'for': 'ProviderWebsite'}).find('a').text.strip() if soup.find('label', {'for': 'ProviderWebsite'}) and soup.find('label', {'for': 'ProviderWebsite'}).find('a') else '-'

    weblabel = soup.find('label', {'for': 'ProviderWebsite'})
    if weblabel:
        web_link = weblabel.find('a')
        if(web_link.text.strip() ==''):
            data['ProviderWebsite'] = '-'
        else:
            web_text = web_link.text.strip()
            data['ProviderWebsite'] = web_text
    else:
        data['ProviderWebsite'] = '-'

    data['About Us'] = soup.find('label', {'for': ''}).text.strip() if soup.find('label', {'for': ''}) and soup.find('label', {'for': ''}).text.strip() else '-'

    setlabel = soup.find('label', string='Setting:')
    if setlabel:
        next_label = setlabel.find_next_sibling('label')
        if next_label:
            setting_text = next_label.text.strip()
            data['Setting'] = setting_text if setting_text else '-'
        else:
            data['Setting'] = '-'
    else:
        data['Setting'] = '-'

    # data['Setting'] = soup.find('label', string='Setting:').find_next_sibling('label').text.strip() if soup.find('label', string='Setting:') and soup.find('label', string='Setting:').find_next_sibling('label') else '-'

    CCAPlabel = soup.find('label', string='Accepts CCAP:')
    if CCAPlabel:
        next_label = CCAPlabel.find_next_sibling('label')
        if next_label:
            text = next_label.text.strip()
            data['Accepts CCAP'] = text if text else '-'
        else:
            data['Accepts CCAP'] = '-'
    else:
        data['Accepts CCAP'] = '-'

    # data['Accepts CCAP'] = soup.find('label', string='Accepts CCAP:').find_next_sibling('label').text.strip() if soup.find('label', string='Accepts CCAP:') and soup.find('label', string='Accepts CCAP:').find_next_sibling('label') else '-'

    liclabel = soup.find('label', string='License Expires:')

    if liclabel:
        next_label = liclabel.find_next_sibling('label')
        if next_label:
            text = next_label.text.strip()
            data['License Expires'] = text if text else '-'
        else:
            data['License Expires'] = '-'
    else:
        data['License Expires'] = '-'

    # data['License Expires'] = soup.find('label', string='License Expires:').find_next_sibling('label').text.strip() if soup.find('label', string='License Expires:') and soup.find('label', string='License Expires:').find_next_sibling('label') else '-'

    licclabel = soup.find('label', string='License Capacity:')

    if licclabel:
        next_label = licclabel.find_next_sibling('label')
        if next_label:
            text = next_label.text.strip()
            data['License Capacity'] = text if text else '-'
        else:
            data['License Capacity'] = '-'
    else:
        data['License Capacity'] = '-'

    # data['License Capacity'] = soup.find('label', string='License Capacity:').find_next_sibling('label').text.strip() if soup.find('label', string='License Capacity:') and soup.find('label', string='License Capacity:').find_next_sibling('label') else '-'

    cclabel = soup.find('label', string='COVID Capacity:')
    if cclabel:
        next_label = cclabel.find_next_sibling('label')
        if next_label:
            text = next_label.text.strip()
            data['COVID Capacity'] = text if text else '-'
        else:
            data['COVID Capacity'] = '-'
    else:
        data['COVID Capacity'] = '-'

    # data['COVID Capacity'] = soup.find('label', string='COVID Capacity:').find_next_sibling('label').text.strip() if soup.find('label', string='COVID Capacity:') and soup.find('label', string='COVID Capacity:').find_next_sibling('label') else '-'

    avlabel = soup.find('label', string='Availability:')

    if avlabel:
        next_label = avlabel.find_next_sibling('label')
        if next_label:
            text = next_label.text.strip()
            data['Availability'] = text if text else '-'
        else:
            data['Availability'] = '-'
    else:
        data['Availability'] = '-'


    # data['Availability'] = soup.find('label', string='Availability:').find_next_sibling('label').text.strip() if soup.find('label', string='Availability:') and soup.find('label', string='Availability:').find_next_sibling('label') else '-'

    lanlabel = soup.find('label', string='Languages Spoken:')
    if lanlabel:
        next_label = lanlabel.find_next_sibling('label')
        if next_label:
            text = next_label.text.strip()
            data['Languages Spoken'] = text if text else '-'
        else:
            data['Languages Spoken'] = '-'
    else:
        data['Languages Spoken'] = '-'


    # data['Languages Spoken'] = soup.find('label', string='Languages Spoken:').find_next_sibling('label').text.strip() if soup.find('label', string='Languages Spoken:') and soup.find('label', string='Languages Spoken:').find_next_sibling('label') else '-'

    ridlabel = soup.find('label', string='RIDE CECE Approval:')
    if ridlabel:
        next_label = ridlabel.find_next_sibling('label')
        if next_label:
            text = next_label.text.strip()
            data['RIDE CECE Approval'] = text if text else '-'
        else:
            data['RIDE CECE Approval'] = '-'
    else:
        data['RIDE CECE Approval'] = '-'

    # data['RIDE CECE Approval'] = soup.find('label', string='RIDE CECE Approval:').find_next_sibling('label').text.strip() if soup.find('label', string='RIDE CECE Approval:') and soup.find('label', string='RIDE CECE Approval:').find_next_sibling('label') else '-'

    cplabel = soup.find('label', string='Contact Person:')
    if cplabel:
        next_label = cplabel.find_next_sibling('label')
        if next_label:
            text = next_label.text.strip()
            data['Contact Person'] = text if text else '-'
        else:
            data['Contact Person'] = '-'
    else:
        data['Contact Person'] = '-'


    # data['Contact Person'] = soup.find('label', string='Contact Person:').find_next_sibling('label').text.strip() if soup.find('label', string='Contact Person:') and soup.find('label', string='Contact Person:').find_next_sibling('label') else '-'

    pslabel = soup.find('label', string='Program Status:')
    if pslabel:
        next_label = pslabel.find_next_sibling('label')
        if next_label:
            text = next_label.text.strip()
            data['Program Status'] = text if text else '-'
        else:
            data['Program Status'] = '-'
    else:
        data['Program Status'] = '-'


    # data['Program Status'] = soup.find('label', string='Program Status:').find_next_sibling('label').text.strip() if soup.find('label', string='Program Status:') and soup.find('label', string='Program Status:').find_next_sibling('label') else '-'

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours_of_operation = {}
    for day in days:
        hours_label = soup.find('label', string=f'{day} :')
        hours = hours_label.find_next_sibling('label').text.strip() if hours_label and hours_label.find_next_sibling('label') else '-'
        hours_of_operation[day] = hours
    data.update(hours_of_operation)

    data['Accreditations'] = soup.find('label', {'for': 'Acrreditatons'}).find_next('span').text.strip() if soup.find('label', {'for': 'Acrreditatons'}) and soup.find('label', {'for': 'Acrreditatons'}).find_next('span') else '-'

    # Selecting the reports section
    reports_section = soup.find('div', class_='panel panel-primary')

    # Finding all <a> tags within the reports section
    if reports_section:
        report_links = reports_section.find_all('a', class_='dontSpin')
        data['Report Count'] = len(report_links) if report_links else '-'
    else:
        data['Report Count'] = '-'

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
csv_header = ['URL', 'ProviderName', 'ProviderFullAddress','Zipcode', 'ProviderTelephone', 'ProviderEmail', 'ProviderWebsite',
              'About Us', 'Setting','Accepts CCAP','License Expires','License Capacity','COVID Capacity','Availability','Languages Spoken','RIDE CECE Approval','Contact Person','Program Status','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
              'Accreditations', 'Report Count', 'Availability : Infant', 'Availability : Preschool', 
              'Availability : School Age', 'Availability : Toddler']

with open('daycare_info.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

    # Loop through IDs from 850 to 870
    for id_value in range(1, 50):
        print(f"Processing ID: {id_value}")
        soup, url = fetch_and_parse_html(id_value)
        data = extract_data(soup, url)
        data_row = [data.get(field, '-') for field in csv_header]
        writer.writerow(data_row)
def clean_csv(file_path):
    with open(file_path, 'r') as infile, open('cleaned_daycare_info.csv', 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames  # Explicitly set the fieldnames from the reader

        if fieldnames is None:
            raise ValueError("No header row found in the input CSV file")

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if not (row['ProviderName'] == '-' and row['ProviderFullAddress'] == '-' and
                    row['ProviderTelephone'] == '-' and row['ProviderEmail'] == '-'):
                writer.writerow(row)

# Clean the CSV by removing rows with all specified columns as '-'
clean_csv('daycare_info.csv')
