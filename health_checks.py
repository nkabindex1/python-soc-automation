import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException , WebDriverException
from openpyxl import Workbook, load_workbook
from selenium.webdriver.edge.service import Service

FILE_NAME = "SARS HEALTH CHECKS.xlsx"
wb = load_workbook(FILE_NAME)
wb.save(FILE_NAME)
uname="admin"
pswd="P@ssw0rd"
site = "https:/10.9.17.218/core/login"

def scrape_iam_site(ip, uname, pswd):
    results = None
    driver_exe = r"C:\Users\s2028387\Documents\python\edgedriver_win64\msedgedriver.exe"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Edge(driver_exe, options=options)
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
    except WebDriverException:
        print("cant get the site") # Site is down
    finally:
        driver.close()
        driver.quit()
    return results

    #driver.minimize_window()

def parse(disk_used, disk_free, disk_total):
    disk_used_percent = None
    disk_free_percent = None
    if "%" in disk_used:# has a percentage
        du = disk_used.split()
        df = disk_free.split()
        dt = disk_total.split()
        disk_used = f"{du[0]} {du[1]}"
        disk_free = f"{df[0]} {df[1]}"
        disk_used_percent = du[2]
        disk_free_percent = df[2]
        disk_total = f"{dt[0]} {dt[1]}"
        # calculate
    else:

        du = disk_used.split()[0]
        dt = disk_total.split()[0]
        df = disk_free.split()[0]
        disk_total = f"{dt} GB"
        disk_used = f"{du} GB"
        disk_free = f"{df} GB"
        dup = round(float(du) / float(dt) * 100)
        disk_used_percent = f"{dup}%"
        disk_free_percent = f"{100 - dup}%"
        # remove space between disk_free and disk_used

    return disk_used, disk_used_percent, disk_free, disk_free_percent, disk_total


#
#
# nlist, disk_free, disk_used, disk_size = scrape_iam_site(site=site, uname=uname, pswd=pswd)
# print(nlist, disk_free, disk_used, disk_size)


# read appliances file

import pandas as pd
#print(pd.read_csv("appliances.csv"))

appliances = pd.read_csv("appliances.csv", encoding='cp1252')
print(appliances.keys())
print(appliances["sheet_name"])
#time.sleep(1000)



for i, row in appliances.iterrows():

    print(f"{i+1}. Scrapping:  apname={row['apname']}, uname= {row['uname']} , ip={row['ipaddr']}, env={row['env']}")
    if row["uname"] is not np.NaN:
        res = scrape_iam_site(ip=row["ipaddr"], uname=row["uname"], pswd=row["pswd"])
        print(res , type(res))
        if res != None:
            notifs, disk_free, disk_used, tot = res
            # parse the data

            # store on the excel sheet
            print(f"notifs: {len(notifs)}, disk_used: {disk_used}, disk_free: {disk_free}, tot: {tot}")

            # parse results
            disk_used, disk_used_percent, disk_free, disk_free_percent, disk_total = parse(disk_used=disk_used, disk_free=disk_free, disk_total=tot)
            if row["sheet_name"] == np.NaN:
                if row["sheet_name"] == "QA":
                    sheet = wb["QA"]
                elif row["sheet_name"] == "DEV":
                    sheet = wb["DEV"]
                elif row["sheet_name"] == "PRE-PROD":
                    sheet = wb["Pre Prod"]
                elif row["sheet_name"] == "prod":
                    sheet = wb["Production"]

                # there is free space , space used, etc
                sheet[row["used_space"]] = f"{disk_used} - {disk_used_percent}"
                sheet[row["free_space"]] = f"{disk_free} - {disk_free_percent}"
                sheet[row["total_space"]] = f"{disk_total}"
                sheet[row["certificate"]] = notifs

            du = f"{disk_used} - {disk_used_percent}"
            df = f"{disk_free} - {disk_free_percent}"
            print(du , df , notifs )
        else:
            print(res, type(res))
wb.save(FILE_NAME)
print("file saved")