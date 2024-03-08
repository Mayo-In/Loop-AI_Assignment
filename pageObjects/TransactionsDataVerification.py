
import pandas as pd
from selenium.webdriver.common.by import By


class TransactionsData:
    # ********************************* Page Objects *********************************

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
# ******************************** Function Logic ********************************

    def __init__(self, driver):
        self.driver = driver

    def clickOn3PChargebacks(self):
        self.driver.find_element(By.XPATH, self.chargebacks_xpath).click()

    def clickOnTransactions(self):
        self.driver.find_element(By.XPATH, self.transactions_xpath).click()

    def setLocationsFilters(self, locations):
        loc_dropdwn = self.driver.find_element(By.XPATH, self.dropdown_locationFilter_xpath)
        self.driver.execute_script("arguments[0].click();", loc_dropdwn)
        clr_btn = self.driver.find_element(By.CSS_SELECTOR, self.button_Clear_css)
        self.driver.execute_script("arguments[0].click();", clr_btn)
        for location in locations:
            self.driver.find_element(By.XPATH, f"//div[@aria-label = '{location}']").click()
        apl_btn = self.driver.find_element(By.CSS_SELECTOR, self.button_Apply_css)
        self.driver.execute_script("arguments[0].click();", apl_btn)

    def setMarketPlaceFilter_xpath(self, marketPlaces):
        mkt_dropdwn = self.driver.find_element(By.XPATH, self.dropdown_marketplaceFilter_xpath)
        self.driver.execute_script("arguments[0].click();", mkt_dropdwn)
        clr_btn = self.driver.find_element(By.CSS_SELECTOR, self.button_Clear_css)
        self.driver.execute_script("arguments[0].click();", clr_btn)
        for marketPlace in marketPlaces:
            self.driver.find_element(By.XPATH, f"//div[@aria-label = '{marketPlace}']").click()
        apl_btn = self.driver.find_element(By.CSS_SELECTOR, self.button_Apply_css)
        self.driver.execute_script("arguments[0].click();", apl_btn)

    def extractCSVFile(self):
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
            transactions = self.driver.find_elements(By.XPATH, "//tr")

            for i in range(len(transactions) - 1):
                transactions_columns = self.driver.find_elements(By.XPATH, f"//tr[{i+1}]/td")
                if len(transactions_columns) == 8:
                    order_ID.append(self.driver.find_element(By.XPATH, f"//tr[{counter}]/td[1]").text)
                    locations.append(self.driver.find_element(By.XPATH, f"//tr[{counter}]/td[2]").text)
                    order_State.append(self.driver.find_element(By.XPATH, f"//tr[{counter}]/td[3]").text)
                    transaction_type.append(self.driver.find_element(By.XPATH, f"//tr[{counter}]/td[4]").text)
                    lost_sale.append(self.driver.find_element(By.XPATH, f"//tr[{counter}]/td[5]").text)
                    net_Payout.append(self.driver.find_element(By.XPATH, f"//tr[{counter}]/td[6]").text)
                    payout_ID.append(self.driver.find_element(By.XPATH, f"//tr[{counter}]/td[7]").text)
                    payout_Date.append(self.driver.find_element(By.XPATH, f"//tr[{counter}]/td[8]").text)
                elif len(transactions_columns) == 5:
                    order_ID.append("NA")
                    locations.append("NA")
                    order_State.append("NA")
                    transaction_type.append(self.driver.find_element(By.XPATH, f"//tr[{counter}]/td[1]").text)
                    lost_sale.append(self.driver.find_element(By.XPATH, f"//tr[{counter}]/td[2]").text)
                    net_Payout.append(self.driver.find_element(By.XPATH, f"//tr[{counter}]/td[3]").text)
                    payout_ID.append(self.driver.find_element(By.XPATH, f"//tr[{counter}]/td[4]").text)
                    payout_Date.append(self.driver.find_element(By.XPATH, f"//tr[{counter}]/td[5]").text)
                counter += 1

            if self.driver.find_element(By.XPATH, self.button_forward_xpath).is_enabled():
                element = self.driver.find_element(By.XPATH, self.button_forward_xpath)
                self.driver.execute_script("arguments[0].click();", element)
            else:
                flag = False
                break

        data_setup = pd.DataFrame({"Order ID": order_ID, "location": locations, "Order State": order_State,
                                   "Transaction Type": transaction_type, "Lost Sale": lost_sale, "Net Payout": net_Payout,
                                   "Payout ID": payout_ID, "Payout Date": payout_Date})
        data_setup.to_csv('Transaction Data.csv')

