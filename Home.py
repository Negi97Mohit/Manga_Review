from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    base_url = 'https://manganato.com/genre-all/'
    driver.get(base_url + '1')
    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.panel-content-genres .content-genres-item'))
    )

    current_page = 1
    while True:
        manga_urls = []

        # Get the URLs of all manga items
        elements = driver.find_elements(By.CSS_SELECTOR, '.panel-content-genres .content-genres-item .genres-item-img.bookmark_check')
        for element in elements:
            manga_url = element.get_attribute('href')
            manga_urls.append(manga_url)

        for manga_url in manga_urls:
            driver.get(manga_url)
            # No need to wait for the page to load explicitly
            # Go back to the previous page
            driver.back()

        try:
            current_page += 1
            driver.get(base_url + str(current_page))
            # Wait for the page to load, adjust the wait time as needed
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'group-page'))
            )
        except:
            break

    driver.quit()

if __name__ == "__main__":
    main()
