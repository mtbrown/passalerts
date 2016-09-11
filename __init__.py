import logging
import shelve
import sys

from scrape import scrape_sections, print_sections
from events import check_events
from config import parse_config, parse_subscriptions

DB_FILE = 'pass.db'
CONFIG_FILE = 'pass.conf'


def main():
    logging.basicConfig(format='%(asctime)s: [%(levelname)s] %(message)s', level=logging.INFO)

    config = parse_config(CONFIG_FILE)
    if config is None:
        sys.exit()

    subscriptions = parse_subscriptions(config)

    cur_sections = scrape_sections(subscriptions.keys(), config['Settings']['quarter'])
    print_sections(cur_sections)

    with shelve.open(DB_FILE) as prev_sections:
        check_events(subscriptions, prev_sections, cur_sections)
        prev_sections.update(cur_sections)


if __name__ == '__main__':
    main()
