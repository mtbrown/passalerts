from passalerts.scrape import Section
from passalerts.events import check_available, check_new_section, check_instructor_change, check_events


def test_check_available():
    """
    Verify basic functionality of check_available().
    """
    prev = {
        '13904': Section(course = 'CPE 464', section = '04', type = 'LAB', id = '13904', instructor = 'Ghanbari,Muhammad K', available = 0, enrolled = 30, waiting = 0),
        '6962': Section(course = 'CPE 464', section = '02', type = 'LAB', id = '6962', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '6961': Section(course = 'CPE 464', section = '01', type = 'LEC', id = '6961', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '13903': Section(course = 'CPE 464', section = '03', type = 'LEC', id = '13903', instructor = 'Ghanbari,Muhammad K', available = 0, enrolled = 30, waiting = 0)
    }

    cur = {
        '13904': Section(course = 'CPE 464', section = '04', type = 'LAB', id = '13904', instructor = 'Ghanbari,Muhammad K', available = 4, enrolled = 26, waiting = 0),
        '6962': Section(course = 'CPE 464', section = '02', type = 'LAB', id = '6962', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '6961': Section(course = 'CPE 464', section = '01', type = 'LEC', id = '6961', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '13903': Section(course = 'CPE 464', section = '03', type = 'LEC', id = '13903', instructor = 'Ghanbari,Muhammad K', available = 0, enrolled = 30, waiting = 0)
    }

    results = list(check_available(prev, cur))
    assert len(results) == 1
    section, extra = results[0]

    assert section.id == '13904'
    assert extra == 4

    results = list(check_available(prev, prev))
    assert len(results) == 0

    results = list(check_available(cur, cur))
    assert len(results) == 0


def test_check_available_multiple():
    """
    If multiple sections become available, all should be included.
    """
    prev = {
        '13904': Section(course = 'CPE 464', section = '04', type = 'LAB', id = '13904', instructor = 'Ghanbari,Muhammad K', available = 0, enrolled = 30, waiting = 0),
        '6962': Section(course = 'CPE 464', section = '02', type = 'LAB', id = '6962', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '6961': Section(course = 'CPE 464', section = '01', type = 'LEC', id = '6961', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '13903': Section(course = 'CPE 464', section = '03', type = 'LEC', id = '13903', instructor = 'Ghanbari,Muhammad K', available = 0, enrolled = 30, waiting = 0)
    }

    cur = {
        '13904': Section(course = 'CPE 464', section = '04', type = 'LAB', id = '13904', instructor = 'Ghanbari,Muhammad K', available = 1, enrolled = 29, waiting = 0),
        '6962': Section(course = 'CPE 464', section = '02', type = 'LAB', id = '6962', instructor = 'Smith,Hugh M', available = 1, enrolled = 24, waiting = 0),
        '6961': Section(course = 'CPE 464', section = '01', type = 'LEC', id = '6961', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '13903': Section(course = 'CPE 464', section = '03', type = 'LEC', id = '13903', instructor = 'Ghanbari,Muhammad K', available = 1, enrolled = 29, waiting = 0)
    }

    results = list(check_available(prev, cur))
    assert len(results) == 3


def test_check_available_duplicate():
    """
    If a section was already previously available, don't process the event again.
    """
    prev = {
        '13904': Section(course = 'CPE 464', section = '04', type = 'LAB', id = '13904', instructor = 'Ghanbari,Muhammad K', available = 3, enrolled = 27, waiting = 0),
        '6962': Section(course = 'CPE 464', section = '02', type = 'LAB', id = '6962', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '6961': Section(course = 'CPE 464', section = '01', type = 'LEC', id = '6961', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '13903': Section(course = 'CPE 464', section = '03', type = 'LEC', id = '13903', instructor = 'Ghanbari,Muhammad K', available = 0, enrolled = 30, waiting = 0)
    }

    cur = {
        '13904': Section(course = 'CPE 464', section = '04', type = 'LAB', id = '13904', instructor = 'Ghanbari,Muhammad K', available = 3, enrolled = 27, waiting = 0),
        '6962': Section(course = 'CPE 464', section = '02', type = 'LAB', id = '6962', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '6961': Section(course = 'CPE 464', section = '01', type = 'LEC', id = '6961', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '13903': Section(course = 'CPE 464', section = '03', type = 'LEC', id = '13903', instructor = 'Ghanbari,Muhammad K', available = 0, enrolled = 30, waiting = 0)
    }

    results = list(check_available(prev, cur))
    assert len(results) == 0


def test_check_available_new_section():
    """
    If a new section is added, it should be considered available.
    """
    prev = {
        '13904': Section(course = 'CPE 464', section = '04', type = 'LAB', id = '13904', instructor = 'Ghanbari,Muhammad K', available = 3, enrolled = 27, waiting = 0),
        '6962': Section(course = 'CPE 464', section = '02', type = 'LAB', id = '6962', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '6961': Section(course = 'CPE 464', section = '01', type = 'LEC', id = '6961', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '13903': Section(course = 'CPE 464', section = '03', type = 'LEC', id = '13903', instructor = 'Ghanbari,Muhammad K', available = 0, enrolled = 30, waiting = 0)
    }

    cur = {
        '13904': Section(course = 'CPE 464', section = '04', type = 'LAB', id = '13904', instructor = 'Ghanbari,Muhammad K', available = 3, enrolled = 27, waiting = 0),
        '6962': Section(course = 'CPE 464', section = '02', type = 'LAB', id = '6962', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '6961': Section(course = 'CPE 464', section = '01', type = 'LEC', id = '6961', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '13903': Section(course = 'CPE 464', section = '03', type = 'LEC', id = '13903', instructor = 'Ghanbari,Muhammad K', available = 0, enrolled = 30, waiting = 0),
        '13905': Section(course='CPE 464', section='05', type='LEC', id='13905', instructor='Ghanbari,Muhammad K', available=30, enrolled=0, waiting=0)
    }

    results = list(check_available(prev, cur))
    assert len(results) == 1

    section, extra = results[0]
    assert section.id == '13905'
    assert extra == 30


def test_check_new_section():
    prev = {
        '13904': Section(course = 'CPE 464', section = '04', type = 'LAB', id = '13904', instructor = 'Ghanbari,Muhammad K', available = 3, enrolled = 27, waiting = 0),
        '6962': Section(course = 'CPE 464', section = '02', type = 'LAB', id = '6962', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '6961': Section(course = 'CPE 464', section = '01', type = 'LEC', id = '6961', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '13903': Section(course = 'CPE 464', section = '03', type = 'LEC', id = '13903', instructor = 'Ghanbari,Muhammad K', available = 0, enrolled = 30, waiting = 0)
    }

    cur = {
        '13904': Section(course = 'CPE 464', section = '04', type = 'LAB', id = '13904', instructor = 'Ghanbari,Muhammad K', available = 3, enrolled = 27, waiting = 0),
        '6962': Section(course = 'CPE 464', section = '02', type = 'LAB', id = '6962', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '6961': Section(course = 'CPE 464', section = '01', type = 'LEC', id = '6961', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '13903': Section(course = 'CPE 464', section = '03', type = 'LEC', id = '13903', instructor = 'Ghanbari,Muhammad K', available = 0, enrolled = 30, waiting = 0),
        '13905': Section(course='CPE 464', section='05', type='LEC', id='13905', instructor='Ghanbari,Muhammad K', available=30, enrolled=0, waiting=0)
    }

    results = list(check_new_section(prev, cur))
    assert len(results) == 1

    section, extra = results[0]
    assert section.id == '13905'
    assert extra == section.id

    results = list(check_new_section(prev, prev))
    assert len(results) == 0


def test_check_instructor_change():
    prev = {
        '13904': Section(course = 'CPE 464', section = '04', type = 'LAB', id = '13904', instructor = 'Ghanbari,Muhammad K', available = 3, enrolled = 27, waiting = 0),
        '6962': Section(course = 'CPE 464', section = '02', type = 'LAB', id = '6962', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '6961': Section(course = 'CPE 464', section = '01', type = 'LEC', id = '6961', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '13903': Section(course = 'CPE 464', section = '03', type = 'LEC', id = '13903', instructor = 'Ghanbari,Muhammad K', available = 0, enrolled = 30, waiting = 0)
    }

    cur = {
        '13904': Section(course = 'CPE 464', section = '04', type = 'LAB', id = '13904', instructor = 'Ghanbari,Muhammad K', available = 3, enrolled = 27, waiting = 0),
        '6962': Section(course = 'CPE 464', section = '02', type = 'LAB', id = '6962', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '6961': Section(course = 'CPE 464', section = '01', type = 'LEC', id = '6961', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 0),
        '13903': Section(course = 'CPE 464', section = '03', type = 'LEC', id = '13903', instructor = 'New Professor', available = 0, enrolled = 30, waiting = 0)
    }

    results = list(check_instructor_change(prev, cur))
    assert len(results) == 1

    section, extra = results[0]
    assert section.id == '13903'
    assert extra == 'New Professor'

    results = list(check_new_section(prev, prev))
    assert len(results) == 0
