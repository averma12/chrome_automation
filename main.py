from selenium import webdriver
import os
import argparse
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

def create_new_tab(driver, url):
    """Create new tab and navigate to URL"""
    # Get current handles
    original_handles = driver.window_handles
    
    # Create new blank tab using Selenium's built-in method
    driver.switch_to.new_window('tab')
    
    # Get new handle
    new_handle = [handle for handle in driver.window_handles if handle not in original_handles][0]
    
    # Switch to new tab
    driver.switch_to.window(new_handle)
    
    # Navigate to URL
    driver.get(url)
    print(f"Navigated to: {url}")

if __name__ == "__main__":
    try:
        # You can specify your profile directory here
        profile_dir = f"{os.path.expanduser('~')}/Library/Application Support/Google/Chrome"
        
        parser = argparse.ArgumentParser()
        parser.add_argument("--profile_dir", type=str, default=profile_dir, help="Path to Chrome profile directory")
        parser.add_argument("--url", type=str, default="https://www.linkedin.com/in/vermaonline/", help="URL to navigate to")
        args = parser.parse_args()
        
        # Connect to Chrome
        driver = connect_to_chrome(args.profile_dir)
        print("Connected to Chrome successfully!")

        # Create a new tab
        create_new_tab(driver, args.url)
        time.sleep(2)  # Wait for tab to load
        
        # List all tabs
        list_tabs(driver)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")