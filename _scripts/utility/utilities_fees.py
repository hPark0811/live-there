"""
This file contains web-scraping tools with selenium via Chrome browser.
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
import pprint
import numpy as np
from collections.abc import Iterable

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
        """Install Chrome driver from unknown developer @ https://github.com/SergeyPirogov/webdriver_manager."""

        print('Unable to load driver from ' + chromedriver_path)

        return webdriver.Chrome(ChromeDriverManager().install())


def get_distribution_company(driver, postal_code):
    # TODO: Develop an option for natural gas
    """
        Retrieve distribution companies by postal code @ ieso.ca
        Currently, this only support electricity usage.
        :param driver: the driver for chrome browser
        :param postal_code: postal code of the searching area
        :return: lists of distributions near the area
    """
    driver.get(DISTRB_POWER_ON_URL)

    # Find the form, and search the postal code.
    post_input = driver.find_element_by_id('pclu')
    post_input.send_keys(postal_code)
    post_input.send_keys(Keys.ENTER)

    # Retrieve search results.
    result_div = driver.find_element_by_id('results')

    # Wait until all children is rendered
    WebDriverWait(result_div, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "strong"))
    )

    results = result_div.find_elements_by_tag_name('strong')
    results = [r.text for r in results]

    return results


def get_bill_options(t='e'):
    """
        Retrieve available distribution companies supported in oeb.com bill calculator
        :param t: either 'e' or 'n' for electrical calculator or natural gas calculator.
        :return: list of distribution companies supported
    """
    page = None
    if t == 'e':
        # Load Electrical bill calculator.
        page = requests.get(EC_CALC_URL)
    elif t == 'n':
        # Load Natural gas bill Calculator.
        page = requests.get(NG_CALC_URL)
    else:
        raise Exception(f'Type t must be either e or n, received: {t}')

    # Web-scraping through BeautifulSoup
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
    if t == 'e':
        url = EC_CALC_URL
    elif t == 'n':
        url = NG_CALC_URL
    else:
        raise Exception(f'Type t must be either e or n, received: {t}')

    driver.get(url)

    # Select utility option.
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


def calculate_pmf(pool):
    """
    Calculate probability mass function over all uniques occurrence of words.
    :param pool: pools of string
    :return: pmf
    """
    counts = {}
    # Counts all the uniques words from pool of string
    for element in pool:
        words = element.lower().split(' ')
        for w in words:
            counts[w] = counts[w] + 1 if w in counts.keys() else 1
    n = len(pool)

    # Probability is (number of occurrence)/total occurrence
    pmf = counts
    for w in pmf.keys():
        pmf[w] /= n

    return pmf


def calculate_score(obj, candidate, pmf):
    """
    Calculate score of obj and candidate words
    :param obj: objective words that is projected on the candidate
    :param candidate: target of the words & built pmf with.
    :param pmf:
    :return: scores which represents total rareness of shared word - penalize for the commonly occurring words
    """
    obj = obj.lower().split(' ')
    candidate = candidate.lower().split(' ')
    shared_words = list(set(obj).intersection(set(candidate)))

    # Scored is calculated as sum of -log probability of shared words - sum of rareness of the shared words.
    return np.sum([-np.log(pmf[w]) for w in shared_words if w in pmf.keys()])


def find_options(obj, pool):
    """
    Find all available options based on the score.
    :param obj:
    :param pool:
    :return:
    """
    pmf = calculate_pmf(pool)
    scores = {}
    for p in pool:
        scores[p] = calculate_score(obj, p, pmf)

    # pprint.pprint(scores)
    # print(o, '|', max(scores, key=scores.get))

    # Available options will be selected from pool with maximum score.
    max_score = max(list(scores.values()))
    # Note: Ambiguity will be length of the below list
    return [k for k, v in scores.items() if v == max_score]


def run_scraper(postal_code):
    average_ec_bills = []
    average_ng_bills = []

    driver = get_chrome_driver()

    postal_codes = []
    # Allow iterable or single element scraping
    if (not isinstance(postal_code, Iterable)) or isinstance(postal_code, str):
        postal_codes = [postal_code]
    else:
        postal_codes = postal_code

    for postal_code in postal_codes:
        try:
            # Retrieve pool and obj
            ec_options = get_bill_options('e')
            ng_options = get_bill_options('n')
            options_candidates = get_distribution_company(driver, postal_code)

            # Find available options for all obj
            available_ec_options = []
            available_ng_options = []
            for o in options_candidates:
                available_ec_options.extend(find_options(o, ec_options))
                available_ng_options.extend(find_options(o, ng_options))

            # Calculate average electricity bills over the available options
            total_ec_bill = 0
            for o in available_ec_options:
                total_ec_bill += get_bill(driver, o, t='e')

            total_ng_bill = 0
            for o in available_ng_options:
                total_ng_bill += get_bill(driver, o, t='n')

            # If len of both list is not zero
            if (len(available_ec_options) != 0 and len(available_ng_options)) != 0:
                average_ec_bill = total_ec_bill / len(available_ec_options)
                average_ng_bill = total_ng_bill / len(available_ng_options)
            else:
                raise Exception(f'{len(available_ng_options)} average NG Options and {len(available_ec_options)} average EC Options')

            # Display summary on every iteration of  university
            print(f'The average electrical bill is { average_ec_bill :.2f}$ sampled from')
            pprint.pprint(available_ec_options)
            print(f'The average natural gas bill is {average_ng_bill :.2f}$ sampled from')
            pprint.pprint(available_ng_options)

            average_ec_bills.append(average_ec_bill)
            average_ng_bills.append(average_ng_bill)

        except Exception:
            print(f'utilities_fees.py: Error occurred during automatic web-scrapping @ {postal_code}')
            average_ec_bills.append(float('nan'))
            average_ng_bills.append(float('nan'))

    driver.close()

    return average_ec_bills, average_ng_bills


if __name__ == "__main__":
    postal_code = input('Please enter available postal code: ')
    run_scraper(postal_code)
