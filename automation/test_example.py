import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_login(driver):
    driver.get("https://demo.dataverse.org/")
    driver.find_element(By.LINK_TEXT, "Log In").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "loginForm:option_username"))
    ).click()  # Click on the Username/Email option

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    ).send_keys("normaluser1")

    driver.find_element(By.NAME, "password").send_keys("admin1", Keys.RETURN)

    # Confirm successful login
    assert WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dataverse-user-menu"))
    ).is_displayed()

def test_dashboard_elements(driver):
    # Confirm main dashboard elements are visible
    elements = ["Add Data", "My Data", "Notifications", "normaluser1"]
    for element in elements:
        assert WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, element))
        ).is_displayed()

def test_dataset_browsing(driver):
    driver.get("https://demo.dataverse.org/dataverse/root")
    # Confirm datasets are listed
    datasets = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "datasetResult"))
    )
    assert len(datasets) > 0

def test_search_functionality(driver):
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "searchForm:query"))
    )
    search_box.clear()
    search_box.send_keys("test", Keys.RETURN)

    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "datasetResult"))
    )
    assert len(results) > 0

def test_account_details(driver):
    driver.find_element(By.ID, "dataverse-user-menu").click()
    driver.find_element(By.LINK_TEXT, "Account Information").click()

    user_email = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "userEmail"))
    ).text

    assert user_email != ""

def test_create_new_dataset(driver):
    driver.get("https://demo.dataverse.org/dataverse/root")
    driver.find_element(By.LINK_TEXT, "Add Data").click()
    driver.find_element(By.LINK_TEXT, "New Dataset").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "datasetForm:title"))
    ).send_keys("Automated Test Dataset")

    driver.find_element(By.NAME, "datasetForm:authorName").send_keys("QA Automation")
    driver.find_element(By.NAME, "datasetForm:datasetContactEmail").send_keys("qatester@example.com")
    driver.find_element(By.NAME, "datasetForm:description").send_keys("This dataset was created via automated testing.")
    driver.find_element(By.NAME, "datasetForm:save" ).click()

    # Verify dataset creation success
    assert WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
    ).is_displayed()

def test_edit_dataset(driver):
    driver.get("https://demo.dataverse.org/dataverse/root")
    driver.find_element(By.LINK_TEXT, "My Data").click()
    driver.find_element(By.LINK_TEXT, "Automated Test Dataset").click()
    driver.find_element(By.LINK_TEXT, "Edit").click()

    desc_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "datasetForm:description"))
    )
    desc_field.clear()
    desc_field.send_keys("Updated dataset description via automation.")
    driver.find_element(By.NAME, "datasetForm:save").click()

    assert WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
    ).is_displayed()

def test_upload_file_to_dataset(driver):
    driver.get("https://demo.dataverse.org/dataverse/root")
    driver.find_element(By.LINK_TEXT, "My Data").click()
    driver.find_element(By.LINK_TEXT, "Automated Test Dataset").click()
    driver.find_element(By.LINK_TEXT, "Upload Files").click()

    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "datafile"))
    )
    file_input.send_keys("/path/to/testfile.txt")  # Update with actual file path
    driver.find_element(By.NAME, "upload").click()

    assert WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
    ).is_displayed()

def test_delete_dataset(driver):
    driver.get("https://demo.dataverse.org/dataverse/root")
    driver.find_element(By.LINK_TEXT, "My Data").click()
    driver.find_element(By.LINK_TEXT, "Automated Test Dataset").click()
    driver.find_element(By.LINK_TEXT, "Edit").click()
    driver.find_element(By.LINK_TEXT, "Delete Dataset").click()
    driver.find_element(By.NAME, "confirmDelete").click()

    assert WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
    ).is_displayed()

def test_logout(driver):
    driver.find_element(By.ID, "dataverse-user-menu").click()
    driver.find_element(By.LINK_TEXT, "Log Out").click()

    # Verify logout by checking for login button
    assert WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Log In"))
    ).is_displayed()