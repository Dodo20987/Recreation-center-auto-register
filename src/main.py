from dotenv import load_dotenv 
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from selenium_stealth import stealth
import time
import random
load_dotenv()
# the links will be stored inside a database in order to keep the modifications for the links
# using sqlite because it is ideal for storing the links locally on my computer
SATURDAY = "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=e96c6509-f24e-d9b9-016e-40336ae63dd0&occurrenceDate=20240921"
SUNDAY = "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=e758edd2-1170-0700-fd9b-1d8bde4262c2&occurrenceDate=20240922"
MONDAY = "https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=44807c6e-20db-5942-10c2-b2e7cfcb32ed&occurrenceDate=20240923"
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
options = webdriver.FirefoxOptions()
options.add_argument("start-maximized")
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
        #stealth(self.driver,
        #languages=["en-US", "en"],
        #vendor="Google Inc.",
        #platform="Win32",
        #webgl_vendor="Intel Inc.",
        #renderer="Intel Iris OpenGL Engine",
        #fix_hairline=True,
        #)
        
    
    def click_register(self):
        print("click register")
        try:
            content_body = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]")))
            content_body = WebDriverWait(content_body,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bm-course-primary-content")))
            content_body = WebDriverWait(content_body,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bm-course-primary-inner")))
            content_body = WebDriverWait(content_body,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bm-booking-info")))

            registerButton = WebDriverWait(content_body,10).until(EC.element_to_be_clickable((By.ID, "bookEventButton")))
            if registerButton.is_displayed() and registerButton.is_enabled():
                # Scroll the element into view before clicking
           #     time.sleep(random.randint(1,5))
                self.driver.execute_script("document.getElementById('temp_wrapper').style.display = 'none';")
                # Now try to click the button
                registerButton.click() 
            else:
                raise RuntimeError("button is not clickable")
            return True 
        except Exception as e:
            print("error: ", e)
#            self.driver.close()
        return False

    def login_page(self):
        try:
            print("login")
#            time.sleep(random.randint(3,6))
            login_button = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginradius-validate-login"]')))
            password_input = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginradius-login-password"]')))
            email_input = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginradius-login-emailid"]')))
            email_input.clear()
            email_input.send_keys(EMAIL)
#            time.sleep(random.randint(3,5))
            password_input.clear()
            password_input.send_keys(PASSWORD)
           # time.sleep(random.randint(1,5))
            if login_button.is_enabled() and login_button.is_displayed():
#                time.sleep(random.randint(1,5))
                self.driver.execute_script("document.getElementById('loading-spinner').style.display = 'none';")
                login_button.click() 
            else:
                raise RuntimeError("button is not clickable")

            return True
        except Exception as e:
            print("button click failed")
            print("error: ", e)
#            self.driver.close()
            return False
    def choose_user(self):
        print("choose user")
        try:
            user_radio = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ParticipantsFamily_FamilyMembers_0__IsParticipating"]')))
            next_button = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div/div[1]/form/div[2]/section/div[3]/div[2]/div/a')))
            if user_radio.is_enabled() and user_radio.is_displayed():
                #time.sleep(random.randint(1,5))
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
#            self.driver.close()
            return False
    def choose_payment_option(self):
        print("choose payment option")
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
#            self.driver.close()
            return False

    def place_order(self):
        print("place order")
        try:
            #TODO : THE process-now-xxx <- number is not constant, change it to find by its class_name
            # cannot access elements wrapped in iframe
            # therefore need to switch to the frame to access the buttons
            print(1)
            time.sleep(random.randint(3,6))
            WebDriverWait(self.driver,10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe.online-store')))
            #self.driver.switch_to.frame(iframe)

            place_order_parent = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/ko-components.checkout.checkout/div[1]')))

            print(2)
            place_order_button = WebDriverWait(place_order_parent,10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'process-now')))
            print(3)
            if place_order_button.is_enabled() and place_order_button.is_displayed():
                time.sleep(random.randint(1,5))
                print(4)
                retries = 0 
                place_order_button.click()
                while retries < 50:
                    try:
                        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout-errors"]')))
                        print("error detected")
                        time.sleep(random.randint(1,3))
                        place_order_button.click()
                        print("click")
                        retries += 1
                    except:
                        print("no error detected")
                        break
                self.driver.switch_to.default_content()
                print(6)
            else:
                raise RuntimeError("button is not clickable")
            print(7)
            return True
        except Exception as e:
            print("error: ", e)
#            self.driver.close()
            return False

    def completeRegister(self):
        self.driver.close()

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

if __name__ == "__main__":
    def main():
        e1 = registerEvent("https://cityofsurrey.perfectmind.com/23615/Clients/BookMe4LandingPages/Class?widgetId=b4059e75-9755-401f-a7b5-d7c75361420d&redirectedFromEmbededMode=False&classId=9f5c4f20-5488-c7ad-3ddc-30126433a269&occurrenceDate=20240924")
        e1.click_register()
        e1.login_page()
        e1.choose_user()
        e1.choose_payment_option()
        e1.place_order()
        #e1.completeRegister()
    #    driver.close()

        parsed_url = urlparse(SATURDAY)
        query_params = parse_qs(parsed_url.query)
        date = query_params["occurrenceDate"][0] 
        d1 = modifyDate(date) 
        d1.incrment_date()
        new_date = d1.get_date()
        query_params["occurrenceDate"] = new_date


    main()