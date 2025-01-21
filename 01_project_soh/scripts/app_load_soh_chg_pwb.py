from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
import time
import os
import shutil

import sys
import os
# Dynamically add the project root to the module search path
script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
project_root = os.path.abspath(os.path.join(script_dir, ".."))  # One level up (project root)
sys.path.append(project_root)  # Add project root to sys.path

from configs.parameter_web_csv import CHG, PWB


def wait_for_file_download(file_path, timeout=600, check_interval=5):
 
    end_time = time.time() + timeout
    last_size = -1

    while time.time() < end_time:
        if os.path.exists(file_path):
            current_size = os.path.getsize(file_path)
            if current_size == last_size:  # File size hasn't changed, assuming download is complete
                print(f"File {file_path} download completed.")
                return True
            last_size = current_size
        else:
            print(f"Waiting for file {file_path} to appear...")

        time.sleep(check_interval)  # Wait before checking again

    print(f"Timed out waiting for the file {file_path} to download.")
    return False


# List of parameter sets
parameter_sets = [CHG,PWB] #
# Define the file path
for params in parameter_sets:

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get(params['url'])

    # Enter username
    username_field = driver.find_element(By.ID, params['user_box'])
    username_field.send_keys(params['user'])

    # Enter password
    password_field = driver.find_element(By.ID, params['pass_box'])
    password_field.send_keys(params['pass'])

    # Locate and click the login button
    go_button = driver.find_element(By.ID, params['login_box'])
    time.sleep(1)
    go_button.click()

    # Wait until the link is present (4. Stock Value AS of Date by SKU)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, params['stock_menu']))
    )

    # Locate the link element by XPath (4. Stock Value AS of Date by SKU)
    link_element = driver.find_element(By.XPATH, params['stock_menu'])
    href = link_element.get_attribute("href")  # Extract the href attribute
    driver.get(href)

    time.sleep(1)
    # Check the checkbox
    checkbox = driver.find_element(By.ID, params['check_box_store'])
    checkbox.click()

    time.sleep(1)
    # Select Stock On Hand from the dropdown
    dropdown = driver.find_element(By.ID, params['dropdown_box'])
    selectSOH = Select(dropdown)
    selectSOH.select_by_value(params['dropdown_opt'])

    time.sleep(1)
    # Enter Date
    yesterday = datetime.now() - timedelta(days=1)
    formatted_date = yesterday.strftime("%Y%m%d")
    date_field = driver.find_element(By.ID, params['date_box'])
    date_field.send_keys(formatted_date)
    
    # Click to export CSV Table
    go_button = driver.find_element(By.ID, params['export_box'])
    time.sleep(2)
    go_button.click()

    time.sleep(1)
    try:
        # Wait for and switch to the alert
        alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert.accept()
    except:
        pass

    # Locate the link element by XPath (4. Stock Value AS of Date by SKU)
    link_element = driver.find_element(By.XPATH, params['your_file_menu'])
    href = link_element.get_attribute("href")  # Extract the href attribute
    driver.get(href)

    # Wait for the table to be present initially
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, params['download_table']))
    )

    file_ready = False   
    Today = datetime.now()
    formatted_date2 = Today.strftime("%Y%m%d")

    while not file_ready:
        # Refresh the page to get the latest status
        driver.refresh()
        time.sleep(10)
        # Wait for the table to be present after refresh
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, params['download_table']))
        )

        # Get the download table
        table = driver.find_element(By.ID, params['download_table'])
        
        # Loop to check each row
        rows = table.find_elements(By.TAG_NAME, "tr")
        file_name = f'{params['pf_name']}{formatted_date2}.CSV'
        for row in rows[1:]:  # Skip header row
            file_cell = row.find_elements(By.TAG_NAME, "td")[0]  # 1st column is the file_name
            status_cell = row.find_elements(By.TAG_NAME, "td")[4]  # 5th column is the status

            # Check the status for the specific date (Day-1)
            if 'waiting.gif' in status_cell.get_attribute('innerHTML'):
                print("File is still being created... Refreshing page to check again.")
                time.sleep(5)
                break  # Exit the for-loop to recheck the whole table again
            elif 'Successful' in status_cell.text and file_name in file_cell.text:
                file_link_cell = row.find_elements(By.TAG_NAME, "td")[0]  # 1st column has the file link
                file_link = file_link_cell.find_element(By.TAG_NAME, "a")
                file_url = file_link.get_attribute("href")
                print("in loop")
                print(f"File is ready to download: {file_url}")
                file_link.click()  # Click to download the file
                file_ready = True
                break 
        
        if file_ready:
            break  # Exit the while-loop if a file is downloaded
    
    # Wait for the file to download fully 
    file_path = rf"{params['download_dir']}{file_name}"
    if wait_for_file_download(file_path):
        print(f"{file_name} is downloading.")
    else:
        print(f"Failed to download {file_name} within the timeout period.")
    
    print("File download complete.")

    # move the file
    soh_path = rf"{params['soh_path']}{params['dest_file_name']}"
    shutil.copy(file_path, soh_path)
    print("Copy to soh folder finished.")
    time.sleep(10)

    # Close the browser and move to the next params
    driver.quit()



