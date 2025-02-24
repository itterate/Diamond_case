from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def get_element_text(driver, path):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, path))
        )
        return element.text.strip()
    except (NoSuchElementException, TimeoutException):
        return ''

def scrape_diamonds():
    url = "https://www.diamondse.info/diamond-prices.asp?shape=Round"
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    
    price_input = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div[1]/table/tbody/tr[2]/td[2]/div[2]/input")))
    price_input.clear()
    price_input.send_keys(30000)
    
    original_window = driver.current_window_handle
    data = []
    
    try:
        for _ in range(1, 300):
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//tbody/tr"))
            )
            
            for i in range(1, 21):
                try:
                    details_button = driver.find_element(By.XPATH, f"/html/body/div[3]/div/div/div/div[2]/table/tbody/tr[{i}]/td/div[5]/span[2]/a/img")
                    driver.execute_script("arguments[0].click();", details_button)
                    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
                    new_window = [w for w in driver.window_handles if w != original_window][0]
                    driver.switch_to.window(new_window)
                    
                    carat = get_element_text(driver, "//td[contains(., 'Carat')]/following-sibling::td")
                    color = get_element_text(driver, "//td[contains(., 'Color')]/following-sibling::td")
                    clarity = get_element_text(driver, "//td[contains(., 'Clarity')]/following-sibling::td")
                    cut = get_element_text(driver, "//td[contains(., 'Cut')]/following-sibling::td")
                    polish = get_element_text(driver, "//td[contains(., 'Polish')]/following-sibling::td")
                    symmetry = get_element_text(driver, "//td[contains(., 'Symmetry')]/following-sibling::td")
                    
                    driver.close()
                    driver.switch_to.window(original_window)
                    cert = get_element_text(driver, f"/html/body/div[3]/div/div/div/div[2]/table/tbody/tr[{i}]/td/div[4]/span[2]")
                    price = get_element_text(driver, f"/html/body/div[3]/div/div/div/div[2]/table/tbody/tr[{i}]/td/div[5]")
                    
                    data.append({
                        'Carat Weight': carat,
                        'Color': color,
                        'Clarity': clarity,
                        'Cut': cut,
                        'Polish': polish,
                        'Symmetry': symmetry,
                        'Report': cert,
                        'Price': price
                    })
                    print(f"{carat}, {color}, {clarity}, {cut}, {polish}, {cert}, {symmetry}, {price}")
                except NoSuchElementException:
                    print(f"Details button not found for row {i} on page {_}.")
                    continue
            
            try:
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div[5]/div[1]"))
                )
                next_page_button.click()
            except TimeoutException:
                print("No more pages to navigate to. Ending scraping.")
                break
    finally:
        pd.DataFrame(data).to_csv("diamonds3.csv", index=False)
        print("Data saved to diamonds3.csv")
        driver.quit()

if __name__ == "__main__":
    scrape_diamonds()
