from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
from utils import get_logger, get_topics


def click_elem(selector):
    WebDriverWait(driver, config.timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
    ).click()


def keys_elem(selector, *keys):
    key_elem =  WebDriverWait(driver, config.timeout).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
    )
    for key in keys:
        key_elem.send_keys(key)


def main():
    try:
        fcm_topics = get_topics()
        if len(fcm_topics) == 0:
            raise Exception('No topics found')
        
        log = get_logger()
        
        driver.get("https://console.firebase.google.com/project/pronto-645f0/notification")

        keys_elem('[name=identifier]', config.login_email, Keys.RETURN)

        keys_elem('[name=password]', config.login_password, Keys.RETURN)

        for fcm_topic in fcm_topics:
            click_elem('.newCampaign')

            keys_elem('.message-title', config.title)

            keys_elem('.message-text', config.message)

            click_elem('button.mat-focus-indicator.mat-raised-button.mat-button-base.mat-primary.ng-star-inserted')

            click_elem('.target-topic-toggle button[name^=mat-button-toggle-group-]')

            keys_elem('.message-topic', fcm_topic)

            click_elem('.cta-bottom .mat-primary')

            click_elem('.action-buttons .mat-raised-button')

            log(f"{fcm_topic} sent")
    finally:
        driver.close()


driver = webdriver.Chrome('./chromedriver')
main()
