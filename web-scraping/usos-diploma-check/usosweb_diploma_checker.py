import requests
from lxml import html
from bs4 import BeautifulSoup
import balloontip
import datetime

CREDENTIALS_FILE_PATH = "<full_path_to_file>/credentials.txt"
LOG_FILE = "<full_path_to_file>/diploma_checks.log"
ENCODE_SHIFT = 5  # should be known in advance; for credentials file
LOGIN_URL = "https://cas.usos.pw.edu.pl/cas/login?service=https%3A%2F%2Fusosweb.usos.pw.edu.pl%2Fkontroler.php%3F_action%3Dlogowaniecas%2Findex&locale=pl"
TARGET_URL = "https://usosweb.usos.pw.edu.pl/kontroler.php?_action=dla_stud/studia/dyplomy/index"


def show_win10_notif(title, msg, duration=5):
    """Windows tooltip notification"""
    balloontip.balloon_tip(title, msg)


def append_to_log(log_file, msg):
    """Append msg string to """
    with open(log_file, "a") as log_f:
        log_f.write(msg + '\n')


def shift_string(in_str, chr_shift=5):
    """Simple encode-decode function"""
    new_str = ""
    for cur_c in in_str:
        new_str += chr(ord(cur_c) + chr_shift)
    return new_str


def read_credentials(txt_file, encode_shift=5):
    """Get credentials from text file where they are slightly decoded"""
    with open(txt_file, "r") as in_f:
        login = shift_string(in_f.readline().strip('\n'), -encode_shift)
        password = shift_string(in_f.readline().strip('\n'), -encode_shift)
    return login, password


def login_and_get_page(login_url: str, target_url: str, credentials: tuple):
    username, password = credentials
    session_requests = requests.session()

    # Get login csrf token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    lt_field = list(set(tree.xpath("//input[@name='lt']/@value")))[0]
    execution_field = list(set(tree.xpath("//input[@name='execution']/@value")))[0]
    event_id_field = list(set(tree.xpath("//input[@name='_eventId']/@value")))[0]

    # Create payload
    payload = {
        "username": username,
        "password": password,
        "lt": lt_field,                 # Example: "LT-5094508-GoTmOeXlUNlJHzLUEIsaWcJcyjx003",
        "execution": execution_field,   # "e1s1",
        "_eventId": event_id_field,     # "submit",
        "submit": "ZALOGUJ"
    }

    # Perform login
    login_result = session_requests.post(LOGIN_URL, data=payload, headers={"referer": login_url})
    # Scrape url
    page_response = session_requests.get(target_url, headers=dict(referer=target_url))

    return page_response, login_result


def parse_diploma_page(page_response):
    """Get info about diploma status from obtained web-page"""
    if page_response.ok:
        page_content = BeautifulSoup(page_response.content, 'html.parser')
    else:
        print(f"E: failed get target url. Status code: {page_response.status_code}")
    cert_table_rows = page_content.select_one('main table')
    cert_table_rows = [x for x in cert_table_rows if x.name == "tr"]
    for i, cont in enumerate(cert_table_rows):
        if "do odbioru" in cont.contents[1].string.strip():
            diploma_ready_status = list(cont.contents[3].stripped_strings)[0]
    return diploma_ready_status


def main(login_url, target_url, credentials_file_path, encode_shift, log_file):
    credentials = read_credentials(credentials_file_path, encode_shift)
    page_response, login_result = login_and_get_page(login_url, target_url, credentials)
    diploma_ready_status = parse_diploma_page(page_response)
    show_win10_notif("Diploma check script", diploma_ready_status)
    check_date = str(datetime.datetime.now())
    log_str = f"{check_date}: {diploma_ready_status}"
    append_to_log(log_file, log_str)


if __name__ == '__main__':
    main(LOGIN_URL, TARGET_URL, CREDENTIALS_FILE_PATH, ENCODE_SHIFT, LOG_FILE)
