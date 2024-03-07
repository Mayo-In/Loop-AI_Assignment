import pytest
from pageObjects.LoginPage import LoginPage
from Utilities.readPrperties import ReadConfig
from Utilities.customLogger import LogGen


class Test_Login:
    url = ReadConfig.getAppURL()
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()
    logger = LogGen.logGen()

    def test_launchURL(self, setup):
        self.logger.info("**********URL Launch***********")
        self.logger.info("Test_001 : Launching the browser and URL")
        self.driver = setup
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        title = self.driver.title
        if title == "Loop":
            assert True
            self.logger.info("Pass: Successfully launched the URL.")
            self.driver.close()
        else:
            self.driver.save_screenshot(".//Screenshots"+"test_launchURL.png")
            self.driver.close()
            self.logger.error("Fail: Failed to launch the URL.")
            assert False

    def test_login(self, setup):
        self.logger.info("**********Login Test***********")
        self.logger.info("Test_002 : Login into the application")
        self.driver = setup
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        self.loginpage = LoginPage(self.driver)
        self.loginpage.setUserName(self.username)
        self.loginpage.setPassWord(self.password)
        self.loginpage.clickLogin()
        self.driver.implicitly_wait(10)
        title = self.driver.title
        if title == "Login | Loop app":
            assert True
            self.logger.info("Pass: Successfully logged into the application.")
        else:
            self.driver.save_screenshot(".//Screenshots" + "test_login.png")
            self.driver.close()
            self.logger.error("Fail: Failed to log into the application.")
            assert False
