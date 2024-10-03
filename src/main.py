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
load_dotenv()
# the links will be stored inside a database in order to keep the modifications for the links
# using sqlite because it is ideal for storing the links locally on my computer
SATURDAY = "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=5911ec72-4f62-48c9-8890-13577fd49c24&occurrenceDate=20241005"
SUNDAY = "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=7daf67f1-dd8d-420d-bc60-42ff9013a683&occurrenceDate=20241006"
THURSDAY = "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=35b4a887-8905-484b-a83f-f66c5cd24261&occurrenceDate=20241003"
FRIDAY = "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=0b285251-a3c0-40f9-ba44-594b25c16b95&occurrenceDate=20241004"
temp = ""
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
PATH_TO_DB = os.getenv("PATH_TO_DB")
TEXT_FILE_PATH = os.getenv("TEXT_FILE_PATH")
options = webdriver.FirefoxOptions()
options.add_argument("start-maximized")
con = None
cur = None
WAITLIST = None
def handle_link_mod(LINK):
    parsed_url = urlparse(LINK)
    query_params = parse_qs(parsed_url.query)
    date = query_params["occurrenceDate"][0] 
    d1 = modifyDate(date) 
    d1.incrment_date()
    new_date = d1.get_date()
    query_params["occurrenceDate"] = new_date
    new_link = modify_url(parsed_url, query_params)
    return new_link

def connect_to_db():
    try:
        con = sqlite3.connect(PATH_TO_DB) 
        
        return True
    except Exception as e:
        print("error: ", e)
        return False
def modify_url(parsed_url, query_params):
    for key, value in query_params.items():
        if isinstance(value, list):
            query_params[key] = value[0]

    new_query_params = urlencode(query_params, doseq = False)
    new_url = urlunparse((
    parsed_url.scheme,
    parsed_url.netloc,
    parsed_url.path,
    parsed_url.params,
    new_query_params,
    parsed_url.fragment))

    return new_url

def get_day():
    current_day = datetime.datetime.now().strftime('%A')
    return current_day

def handle_registration(LINK):
    e1 = registerEvent(LINK)
    if not e1.click_register():
        raise RuntimeError("could not click register or waitlist button")
    if not e1.login_page():
        raise RuntimeError("could not log the user in")
    if not e1.choose_user():
        raise RuntimeError("could not select desired user")
    if not e1.choose_payment_option():
        raise RuntimeError("could not choose the membership option for payment")
    if WAITLIST:
        e1.completeRegister()

    if not e1.place_order():
        raise RuntimeError("could not complete the checkout")
    e1.completeRegister()

class modifyDate:
    def __init__(self, date_string):
        # the key signifies the month 1 - 12
        # the value in the dictionary signify the day for the corresponding month
        self.__DAYINMONTHS = {1 : 31, 2 : 28, 3 : 31,4 : 30, 5 : 31, 6 : 30,
                              7 : 31,8 : 31,9 : 30, 10 : 31, 11 : 30,12 : 31}
        self.date_string = date_string
        self.__day_str = self.__get_day()
        self.__month_str = self.__get_month()
        self.__year_str = self.__get_year()

    def __get_day(self):
        return self.date_string[-2:]

    def __get_year(self):
        return self.date_string[0:4]

    def __get_month(self):
        return self.date_string[4:6]

    def __is_leap_year(self):
        year_num = int(self.__year_str)
        return year_num % 4 == 0

    def incrment_date(self):
        day_increment = int(self.__day_str) + 7
        month_num = int(self.__month_str)
        year_num = int(self.__year_str)
        max_days = self.__DAYINMONTHS[month_num]

        if(month_num == 2):
            if(self.__is_leap_year()):
                max_days += 1 

        if(day_increment > max_days):
            if(month_num == 12):
                month_num = 1
                year_num += 1
                self.__year_str = str(year_num)
            else:
                month_num +=1
            next_month_day = self.__DAYINMONTHS[month_num]
            if(self.__is_leap_year() and month_num == 2):
                day_increment = day_increment % 29 
            else:
                day_increment = day_increment % next_month_day 

            self.__month_str = str(month_num) if month_num >= 10 else "0" + str(month_num)

        self.__day_str = str(day_increment) if day_increment >= 10 else "0" + str(day_increment)

        self.date_string = self.__year_str + self.__month_str + self.__day_str 

    def get_date(self):
        return self.date_string

class registerEvent:
    def __init__(self,link):
        self.driver = webdriver.Firefox(options=options)
        self.driver.get(link)
        
    def click_register(self) -> bool:
        print("click register")
        try:
            content_body = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]")))
            content_body = WebDriverWait(content_body,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bm-course-primary-content")))
            content_body = WebDriverWait(content_body,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bm-course-primary-inner")))
            content_body = WebDriverWait(content_body,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bm-booking-info")))

            registerButton = WebDriverWait(content_body,10).until(EC.element_to_be_clickable((By.ID, "bookEventButton")))
            textContent = registerButton.text
            if textContent == "WAITLIST":
                WAITLIST = True
            elif textContent == "REGISTER":
                WAITLIST = False
            else:
                self.driver.close()
                return False

            if registerButton.is_displayed() and registerButton.is_enabled():

                self.driver.execute_script("document.getElementById('temp_wrapper').style.display = 'none';")
                registerButton.click() 
            else:
                raise RuntimeError("button is not clickable")
            return True 
        except Exception as e:
            print("error: ", e)
            self.driver.close()
        return False

    def login_page(self) -> bool:
        try:
            login_button = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginradius-validate-login"]')))
            password_input = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginradius-login-password"]')))
            email_input = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginradius-login-emailid"]')))
            email_input.clear()
            email_input.send_keys(EMAIL)
            password_input.clear()
            password_input.send_keys(PASSWORD)
            if login_button.is_enabled() and login_button.is_displayed():
                self.driver.execute_script("document.getElementById('loading-spinner').style.display = 'none';")
                login_button.click() 
            else:
                raise RuntimeError("button is not clickable")

            return True
        except Exception as e:
            print("error: ", e)
            self.driver.close()
            return False
    def choose_user(self) -> bool:
        print("choose user")
        try:
            user_radio = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ParticipantsFamily_FamilyMembers_0__IsParticipating"]')))
            next_button = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div/div[1]/form/div[2]/section/div[3]/div[2]/div/a')))
            if user_radio.is_enabled() and user_radio.is_displayed():
                self.driver.execute_script("document.getElementById('ajaxRequestStatus_attendance').style.display = 'none';")
                user_radio.click()
            else:
                raise RuntimeError("button is not clickable")
            if next_button.is_enabled() and next_button.is_displayed():
                time.sleep(random.randint(1,3))
                self.driver.execute_script("arguments[0].click();", next_button)
            else:
                raise RuntimeError("button is not clickable")
            return True
        except Exception as e:
            print("error: ", e)
            self.driver.close()
            return False
    def choose_payment_option(self) -> bool:
        try:
            membership_option = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div[4]/div[1]/div/ul/li[1]/div/table/tbody/tr[2]')))
            radio_button = WebDriverWait(membership_option,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'holiday-radio-btn')))
            next_button = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div[5]/a')))
            html = radio_button.get_attribute("outerHTML")
            radio_button.click()

            if next_button.is_enabled() and next_button.is_displayed():
                time.sleep(random.randint(1,5))
                next_button.click()
            else:
                raise RuntimeError("next button is not clickable :( ")
            return True
            
        except Exception as e:
            print("error: ", e)
            self.driver.close()
            return False

    def place_order(self) -> bool:
        try:
            
            time.sleep(random.randint(3,6))
            WebDriverWait(self.driver,10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe.online-store')))

            place_order_parent = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/ko-components.checkout.checkout/div[1]')))

            place_order_button = WebDriverWait(place_order_parent,10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'process-now')))
            if place_order_button.is_enabled() and place_order_button.is_displayed():
                time.sleep(random.randint(1,5))
                print(4)
                retries = 0 
                place_order_button.click()
                while retries < 100: 
                    try:
                        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout-errors"]')))
                        print("error detected")
                        time.sleep(random.randint(1,3))
                        place_order_button.click()
                        retries += 1
                    except:
                        print("no error detected")
                        break
                self.driver.switch_to.default_content()
                if retries > 100:
                    return False
            else:
                raise RuntimeError("button is not clickable")
            return True
        except Exception as e:
            print("error: ", e)
            self.driver.close()
            return False

    def completeRegister(self):
        self.driver.close()


if __name__ == "__main__":
    def main():
        con = sqlite3.connect(PATH_TO_DB)
        cur = con.cursor()
        curr_day = get_day().upper()
        q_str = f"SELECT link FROM links WHERE registerDay = '{curr_day}'"
        res = cur.execute(q_str)
        registration_link = res.fetchone()[0]
        print(registration_link)
        try:
            handle_registration(registration_link)
        except Exception as e:
            print("registration unsucessful")
        new_link = handle_link_mod(registration_link)
        u_str = f"UPDATE links SET link = '{new_link}' WHERE registerday = '{curr_day}'"
        cur.execute(u_str)
        con.commit()
        con.close()
        file = open(TEXT_FILE_PATH, 'a')
        file.write(f'{datetime.datetime.now()}' + ' - The script ran \n')
        file.close()
    main()