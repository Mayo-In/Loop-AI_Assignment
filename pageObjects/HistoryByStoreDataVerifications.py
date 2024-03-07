from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


class HistoryByStoreData:
    # ********************************* Page Objects *********************************

    chargebacks_xpath = "//span[normalize-space()='3P Chargebacks']"
    historyByStore_xpath = "//span[normalize-space()='History by Store']"
    table_xpath = "//table[@class='MuiTable-root css-l6sbfr-MuiTable-root']"
    reversals_dropdown_id = "drilldown-options-fc"
    option_reversals_xpath = "//p[text() ='Reversals']"
    # table_cellValue_xpath = "//*[@id='view-table-id']/div/table/tbody/tr[1]/td[2]"
    button_forward_xpath = "//*[@id='main_start_app']/main/div/div/div[4]/div/div[2]/div/button[2]"
    button_backward_xpath = "//*[@id='main_start_app']/main/div/div/div[4]/div/div[2]/div/button[1]"

    # ******************************** Function Logic ********************************

    def __init__(self, driver):
        self.driver = driver

    def clickOn3PChargebacks(self):
        self.driver.find_element(By.XPATH, self.chargebacks_xpath).click()

    def clickOnHistoryByStore(self):
        self.driver.find_element(By.XPATH, self.historyByStore_xpath).click()

    def getOrderStatus(self):
        acc_value = self.driver.find_element(By.ID, self.reversals_dropdown_id).text
        return acc_value

    def tableDataCalculation(self, column):

        values = []
        flag = True
        i = column + 1
        while flag:
            is_exist = True
            counter = 0
            while is_exist:
                try:
                    counter += 1
                    value = self.driver.find_element(By.XPATH,
                                                     f"//div[@id='view-table-id']/div/table/tbody/tr[{counter}]/td[{i}]/h6").text
                    num = float(value.replace('$', '').replace(',', ''))
                    values.append(num)
                except NoSuchElementException:
                    is_exist = False
                    break

            if self.driver.find_element(By.XPATH, self.button_forward_xpath).is_enabled():
                element = self.driver.find_element(By.XPATH, self.button_forward_xpath)
                self.driver.execute_script("arguments[0].click();", element)
                # self.driver.find_element(By.XPATH, self.button_forward_xpath).click()
            else:
                flag = False
                break

        total = sum(values)
        acc_total = "%.2f" % round(total, 2)
        return acc_total

    def getMonth(self, column):
        i = column + 1
        monthName = self.driver.find_element(By.XPATH,
                                             f"//*[@id='view-table-id']/div/table/thead/tr/th[{i}]/div/div/h6").text
        return monthName

    def getGrandTotal(self, column):
        i = column + 1
        grandTotal = self.driver.find_element(By.XPATH,
                                              f"//*[@id='view-table-id']/div/table/tbody/tr[12]/td[{i}]/h6").text
        total = float(grandTotal.replace('$', '').replace(',', ''))
        return total
