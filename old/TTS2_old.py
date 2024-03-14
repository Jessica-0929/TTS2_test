import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TTS2_Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up WinAppDriver
        desired_caps = {
            "app": "C:\\Program Files\\Atlas Copco\\TTS2\\AtlasCopco.TTS2.RndService.exe",
            "platformName": "Windows",
            "deviceName": "WindowsPC"
        }
        cls.driver = WebDriver(command_executor='http://127.0.0.1:4723', desired_capabilities=desired_caps)

    @classmethod
    def tearDownClass(self):
        if self.driver is not None:
            self.driver.quit()

    def test_connect_device(self):
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.NAME, "L0560008")))
        self.driver.find_element(By.NAME, "L0560008").click()
        self.driver.find_element(By.NAME, "Connect").click()

        # Wait until "information" is displayed
        WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.NAME, "Information")))

        # Assert the "information" is displayed
        info_button = self.driver.find_element(By.NAME, "Information")
        self.assertTrue(info_button.is_displayed(), "The device is not connected")


    def test_read_device(self):
        self.driver.find_element_by_accessibility_id("ReadButtons").click()

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TTS2_Tests)
    unittest.TextTestRunner(verbosity=2).run(suite)
