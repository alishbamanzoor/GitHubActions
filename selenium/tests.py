# for this to work first run this in terminal "pip install selenium"
# then go to " https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/" and download the matching driver by seeing version on my edge browser
# then extract the zip file and place "msedgedriver.exe" in the same directory
# then run "cd "path of this folder i.e selenium folder""
# then run "python"
import os
import pathlib
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri() 

# driver = webdriver.Chrome()
# because im testing on microsoft edge browser
driver = webdriver.Edge()

class WebpageTests(unittest.TestCase):
    def test_title(self):
        driver.get(file_uri("counter.html"))
        self.assertEqual(driver.title, "Counter")

    def test_increase(self):
        driver.get(file_uri("counter.html"))
        # because "increase = driver.find_element_by_id("increase")" is outdated now and import By for this to work as well
        increase = driver.find_element(By.ID, "increase")
        increase.click()
        # because "driver.find_element_by_tag_name("h1")" is also outdated
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "1")

    def test_decrease(self):
        driver.get(file_uri("counter.html"))
        decrease = driver.find_element(By.ID, "decrease")
        for i in range(3):
            decrease.click()
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "-1")

    def test_multiple_increase(self):
        driver.get(file_uri("counter.html"))
        increase = driver.find_element(By.ID, "increase")
        for i in range(3):
            increase.click()
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "3")

if __name__ == "__main__":
    unittest.main()

# in python interpreter "increase = driver.find_element_by_id("increase")" is no longer supported so instead of this we first run "from selenium.webdriver.common.by import By" then run "increase = driver.find_element(By.ID, "increase")"