import pytest
from selenium import webdriver


@pytest.fixture()
def setup():
    driver = webdriver.Chrome()
    return driver

# ################ pytest HTML Report ################


# It is hook for Adding Environment info to HTML Report
def pytest_configure(config):
    config._metadata = {
        "Project Name": "Loop Assignment",
        "Module Name": "Part1: Data Verification",
        "Tester": "Mayuri"
    }
