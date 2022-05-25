from datetime import date
import calendar
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.options import Options
from ldap3 import Connection, Server, ALL, SAFE_SYNC
import time
from openpyxl import Workbook, load_workbook
from openpyxl.chart import Reference, Series, LineChart

"""
    public variables: 
    variables for the last months date, this is because the stats are for the past month, extract only the year and month
"""

dates = {
    "month": date.today().month - 1,
    "year": date.today().year,
}

website = {
    "username":"admin",
    "password":"X0!4n!1998",
    "url":"https://myidentity.sars.gov.za/itim/console/jsp/logon/Login.jsp"
}

server = {
    "name":"prodIAM03",
    "port":389,
    "dir":"ou=SARS,dc=sars",
}



LAST_MONTH = date.today().month - 1
YEAR = date.today().year
USERNAME = "s2028387"
PASSWORD = "Nk@b!nd31998"  # input(f"pswd for {uname}?")
WEBSITE = "https://myidentity.sars.gov.za/itim/console/jsp/logon/Login.jsp"


def write(text):
    text_file = open("sample.txt", "w")
    n = text_file.write(text)
    text_file.close()


def get_filter(category):

    if category == "third_party":
        return ""

    elif category == "pps":
        return
    return 0



wb = load_workbook \
    (r'C:\Users\s2028387\Documents\Identity & Access Management\Monthly stats\ISIM-ISAM Stats Jan 2022.xlsx')
from selenium import webdriver
server = Server("prodIAM03", port=389, get_info=ALL)
conn = Connection(server, client_strategy=SAFE_SYNC, auto_bind=True)
is_binded = conn.bind()
year = date.today().year
month = f"0{LAST_MONTH}" if LAST_MONTH < 10 else LAST_MONTH
pswd_last_change = f"{year}{month}"

def search(f):
    _, _, results, _ = conn.search('ou=SARS,dc=sars', f)
    return len(results)


def get_account_changes():
    """"""
    driver_exe = r"C:\Users\s2028387\Documents\python\edgedriver_win64\msedgedriver.exe"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Edge(driver_exe, options=options)
    driver.get(WEBSITE)

    """
        login to myidentity 
    """

    elements = {
        "portfolio_canvas_area": {By.ID, "portfolio_canvas_area"},
        "username": {By.ID, "j_username"},
    }


    driver.find_element(By.ID, "j_username").send_keys(USERNAME)
    driver.find_element(By.ID, "j_password").send_keys(PASSWORD)
    driver.find_element(By.ID, "button.ok").click()

    """
        to choose items on a navigation we need to change frames, until the frame we want to select 
    """




    time.sleep(5)
    portfolio_canvas_area = driver.find_element(By.ID, "portfolio_canvas_area")
    driver.switch_to.frame(portfolio_canvas_area)  # portfolio_area
    portfolio_area = driver.find_element(By.ID, "portfolio_area")
    driver.switch_to.frame(portfolio_area)  # taskEntriesFrame ,
    taskEntriesFrame = driver.find_element(By.ID, "taskEntriesFrame")
    driver.switch_to.frame(taskEntriesFrame)  # taskEntriesFrame ,
    driver.find_element(By.XPATH, "//a[contains(@id,'treeSel(50)')]").click()
    driver.refresh()
    write(driver.page_source)
    portfolio_canvas_area = driver.find_element(By.ID, "portfolio_canvas_area")
    driver.switch_to.frame(portfolio_canvas_area)  # portfolio_area
    portfolio_area = driver.find_element(By.ID, "portfolio_area")
    driver.switch_to.frame(portfolio_area)  # taskEntriesFrame ,
    taskEntriesFrame = driver.find_element(By.ID, "taskEntriesFrame")
    driver.switch_to.frame(taskEntriesFrame)  # taskEntriesFrame ,
    driver.find_element(By.XPATH, "//a[contains(@id,'treeSel(55)')]").click()
    driver.refresh()

    portfolio_canvas_area = driver.find_element(By.ID, "portfolio_canvas_area")
    driver.switch_to.frame(portfolio_canvas_area)  # portfolio_area
    canvas_area = driver.find_element(By.ID, "canvas_area")
    driver.switch_to.frame(canvas_area)
    canvas_task_frame = driver.find_element(By.ID, "canvas_task_frame")
    driver.switch_to.frame(canvas_task_frame)
    request_type = Select(driver.find_element(By.ID, "id.view.request.type"))
    request_type.select_by_index(5)

    #
    driver.find_element(By.ID, "id_request_filter_start_date_db").click()
    # id_request_filter_start_date_dc_comboMonth
    # id_request_filter_start_date_dc_comboYear
    start_date_dc_comboMonth = Select(driver.find_element(By.ID, "id_request_filter_start_date_dc_comboMonth"))
    # start_date_dc_comboMonth.select_by_index(2) # select by visible text
    start_date_dc_comboMonth.select_by_visible_text(calendar.month_name[LAST_MONTH])

    start_date_dc_comboYear = Select(driver.find_element(By.ID, "id_request_filter_start_date_dc_comboYear"))
    # start_date_dc_comboYear.select_by_index(2)
    start_date_dc_comboYear.select_by_visible_text(str(YEAR))
    driver.find_element(By.XPATH, "//input[@value='OK']").click()

    # id_request_filter_end_date_db
    driver.find_element(By.ID, "id_request_filter_end_date_db").click()
    end_date_dc_comboMonth = Select(driver.find_element(By.ID, "id_request_filter_end_date_dc_comboMonth"))
    # start_date_dc_comboMonth.select_by_index(2) # select by visible text
    end_date_dc_comboMonth.select_by_visible_text(calendar.month_name[LAST_MONTH])

    end_date_dc_comboYear = Select(driver.find_element(By.ID, "id_request_filter_end_date_dc_comboYear"))
    # start_date_dc_comboYear.select_by_index(2)
    end_date_dc_comboYear.select_by_visible_text(str(YEAR))
    # must contain the last day of the month

    last_day_of_the_month = calendar.monthrange(YEAR, LAST_MONTH)[1]
    driver.find_element(By.ID, f"id_request_filter_end_date_dc_2022_3_{last_day_of_the_month}").click()
    driver.find_element(By.CSS_SELECTOR, "#id_request_filter_end_date_dc_calDivTable > tbody > "
                                         "tr:nth-child(3) > td > input:nth-child(1)").click()

    driver.find_element(By.ID, "id_request_filter_request_find").click()
    time.sleep(15)
    account_change = driver.find_element(By.ID, "id_request_filter_results").text.split()
    driver.close()
    print(account_change)
    return int(account_change[0])

if is_binded:

    third_party = search('(objectClass=sgExtOrganization)')
    active_accounts = search('(&(erPersonStatus=0)(Uid=S*))')
    pps_enrolled = search("(&(erLostPasswordAnswer=*)(erUid=S*)(erAccountStatus=0))")
    password_self_service = search \
        (f"(&(erUid=s*)(erPswdLastChanged={pswd_last_change}*)(!"
         f"(erpasswordlastchangedby=erglobalid=2251451094207261474,"
         f"ou=0,ou=people,erglobalid=00000000000000000000,ou=SARS,dc=sars))"
         f"(!(erpasswordlastchangedby=erglobalid=3636261443533632627,ou=0,ou=people,erglobalid=00000000000000000000,"
         f"ou=SARS,dc=sars))(!(erpasswordlastchangedby=erglobalid=5257726835634786289,ou=0,ou=people,"
         f"erglobalid=00000000000000000000,ou=SARS,dc=sars))(!(erpasswordlastchangedby=erglobalid=1528512649986509803,"
         f"ou=0,ou=people,erglobalid=00000000000000000000,ou=SARS,dc=sars)))") + get_account_changes()
    active_dha = search('(uid=H*)')
    active_saps = search('(uid=P*)')

    # get all the other filters , there's two sides to password self-service
    print(f"{active_accounts} {pps_enrolled} {password_self_service} {active_dha} {active_saps} {third_party}")

    wb["Dec 2021"]["a1"] = f"ISIM / ISAM Stats - {calendar.month_name[LAST_MONTH]} {YEAR}"
    wb["Dec 2021"]["b4"] = active_accounts
    wb["Dec 2021"]["b5"] = pps_enrolled
    wb["Dec 2021"]["b6"] = active_dha
    wb["Dec 2021"]["b7"] = active_saps
    wb["Dec 2021"]["b8"] = password_self_service
    wb["Dec 2021"]["b9"] = third_party
    wb["Dec 2021"].title = f"{calendar.month_name[LAST_MONTH]} {YEAR}"
    # change the sheetname,
    print(wb["Dec 2021"])
    print(wb["Dec 2021"]._charts)
    #change title on a1

wb.save(r'C:\Users\s2028387\Documents\Identity & Access Management\Monthly stats\ISIM-ISAM Stats.xlsx')

# connect to myidenity website scrape the data required data

# add it to the excelsheet
