from selenium import webdriver
from collections import namedtuple
from tabulate import tabulate
from bs4 import BeautifulSoup, NavigableString
import logging

PASS_URL = "http://pass.calpoly.edu/main.html"

QUARTER = "Fall"
WATCH_LIST = ["EE 308", "ENGL 134", "CPE 464", "CPE 329"]


Section = namedtuple("Section", "course section type id professor available enrolled waiting")


def main():
    logging.basicConfig(format='%(asctime)s: [%(levelname)s] %(message)s', level=logging.INFO)

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  # wait 10 seconds for elements to load for entire session
    init_session(driver, PASS_URL, QUARTER)

    logging.info("Selecting courses")
    select_courses(driver, WATCH_LIST)

    logging.info("Parsing sections")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    section_info = parse_sections(soup)

    logging.info("Finished")

    print_sections(section_info)


def init_session(driver, url, quarter):
    driver.get(url)

    # if multiple quarters available, select quarter specified by parameter
    if len(driver.find_elements_by_xpath("//li[contains(text(), 'Select A Quarter')]")):
        driver.find_element_by_xpath("//button[contains(text(), '{0}')]".format(quarter)).click()

    if len(driver.find_elements_by_id("modalNewContainer")):
        driver.find_element_by_id("dismissNew").click()  # dismiss "What's New"


def select_courses(driver, course_list):
    # Find "Search by Department" list, add each course in watch list
    dept_list = driver.find_element_by_xpath("//select[@class='filter-section border-all'][@data-filter='dept']")
    for course in course_list:
        dept, course_num = course.split(" ")
        dept_list.find_element_by_xpath("./option[contains(text(), '{0}')]".format(dept)).click()

        # Locate course in table by finding 'tr' node with 'td' children containing department and course number
        course_row = driver.find_element_by_xpath(
            "//table/tbody/tr[td[contains(text(), '{0}')] and td[contains(text(), '{1}')]]".format(dept, course_num))
        course_row.find_element_by_css_selector(".btn.btn-select").click()  # click "Select Course"

    driver.find_element_by_css_selector(".right.btn.btn-next").click()  # Continue to choose sections


def parse_sections(soup):
    section_info = dict.fromkeys(WATCH_LIST)

    selected_courses = soup.find_all(class_="select-course")
    for course in selected_courses:
        course_name = course.text.split('-')[0].strip()
        course_name = " ".join(course_name.split())  # remove duplicate spaces
        if course_name not in WATCH_LIST:
            continue  # Skip classes that aren't in watch list, e.g. labs that are auto added

        section_info[course_name] = []
        for section in course.find_all("table"):
            for row in section.tbody:
                if isinstance(row, NavigableString) or row.find(class_="section-notes"):
                    continue  # skip rows containing section notes

                col = row.find(class_="sectionNumber")
                if col is None:
                    continue

                info = []
                for _ in range(len(Section._fields) - 1):
                    info.append(col.text.strip())
                    col = col.find_next_sibling("td")
                section_info[course_name].append(Section(course_name, *info))

    return section_info


def print_sections(section_info):
    for course, sections in section_info.items():
        print(tabulate(sections, headers=Section._fields))
        print()


if __name__ == "__main__":
    main()
