import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException , WebDriverException
from openpyxl import Workbook, load_workbook
from selenium.webdriver.edge.service import service

from utils import parse

def scrape_isim(sites):
    """

    :param sites: dictionary of all sites to be scraped
    :return: total , percentage of the scraped data
    """

    if( type(sites) is not list()):
        0
    else:

        results = None
        driver_exe = r"C:\Users\s2028387\Documents\python\edgedriver_win64\msedgedriver.exe"
        # options = Options()
        # options.add_argument("--headless")
        # options.add_argument("--window-size=1440, 900")
        # driver = webdriver.Edge(driver_exe, options=options)
        # driver.set_window_size(1440, 900)
        driver = webdriver.Edge(driver_exe)



        try:
            site = f"https:/{ip}"
            # connect site
            print(site)
            driver.get(site)
            try:
                driver.find_element(By.ID, "details-button").click()
                driver.find_element(By.ID, "proceed-link").click()
            except NoSuchElementException:
                print("Element does not exist")

            driver.find_element(By.ID, "login_user_id").send_keys(uname)
            driver.find_element(By.ID, "login_password").send_keys(pswd)
            driver.find_element(By.ID, "login_submit").click()
            # time.sleep(5)

            # wait until the elements have been created
            try:

                notification_list = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "notification-list"))
                )
                notification_list = notification_list.text
            except:
                driver.quit()

            notification_list = driver.find_element(By.ID, "notification-list").text
            disk_free = driver.find_element(By.ID, "disk-free").text
            disk_used = driver.find_element(By.ID, "disk-used").text
            disk_size = driver.find_element(By.ID, "disk-size").text
            results = notification_list.split('\n'), disk_free, disk_used, disk_size

            # then you parse it here
        except WebDriverException:
            print("cant get the site") # Site is down
        finally:
            driver.close()
            driver.quit()
        return results

