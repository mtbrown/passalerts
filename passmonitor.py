__author__ = 'mark'

import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

PASS_URL = "http://pass.calpoly.edu/main.html"
WATCH_LIST = ["EE 307"]


def main():
    driver = webdriver.Firefox()

    driver.get(PASS_URL)
    driver.find_element_by_id("dismissNew").click()  # dismiss "What's New"

    # Find "Search by Department" list, select each course in watchlist
    dept_list = driver.find_element_by_xpath("//select[@class='filter-section border-all'][@data-filter='dept']")

    for course in WATCH_LIST:
        dept, course_num = course.split(" ")
        dept_list.find_element_by_xpath("./option[contains(text(), '" + dept + "')]").click()

        time.sleep(3)
        #course_row = driver.find_element_by_xpath("//table/tbody/tr")

        course_row = driver.find_element_by_xpath("//table/tbody/tr[contains(td, {0})]".format(course_num))

    #print(driver.page_source)
    #driver.save_screenshot("cap.png")


if __name__ == "__main__":
    main()
