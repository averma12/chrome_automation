from selenium import webdriver
import platform
import os
import argparse
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import json
import re
import urllib.parse
from urllib.parse import urlparse, parse_qs
from typing import Optional

def get_default_profile_path():
    """Get the default Chrome profile path based on OS"""
    if platform.system() == "Windows":
        return os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')
    elif platform.system() == "Darwin":  # MacOS
        return os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'Google', 'Chrome')
    else:  # Linux
        return os.path.join(os.path.expanduser('~'), '.config', 'google-chrome')

def connect_to_chrome(profile_dir=None):
    """
    Connect to existing Chrome instance with optional profile
    Args:
        profile_dir (str): Path to Chrome profile directory (optional)
    """
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "localhost:9222") #This connects to existing chrome instance
    
    # Add profile directory if specified
    if profile_dir:
        chrome_options.add_argument(f"user-data-dir={profile_dir}")
    
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

def extract_linkedin_username(url: str) -> Optional[str]:
    """
    Extracts the username from a LinkedIn profile URL, supporting various patterns and international domains.
    Uses only Python standard library.
    
    Args:
    url (str): The LinkedIn profile URL.
    
    Returns:
    Optional[str]: The extracted username, or None if no match is found.
    
    Examples of supported URL formats:
    - https://www.linkedin.com/in/username
    - https://de.linkedin.com/in/username
    - https://www.linkedin.com/in/username/
    - https://www.linkedin.com/in/username?lang=en
    - https://www.linkedin.com/pub/username
    - https://www.linkedin.com/profile/view?id=username
    - linkedin.com/in/username
    """
    
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Check if it's a LinkedIn domain
    if not re.search(r'linkedin\.com$', parsed_url.netloc):
        return None
    
    # Extract path and query
    path = parsed_url.path
    query = parse_qs(parsed_url.query)
    
    # Patterns for username extraction
    patterns = [
        r'/in/([^/?]+)',
        r'/company/([^/?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, path)
        if match:
            username = match.group(1).rstrip('/')
            return decode_profile_id(username)
    
    # Check for profile/view?id= format
    if path.startswith('/profile/view') and 'id' in query:
        username = query['id'][0]
        return decode_profile_id(username)
    
    return None

def decode_profile_id(profile_id):
    try:
        return urllib.parse.unquote(profile_id)
    except Exception as e:
        print(f"Error decoding profile ID '{profile_id}': {e}")
        return profile_id  # Return the original string if decoding fails


def take_screenshot(driver, filename):
    """Take a screenshot and save it to a file"""
    # Ensure the screenshots directory exists
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
    
    # Save the screenshot
    filepath = os.path.join('screenshots', filename)
    driver.save_screenshot(filepath)
    print(f"Screenshot saved: {filepath}")

def list_tabs(driver):
    """List all open tabs and their URLs"""
    print("\nOpen tabs:")
    try:
        # Get all window handles first
        handles = driver.window_handles
        
        for i, handle in enumerate(handles):
            # Switch to window with a small delay
            driver.switch_to.window(handle)
            time.sleep(0.5)  # Add small delay to let switch complete
            
            # Get URL with error handling
            try:
                current_url = driver.current_url
                print(f"Tab {i}: {current_url}")
            except Exception as e:
                print(f"Tab {i}: Unable to get URL - {str(e)}")
        
        return handles
    except Exception as e:
        print(f"Error listing tabs: {str(e)}")
        return []

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

def get_all_page_text(driver):
    """Get all visible text using JavaScript"""
    return driver.execute_script(
        "return document.body.innerText"
    )


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
        username = extract_linkedin_username(args.url)
        url = f"https://www.linkedin.com/in/{username}/details/experience/"
        create_new_tab(driver, url)
        time.sleep(2)  # Wait for tab to load
        text = get_all_page_text(driver)
        print(text)
        
        # List all tabs
        list_tabs(driver)
        profile_url = driver.current_url
        print(profile_url)
        create_new_tab(driver, profile_url)
        time.sleep(2)  # Wait for tab to load
        
        # Take screenshot
        if "linkedin.com" in driver.current_url:
            username = extract_linkedin_username(driver.current_url)
            if username:
                #create_new_tab(driver, f"https://www.linkedin.com/in/{username}/details/experience/")
                take_screenshot(driver, f"{username}.png")
                text = get_all_page_text(driver)
                print(text)
            else:
                print("Failed to extract LinkedIn username from the current URL.")
        else:
            print("Current URL is not a LinkedIn profile.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")