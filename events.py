import logging
from collections import namedtuple


Event = namedtuple('Event', 'event message course section')

def check_available(prev_sections, cur_sections):
    """
    Checks if there are currently seats available in the section list. If there were already
    seats available in the previous section list, False is returned to prevent multiple
    notification triggers.
    """
    for id, section in cur_sections.items():
        if section.available > 0:
            # Ignore if the section was previously available
            if id in prev_sections and prev_sections[id].available > 0:
                continue
            yield (section, section.available)


def check_new_section(prev_sections, cur_sections):
    """
    Checks if a new section has been added.
    """
    for id, section in cur_sections.items():
        if id not in prev_sections:
            yield (section, section.id)


def check_instructor_change(prev_sections, cur_sections):
    """
    Checks if the instructor has been modified for any of the sections.
    """
    for id, section in prev_sections.items():
        if id not in cur_sections:
            continue  # section was removed since last update
        if section.instructor != cur_sections[id].instructor:
            yield (section, section.instructor)


event_checkers = {
    'available': check_available,
    'new_section': check_new_section,
    'instructor_change': check_instructor_change
}


humanize_event = {
    'available': "{extra} seat(s) are now available in section {section} of {course}.",
    'new_section': "A new section was added for {course}: {extra}",
    'instructor_change': "The instructor for section {section} of {course} was changed to {extra}.",
}


def check_events(subscriptions, prev_courses, cur_courses):
    for course, subscription in subscriptions.items():
        if course not in prev_courses:
            continue  # if course was just added, can't check for changes

        for event in subscription.events:
            if event not in event_checkers:
                logging.warning('Unrecognized event "{0}" in {1} subscription'.format(event, course))
                continue

            for section, extra in event_checkers[event](prev_courses[course], cur_courses[course]):
                logging.info("Detected event: {0}, {1}, {2}".format(event, course, section))
                message = humanize_event[event].format(section=section.section, course=course, extra=extra)
                yield Event(event, message, course, section)
