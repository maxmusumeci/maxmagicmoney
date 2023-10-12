from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

def go_to_card_page(link):
    link.click()
    time.sleep(2)
    driver.back()
    time.sleep(2)
def upon_enter_website():
    wait = WebDriverWait(driver, 5)
    agree_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button/span[text()='AGREE']")))
    agree_button.click()
    time.sleep(2)
    initial_login_button = driver.find_element(By.XPATH, "//a[@class='nav-link dropdown-toggle'][@data-target='#login-modal']")
    initial_login_button.click()
    username_field = driver.find_element(By.ID, 'layout-modal-email-email')
    password_field = driver.find_element(By.ID,'layout-modal-email-password')
    time.sleep(.5)
    username_field.send_keys('username')
    time.sleep(.5)
    password_field.send_keys('password')
    login_button = driver.find_element(By.XPATH, "//div[@class='form-group']//input[@type='submit'][@value='Log In']")
    driver.execute_script("arguments[0].scrollIntoView();", login_button)
    login_button.click()
    time.sleep(5)

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
  "download.default_directory": r"\Time_series_data\cards_for_2023-09-25T15:07:47Z_video",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

# Initialize WebDriver with options
driver = webdriver.Chrome(options=chrome_options)
url = "https://www.mtggoldfish.com/deck/5820590#paper"
driver.get(url)
upon_enter_website()
print("logged in")
soup = BeautifulSoup(driver.page_source, 'html.parser')
print("prarsed")
target_div = soup.find('div', {'class': 'tab-pane active', 'id': 'tab-online'})
narrower_target_div = target_div.find('div', {"class": "deck-table-container"})


card_hrefs = []
for span in narrower_target_div.find_all('span', {'class': 'card_id card_name'}):
    a_tag = span.find('a')
    if a_tag:
        card_id = a_tag.get('href')
        if card_id:
            card_hrefs.append(card_id)

print("hrefs")

for href in card_hrefs:
    url = f"https://www.mtggoldfish.com/{href}"
    driver.get(url)

    driver.execute_script(f"window.scrollBy(0, {600});")
    try:
        download_btn = driver.find_element(By.CSS_SELECTOR, '.price-history-download-container a.btn')
        driver.execute_script("arguments[0].click();", download_btn)  # Using JS to click
    except Exception as e:
        print(f"Could not click the button: {e}")



driver.quit()