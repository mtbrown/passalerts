import configparser
import logging
from collections import namedtuple


# Specifies the required sections and parameters expected in the configuration file.
# The first level describes required sections, and the second level described required
# parameters for each section. The third level describes valid arguments, if applicable.
# Finally, the fourth level describes additional required section parameters if the
# associated argument is used.
REQUIRED = {
    'Settings': {
        'quarter': ('Fall', 'Winter', 'Spring', 'Summer'),
        'mode': {
            'continuous': ('delay', ),
            'cron': None
        }
    },
    'Notifications': {
        'service': {
            'pushbullet': ('api_key', ),
            'pushover': ('api_key', 'user_key')
        }
    }
}

Subscription = namedtuple("Subscription", "course sections events")


def parse_config(config_file):
    parser = configparser.ConfigParser()
    parser.read(config_file)

    if not verify_config(parser):
        return None

    return parser


def parse_subscriptions(config):
    subscriptions = {}
    for section in config.sections():
        if section in REQUIRED:
            continue
        if not config[section].getboolean('enabled', fallback=False):
            continue

        events = config[section].get('events', fallback="")
        sections = config[section].get('sections', fallback="")
        subscriptions[section] = Subscription(section, str_to_list(sections), str_to_list(events))
    return subscriptions


def str_to_list(s):
    table = str.maketrans('', '', '[]" ')  # delete '[', ']', '"', and ' ' characters
    return s.strip().translate(table).split(',')


def verify_config(parser):
    for section, settings in REQUIRED.items():
        if section not in parser:
            logging.error('Invalid configuration file, must provide a "[{0}]" section'.format(section))
            return False
        for setting, valid_args in settings.items():
            # Verify that required settings are specified under section header
            if setting not in parser[section]:
                logging.error('Invalid configuration file, "{0}" parameter required under "[{1}]"'.format(
                    setting, section))
                return False

            # Verify that provided argument is within the valid argument list, if specified
            arg = parser[section][setting]
            if valid_args and arg not in valid_args:
                logging.error('Invalid argument "{0}" for "{1}" parameter'.format(arg, setting))
                return False

            # Verify that other parameter dependencies are also fulfilled
            if valid_args and isinstance(valid_args, dict) and valid_args[arg]:
                for dependency in valid_args[arg]:
                    if dependency not in parser[section]:
                        logging.error('"{0}" parameter required when using "{1}" for "{2}"'.format(
                            dependency, arg, setting))
                        return False
    return True
