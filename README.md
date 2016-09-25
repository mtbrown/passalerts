[![Build Status](https://travis-ci.org/mtbrown/passalerts.svg?branch=master)](https://travis-ci.org/mtbrown/passalerts)

# PASS Alerts

PASS Alerts monitors the Cal Poly registration system (PASS) and helps you register for high demand classes.
Alerts are configurable and can be sent when a seat becomes available in a class, a new section is opened, or even on user-defined custom events.

## Installation

Simply clone the respository and install the dependencies with pip.

```
$ git clone https://github.com/mtbrown/passalerts.git
$ cd passalerts
$ pip install -r requirements.txt
```

## Configuration

All configuration occurs in `pass.conf`.

Sample configuration file:
```
[Settings]
quarter = Fall
mode = continuous
delay = 20
driver = Chrome
print = True

[Notifications]
service = pushbullet
api_key = <redacted>

# Subscriptions
[CPE 357]
enabled = true
events = ["available"]

[CPE 464]
enabled = true
events = ["available", "instructor_change"]
```

#### Settings
* **quarter**: The current regirstration quarter. Used to select the correct quarter when registration is open for multiple quarters.
* **mode**: PASS Alerts can run in *cron* mode or *continuous* mode. *cron* mode will execute the script once and then exit. *continuous* mode will run the script forever in a loop for long-term usage.
* **delay**: Only applicable for continuous mode. Specifies the delay in minutes between each time PASS is scraped and notifications are sent. The delay must be at least 5 minutes or it will be ignored.
* **driver**: The selenium webdriver to use when scraping PASS. Possible options include *Chrome* or *Firefox*. See the advanced section below for information about using *PhantomJS*.
* **print**: When *True*, the current status of monitored sections will be printed in the console every update.

#### Notifications
* **service**: Supported services currently include *pushbullet* and *pushover*.
  * **pushbullet**: Requires an additional parameter *api_key* found on your Account Settings page.
  * **pushover**: Requires additional parameters *api_key* and *user_key*.

#### Subscriptions
Course subscriptions make up the rest of the configuration file. The course name must be the header of the section.

The following parameters can be specified for subscriptions:
* **enabled**: A simple toggle that will disable the subscription when *False*.
* **events**: A list of event strings that specify the events you want to be notified of.
  * **"available"**: Triggers when a seat becomes available in any section of the course.
  * **"new_section"**: Triggers when a new section is added for the course.
  * **"instructor_change"**: Triggers when the intructor is changed for any of the sections of the course.

## Usage
Execute the script by running `passalerts.py`.
```
$ python passalerts.py
```

## License

TODO: Write license