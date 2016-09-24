import logging
import shelve
import sys
import os
import time

from .events import check_events
from .notifications import notify
from .scrape import scrape_courses, print_sections

from passalerts.config import parse_config, parse_subscriptions


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DB_FILE = os.path.realpath(os.path.join(BASE_DIR, os.pardir, 'pass.db'))  # ../pass.db
CONFIG_FILE = os.path.realpath(os.path.join(BASE_DIR, os.pardir, 'pass.conf'))  # ../pass.conf


def main():
    logging.basicConfig(format='%(asctime)s: [%(levelname)s] %(message)s', level=logging.INFO)

    config = parse_config(CONFIG_FILE)
    if config is None:
        sys.exit()

    subscriptions = parse_subscriptions(config)

    while True:
        cur_courses = scrape_courses(subscriptions.keys(), config)

        if config['Settings'].get('print', fallback='') == 'True':
            print_sections(cur_courses)

        with shelve.open(DB_FILE) as prev_courses:
            for event in check_events(subscriptions, prev_courses, cur_courses):
                notify(config, event.message)
            prev_courses.update(cur_courses)

        if config['Settings'].get('mode', fallback='') != 'continuous':
            break
        time.sleep(max(config['Settings'].getint('delay'), 5) * 60)


if __name__ == '__main__':
    main()
