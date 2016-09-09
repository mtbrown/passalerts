import logging
import shelve
import sys

from scrape import scrape_sections, print_sections
from events import check_events
from config import parse_config

DB_FILE = 'pass.db'
CONFIG_FILE = 'pass.conf'


def main():
    logging.basicConfig(format='%(asctime)s: [%(levelname)s] %(message)s', level=logging.INFO)

    config = parse_config(CONFIG_FILE)
    if config is None:
        sys.exit()

    cur_sections = scrape_sections(["CPE 357", "CPE 329", "CPE 321"], 'Fall')
    print_sections(cur_sections)

    with shelve.open(DB_FILE) as prev_sections:
        check_events(None, prev_sections, cur_sections)  # TODO: parse event list from config
        prev_sections.update(cur_sections)


if __name__ == '__main__':
    main()
