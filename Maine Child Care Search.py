import pandas as pd
from playwright.sync_api import sync_playwright
import time

def format_address_for_maps(address, zipcode):
    # Format the address for Google Maps directions
    formatted_address = address.replace(' ', '+').replace(',', '%2C')
    return f'https://www.google.com/maps?saddr={zipcode}&daddr={formatted_address}'

def scrape_zipcodes(zipcodes):
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()

        # Navigate to the website
        page.goto('https://search.childcarechoices.me/')
        time.sleep(1)
        page.click('input#rbSearchTypeZip')
        time.sleep(1)
        # Prepare to store results
        results = []

        for zipcode in zipcodes:
            # Fill the input field with the ZIP code
            page.fill('input[name="ctl00$MainContent$txtZip"]', zipcode)
            time.sleep(1)
            print(f"Scraping Happening for ZipCode : {zipcode} ")
            # Click the "Find Programs" button
            page.click('input[name="ctl00$MainContent$Button1"]')
            
            # Wait for the results to load
            page.wait_for_timeout(2000)
            results_text = page.text_content('h3#results-num-found')
            print(results_text)
            print("\n")

            # Extract data from the results
            providers = page.query_selector_all('div.address')
            details = page.query_selector_all('div.details')
            subdetails = page.query_selector_all('div.subdetails')
            ratings = page.query_selector_all('div.number img')

            for provider, detail, subdetail, rating in zip(providers, details, subdetails, ratings):
                provider_name = provider.text_content().strip()
                address = detail.inner_html().split('<br>')[0].strip()
                phone = detail.inner_html().split('PHONE: ')[1].strip().split('<br>')[0]
                
                subdetail_text = subdetail.inner_html()
                provider_type = subdetail_text.split('Provider Type: ')[1].split('<br>')[0]
                open_infant_slots = subdetail_text.split('Open Infant Slots, 6 weeks to 1 year old: ')[1].split('<br>')[0]
                open_toddler_slots = subdetail_text.split('Open Toddler Slots, 1-2 years old: ')[1].split('<br>')[0]
                open_preschool_slots = subdetail_text.split('Open Preschool Slots, 3-5 years old: ')[1].split('<br>')[0]
                open_school_age_slots = subdetail_text.split('Open School Age Slots, 5 years or older: ')[1].split('<br>')[0]
                accepts_ccap = subdetail_text.split('Accepts CCAP: ')[1].split('<')[0].strip()
                
                star_rating = rating.get_attribute('alt').strip()

                # Generate the driving direction link
                driving_direction = format_address_for_maps(address, zipcode)

                results.append({
                    'Zip Code': zipcode,
                    'Provider Name': provider_name,
                    'Address': address,
                    'Phone': phone,
                    'Provider Type': provider_type,
                    'Open Infant Slots': open_infant_slots,
                    'Open Toddler Slots': open_toddler_slots,
                    'Open Preschool Slots': open_preschool_slots,
                    'Open School Age Slots': open_school_age_slots,
                    'Accepts CCAP': accepts_ccap,
                    'Star Rating': star_rating,
                    'Driving Direction': driving_direction,
                })

            # Click the "Search Child Care" button to reset the search
            page.click('button#search-tab')
            page.wait_for_timeout(2000)

        # Convert results to DataFrame and save to CSV
        df = pd.DataFrame(results)
        df.to_csv('childcare_programs.csv', index=False)
        print("Data Saved to Childcare_programs.csv ")

        # Remove duplicates from the CSV file
        df = pd.read_csv('childcare_programs.csv')
        df = df.drop_duplicates()
        df.to_csv('childcare_programs.csv', index=False)
        print("Duplicates Removed and Data Saved to Childcare_programs.csv")

        # Close the browser
        browser.close()

if __name__ == "__main__":
    # List of ZIP codes to process
    zipcodes = ['03901','03902','03903','03904','03905','03906','03907','03908','03909','03910','03911','04001','04002','04003','04004','04005','04006','04008','04009','04010','04011','04013','04014','04015','04017','04019','04020','04021','04022','04024','04027','04028','04029','04030','04032','04033','04034','04037','04038','04039','04040','04041','04042','04043','04046','04047','04048','04049','04050','04051','04053','04054','04055','04056','04057','04061','04062','04063','04064','04066','04068','04069','04070','04071','04072','04073','04074','04076','04077','04078','04079','04082','04083','04084','04085','04086','04087','04088','04090','04091','04092','04093','04094','04095','04096','04097','04098','04101','04102','04103','04104','04105','04106','04107','04108','04109','04110','04112','04116','04122','04123','04124','04210','04211','04212','04216','04217','04219','04220','04221','04222','04223','04224','04225','04226','04227','04228','04230','04231','04234','04236','04237','04238','04239','04240','04241','04243','04250','04252','04253','04254','04255','04256','04257','04258','04259','04260','04261','04262','04263','04265','04266','04267','04268','04270','04271','04274','04275','04276','04280','04281','04282','04284','04285','04286','04287','04289','04290','04291','04292','04294','04330','04332','04333','04336','04338','04341','04342','04343','04344','04345','04346','04347','04348','04349','04350','04351','04352','04353','04354','04355','04357','04358','04359','04360','04363','04364','04401','04402','04406','04408','04410','04411','04412','04413','04414','04415','04416','04417','04418','04419','04420','04421','04422','04424','04426','04427','04428','04429','04430','04431','04434','04435','04438','04441','04442','04443','04444','04448','04449','04450','04451','04453','04454','04455','04456','04457','04459','04460','04461','04462','04463','04464','04468','04469','04471','04472','04473','04474','04475','04476','04478','04479','04481','04485','04487','04488','04489','04490','04491','04492','04493','04495','04496','04497','04530','04535','04537','04538','04539','04541','04543','04544','04547','04548','04549','04551','04553','04555','04556','04558','04562','04563','04564','04565','04568','04570','04571','04572','04573','04574','04575','04576','04578','04579','04605','04606','04607','04609','04611','04612','04613','04614','04616','04617','04619','04622','04623','04624','04625','04626','04627','04628','04629','04630','04631','04634','04635','04637','04640','04642','04643','04644','04645','04646','04648','04649','04650','04652','04653','04654','04655','04657','04658','04660','04662','04664','04666','04667','04668','04669','04671','04673','04674','04675','04676','04677','04679','04680','04681','04683','04684','04685','04686','04691','04693','04694','04730','04732','04733','04734','04735','04736','04737','04738','04739','04740','04741','04742','04743','04744','04745','04746','04747','04750','04751','04756','04757','04758','04760','04761','04762','04763','04764','04765','04766','04768','04769','04772','04773','04774','04776','04777','04779','04780','04781','04783','04785','04786','04787','04841','04843','04847','04848','04849','04850','04851','04852','04853','04854','04855','04856','04858','04859','04860','04861','04862','04863','04864','04865','04901','04903','04910','04911','04912','04915','04917','04918','04920','04921','04922','04923','04924','04925','04926','04927','04928','04929','04930','04932','04933','04935','04936','04937','04938','04939','04940','04941','04942','04943','04944','04945','04947','04949','04950','04951','04952','04953','04955','04956','04958','04961','04962','04963','04964','04965','04966','04967','04969','04970','04971','04972','04973','04974','04975','04976','04978','04979','04981','04982','04983','04984','04985','04986','04987','04988','04989','04992']  # Replace with your list of ZIP codes
    scrape_zipcodes(zipcodes)
