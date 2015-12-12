import time
from selenium import webdriver

PASS_URL = "http://pass.calpoly.edu/main.html"
WATCH_LIST = ["EE 307"]


def main():
    driver = webdriver.Firefox()
    driver.get(PASS_URL)

    select_courses(driver)
    parse_sections(driver)


def select_courses(driver):
    driver.find_element_by_id("dismissNew").click()  # dismiss "What's New"

    # Find "Search by Department" list, add each course in watch list
    dept_list = driver.find_element_by_xpath("//select[@class='filter-section border-all'][@data-filter='dept']")
    for course in WATCH_LIST:
        dept, course_num = course.split(" ")
        dept_list.find_element_by_xpath("./option[contains(text(), '{0}')]".format(dept)).click()

        time.sleep(2)
        # Locate course in table by finding 'tr' node with 'td' children containing department and course number
        course_row = driver.find_element_by_xpath(
            "//table/tbody/tr[td[contains(text(), '{0}')] and td[contains(text(), '{1}')]]".format(dept, course_num))
        course_row.find_element_by_css_selector(".btn.btn-select").click()  # click "Select Course"

    time.sleep(2)
    driver.find_element_by_css_selector(".right.btn.btn-next").click()  # Continue to choose sections


def parse_sections(driver):
    time.sleep(2)
    selected_courses = driver.find_elements_by_xpath("//div[@class='select-course']")

    for course in selected_courses:
        course_name = course.text.split('-')[0].strip()
        if course_name not in WATCH_LIST:
            continue  # Skip classes that aren't in watch list, e.g. labs that are auto added

        for section in course.find_elements_by_xpath("./table/tbody/tr"):
            info = [elem.text for elem in section.find_elements_by_xpath("./td")]
            if len(info) < 5:
                continue  # Skip table rows that aren't sections, e.g. "Section Notes"

            print(info)


if __name__ == "__main__":
    main()
