import logging
import shelve

from scrape import scrape_sections, print_sections
from events import check_events

DB_FILE = 'pass.db'


def main():
    logging.basicConfig(format='%(asctime)s: [%(levelname)s] %(message)s', level=logging.INFO)

    cur_sections = scrape_sections(["CPE 357", "CPE 329", "CPE 321"], 'Fall')
    print_sections(cur_sections)

    with shelve.open(DB_FILE) as prev_sections:
        check_events(None, prev_sections, cur_sections)  # TODO: parse event list from config
        prev_sections.update(cur_sections)


if __name__ == '__main__':
    main()
