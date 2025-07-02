from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import sqlite3
import time
import random
import datetime
import modify_date as md
import register_event as register

load_dotenv()
# the links will be stored inside a database in order to keep the modifications for the links
# using sqlite because it is ideal for storing the links locally on my computer

temp = ""
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
PATH_TO_DB = os.getenv("PATH_TO_DB")
TEXT_FILE_PATH = os.getenv("TEXT_FILE_PATH")
con = None
cur = None
WAITLIST = None


def handle_link_mod(LINK):
    parsed_url = urlparse(LINK)
    query_params = parse_qs(parsed_url.query)
    date = query_params["occurrenceDate"][0]
    d1 = md.modifyDate(date)
    d1.incrment_date()
    new_date = d1.get_date()
    query_params["occurrenceDate"] = new_date
    new_link = modify_url(parsed_url, query_params)
    return new_link


def modify_url(parsed_url, query_params):
    for key, value in query_params.items():
        if isinstance(value, list):
            query_params[key] = value[0]

    new_query_params = urlencode(query_params, doseq=False)
    new_url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query_params,
            parsed_url.fragment,
        )
    )

    return new_url


def get_day():
    current_day = datetime.datetime.now().strftime("%A")
    return current_day


def handle_registration(LINK):
    e1 = register.registerEvent(LINK)
    if not e1.click_register():
        raise RuntimeError("could not click register or waitlist button")
    if not e1.login_page(EMAIL, PASSWORD):
        raise RuntimeError("could not log the user in")
    if not e1.choose_user():
        raise RuntimeError("could not select desired user")
    if not e1.choose_payment_option():
        raise RuntimeError("could not choose the membership option for payment")
    if e1.get_wait_list() == True:
        e1.completeRegister()
        print("waitlisted")
        return e1

    if not e1.place_order():
        raise RuntimeError("could not complete the checkout")
    #e1.completeRegister()
    return e1

# use this for starting the script early and then waiting until the target time
def wait_until_target_time(wait_until):
    now = datetime.datetime.now() 
    target_time = datetime.datetime.strptime(wait_until, "%H:%M").replace(
        year = now.year, month = now.month, day = now.day
    )
    if now > target_time:
        print("target time has passed")
        return

    seconds_to_wait = (target_time - now).total_seconds()
    print(f"waiting for {seconds_to_wait} seconds")
    time.sleep(seconds_to_wait)

def main():
    if PATH_TO_DB is None:
        raise ValueError("path to db is None")
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    curr_day = get_day().upper()
    q_str = f"SELECT link FROM links WHERE registerDay = '{curr_day}'"
    res = cur.execute(q_str)
    registration_link = res.fetchone()[0]
    # print(registration_link)
    registered = None
    response_string = ""
    try:
        reg = handle_registration(registration_link)
    #            handle_registration("https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=afe19048-8caf-d2ff-7ede-63afb9c2e80c&occurrenceDate=20241026")
        response_string = "Success"
        if(reg.get_wait_list() == True):
            response_string = "Waitlisted"
    except Exception as e:
        print("registration unsucessful")
        response_string = "Failure"
    new_link = handle_link_mod(registration_link)
    u_str = f"UPDATE links SET link = '{new_link}' WHERE registerday = '{curr_day}'"
    cur.execute(u_str)
    con.commit()
    con.close()
    file = open(str(TEXT_FILE_PATH), "a")
    file.write(
        f"{datetime.datetime.now()}" + " - The script ran " + response_string + "\n"
    )
    file.close()


if __name__ == "__main__":
    main()
