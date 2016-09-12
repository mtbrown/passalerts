import logging
import shelve
import sys

from scrape import scrape_sections, print_sections
from events import check_events
from config import parse_config, parse_subscriptions
from notifications import notify

DB_FILE = 'pass.db'
CONFIG_FILE = 'pass.conf'


def main():
    logging.basicConfig(format='%(asctime)s: [%(levelname)s] %(message)s', level=logging.INFO)

    config = parse_config(CONFIG_FILE)
    if config is None:
        sys.exit()

    subscriptions = parse_subscriptions(config)

    cur_courses = scrape_sections(subscriptions.keys(), config['Settings']['quarter'])
    print_sections(cur_courses)

    with shelve.open(DB_FILE) as prev_courses:
        for event in check_events(subscriptions, prev_courses, cur_courses):
            notify(config, event.message)
        prev_courses.update(cur_courses)


if __name__ == '__main__':
    main()
