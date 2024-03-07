from selenium import webdriver
from selenium.webdriver.common.by import By


class LoginPage:

    # **********************************Page Objects**********************************
    textbox_username_id = ":r1:"
    textbox_password_id = ":r2:"
    button_login_xpath = "//button[normalize-space()='Login']"
    dropdown_profile_css = ".MuiTypography-root.MuiTypography-h3.css-vtwz03-MuiTypography-root"
    button_logout_xpath = "//*[@id='primary-search-account-menu']/div[3]/ul/li[3]"
    # *********************************Function Logics*********************************

    def __init__(self, driver):
        self.driver = driver

    def setUserName(self, username):
        self.driver.find_element(By.ID, self.textbox_username_id).clear()
        self.driver.find_element(By.ID, self.textbox_username_id).send_keys(username)

    def setPassWord(self, password):
        self.driver.find_element(By.ID, self.textbox_password_id).clear()
        self.driver.find_element(By.ID, self.textbox_password_id).send_keys(password)

    def clickLogin(self):
        self.driver.find_element(By.XPATH, self.button_login_xpath).click()

    def clickLogout(self):
        self.driver.find_element(By.CSS_SELECTOR, self.dropdown_profile_css).click()
        self.driver.find_element(By.XPATH, self.button_logout_xpath).click()
