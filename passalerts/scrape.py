from selenium import webdriver
from collections import namedtuple
from bs4 import BeautifulSoup, NavigableString
import logging
import tabulate

PASS_URL = "http://pass.calpoly.edu/main.html"

Section = namedtuple("Section", "course section type id instructor available enrolled waiting")


def scrape_courses(course_list, config):
    logging.info("Initializing webdriver")
    driver = getattr(webdriver, config['Settings']['driver'])()
    driver.implicitly_wait(1)  # wait 1 second for elements to load for entire session
    init_session(driver, PASS_URL, config['Settings']['quarter'])

    logging.info("Selecting courses")
    select_courses(driver, course_list)

    logging.info("Parsing sections")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    section_info = parse_sections(soup, course_list)

    driver.quit()
    logging.info("Finished")
    return section_info


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


def parse_sections(soup, course_list):
    section_info = {key: {} for key in course_list}

    selected_courses = soup.find_all(class_="select-course")
    for course in selected_courses:
        course_name = course.text.split('-')[0].strip()
        course_name = " ".join(course_name.split())  # remove duplicate spaces
        if course_name not in course_list:
            continue  # Skip classes that aren't in watch list, e.g. labs that are auto added

        for section in course.find_all("table"):
            for row in section.tbody:
                if isinstance(row, NavigableString) or row.find(class_="section-notes"):
                    continue  # skip rows containing section notes

                # All table rows containing section info start with this identifier, use as reference
                col = row.find(class_="sectionNumber")
                if col is None:
                    continue

                # Traverse columns for each field of a new Section
                info = []
                for _ in range(len(Section._fields) - 1):
                    info.append(col.text.strip())
                    col = col.find_next_sibling("td")

                section = Section(course=course_name, section=info[0], type=info[1],
                                  id=info[2], instructor=info[3], available=int(info[4]),
                                  enrolled=int(info[5]), waiting=int(info[6]))
                section_info[course_name][section.id] = section

    return section_info


def print_sections(section_info):
    for course, sections in section_info.items():
        print(tabulate([info for _, info in sections.items()], headers=Section._fields))
        print()
