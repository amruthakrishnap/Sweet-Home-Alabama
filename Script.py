import requests
from bs4 import BeautifulSoup
import csv

# Function to fetch and parse the HTML content
def fetch_and_parse_html(id_value):
    url = f"https://apps.dhr.alabama.gov/daycare/daycare_results?ID={id_value}"
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

# Function to extract text based on label
def extract_label_value(soup, label):
    label_span = soup.find('span', string=lambda text: text and label in text)
    if label_span:
        value_span = label_span.find_next_sibling('span')
        if value_span:
            return value_span.text.strip()
    return "N/A"

# Helper function to extract text from tags
def find_text_by_label(soup, label):
    label_element = soup.find('span', string=label)
    if label_element:
        return label_element.find_next('span').text.strip()
    return "N/A"

# Function to count items in sections
def count_section_items(soup, section_label):
    section = soup.find('small', string=section_label)
    if section:
        table = section.find_next('table')
        if table:
            rows = table.find_all('tr')
            # If there's only one row and it contains "No" (e.g., "No Accreditations"), return the corresponding text
            if len(rows) == 1 and "No" in rows[0].text:
                return rows[0].text.strip()
            # Otherwise, return the count of rows (excluding the header if present)
            else:
                return len(rows) - 1
    return "NA"

# Extract data from HTML
def extract_data(soup):
    data = {}
    data['licensee'] = find_text_by_label(soup, "Licensee:")
    data['facility'] = find_text_by_label(soup, "Facility:")
    data['status'] = soup.find(string="Status:").find_next(string=True).strip() if soup.find(string="Status:") else "N/A"

    director_full_text = soup.find(string=lambda x: x and "Director" in x)
    data['director'] = director_full_text.split('-')[0].strip() if director_full_text else "N/A"

    data['phone'] = soup.find(string="Phone:").find_next(string=True).strip() if soup.find(string="Phone:") else "N/A"
    data['star_rating'] = extract_label_value(soup, "Alabama Quality Star Rating:")
    data['rating_expiry'] = soup.find(string=lambda x: "Rating Expiration Date:" in x)
    data['rating_expiry'] = data['rating_expiry'].find_next(string=True).strip() if data['rating_expiry'] else "N/A"
    
    data['daytime_hours'] = soup.find(string="Daytime Hours:").find_next(string=True).strip() if soup.find(string="Daytime Hours:") else "N/A"
    data['nighttime_hours'] = soup.find(string="Nighttime Hours:").find_next(string=True).strip() if soup.find(string="Nighttime Hours:") else "N/A"
    data['daytime_ages'] = soup.find(string="Daytime Ages:").find_next(string=True).strip() if soup.find(string="Daytime Ages:") else "N/A"
    data['nighttime_ages'] = soup.find(string="Nighttime Ages:").find_next(string=True).strip() if soup.find(string="Nighttime Ages:") else "N/A"

    data['street_address'] = extract_address(soup, "Street Address:")

    map_link_element = soup.find('a', string="Click for Interactive Map")
    data['map_link'] = map_link_element['href'] if map_link_element else "N/A"

    data['accreditations'] = count_section_items(soup, "List of Accreditations")
    data['adverse_actions'] = count_section_items(soup, "List of Adverse Actions")
    data['complaints'] = count_section_items(soup, "List of Substantiated Complaints")
    data['evaluation_reports'] = count_section_items(soup, "List of Evaluation/Deficiency Reports")

    return data

def extract_address(soup, label):
    address_lines = []
    label_span = soup.find('span', string=lambda text: text and label in text)
    if label_span:
        next_element = label_span.find_next_sibling()
        while next_element and (next_element.name == 'span' or next_element.name == 'br'):
            if next_element.name == 'span':
                address_lines.append(next_element.text.strip())
            next_element = next_element.find_next_sibling()
    return "\n".join(address_lines) if address_lines else "N/A"

# Prepare CSV file
csv_header = ['URL', 'Licensee', 'Facility', 'Status', 'Director', 'Phone', 'Daytime Hours', 'Nighttime Hours',
              'Daytime Ages', 'Nighttime Ages', 'Street Address', 
              'Click for Interactive Map', 'Alabama Quality Star Rating', 'Rating Expiration Date',
              'Accreditations', 'Adverse Actions', 'Substantiated Complaints', 'Evaluation/Deficiency Reports']

# Open CSV file in write mode
with open('daycare_info.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

    # Loop through IDs starting from 1
    for id_value in range(1, 5000):  # Set a high range to ensure processing continues until conditions met
        print(f"Processing ID: {id_value}")
        soup = fetch_and_parse_html(id_value)
        data = extract_data(soup)
        
        # Check if all critical fields are "N/A"
        if all(data[field] == "N/A" for field in ['licensee', 'facility', 'status','phone', 
                                                  'daytime_hours', 'nighttime_hours', 'daytime_ages', 'nighttime_ages']):
            print(f"Stopping as all critical fields are N/A for ID: {id_value}")
            break
        
        data_row = [f"https://apps.dhr.alabama.gov/daycare/daycare_results?ID={id_value}"] + [data[field] for field in ['licensee', 'facility', 'status', 'director', 'phone', 
                                                           'daytime_hours', 'nighttime_hours', 'daytime_ages', 
                                                           'nighttime_ages','street_address', 
                                                           'map_link', 'star_rating', 'rating_expiry',
                                                           'accreditations', 'adverse_actions', 
                                                           'complaints', 'evaluation_reports']]
        writer.writerow(data_row)

print("Data saved to daycare_info.csv")
