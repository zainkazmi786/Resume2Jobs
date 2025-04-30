import sys
import os
from typing import Union
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import random
from datetime import date , datetime
import time
from langchain.tools import Tool

from . import formatting
# import formatting
import json

from config import jobss
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth





# --- Job Search Parameters ---
# JOBTITLES =  [
#         "Web Developer",
#         "Frontend Developer",
#         "Full-Stack Developer",
#         "Software Engineer",
#         "AI Engineer"
#     ]
# LOCATION = "Pakistan"

job_records = {"id": "zainkazmi258@gmail.com", "job_records_to_scrape": [{"job_title": "Web Developer", "city": "Haripur", "country": "Pakistan", "workplace": ["Remote", "On-site", "Hybrid"], "experience_level": ["Internship", "Entry Level"]}, {"job_title": "Frontend Developer", "city": "Haripur", "country": "Pakistan", "workplace": ["Remote", "On-site", "Hybrid"], "experience_level": ["Internship", "Entry Level"]}, {"job_title": "Full Stack Developer", "city": "Haripur", "country": "Pakistan", "workplace": ["Remote", "On-site", "Hybrid"], "experience_level": ["Internship", "Entry Level"]}]}

def select_experience_levels(driver ,levels):
    """
    Selects the given experience levels from the dropdown and applies the filter.
    
    :param driver: Selenium WebDriver instance
    :param levels: List of experience levels to select (e.g., ["Internship", "Entry Level"])
    """

    if not hasattr(select_experience_levels, "counter"):
        select_experience_levels.counter = 0

    level_mapping = {
        "Internship": "experience-1",
        "Entry Level": "experience-2",
        "Associate": "experience-3",
        "Mid-Senior Level": "experience-4",
        "Director": "experience-5",
        "Executive": "experience-6"
    }
        
    # Click the experience filter button
    try:
        filter_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, os.getenv("FILTER_BY_EXP_ID")))
        )
        filter_button.click()
    except Exception as e:
        print("Error clicking filter button:", e)
        return


    if select_experience_levels.counter != 0:
        try:
            # Wait for the dropdown to be visible
            time.sleep(2)  # Adding a small delay before checking for the reset button
            reset = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, os.getenv("RESET_BUTTON_EXP")))
            )

            # Ensure it only clicks if the button text is "Reset"
            if reset.find_element(By.TAG_NAME, "span").text == "Reset":
                reset.click()

            random_delay(3, 5)
            print("reset clicked")
            time.sleep(2)
        except TimeoutException:
            print("❌ Timeout: Experience filter dropdown not visible.")
            return


    # Select the checkboxes for the specified experience levels
    for level in levels:
        if level in level_mapping:
            checkbox_id = level_mapping[level]
            label_xpath = f"//label[@for='{checkbox_id}']"

            try:
                random_delay(1,3)
                label = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, label_xpath))
                )
                label.click()
                # a = input("does it click")
                print(f"Selected: {level}")
                # random_delay(1,3)
            except Exception as e:
                print(f"Error selecting {level}:", e)

    # Click the apply button
    try:
        random_delay(2, 4)

        for _ in range(3):  # Retry up to 3 times
            try:
                apply_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, os.getenv("APPLY_BUTTON_EXP_XPATH")))
                )
                apply_button.click()
             
                select_experience_levels.counter += 1

                print("✅ Applied filter successfully .")
                random_delay(3, 6)
                break  # Exit loop if successful
            except StaleElementReferenceException:
                print("🔄 Element became stale, retrying ...")
            except TimeoutException:
                print("❌ Apply button not found within time.")
                break
        else:
            print("❌ Failed to apply filter after multiple attempts.")
    except Exception as e:
        print("❌ Error clicking apply button:", e)

def select_workplace_type(driver ,levels):
    """
    Selects the given workplace type from the dropdown and applies the filter.
    
    :param driver: Selenium WebDriver instance
    :param levels: List of experience levels to select (e.g., ["Internship", "Entry Level"])
    """
    if not hasattr(select_workplace_type, "counter"):
        select_workplace_type.counter = 0

    level_mapping = {
        "On-site": "workplaceType-1",
        "Remote": "workplaceType-2",
        "Hybrid": "workplaceType-3"
    }

    # Click the experience filter button
    try:
        filter_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, os.getenv("FILTER_BY_WORKPLACE_ID")))
        )
        filter_button.click()

    except Exception as e:
        print("Error clicking filter button:", e)
        return
    
    if select_workplace_type.counter != 0:
        try:
            reset = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, os.getenv("RESET_BUTTON_WORKPLACE")))
            )

            # Ensure it only clicks if the button text is "Reset"
            if reset.find_element(By.TAG_NAME, "span").text == "Reset":
                reset.click()


            random_delay(3,4)
        except TimeoutException:
            print("❌ Timeout: Experience filter dropdown not visible.")
            return



    # Select the checkboxes for the specified experience levels
    for level in levels:
        if level in level_mapping:
            checkbox_id = level_mapping[level]
            label_xpath = f"//label[@for='{checkbox_id}']"

            try:
                random_delay(2,4)
                label = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, label_xpath))
                )
                label.click()
                print(f"Selected: {level}")
                
            except Exception as e:
                print(f"Error selecting {level}:", e)

    # Click the apply button
    try:

        for _ in range(3):  # Retry up to 3 times
            try:
                apply_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, os.getenv("APPLY_BUTTON_WORKPLACE_XPATH")))
                )
                apply_button.click()
                select_workplace_type.counter += 1

                print("✅ Applied filter successfully.")
                break  
            except StaleElementReferenceException:
                print("🔄 Element became stale, retrying...")
            except TimeoutException:
                print("❌ Apply button not found within time.")
                break
        else:
            print("❌ Failed to apply filter after multiple attempts.")
    except Exception as e:
        print("❌ Error clicking apply button:", e)



def scrape_jobs(driver, jobtitle, workplacelist, explist, city, country):
    try:
        # Wait for the job list to be available
        try:
            jobs_list = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, os.getenv("JOB_UL")))
            )
        except TimeoutException:
            print("Timeout: Job list (ul) element not found.")
            driver.save_screenshot("error_job_list.png")
            return 0
        
        jobs = jobs_list.find_elements(By.XPATH, "./li")
        print(f"Found {len(jobs)} jobs on current page.")

        for index, job in enumerate(jobs):
            try:
                random_delay(2, 3)
                driver.execute_script("arguments[0].scrollIntoView(true);", job)
                
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(job)).click()
                except (TimeoutException, ElementClickInterceptedException) as e:
                    print(f"Error clicking job {index+1}: {e}")
                    driver.save_screenshot(f"error_click_job_{index+1}.png")
                    continue

                random_delay(1, 2)

                try:
                    a_tag = job.find_element(By.XPATH, ".//a")
                    job_link = a_tag.get_attribute("href")
                except NoSuchElementException:
                    print(f"a-tag not found inside job {index+1}")
                    driver.save_screenshot(f"error_a_tag_{index+1}.png")
                    continue

                try:
                    description = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, os.getenv("JOB_DESC")))
                    ).text.strip()
                except TimeoutException:
                    print(f"Timeout: Job description not found for job {index+1}")
                    driver.save_screenshot(f"error_description_{index+1}.png")
                    continue

                print(f"Scraped job {index+1}/{len(jobs)} on current page.")

                # Extract and save job
                job_entry = formatting.extract_job_fields(description)
                job_entry.update({
                    "job_link": job_link,
                    "job_searched": jobtitle,
                    "city": city,
                    "country": country,
                    "workplace_type": workplacelist,
                    "experience_levels": explist,
                    "scraped_date": date.today().strftime("%Y-%m-%d"),
                    "createdAt": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                })

                jobss.insert_one(job_entry)
                print("Successfully inserted job into database.")

            except Exception as e:
                print(f"Unexpected error scraping job {index+1}: {e}")
                driver.save_screenshot(f"unexpected_error_job_{index+1}.png")
                continue

    except Exception as e:
        print(f"Critical error in scrape_jobs function: {e}")
        driver.save_screenshot("critical_error_scrape_jobs.png")
        return 0

    return len(jobs) if "jobs" in locals() else 0




def go_to_next_page(driver , current_page):
    try:
        next_button_xpath = os.getenv("NEXT_BUTTON")
        # Try clicking the "Next" button
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, next_button_xpath))
        )
        next_button.click()
        time.sleep(2)
        print(f"Moved to next page using 'Next' button")
        return True

    except (NoSuchElementException, TimeoutException):
        print("Next button not found, trying page number...")

        try:
            pagination_div = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list__pagination"))
            )

            pagination_ul = pagination_div.find_element(By.TAG_NAME, "ul")

            next_page_xpath = f".//li[@data-test-pagination-page-btn='{current_page + 1}']/button"
            next_page_button = pagination_ul.find_element(By.XPATH, next_page_xpath)

            next_page_button.click()
            time.sleep(2)
            print(f"Moved to page {current_page + 1} using pagination numbers")
            return True

        except (NoSuchElementException, TimeoutException):
            print("No more pages available.")
            return False

    
def enter_search_criteria( driver ,job_title, city ,country , delay_function):
    """
    Enters job title and location into the search fields.
    
    Args:

    - driver: Selenium WebDriver instance.
    - job_title: The job title to search for.
    - location: The location to search in.
    - delay_function: Function to introduce a random delay.
    
    Handles exceptions and captures screenshots in case of failure.
    """
    try:
        # --- Locate Search Input Fields ---
        input_fields = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "basic-input"))
        )

        if len(input_fields) >= 2:
            # First input is for job title
            job_search = input_fields[0]
            job_search.clear()
            job_search.send_keys(job_title)
            delay_function(1, 2)

            # Second input is for location
            location_input = input_fields[1]
            location_input.clear()
            location_input.send_keys(city + ", " + country)
            delay_function(1, 2)

            # --- Handle Location Suggestions ---
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, os.getenv("LOCATION_SUGGESTION_UL")))
            )
            location_input.send_keys(Keys.DOWN)
            delay_function(0.5, 1)
            location_input.send_keys(Keys.ENTER)

    except TimeoutException:
        print("❌ Timeout: The input fields were not found within the specified time.")
        driver.save_screenshot("timeout_error.png")
    except NoSuchElementException:
        print("❌ Error: The input fields could not be located.")
        driver.save_screenshot("element_not_found_error.png")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        driver.save_screenshot("unexpected_error.png")

def get_stealth_driver():
    try:
        chrome_options = Options()
        chrome_options.add_argument(f"user-agent={random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'
        ])}")

        # Stealth and optimization options
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-webgl")
        chrome_options.add_argument("--headless")  # optional

        service = Service("C:/Users/Hp/Downloads/chromedriver-win64/chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

        return driver
    except Exception as e:
        print(f"❌ Error initializing Chrome: {e}")

# --- Random Delay Function ---
def random_delay(min=1, max=6):
    time.sleep(random.uniform(min, max))


    # --- Login to LinkedIn ---
def login(driver):
    driver.get("https://www.linkedin.com/jobs")
    random_delay(3, 5)

    # Enter email and password
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "session_key"))
    )
    email_input.send_keys(os.getenv("LINKEDIN_EMAIL"))

    password_input = driver.find_element(By.ID, "session_password")
    password_input.send_keys(os.getenv("LINKEDIN_PASSWORD"))

    # Click login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    random_delay(2, 4)
    random_delay(2, 4)

# --- Navigate to Jobs Page ---


def scrape_jobs_and_store( jobtitles, city, country, workplacelist, explist):
    driver = get_stealth_driver()

    """Scrapes jobs and stores the data in MongoDB."""
    login(driver)
    for i, jobtitle in enumerate(jobtitles):
        enter_search_criteria(driver ,jobtitle, city[i], country[i], random_delay)
        
        # Select workplace type if different from the last job (avoiding IndexError)
        if (i == 0 or workplacelist[i] != workplacelist[i - 1]):
            time.sleep(4)
            select_workplace_type(driver ,workplacelist[i])
            time.sleep(6)  # Adding a small random delay
        
        # Select experience level if different from the last 
        if (i == 0 or explist[i] != explist[i - 1]):
            select_experience_levels(driver ,explist[i])
        
        time.sleep(5)  # Delay before scraping
        
        current_page = 1
        total_jobs = 0
        
        while True:
            print("starting")
            job_count = scrape_jobs(driver ,jobtitle, workplacelist[i], explist[i], city[i], country[i])
            total_jobs += job_count
            
            if job_count == 0 or not go_to_next_page(driver , current_page):
                break
            current_page += 1
            print(f"Completed Scraping for {jobtitle} on page {current_page}")

        print(f"Completed scraping for {jobtitle}. Total jobs scraped: {total_jobs}")

    print("✅ Successfully scraped all jobs.")
    driver.quit()

def scraping_tool(input_data: Union[str, dict]):
    """LangChain tool wrapper for job scraping based on job records."""

    try:
        # Load JSON string if necessary
        if isinstance(input_data, str):
            input_data = json.loads(input_data)
    except json.JSONDecodeError:
        return {"error": "Invalid input format. Must be a valid JSON string or dict."}

    try:
        jobrecords = input_data.get("job_records_to_scrape")
        if not isinstance(jobrecords, list) or not jobrecords:
            return {"status": "Failed", "message": "No job records provided."}

        # Extract fields
        jobtitles = [job["job_title"] for job in jobrecords]
        cities = [job["city"] for job in jobrecords]
        countries = [job["country"] for job in jobrecords]
        workplacelist = [job["workplace"] for job in jobrecords]
        explist = [job["experience_level"] for job in jobrecords]

        load_dotenv()
        scrape_jobs_and_store(jobtitles, cities, countries, workplacelist, explist)

        
        return {"status": "Success", "message": "Scraping completed."}

    except Exception as e:
        return {"status": "Failed", "message": f"Error occurred: {str(e)}"}


job_scraping_tool = Tool(
    name="Job Scraping Tool",
    func=scraping_tool,
    description=(
        "Use this tool to scrape job listings for a given user, based on a list of job records. "
        "Each job record includes details like job title, city, country, workplace types, and experience levels.\n\n"
        "**Input Format:** A STRING (json) with the following structure:\n"
        "- 'id': string (e.g., '123@gmail.com') — Unique identifier for the user.\n"
        "- 'job_records_to_scrape': list of job entries, where each entry is a dictionary with:\n"
        "  - 'job_title': string (e.g., 'Web Developer')\n"
        "  - 'city': string (e.g., 'Lahore')\n"
        "  - 'country': string (e.g., 'Pakistan')\n"
        "  - 'workplace': list of workplace types (e.g., ['Remote', 'On-site'])\n"
        "  - 'experience_level': list of experience levels (e.g., ['Internship', 'Entry Level'])\n\n"
        "This tool is typically used when job records are missing from the database and need to be fetched via scraping."
    )
)

if __name__ == "__main__":
    # Example usage
    job_id = "12345"  # Replace with actual job ID
    scraping_tool(job_records)


        