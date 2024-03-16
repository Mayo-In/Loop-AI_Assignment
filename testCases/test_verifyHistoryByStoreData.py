import time

import pytest
from pageObjects.HistoryByStoreDataVerifications import HistoryByStoreData
from pageObjects.LoginPage import LoginPage
from Utilities.readPrperties import ReadConfig
from Utilities.customLogger import LogGen


class Test_HistoryByStore:
    url = ReadConfig.getAppURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    logger = LogGen.logGen()

    def test_navigateToDataTable(self, setup):
        self.logger.info("*********** Data Table ***********")
        self.logger.info("Test_003 : Navigating to the Data Table")
        self.driver = setup
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        self.loginpage = LoginPage(self.driver)
        self.loginpage.setUserName(self.username)
        self.loginpage.setPassWord(self.password)
        self.loginpage.clickLogin()
        self.driver.implicitly_wait(10)

        self.dataTable = HistoryByStoreData(self.driver)
        self.dataTable.clickOn3PChargebacks()
        self.dataTable.clickOnHistoryByStore()
        self.orderStatus = self.dataTable.getOrderStatus()
        if self.orderStatus == "Reversals":
            assert True
            self.logger.info("Pass: Successfully navigated to the Data Table.")
        else:
            self.driver.save_screenshot(".//Screenshots" + "test_navigateToDataTable.png")
            self.driver.close()
            self.logger.error("Fail: Failed to navigate to the Data Table.")
            assert False
        time.sleep(30)
        self.logger.info("*********** Data Table Verification ***********")
        self.logger.info("Test_004 : Calculate the Data for Each Month")

        for i in range(1,8):
            exp_total = float(self.dataTable.getGrandTotal(i))
            calculated_total = float(self.dataTable.tableDataCalculation(i))
            month_name = self.dataTable.getMonth(i)
            print(f"exp_total = {exp_total}")
            print(f"calculated total = {calculated_total}")

            if calculated_total == exp_total:
                assert True
                self.logger.info(f"Pass: The grand total {exp_total} is matching with calculated value {calculated_total} for the {month_name}.")
            else:
                self.driver.save_screenshot(".//Screenshots" + "test_verifyData.png")
                self.logger.error(f"Fail: The grand total expected value {exp_total} is not matching with calculated value {calculated_total} for the {month_name}.")
                assert False

            self.driver.refresh()
            time.sleep(30)

