from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

WAITTIME = 10000
SLEEPSEC = 3
LOOP = -1 # -1 for infinite
REPLACING_COURSE = "컴퓨터 비전 개론"

def check_availability(driver):
    availability = WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//table[@id='listTable']//tr[2]/td[11]"))).get_attribute("innerHTML")
    current_enrollment = driver.find_element("xpath", "//table[@id='listTable']//tr[2]/td[12]").get_attribute("innerHTML")
    return availability > current_enrollment

def enroll(driver):
    table = driver.find_element("xpath", "//table[@id='courseList']/tbody")
    for tr in table.find_elements(By.TAG_NAME, "tr"):
        if tr.find_element("xpath", "./td[8]").get_attribute("innerHTML") == REPLACING_COURSE:
            tr.find_element("xpath", "./td[15]/a").click()
            break
    driver.switch_to.alert.accept()
    driver.refresh()
    # WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//div[@id='assistSearch']//img"))).click()
    driver.find_element("xpath", "//table[@id='listTable']//tr[2]/td[21]/a").click()
    time.sleep(1000)

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 2)

    driver.get("https://cais.kaist.ac.kr/courseRegistration")
    
    # WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((By.XPATH, "//div[@class='menu_body']//li[3]"))).click()
    i = 1
    while(not check_availability(driver)):
        print("not available")
        i += 1
        time.sleep(SLEEPSEC)
        if (i > LOOP and LOOP != -1):
            break
        driver.refresh()

    enroll(driver)

    # a[@id='courseRegistration']