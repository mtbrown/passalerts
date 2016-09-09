import configparser
import logging


# Specifies the required sections and parameters expected in the configuration file.
# The first level describes required sections, and the second level described required
# parameters for each section. The third level describes valid arguments, if applicable.
# Finally, the fourth level describes additional required section parameters if the
# associated argument is used.
REQUIRED = {
    'Settings': {
        'quarter': ('Fall', 'Winter', 'Spring', 'Summer'),
    },
    'Notifications': {
        'service': {
            'pushbullet': ('api_key', )
        }
    }
}


def parse_config(config_file):
    config = {}

    parser = configparser.ConfigParser()
    parser.read(config_file)

    if not verify_config(parser):
        return None

    config['quarter'] = parser['Settings']['quarter']
    if config['quarter'] is None or config['quarter'] not in ('Fall', 'Winter', 'Spring', 'Summer'):
        logging.error('Invalid quarter parameter in {0}: {1}'.format(config_file, config['quarter']))
        return None

    # Remaining sections specify courses that should be monitored
    for section in parser.sections().remove('Settings'):
        pass


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
            if valid_args and isinstance(valid_args, dict):
                for dependency in valid_args[arg]:
                    if dependency not in parser[section]:
                        logging.error('"{0}" parameter required when using "{1}" for "{2}'.format(
                            dependency, arg, setting))
                        return False
    return True



