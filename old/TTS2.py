import unittest
import time
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TTS2_Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up Appium WebDriver
        desired_caps = {
            "app": "C:\\Program Files\\Atlas Copco\\TTS2\\AtlasCopco.TTS2.RndService.exe",
            "platformName": "Windows",
            "deviceName": "WindowsPC"
        }
        cls.driver = webdriver.Remote(command_executor='http://127.0.0.1:4723', desired_capabilities=desired_caps)

    
    @classmethod
    def tearDownClass(cls):
        if cls.driver is not None:
            cls.driver.quit()
    
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
        WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.NAME, "Read from tool")))
        # time.sleep(20)
        WebDriverWait(self.driver, 120).until_not(EC.presence_of_element_located((By.NAME, "Read from tool")))
        # Verify that the "Read from tool" element is not displayed
        read_tool_element = self.driver.find_elements(By.NAME, "Read from tool")
        self.assertEqual(len(read_tool_element), 0, "Read device failed")

    def read_hardware_info(self):
        hardware_info_element = self.driver.find_element_by_class_name("HardwareInformationView")
        sub_elements = hardware_info_element.find_elements_by_xpath(".//*")

        sub_elements_text = []
        for sub_element in sub_elements:
            sub_elements_text.append(sub_element.text)
        
        return sub_elements_text


    def test_wlan_settings(self):
        # get the list of sub elements
        hardware_info_texts = self.read_hardware_info()
        
        # print out the list of sub elements, or do something else...
        for text in hardware_info_texts:
            if "Odin" in text:
                print("\n Radio module: Odin")
            elif "Bluetooth" in text:
                print("\nRadio module: Bluetooth")
        
        self.driver.find_element_by_accessibility_id("WirelessSettingsTab").click()

        radio_settings_view = self.driver.find_element_by_class_name("RadioSettingsView")

        # 在 RadioSettingsView 区域内查找 ClassName 为 ComboBox 的按键
        radio_settings_view.find_element_by_class_name("ComboBox").click()

        time.sleep(2)
        self.driver.find_element_by_name("WLAN").click()


        # choose channels
        WLAN_settings_view = self.driver.find_element_by_class_name("StbWifiSettingsView")

        Selected_channels = WLAN_settings_view.find_element_by_accessibility_id("ComboBox_SelectedChannels")
        Selected_channels.click()
        time.sleep(0.5)

        # List_Box = self.driver.find_element_by_class_name("ListBoxItem")
        Popup = self.driver.find_element_by_class_name("Popup")
        # Popup.find_element_by_name("Channel 2 (Default channels)").click()
        checkboxes = Popup.find_elements_by_class_name("CheckBox")


        for checkbox in checkboxes[:16]:
            toggle_state = checkbox.get_attribute("Toggle.ToggleState")
            if toggle_state == "0":
                checkbox.click()

        Popup.find_element_by_accessibility_id("PageDown").click()
        time.sleep(1)

        for checkbox in checkboxes[16:32]:  
            toggle_state = checkbox.get_attribute("Toggle.ToggleState")
            if toggle_state == "0":
                checkbox.click()

        Popup.find_element_by_accessibility_id("PageDown").click()
        time.sleep(1)

        for checkbox in checkboxes[32:38]:  
            toggle_state = checkbox.get_attribute("Toggle.ToggleState")
            if toggle_state == "0":
                checkbox.click()

        # save the changes
        # self.driver.find_element_by_accessibility_id("WriteButtons").click()
        # time.sleep(2)
        Selected_channels.click()
        self.driver.find_element_by_accessibility_id("WriteButtons").click()

        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "Ok")))
            self.driver.find_element_by_name("Ok").click()
        except TimeoutException:
            print("Nothing updated, continuing...")
        except NoSuchElementException:
            print("Nothing updated, continuing...")


        # assertion part
        # read again the information, check the popup channels
        self.driver.find_element_by_accessibility_id("ReadButtons").click()
        WebDriverWait(self.driver, 120).until_not(EC.presence_of_element_located((By.NAME, "Read from tool")))

        Selected_channels = WLAN_settings_view.find_element_by_accessibility_id("ComboBox_SelectedChannels")
        Selected_channels.click()
        time.sleep(0.5)

        # List_Box = self.driver.find_element_by_class_name("ListBoxItem")
        Popup = self.driver.find_element_by_class_name("Popup")
        # Popup.find_element_by_name("Channel 2 (Default channels)").click()
        checkboxes_assert = Popup.find_elements_by_class_name("CheckBox")

        all_checked = all(checkbox.get_attribute("Toggle.ToggleState") == "1" for checkbox in checkboxes_assert[22:38])
        assert all_checked, "test failed"

        # pop back the page
        Popup.find_element_by_accessibility_id("PageUp").click()
        Popup.find_element_by_accessibility_id("PageUp").click()
        Selected_channels.click()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TTS2_Tests)
    unittest.TextTestRunner(verbosity=2).run(suite)
