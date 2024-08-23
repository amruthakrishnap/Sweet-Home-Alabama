import os
import csv
import time
from playwright.sync_api import sync_playwright

def safe_text(locator, timeout=2000):
    try:
        return locator.text_content(timeout=timeout).strip()
    except:
        return "N/A"

def scrape_and_save_data(page, csv_writer, zipcode):
    page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_LicenseNumberLabel_0').wait_for(timeout=5000)

    license_number = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_LicenseNumberLabel_0'))
    facility_name = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_FacilityNameLabel_0'))
    address = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_FacilityStreetLabel_0')) + "\n" + \
              safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_FacilityCityLabel_0')) + ", " + \
              safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_FacilityStateLabel_0')) + " " + \
              safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_FacilityZipLabel_0')) + "\n" + \
              safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_CountyNameLabel_0')) + " County"
    email = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_EmailLabel_0 a')).replace('mailto:', '')
    facility_type = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_FacilityTypeLabel_0'))
    phone = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_PhoneLabel_0 a'))
    fax = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_FaxLabel_0'))
    subsidy_program = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_SubsidyLabel_0'))
    last_inspection_date = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_InspectionDateLabel_0'))
    classification = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_ClassDescriptionLabel_0'))
    sanitation_score = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptBasicFacilityInfo_SanitationScoreLabel_0'))
    license_type = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptLicenseInfo_lblLicenseType_0'))
    effective_date = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptLicenseInfo_lblFromDate_0'))
    age_range = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptLicenseInfo_lblAgeRange_0'))
    total_points = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptLicenseInfo_rptScores_0_lblTotalScore_0'))
    approved_capacity_1st_shift = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptLicenseInfo_lblFirstShiftCapacity_0'))
    license_restrictions = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptLicenseInfo_rptRestrictions_0_lblRestriction_0'))

    # Additional Details
    program_standards_points = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptLicenseInfo_rptScores_0_lblProgramStandardsPoints_0'))
    max_program_standards_points = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptLicenseInfo_rptScores_0_lblProgramStandardsMaxPoints_0'))
    educational_standards_points = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptLicenseInfo_rptScores_0_lblEducationalStandardsPoints_0'))
    max_educational_standards_points = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptLicenseInfo_rptScores_0_lblEducationalStandardsMaxPoints_0'))
    quality_points_earned = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptLicenseInfo_rptScores_0_lblThirdScorePoints_0'))
    max_quality_points = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_rptLicenseInfo_rptScores_0_lblMaxThirdScorePoints_0'))
    owner_name = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_lblOwnerName'))
    mailing_address = safe_text(page.locator('#dnn_ctr1464_View_FacilityDetail_lblOwnerMailingAddress')).replace('<br>', '\n').strip()
    print(f"Scraping For License Number : {license_number}")

    # Write to CSV
    csv_writer.writerow({
        'zipcode': zipcode,
        'License Number': license_number,
        'Facility Name': facility_name,
        'Address': address,
        'Email Address': email,
        'Facility/Program Type': facility_type,
        'Phone': phone,
        'Fax': fax,
        'Subsidy Program': subsidy_program,
        'Last Inspection Date': last_inspection_date,
        'Classification': classification,
        'Sanitation Score': sanitation_score,
        'License Type': license_type,
        'Effective Date': effective_date,
        'Age Range': age_range,
        'Total Points': total_points,
        'Approved Capacity (1st Shift)': approved_capacity_1st_shift,
        'License Restrictions': license_restrictions,
        'Program Standards Points Earned': program_standards_points,
        'Max Program Standards Points': max_program_standards_points,
        'Educational Standards Points Earned': educational_standards_points,
        'Max Educational Standards Points': max_educational_standards_points,
        'Quality Points Earned': quality_points_earned,
        'Max Quality Points': max_quality_points,
        'Owner Name': owner_name,
        'Mailing Address': mailing_address
    })

def process_page(page, csv_writer, zipcode):
    for i in range(10):  # Loop through possible rows
        row_selector = f'#dnn_ctr1464_View_rgSearchResults_ctl00__{i}'
        try:
            row = page.locator(row_selector)
            row.locator('a[href*="__doPostBack"]').first.click()
            scrape_and_save_data(page, csv_writer, zipcode)
            page.locator('#dnn_ctr1464_View_btnReturnToList').click()
            page.wait_for_load_state('domcontentloaded')
        except Exception as e:
            break

def click_page_number(page, page_number):
    try:
        page_link_selector = f'div.rgWrap.rgNumPart a:nth-of-type({page_number})'
        page.wait_for_selector(page_link_selector, timeout=10000)
        page_link = page.query_selector(page_link_selector)
        if page_link:
            page_link.click()
            print(f"Scraping For Page : {page_number}")
            page.wait_for_load_state('domcontentloaded')
            return True
        else:
            return False
    except Exception as e:
        return False

def extract_total_pages(page):
    try:
        page.wait_for_selector('div.rgWrap.rgInfoPart strong:nth-of-type(2)', timeout=5000)
        total_pages_element = page.query_selector('div.rgWrap.rgInfoPart strong:nth-of-type(2)')
        
        if total_pages_element:
            total_pages_text = total_pages_element.inner_text().strip()
            total_pages = int(total_pages_text)
            print(f"Total pages available for scrape: {total_pages}")
            return total_pages
        else:
            print("Only one page available for scrape.")
            return 1  # Assuming only one page if the total pages element is not found
    except Exception as e:
        print("Only one page available for scrape")
        return 1  # Default to one page if there's an error

def load_existing_zipcodes(file_path):
    if not os.path.exists(file_path):
        return set()

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return {row['zipcode'] for row in reader}

def remove_duplicates(file_path):
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8') as infile:
        reader = list(csv.DictReader(infile))
        unique_rows = {row['License Number']: row for row in reader}

    with open(file_path, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = reader[0].keys()
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_rows.values())

def main():
    zipcodes = ["27713", "27858", "27526", "27284", "28655", "27410", "28110", "27834", "27407", "27603", "27892","28366","27107","28540"]  # List of ZIP codes to process
    output_file = 'childcare_data.csv'
    existing_zipcodes = load_existing_zipcodes(output_file)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['zipcode', 'License Number', 'Facility Name', 'Address', 'Email Address', 'Facility/Program Type',
                          'Phone', 'Fax', 'Subsidy Program', 'Last Inspection Date', 'Classification', 'Sanitation Score',
                          'License Type', 'Effective Date', 'Age Range', 'Total Points', 'Approved Capacity (1st Shift)',
                          'License Restrictions', 'Program Standards Points Earned', 'Max Program Standards Points',
                          'Educational Standards Points Earned', 'Max Educational Standards Points', 'Quality Points Earned',
                          'Max Quality Points', 'Owner Name', 'Mailing Address']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header only if the file is empty
            if csvfile.tell() == 0:
                writer.writeheader()

            for zipcode in zipcodes:
                if zipcode in existing_zipcodes:
                    print(f"Skipping ZIP code {zipcode} as it has already been processed.")
                    continue
                
                try:
                    page.goto('https://ncchildcare.ncdhhs.gov/childcaresearch')
                    time.sleep(3)
                    print(f"Starting to scrape for ZIP code: {zipcode}")
                    
                    # Enter ZIP code and search
                    page.locator('input[name="dnn$ctr1464$View$txtZipCode"]').fill(zipcode)
                    time.sleep(2)
                    
                    # Click the search button
                    page.locator('input[name="dnn$ctr1464$View$btnSearch"]').click()
                    page.wait_for_load_state('domcontentloaded')
                    
                    # Find the total number of pages
                    total_pages = extract_total_pages(page)
                    if not total_pages:
                        continue
                    
                    for page_number in range(1, total_pages + 1):
                        process_page(page, writer, zipcode)
                        if page_number < total_pages:
                            clicked = click_page_number(page, page_number + 1)
                            if not clicked:
                                break
                except Exception as e:
                    print(f"Error processing ZIP code {zipcode}: {e}")

        # Remove duplicates
        remove_duplicates(output_file)
        print("Duplicates removed, script completed.")
        browser.close()

if __name__ == "__main__":
    main()
