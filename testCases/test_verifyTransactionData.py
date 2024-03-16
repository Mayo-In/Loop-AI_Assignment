import pytest
from pageObjects.TransactionsDataVerification import TransactionsData
from pageObjects.LoginPage import LoginPage
from Utilities.readPrperties import ReadConfig
from Utilities.customLogger import LogGen


class Test_Transaction:
    url = ReadConfig.getAppURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    logger = LogGen.logGen()
    locs = ["Artisan Alchemy", "Blissful Buffet"]
    mkts = ["Grubhub"]

    def test_transactions(self, setup):
        self.logger.info("*********** Data Table ***********")
        self.logger.info("Test_005 : Navigating to Transactions Page")
        self.driver = setup
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        self.loginpage = LoginPage(self.driver)
        self.loginpage.setUserName(self.username)
        self.loginpage.setPassWord(self.password)
        self.loginpage.clickLogin()
        self.driver.implicitly_wait(30)

        self.transactionTable = TransactionsData(self.driver)
        self.transactionTable.clickOn3PChargebacks()
        self.transactionTable.clickOnTransactions()
        pageTitle = self.driver.title

        if pageTitle == "Loop - 3P Chargebacks - Transactions":
            assert True
            self.logger.info("Pass: Successfully navigated to the Transactions Page.")
        else:
            self.driver.save_screenshot(".//Screenshots" + "test_transactions.png")
            self.driver.close()
            self.logger.error("Fail: Failed to navigate to the Transactions Page.")
            assert False

        self.transactionTable.setLocationsFilters(self.locs)

        self.transactionTable.setMarketPlaceFilter_xpath(self.mkts)

        self.transactionTable.extractCSVFile()

