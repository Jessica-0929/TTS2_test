import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logging.basicConfig(filename='test_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

@pytest.fixture(scope="session")
def winappdriver():
    desired_caps = {
        "app": "C:\\Program Files\\Atlas Copco\\TTS2\\AtlasCopco.TTS2.RndService.exe",
        "platformName": "Windows",
        "deviceName": "WindowsPC"
    }
    driver = webdriver.Remote(command_executor='http://127.0.0.1:4723', desired_capabilities=desired_caps)
    yield driver
    driver.quit()

def test_click_button(winappdriver):
    WebDriverWait(winappdriver, 20).until(EC.element_to_be_clickable((By.NAME, "?"))).click()
    time.sleep(5)

def test_manual_link():
    driver = webdriver.Chrome(executable_path='E:\\AutoTestTTS2\\chromedriver-win64\\chromedriver.exe')
    try:
        driver.get("https://picontent.atlascopco.com/cont/internal/dir/8f/17739535627__html5_internal/en-US/index.html")
        time.sleep(10)
        assert "ToolsTalk Service 2 Service" in driver.page_source, "Manual not working"
        logging.info("test_TTS2_manual passed")
    finally:
        driver.quit()


if __name__ == '__main__':
    pytest.main(['-v','-s'])