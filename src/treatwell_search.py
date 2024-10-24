from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def main():
    print("Starting Treatwell search script.")
    try:
        name = input("Enter salon name: ")
    except Exception as e:
        print(f"Error with input: {e}")
        return

    print(f"Salon Name: {name}")

    # Set up Selenium WebDriver with headless Chrome
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        # Go to Treatwell Germany
        driver.get('https://www.treatwell.de/')
        print("Opened Treatwell website.")

        # Allow the page to load
        time.sleep(2)

        # Accept cookie consent if it appears
        try:
            consent_button = driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
            consent_button.click()
            time.sleep(2)
            print("Accepted cookie consent.")
        except Exception as e:
            print("Cookie consent popup did not appear or could not be clicked.")

        # Step 1: Click on the "Salonname" tab
        try:
            salon_name_tab = driver.find_element(By.XPATH, '//div[contains(@class, "TabBarItem-module--label--1ac881") and text()="Salonname"]')
            salon_name_tab.click()
            time.sleep(1)
            print("Clicked on 'Salonname' tab.")
        except Exception as e:
            print(f"Error clicking 'Salonname' tab: {e}")
            return

        # Step 2: Find the input field using placeholder text
        try:
            print("Trying to find search input by placeholder...")
            search_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Nach Salonnamen suchen"]'))
            )
            print("Search input found by placeholder.")
        except Exception as e:
            print(f"Error finding the search input: {e}")
            return

        # Interact with the search input field
        try:
            search_input.click()  # Focus the input field
            search_input.clear()
            search_input.send_keys(name)
            time.sleep(2)  # Wait for suggestions to load
        except Exception as e:
            print(f"Error interacting with the search input: {e}")
            return

        # Step 3: Wait for and select the exact matching salon name from the dropdown suggestions
        try:
            print("Waiting for dropdown suggestions...")

            # Use a more specific selector to wait for suggestions
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul[class*='DropdownSuggestions-module--items'] li"))
            )
            suggestions = driver.find_elements(By.CSS_SELECTOR, "ul[class*='DropdownSuggestions-module--items'] li")

            # Log all suggestions for debugging purposes
            print("Dropdown suggestions found:")
            for i, suggestion in enumerate(suggestions):
                print(f"{i+1}. {suggestion.text}")

            # Look for an exact match within the suggestions
            found = False
            for suggestion in suggestions:
                if name.lower() in suggestion.text.lower():
                    # Scroll into view to ensure visibility
                    driver.execute_script("arguments[0].scrollIntoView(true);", suggestion)
                    suggestion.click()  # Select the matching salon
                    found = True
                    time.sleep(1)
                    print(f"Selected salon: {suggestion.text}")
                    break

            if not found:
                print(f"No exact match found for {name}.")
                return

        except Exception as e:
            print(f"Error selecting salon from suggestions: {e}")
            return

        # Step 4: Click the "Auf Treatwell finden" button to proceed
        try:
            find_button = driver.find_element(By.XPATH, '//button[contains(text(), "Auf Treatwell finden")]')
            find_button.click()
            time.sleep(5)  # Wait for the search results to load

            # Get the URL of the salon's page
            current_url = driver.current_url
            print("Yes")
            print("Link:", current_url)
        except Exception as e:
            print(f"Error clicking 'Auf Treatwell finden' button: {e}")
            return

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()
        print("Closed the browser and ended the script.")

if __name__ == '__main__':
    main()