from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_login_dataverse():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://dataverse-internal.iq.harvard.edu/")

    # Click login
    driver.find_element(By.LINK_TEXT, "Log In").click()
    time.sleep(2)  # wait for login page to load

    # Enter credentials
    driver.find_element(By.NAME, "username").send_keys("SmokeTest25")
    driver.find_element(By.NAME, "password").send_keys("admin1", Keys.RETURN)
    time.sleep(3)  # wait for login to complete

    assert "Dataverse" in driver.title
    driver.quit()
