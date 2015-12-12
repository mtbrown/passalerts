import time
from selenium import webdriver

PASS_URL = "http://pass.calpoly.edu/main.html"
WATCH_LIST = ["EE 307"]


def main():
    driver = webdriver.Firefox()

    driver.get(PASS_URL)
    driver.find_element_by_id("dismissNew").click()  # dismiss "What's New"

    # Find "Search by Department" list
    dept_list = driver.find_element_by_xpath("//select[@class='filter-section border-all'][@data-filter='dept']")

    for course in WATCH_LIST:
        dept, course_num = course.split(" ")
        dept_list.find_element_by_xpath("./option[contains(text(), '{0}')]".format(dept)).click()

        time.sleep(2)
        # Locate course in table by finding 'tr' node with 'td' children containing department and course number
        course_row = driver.find_element_by_xpath(
            "//table/tbody/tr[td[contains(text(), '{0}')] and td[contains(text(), '{1}')]]".format(dept, course_num))
        course_row.find_element_by_css_selector(".btn.btn-select").click()  # click "Select Course"


if __name__ == "__main__":
    main()
