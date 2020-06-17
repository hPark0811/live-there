"""
This file contains webscrapting tools with selenium via Chrome browser. 
Before usage, please download appropriate Chrome driver from https://chromedriver.chromium.org/downloads and name it "chromedriver" in the root directory.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as Soup
from webdriver_manager.chrome import ChromeDriverManager

import re
import os
import requests
# import jellyfish


EC_CALC_URL = r'https://www.oeb.ca/_html/calculator/billcalc.php'
NG_CALC_URL = r'https://www.oeb.ca/_html/calculator/gasbillcalc.php'
DISTRB_POWER_ON_URL = r'http://www.ieso.ca/Learn/Ontario%20Power%20System/Overview%20of%20Sector%20Roles/Find%20Your%20LDC'

# Please install the appropriate version of Chrome driver and name it "chromedriver". 
chromedriver_path = os.getcwd() + "/chromedriver"


def get_chrome_driver():
    try:
        """Load Chrome driver from chromedriver_path."""
        return webdriver.Chrome(chromedriver_path)
    except:
        """Install Chrome driver from unknown developer: https://github.com/SergeyPirogov/webdriver_manager."""        

        print('Unable to load driver from '+chromedriver_path)

        return webdriver.Chrome(ChromeDriverManager().install())


def get_distribution_company(driver, postal_code):
    """
        Retrieve distribution companies by postal code from ieso.ca
        :param driver: the driver for chrome browser
        :param postal_code: postal code of the searching area
        :return: lists of distributions near the area
    """
    driver.get(DISTRB_POWER_ON_URL)

    # Find the form, and search the postal code.
    post_input = driver.find_element_by_id('pclu')
    post_input.send_keys(postal_code)
    post_input.send_keys(Keys.ENTER)

    # Retreive search results.
    result_div = driver.find_element_by_id('results')
    
    element = WebDriverWait(result_div, 10).until(
        # Wait until all children is rendered
        EC.presence_of_element_located((By.TAG_NAME, "strong"))
    )
    results = result_div.find_elements_by_tag_name('strong')
    results = [r.text for r in results]

    return results
    

def get_bill_options(t='e'):
    """
        Retrieve available distribution companies supported in oeb.com bill calcalator
        :param t: either 'e' or 'n' for electrical calculator or natural gas calculator.
        :return: list of distribution companies supported
    """
    page = None
    if t=='e':
        # Load Electrical bill calculator.
        page = requests.get(EC_CALC_URL)
    elif t=='n':
        # Load Natural gas bill Calculator.
        page = requests.get(NG_CALC_URL)
    else:
        raise Exception(f'Type t must be either e or n, received: {t}')
    
    # Webscraping through BeutifulSoup
    soup = Soup(page.content, 'html.parser')

    # Find select-options 
    select = soup.find(id='ddCompanies')
    options = select.find_all('option')
    distribution_companies = [o['value'] for o in options][1:]
    
    return distribution_companies


def get_bill(driver, utility_company, t='e'):
    """
        Retrieve default bill calculation from oeb.com
        :param driver: selenium driver
        :param utility_company: selected company from get_bill_options
        :param t: either 'e' or 'n' for electrical calculator or natural gas calculator.
        :return: calculated bill in float
    """
    url = None
    if t=='e':
        url = EC_CALC_URL
    elif t=='n':
        url = NG_CALC_URL
    else:
        raise Exception(f'Type t must be either e or n, received: {t}')

    driver.get(url) 

    # Select utitlity option.
    options = driver.find_element_by_id('ddCompanies')
    for o in options.find_elements_by_tag_name('option'):
        if o.get_attribute('value') == utility_company:
            o.click()
            break
    
    # Click Calculate button.
    driver.find_element_by_name('btnCalculateRetail').click()
    all_td = driver.find_elements_by_class_name('total')

    # Find the Calculation.
    bill = -1
    for td in all_td:
        if '$' in td.text:
            bill = re.findall(r'\d+\.\d+', td.text)[0]
            break
    
    return float(bill)


# def cross_jelly(candidate, pools):
#     def fish_hooked(a, b):        
#         # TODO: FIX THIS DUMB
#         # real fucked up naive shit
#         print(a, b, jellyfish.levenshtein_distance(a, b))
#         print(len(a.split(' ')) + len(b.split(' ')))
#         return jellyfish.levenshtein_distance(a, b)/(len(a.split(' ')) + len(b.split(' '))) > 0.3

#     for p in pools:
#         if fish_hooked(candidate, p):
#             return p
#     return None

        
if __name__ == "__main__":
    # Webscraping automation example.
    driver = get_chrome_driver()
    ec_options = get_bill_options()
    ng_options = get_bill_options('n')
    option_candidates = get_distribution_company(driver, 'N0L 1E0')
    print(get_bill(driver, ec_options[0]))
    print(get_bill(driver, ng_options[0], 'n'))
    driver.close()

    # TODO: Automate webscrapter and save the data
