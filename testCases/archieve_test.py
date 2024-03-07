import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

chargebacks_xpath = "//span[normalize-space()='3P Chargebacks']"
transactions_xpath = "//span[normalize-space()='Transactions']"
dropdown_locationFilter_xpath = "//*[@id='main_start_app']/main/div/div/header/div/div/button[1]"
button_Clear_xpath = "/html/body/div[6]/div[3]/div[1]/div[2]/button"
button_Apply_xpath = "/html/body/div[6]/div[3]/div[3]/button[2]"
dropdown_marketplaceFilter_xpath = "//*[@id='main_start_app']/main/div/div/header/div/div/button[3]"
table_xpath = "//*[@id='view-table-id']/div/table"
button_forward_xpath = "//*[@id='simple-tabpanel-overview']/div[2]/div[2]/div[2]/div/button[2]"

driver = webdriver.Chrome()
driver.get("https://app.tryloop.ai/login/password")
driver.implicitly_wait(10)
driver.maximize_window()
driver.find_element(By.ID, ":r1:").send_keys("qa-engineer-assignment@test.com")
driver.find_element(By.ID, ":r2:").send_keys("QApassword123$")
driver.find_element(By.XPATH, "//button[normalize-space()='Login']").click()
driver.implicitly_wait(20)
driver.find_element(By.XPATH, "//span[normalize-space()='3P Chargebacks']").click()
driver.find_element(By.XPATH, "//span[normalize-space()='Transactions']").click()
time.sleep(20)


def setLocationsFilters(locations):
    loc_dropdwn = driver.find_element(By.XPATH, dropdown_locationFilter_xpath)
    driver.execute_script("arguments[0].click();", loc_dropdwn)
    WebDriverWait(driver,30).until(ec.presence_of_element_located((By.XPATH, button_Clear_xpath))).click()
    # clr_btn = driver.find_element(By.XPATH, button_Clear_xpath)
    # driver.execute_script("arguments[0].click();", clr_btn)
    for location in locations:
        driver.find_element(By.XPATH, f"//div[@aria-label = '{location}']").click()
    time.sleep(15)
    driver.implicitly_wait(20)
    # WebDriverWait(driver,30).until(ec.presence_of_element_located((By.XPATH, button_Apply_xpath))).click()
    apl_btn = driver.find_element(By.XPATH, button_Apply_xpath)
    driver.execute_script("arguments[0].click();", apl_btn)



def setMarketPlaceFilter_xpath(marketPlaces):
    mkt_dropdwn = driver.find_element(By.XPATH, dropdown_marketplaceFilter_xpath)
    driver.execute_script("arguments[0].click();", mkt_dropdwn)
    time.sleep(15)
    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, button_Clear_xpath))).click()
    # clr_btn = driver.find_element(By.XPATH, button_Clear_xpath)
    # driver.execute_script("arguments[0].click();", clr_btn)
    for marketPlace in marketPlaces:
        driver.find_element(By.XPATH, f"//div[@aria-label = '{marketPlace}']").click()
    time.sleep(15)
    WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, button_Apply_xpath))).click()
    # apl_btn = driver.find_element(By.XPATH, button_Apply_xpath)
    # driver.execute_script("arguments[0].click();", apl_btn)

def extractCSVFile():
    transaction_result = []

    flag = True
    order_ID = []
    locations = []
    order_State = []
    transaction_type = []
    lost_sale = []
    net_Payout = []
    payout_ID = []
    payout_Date = []

    while flag:
        counter = 1
        transactions_rows = driver.find_elements(By.XPATH, "//tr")

        for i in range(len(transactions_rows)-1):
            transactions_columns = driver.find_elements(By.XPATH, "//tr/td")
            if transactions_columns == 8:
                order_ID.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[1]").text)
                locations.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[2]").text)
                order_State.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[3]").text)
                transaction_type.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[4]").text)
                lost_sale.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[5]").text)
                net_Payout.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[6]").text)
                payout_ID.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[7]").text)
                payout_Date.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[8]").text)
            elif transactions_columns == 5:
                transaction_type.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[1]").text)
                lost_sale.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[2]").text)
                net_Payout.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[3]").text)
                payout_ID.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[4]").text)
                payout_Date.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[5]").text)
            counter += 1

        if driver.find_element(By.XPATH, button_forward_xpath).is_enabled():
            element = driver.find_element(By.XPATH, button_forward_xpath)
            driver.execute_script("arguments[0].click();", element)
        else:
            flag = False
            break

    data_setup = pd.DataFrame({"Order ID": order_ID,"location": locations,"Order State": order_State,"Transaction Type": transaction_type,
                               "Lost Sale": lost_sale,"Net Payout": net_Payout,"Payout ID": payout_ID, "Payout Date": payout_Date})
    data_setup.to_csv('Transaction Data.csv')
    # data_setup.to_excel('Transaction Data.xls')


locs = ["Artisan Alchemy", "Blissful Buffet"]
mkts = ["Grubhub"]
setLocationsFilters(locs)
time.sleep(15)
setMarketPlaceFilter_xpath(mkts)
time.sleep(15)
extractCSVFile()