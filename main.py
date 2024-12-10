from selenium import webdriver
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def connect_to_chrome(profile_directory=None):
    """
    Connect to Chrome with optional profile directory
    Args:
        profile_directory (str): Path to Chrome profile directory (optional)
    """
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
    
    if profile_directory:
        chrome_options.add_argument(f"user-data-dir={profile_directory}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def open_new_tab(driver, url):
    """Open a new tab with specified URL"""
    # Execute JavaScript to open new tab
    driver.execute_script(f"window.open('{url}', '_blank');")
    # Switch to the newly opened tab (it will be the last handle)
    driver.switch_to.window(driver.window_handles[-1])
    print(f"Opened new tab with URL: {url}")

def list_tabs(driver):
    """List all open tabs and their URLs"""
    print("\nOpen tabs:")
    for i, handle in enumerate(driver.window_handles):
        driver.switch_to.window(handle)
        print(f"Tab {i}: {driver.current_url}")
    return driver.window_handles

if __name__ == "__main__":
    try:
        # You can specify your profile directory here
        profile_dir = f"{os.path.expanduser('~')}/Library/Application Support/Google/Chrome"
        
        # Connect to Chrome
        driver = connect_to_chrome(profile_dir)
        print("Connected to Chrome successfully!")
        
        # Open a new tab with Google
        open_new_tab(driver, "https://www.google.com")
        time.sleep(2)  # Wait for tab to load
        
        # List all tabs
        list_tabs(driver)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")