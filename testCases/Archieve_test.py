import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


username = "qa-engineer-assignment@test.com"
password = "QApassword123$"
url = "https://app.tryloop.ai/login/password"

textbox_username_id = ":r1:"
textbox_password_id = ":r2:"
button_login_xpath = "//button[normalize-space()='Login']"
chargebacks_xpath = "//span[normalize-space()='3P Chargebacks']"
transactions_xpath = "//span[normalize-space()='Transactions']"
dropdown_locationFilter_xpath = "//*[@id='main_start_app']/main/div/div/header/div/div/button[1]"
button_Clear_css = "body > div.MuiPopover-root.MuiModal-root.css-eugp8i-MuiModal-root-MuiPopover-root > \
div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation8.MuiPopover-paper.css-s0yj2b-MuiPaper-root-MuiPopover-paper > \
div.MuiBox-root.css-ypkdm9 > div.MuiBox-root.css-bbyuxu > button"
button_Apply_css = "body > div.MuiPopover-root.MuiModal-root.css-eugp8i-MuiModal-root-MuiPopover-root > \
div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation8.MuiPopover-paper.css-s0yj2b-MuiPaper-root-MuiPopover-paper > \
div.MuiBox-root.css-13ev6ou > button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeSmall.MuiButton-containedSizeSmall.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeSmall.MuiButton-containedSizeSmall.css-1un93pa-MuiButtonBase-root-MuiButton-root"
dropdown_marketplaceFilter_xpath = "//*[@id='main_start_app']/main/div/div/header/div/div/button[3]"
table_xpath = "//*[@id='view-table-id']/div/table"
button_forward_xpath = "//*[@id='simple-tabpanel-overview']/div[2]/div[2]/div[2]/div/button[2]"
button_download_xpath = "//*[@id='simple-tabpanel-overview']/div[2]/div[2]/div[1]/div[2]/div"

driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(20)
driver.maximize_window()
driver.find_element(By.ID, textbox_username_id).send_keys(username)
driver.find_element(By.ID, textbox_password_id).send_keys(password)
driver.find_element(By.XPATH, button_login_xpath).click()
driver.implicitly_wait(20)
driver.find_element(By.XPATH, chargebacks_xpath).click()
driver.find_element(By.XPATH, transactions_xpath).click()
driver.implicitly_wait(20)

def select1(locations):
    loc_dropdwn = driver.find_element(By.XPATH, dropdown_locationFilter_xpath)
    driver.execute_script("arguments[0].click();", loc_dropdwn)
    clr_btn = driver.find_element(By.CSS_SELECTOR, button_Clear_css)
    driver.execute_script("arguments[0].click();", clr_btn)
    for location in locations:
        driver.find_element(By.XPATH, f"//div[@aria-label = '{location}']").click()
    apl_btn = driver.find_element(By.CSS_SELECTOR, button_Apply_css)
    driver.execute_script("arguments[0].click();", apl_btn)
    driver.implicitly_wait(20)

def select2(marketPlaces):
    mkt_dropdwn = driver.find_element(By.XPATH, dropdown_marketplaceFilter_xpath)
    driver.execute_script("arguments[0].click();", mkt_dropdwn)
    clr_btn = driver.find_element(By.CSS_SELECTOR, button_Clear_css)
    driver.execute_script("arguments[0].click();", clr_btn)
    for marketPlace in marketPlaces:
        driver.find_element(By.XPATH, f"//div[@aria-label = '{marketPlace}']").click()
    apl_btn = driver.find_element(By.CSS_SELECTOR, button_Apply_css)
    driver.execute_script("arguments[0].click();", apl_btn)
    driver.implicitly_wait(20)


def extractCSVFile():

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
        transactions = driver.find_elements(By.XPATH, "//tr")

        for i in range(len(transactions) - 1):
            transactions_columns = driver.find_elements(By.XPATH, f"//tr[{i+1}]/td")
            print(len(transactions_columns))
            if len(transactions_columns) == 8:
                order_ID.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[1]").text)
                locations.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[2]").text)
                order_State.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[3]").text)
                transaction_type.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[4]").text)
                lost_sale.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[5]").text)
                net_Payout.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[6]").text)
                payout_ID.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[7]").text)
                payout_Date.append(driver.find_element(By.XPATH, f"//tr[{counter}]/td[8]").text)
            elif len(transactions_columns) == 5:
                order_ID.append("NA")
                locations.append("NA")
                order_State.append("NA")
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

    data_setup = pd.DataFrame({"Order ID": order_ID, "location": locations, "Order State": order_State,
                               "Transaction Type": transaction_type, "Lost Sale": lost_sale, "Net Payout": net_Payout,
                               "Payout ID": payout_ID, "Payout Date": payout_Date})
    data_setup.to_csv('Archive Transaction Data.csv')


locations = ["Artisan Alchemy", "Blissful Buffet"]
marketPlaces = ["Grubhub"]
select1(locations)
select2(marketPlaces)
time.sleep(20)
extractCSVFile()


