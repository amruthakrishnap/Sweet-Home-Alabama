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
    zipcodes = ["27713","27858","27526","27284","28655","27410","28110","27834","27407","27603","28216","27529","28601","27405","28205","27265","27707","27107","28540","27106","27502","28546","28117","27360","27513","27705","28210","28273","28645","27615","27520","27215","27606","28262","28105","27540","27516","27613","28806","28213","27604","28306","28376","28212","28412","28451","27704","27127","28115","28214","27105","28092","27330","28079","28208","27909","28054","27292","27217","28403","27612","27893","27295","28348","27560","28226","28625","28562","27530","27320","27030","28411","28677","28304","27205","28052","28792","28056","28607","28104","28278","27609","27103","28311","28803","28409","27302","28405","27527","28270","28358","27332","27614","27511","27545","28146","27514","28211","28217","27253","27534","28752","28303","28031","27104","27804","28602","27455","28734","28715","28560","28086","27012","27278","27597","28112","27517","28081","27539","28144","27577","28590","28328","28150","28012","27607","27028","28001","27565","27591","28152","28681","28083","28326","28443","27262","28658","27870","27549","28390","27260","28037","28804","28379","28147","27889","28352","27701","28613","28209","27537","27288","28120","28787","27712","27312","28704","27501","28461","28334","27203","28786","28075","28401","27263","28570","28036","28659","28043","27401","28739","27101","28630","27546","28504","28532","28712","28312","28805","27576","28574","28906","27403","28547","27896","27801","27617","28374","27518","28034","27592","27803","27344","28327","27596","28501","28139","28779","27886","28539","27317","28203","28472","28732","27409","28716","27856","27523","27021","28714","27408","28301","28202","27244","27006","28023","28164","27358","28791","27536","28557","27282","28387","27525","27504","27055","27370","28365","28307","27574","28584","27510","28206","28315","27524","27892","28697","28021","28360","27023","27863","27214","28801","28016","28467","28364","28748","27932","27040","28134","28551","27249","27958","27948","28711","28372","28580","27522","28650","27608","27025","28462","28778","28460","27573","28638","28377","28345","28457","27944","27298","28612","27910","28425","28610","28723","27601","27052","28777","28470","28168","28516","28721","28103","28166","28904","27301","28384","28138","28333","28753","27045","27377","28513","28340","28621","28170","28445","27542","28754","28204","28207","27357","28107","27017","28690","27828","27569","28337","27376","28310","28469","28429","28713","27310","28174","28731","27557","27571","28466","27048","28465","27983","28657","27882","28320","28785","28422","27051","28090","27949","27822","28080","28114","28730","27018","27239","28604","28771","27371","28518","28128","28761","27505","28759","27041","28586","27258","27817","27325","27316","28127","27043","27509","28097","28040","27850","28463","27962","28428","27954","27583","27521","27572","28719","28543","28694","27823","27313","27013","28673","28768","28705","28382","28762","28675","28073","28530","28431","28339","28383","28782","27589","28124","27349","28479","28398","28722","28371","27807","28789","28163","27605","28572","27503","27837","27020","28391","28129","27563","28305","28356","28578","27855","27350","28701","28901","28609","27306","28458","28135","28642","28555","28678","27299","27851","28544","28394","27243","28651","28640","27235","28386","28634","28366","28636","27011","27891","28344","27921","28323","28468","28351","27379","27864","27209","28018","28478","28433","28692","27562","27976","27544","28756","27248","27027","27809","28741","27341","28751","28456","28643","27880","28160","28318","28726","28594","27830","28585","27839","27050","28223","27581","27311","28349","27883","27810","27207","28338","28729","27871","28098","28453","27541","27009","27326","28512","27929","27019","28905","28790","28542","28635","28605","27805","27283","27281","28341","27708","27816","27229","27874","27959","27844","28654","27925","27412","28088","27233","28676","27937","27053","27356","28626","28742","28071","28441","28159","28773","28515","28032","28480","28571","28137","27970","28525","28665","28454","28746","28033","28533","27846","28420","27355","28373","28669","28763","28125","28423","28526","28698","27109","27831","27832","28444","28523","28689","27865","27845","28670","28020","27852","28357","28395","27110","27508","27939","27924","28464","28622","27890","28660","28709","28743","27046","28679","27820","28396","28747","28119","27806","28455","27024","27812","27231","28538","27808","27559","28618","27007","28430","27695","28385","28167","28133","27212","28450","28369","28421","28685","28449","27926","27054","28347","27981","28435","27551","28617","27507","28393","28091","27986","27928","28573","28343","28399","27950","27888","28529","27305","27869","28623","27938","27016","28582","28508","28392","28740","28615","27411","27814","27935","28606","28521","27208","27553","28637","27315","27980","28684","27884","27343","27568","27842","28438","27252","27920","28436","28682","28432","27824","28783","28649","28693","27829","28717","28510","28447","28627","28683","28624","27957","27860","27047","27897","27927","28774","27242","27973","28009","28006","27818","28442","27947","27966","27946","27849","27847","28644","27826","27291","28531","27974","27857","27022","27876","28772","28527","28101","27843","27268","27506","28363","27878","28359","28631","28781","28007","28902","28766","28736","27916","28439","28448","27866","27922","27014","28332","27919","28556","27953","27813","27885","28579","27917","27960","27942","27979","27964","27819","28072","27853","27936","28274","27314","27531","28109","28528","28511","27862","28646","27923","28707","28718","28775","28452","28330","28519","27941","28702","28745","28017","27555","27872","28663","27943","28553","28757","28619","28325","27967","28077","28671","28434","27915","28909","27582","28308","27965","28577","27978","28042","27985","27969","27873","28524","27374","28735","27879","28667","27840","27247","27556","27351","28350","28708","27533","28587","27972","28575","28552","28672","27968","28375","27042","27956","27584","28367","28169","28520","28664","28668","27875","28788","28581","28076","28611","28720","28342","28089","28616","27982","27827","27201","28368","27259","27342","28102","27202","27861","28725","28554","27825","28749","28136","27594","27213","27256","28641","28733","28331","28652","28666","28362","27340","27821","28424","28628","28108","27841","28589","28653","28024","28378","28039","27881","28537","27877","28041"]  # List of ZIP codes to process
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
