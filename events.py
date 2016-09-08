def check_events(events, prev_sections, cur_sections):
    pass


def check_available(prev_sections, cur_sections):
    """
    Checks if there are currently seats available in the section list. If there were already
    seats available in the previous section list, False is returned to prevent multiple
    notification triggers.
    """
    for id, section in prev_sections.items():
        if section.available > 0:
            return False
    for id, section in cur_sections.items():
        if section.available > 0:
            return True
    return False


def check_new_section(prev_sections, cur_sections):
    """
    Checks if a new section has been added.
    """
    for id, section in cur_sections.items():
        if id not in prev_sections:
            return True
    return False


def check_instructor_change(prev_sections, cur_sections):
    """
    Checks if the instructor has been modified for any of the sections.
    """
    for id, section in prev_sections:
        if id not in cur_sections:
            continue  # section was removed since last update
        if section.instructor != cur_sections[id].instructor:
            return True
    return False