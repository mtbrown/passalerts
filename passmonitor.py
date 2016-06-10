import time
from selenium import webdriver
from collections import namedtuple
from tabulate import tabulate

PASS_URL = "http://pass.calpoly.edu/main.html"

QUARTER = "Fall"
WATCH_LIST = ["EE 308", "ENGL 134", "CPE 464", "CPE 329"]


Section = namedtuple("Section", "course section type number professor available enrolled waiting")


def main():
    driver = webdriver.Chrome()
    driver.get(PASS_URL)

    select_courses(driver, WATCH_LIST)
    section_info = parse_sections(driver)

    print_sections(section_info)


def select_courses(driver, course_list):
    # if multiple quarters available, select value specified by QUARTER
    if len(driver.find_elements_by_xpath("//li[contains(text(), 'Select A Quarter')]")):
        driver.find_element_by_xpath("//button[contains(text(), '{0}')]".format(QUARTER)).click()

    if len(driver.find_elements_by_id("modalNewContainer")):
        driver.find_element_by_id("dismissNew").click()  # dismiss "What's New"

    # Find "Search by Department" list, add each course in watch list
    dept_list = driver.find_element_by_xpath("//select[@class='filter-section border-all'][@data-filter='dept']")
    for course in course_list:
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
    section_info = dict.fromkeys(WATCH_LIST)

    time.sleep(2)
    selected_courses = driver.find_elements_by_xpath("//div[@class='select-course']")
    for course in selected_courses:
        course_name = course.text.split('-')[0].strip()
        if course_name not in WATCH_LIST:
            continue  # Skip classes that aren't in watch list, e.g. labs that are auto added

        section_info[course_name] = []
        for section in course.find_elements_by_xpath("./table/tbody/tr"):
            info = [elem.text for elem in section.find_elements_by_xpath("./td[not(.//input)]")]
            if len(info) < 5:
                continue  # Skip table rows that aren't sections, e.g. "Section Notes"
            section_info[course_name].append(Section(course_name, *info[0:7]))

    return section_info


def print_sections(section_info):
    for course, sections in section_info.items():
        print(tabulate(sections, headers=Section._fields))
        print()


if __name__ == "__main__":
    main()
