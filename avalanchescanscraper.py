from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pprint
import time
import csv
import os 

DRIVER = "chrome"
txt_path = "C:\\Users\\samom\\Desktop\\crypto tracker\\Scrapers"


def webdriver_function():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://avascan.info/blockchain/all/transactions")
    pages = 1
    hashtags_list = []

    for i in range(pages):
        hashtags = driver.find_elements(By.CLASS_NAME, "link-address")
        for hashtag in hashtags:
            if hashtag.text.startswith('0x') and len(hashtag.text) == 42:
                hashtags_list.append(hashtag.text.strip())
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        wait = WebDriverWait(driver, 20)
        next_page_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-cy="next"]')))        
        driver.execute_script("arguments[0].scrollIntoView(true);", next_page_btn)
        
        time.sleep(2)
    
    pprint.pprint(hashtags_list)
    driver.quit()
    
    return hashtags_list

def runindex(hashtags_list):
    run_count_file = os.path.join(txt_path, "run_count_avalanche.txt")
    if os.path.exists(run_count_file):
        with open(run_count_file, "r") as file:
            run_count = int(file.read().strip()) + 1
    else:
        run_count = 1

    with open(run_count_file, "w") as file:
        file.write(str(run_count))
    download_path = f"C:\\Users\\samom\\Desktop\\crypto tracker\\CSV Before Scan\\avalanchescanscrapeddata_{run_count}.csv"
    with open(download_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['From'])
        writer.writerows([[hashtag] for hashtag in hashtags_list])
    print(hashtags_list)

hashtags_list = webdriver_function()
runindex(hashtags_list)