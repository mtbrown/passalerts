from passalerts.scrape import Section, parse_sections
from bs4 import BeautifulSoup

test_config = {
    'Settings': {
        'quarter': 'Fall',
        'mode': 'cron',
        'driver': 'PhantomJS'
    },
    'Notifications': {
        'service': 'pushbullet',
        'api_key': None
    }
}

course_list = ['EE 308', 'ENGL 134', 'CPE 464', 'CPE 329']


def test_parse_sections():
    soup = BeautifulSoup(open('test.html').read(), 'html.parser')
    result = parse_sections(soup, course_list)

    assert result == {
        'CPE 329': {
            '4487': Section(course = 'CPE 329', section = '03', type = 'LEC', id = '4487', instructor = 'Irber,Alfred', available = 3, enrolled = 29, waiting = 0),
            '2770': Section(course = 'CPE 329', section = '01', type = 'LEC', id = '2770', instructor = 'Irber,Alfred', available = 0, enrolled = 32, waiting = 0),
            '4488': Section(course = 'CPE 329', section = '04', type = 'LAB', id = '4488', instructor = 'Irber,Alfred', available = 3, enrolled = 29, waiting = 0),
            '2771': Section(course = 'CPE 329', section = '02', type = 'LAB', id = '2771', instructor = 'Irber,Alfred', available = 0, enrolled = 32, waiting = 0)
        },
        'ENGL 134': {
            '4271': Section(course = 'ENGL 134', section = '24', type = 'LEC', id = '4271', instructor = 'Brinkmeyer,Emma E', available = 0, enrolled = 23, waiting = 1),
            '5191': Section(course = 'ENGL 134', section = '51', type = 'LEC', id = '5191', instructor = 'Swanson,Justin Andrew', available = 0, enrolled = 22, waiting = 1),
            '3769': Section(course = 'ENGL 134', section = '12', type = 'LEC', id = '3769', instructor = 'Wishnewsky,Sarah M', available = 0, enrolled = 22, waiting = 1),
            '4273': Section(course = 'ENGL 134', section = '26', type = 'LEC', id = '4273', instructor = 'Sanders,Kristin D', available = 0, enrolled = 23, waiting = 2),
            '3970': Section(course = 'ENGL 134', section = '19', type = 'LEC', id = '3970', instructor = 'Fetters,Ian J', available = 0, enrolled = 22, waiting = 6),
            '14843': Section(course = 'ENGL 134', section = '62', type = 'LEC', id = '14843', instructor = 'Pignatelli,Savannah Kathlene', available = 0, enrolled = 22, waiting = 0),
            '2627': Section(course = 'ENGL 134', section = '04', type = 'LEC', id = '2627', instructor = 'Preston,Alison TJ', available = 0, enrolled = 23, waiting = 1),
            '4051': Section(course = 'ENGL 134', section = '21', type = 'LEC', id = '4051', instructor = 'Bartel,Jonathan Eric', available = 0, enrolled = 22, waiting = 0),
            '4649': Section(course = 'ENGL 134', section = '28', type = 'LEC', id = '4649', instructor = 'Green,Sean M', available = 0, enrolled = 22, waiting = 0),
            '2868': Section(course = 'ENGL 134', section = '07', type = 'LEC', id = '2868', instructor = 'Senn,Melanie R', available = 0, enrolled = 22, waiting = 8),
            '1558': Section(course = 'ENGL 134', section = '03', type = 'LEC', id = '1558', instructor = 'Preston,Alison TJ', available = 0, enrolled = 22, waiting = 0),
            '4270': Section(course = 'ENGL 134', section = '23', type = 'LEC', id = '4270', instructor = 'Smith,Daniel T', available = 0, enrolled = 22, waiting = 2),
            '3971': Section(course = 'ENGL 134', section = '20', type = 'LEC', id = '3971', instructor = 'Gotsick,Jonathan Sawyer', available = 0, enrolled = 23, waiting = 2),
            '2893': Section(course = 'ENGL 134', section = '08', type = 'LEC', id = '2893', instructor = 'Bates,Brian R', available = 0, enrolled = 22, waiting = 2),
            '4654': Section(course = 'ENGL 134', section = '34', type = 'LEC', id = '4654', instructor = 'Wishnewsky,Sarah M', available = 2, enrolled = 20, waiting = 0),
            '2573': Section(course = 'ENGL 134', section = '01', type = 'LEC', id = '2573', instructor = 'Green,Sean M', available = 0, enrolled = 22, waiting = 4),
            '5170': Section(course = 'ENGL 134', section = '42', type = 'LEC', id = '5170', instructor = 'Maddox,Sean Robert', available = 1, enrolled = 21, waiting = 0),
            '3752': Section(course = 'ENGL 134', section = '11', type = 'LEC', id = '3752', instructor = 'St. John,Leslie A', available = 0, enrolled = 22, waiting = 2),
            '4269': Section(course = 'ENGL 134', section = '22', type = 'LEC', id = '4269', instructor = 'Bates,Brian R', available = 0, enrolled = 22, waiting = 2),
            '5192': Section(course = 'ENGL 134', section = '52', type = 'LEC', id = '5192', instructor = 'Sanders,Kristin D', available = 0, enrolled = 23, waiting = 0),
            '1556': Section(course = 'ENGL 134', section = '05', type = 'LEC', id = '1556', instructor = 'Green,Sean M', available = 0, enrolled = 23, waiting = 1),
            '6859': Section(course = 'ENGL 134', section = '49', type = 'LEC', id = '6859', instructor = 'Erdiakoff,Harrison', available = 1, enrolled = 21, waiting = 0),
            '4953': Section(course = 'ENGL 134', section = '36', type = 'LEC', id = '4953', instructor = 'Bradfield,Scott M', available = 0, enrolled = 22, waiting = 0),
            '3965': Section(course = 'ENGL 134', section = '16', type = 'LEC', id = '3965', instructor = 'Bartel,Jonathan Eric', available = 0, enrolled = 22, waiting = 2),
            '5168': Section(course = 'ENGL 134', section = '43', type = 'LEC', id = '5168', instructor = 'Bartel,Jonathan Eric', available = 0, enrolled = 22, waiting = 1),
            '14503': Section(course = 'ENGL 134', section = '57', type = 'LEC', id = '14503', instructor = 'St. John,Leslie A', available = 0, enrolled = 23, waiting = 7),
            '14504': Section(course = 'ENGL 134', section = '58', type = 'LEC', id = '14504', instructor = 'Marini,Amelia Lynn', available = 0, enrolled = 24, waiting = 12),
            '5190': Section(course = 'ENGL 134', section = '50', type = 'LEC', id = '5190', instructor = 'Brinkmeyer,Emma E', available = 0, enrolled = 23, waiting = 0),
            '3771': Section(course = 'ENGL 134', section = '14', type = 'LEC', id = '3771', instructor = 'Ruszczycky,Steven A', available = 0, enrolled = 22, waiting = 0),
            '3770': Section(course = 'ENGL 134', section = '13', type = 'LEC', id = '3770', instructor = 'Johnston,Sarah Ruth', available = 0, enrolled = 23, waiting = 2),
            '5180': Section(course = 'ENGL 134', section = '47', type = 'LEC', id = '5180', instructor = 'Gotsick,Jonathan Sawyer', available = 0, enrolled = 22, waiting = 4),
            '4651': Section(course = 'ENGL 134', section = '31', type = 'LEC', id = '4651', instructor = 'Bradfield,Scott M', available = 0, enrolled = 22, waiting = 0),
            '5171': Section(course = 'ENGL 134', section = '44', type = 'LEC', id = '5171', instructor = 'Bates,Brian R', available = 0, enrolled = 23, waiting = 5),
            '4955': Section(course = 'ENGL 134', section = '38', type = 'LEC', id = '4955', instructor = 'Swanson,Justin Andrew', available = 0, enrolled = 23, waiting = 1),
            '14844': Section(course = 'ENGL 134', section = '06', type = 'LEC', id = '14844', instructor = 'Pignatelli,Savannah Kathlene', available = 0, enrolled = 22, waiting = 0),
            '4954': Section(course = 'ENGL 134', section = '37', type = 'LEC', id = '4954', instructor = 'Senn,Melanie R', available = 0, enrolled = 23, waiting = 2),
            '4653': Section(course = 'ENGL 134', section = '33', type = 'LEC', id = '4653', instructor = 'Swanson,Justin Andrew', available = 0, enrolled = 22, waiting = 0),
            '14897': Section(course = 'ENGL 134', section = '67', type = 'LEC', id = '14897', instructor = 'Martin-Elston,Erin J', available = 0, enrolled = 20, waiting = 1),
            '5169': Section(course = 'ENGL 134', section = '41', type = 'LEC', id = '5169', instructor = 'Swanson,Justin Andrew', available = 0, enrolled = 22, waiting = 0),
            '14849': Section(course = 'ENGL 134', section = '65', type = 'LEC', id = '14849', instructor = 'Anderson,Kevin B', available = 0, enrolled = 23, waiting = 3),
            '14729': Section(course = 'ENGL 134', section = '60', type = 'LEC', id = '14729', instructor = 'Martin-Elston,Erin J', available = 0, enrolled = 22, waiting = 0),
            '3772': Section(course = 'ENGL 134', section = '15', type = 'LEC', id = '3772', instructor = 'Ferree,Scott A', available = 0, enrolled = 23, waiting = 1),
            '4655': Section(course = 'ENGL 134', section = '35', type = 'LEC', id = '4655', instructor = 'Senn,Melanie R', available = 0, enrolled = 22, waiting = 1),
            '14852': Section(course = 'ENGL 134', section = '66', type = 'LEC', id = '14852', instructor = 'Belknap,Jacquelyn N', available = 0, enrolled = 22, waiting = 5),
            '3969': Section(course = 'ENGL 134', section = '17', type = 'LEC', id = '3969', instructor = 'Belknap,Jacquelyn N', available = 0, enrolled = 22, waiting = 1),
            '6862': Section(course = 'ENGL 134', section = '30', type = 'LEC', id = '6862', instructor = 'Marini,Amelia Lynn', available = 1, enrolled = 21, waiting = 0),
            '5172': Section(course = 'ENGL 134', section = '45', type = 'LEC', id = '5172', instructor = 'Marini,Amelia Lynn', available = 0, enrolled = 22, waiting = 0),
            '5178': Section(course = 'ENGL 134', section = '46', type = 'LEC', id = '5178', instructor = 'Ghori,Hajera Anees', available = 0, enrolled = 22, waiting = 0),
            '3973': Section(course = 'ENGL 134', section = '18', type = 'LEC', id = '3973', instructor = 'St. John,Leslie A', available = 0, enrolled = 22, waiting = 0),
            '4272': Section(course = 'ENGL 134', section = '25', type = 'LEC', id = '4272', instructor = 'Smith,Daniel T', available = 0, enrolled = 22, waiting = 3),
            '4645': Section(course = 'ENGL 134', section = '27', type = 'LEC', id = '4645', instructor = 'Green,Sean M', available = 1, enrolled = 21, waiting = 1),
            '4289': Section(course = 'ENGL 134', section = '09', type = 'LEC', id = '4289', instructor = 'Bates,Brian R', available = 0, enrolled = 22, waiting = 1),
            '6861': Section(course = 'ENGL 134', section = '40', type = 'LEC', id = '6861', instructor = 'Maddox,Sean Robert', available = 0, enrolled = 22, waiting = 0)
        },
        'EE 308': {
            '2516': Section(course = 'EE 308', section = '01', type = 'LEC', id = '2516', instructor = 'Smilkstein,Tina Harriet', available = 9, enrolled = 27, waiting = 0)
        },
        'CPE 464': {
            '6962': Section(course = 'CPE 464', section = '02', type = 'LAB', id = '6962', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 54),
            '13903': Section(course = 'CPE 464', section = '03', type = 'LEC', id = '13903', instructor = 'Ghanbari,Muhammad K', available = 0, enrolled = 30, waiting = 29),
            '13904': Section(course = 'CPE 464', section = '04', type = 'LAB', id = '13904', instructor = 'Ghanbari,Muhammad K', available = 0, enrolled = 30, waiting = 29),
            '6961': Section(course = 'CPE 464', section = '01', type = 'LEC', id = '6961', instructor = 'Smith,Hugh M', available = 0, enrolled = 25, waiting = 54)
        }
    }


def test_parse_sections_empty():
    soup = BeautifulSoup('', 'html.parser')
    result = parse_sections(soup, course_list)

    assert result == {
        'CPE 329': {},
        'CPE 464': {},
        'EE 308': {},
        'ENGL 134': {}
    }
