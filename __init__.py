import logging

from scrape import scrape_sections, print_sections


def main():
    logging.basicConfig(format='%(asctime)s: [%(levelname)s] %(message)s', level=logging.INFO)

    section_info = scrape_sections(["CPE 357", "CPE 329", "CPE 321"], 'Fall')
    print_sections(section_info)


if __name__ == '__main__':
    main()
