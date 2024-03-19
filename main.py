import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome, ChromeOptions
import time

# //a[contains(@href, 'huggingface') and not(contains(@class, 'tn btn-sm fw-bold btn-light ms-0 p-1 ps-2 pe-2'))]
# //a[contains(@class,"fs-5")]
# //li[contains(@class,"page-item next  m-1")]


def scrape_voice_models():
    # Setup undetected-chromedriver
    options = ChromeOptions()
    options.add_argument("--headless")  # Optional: Run in headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    # Instantiate undetected-chromedriver
    driver = Chrome(options=options)

    # Navigate to the website
    driver.get("https://voice-models.com")

    try:
        # Wait for page elements to load (adjust waiting time as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        print("Page Title:", driver.title)

        # You can further scrape the page by finding elements using various selectors
        # For instance:
        # element = driver.find_element(By.XPATH, "//div[@class='example']")
        # print(element.text)

        for i in range(2):
            try:
                links = driver.find_elements(
                    By.XPATH, "//a[contains(@href, 'huggingface') and not(contains(@class, 'tn btn-sm fw-bold btn-light ms-0 p-1 ps-2 pe-2'))]")

                text = driver.find_elements(
                    By.XPATH, "//a[contains(@class,'fs-5')]")
                with open('voice_models.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    for i in range(len(links)):
                        writer.writerow(
                            [text[i].text, links[i].get_attribute('href')])

                next_page_button = driver.find_element(
                    By.XPATH, "//li[contains(@class,'page-item next  m-1')]")

                next_page_button.click()
                while (True):
                    new_links = driver.find_elements(
                        By.XPATH, "//a[contains(@href, 'huggingface') and not(contains(@class, 'tn btn-sm fw-bold btn-light ms-0 p-1 ps-2 pe-2'))]")
                    if (links[0] != new_links[0]):
                        break
                    time.sleep(0.5)

            except Exception as e:
                print("Error occurred while scraping:", str(e))

    finally:
        # Close the browser session
        driver.quit()


# Call the function to execute scraping
scrape_voice_models()
