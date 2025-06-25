from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import time
import random

options = webdriver.FirefoxOptions()
options.add_argument("start-maximized")


class registerEvent:
    def __init__(self, link):
        self.driver = webdriver.Firefox(options=options)
        self.driver.get(link)
        self.WAITLIST = False
    def get_wait_list(self):
        return self.WAITLIST

    def click_register(self) -> bool:
        try:
            content_body = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]"))
            )
            content_body = WebDriverWait(content_body, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".bm-course-primary-content")
                )
            )
            content_body = WebDriverWait(content_body, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".bm-course-primary-inner")
                )
            )
            content_body = WebDriverWait(content_body, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".bm-booking-info"))
            )

            registerButton = WebDriverWait(content_body, 10).until(
                EC.element_to_be_clickable((By.ID, "bookEventButton"))
            )
            textContent = registerButton.text
            if textContent == "WAITLIST":
                self.WAITLIST = True
            elif textContent == "REGISTER":
                self.WAITLIST = False
            else:
                self.driver.close()
                print(
                    "could not click the register or waitlist button, too late to register"
                )
                return False

            if registerButton.is_displayed() and registerButton.is_enabled():
                self.driver.execute_script(
                    "document.getElementById('temp_wrapper').style.display = 'none';"
                )
                registerButton.click()
            else:
                raise RuntimeError("button is not clickable")
            return True
        except Exception as e:
            print("error: ", e)
            self.driver.close()
        return False

    def login_page(self, EMAIL, PASSWORD) -> bool:
        try:
            login_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="loginradius-validate-login"]')
                )
            )
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="loginradius-login-password"]')
                )
            )
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="loginradius-login-emailid"]')
                )
            )
            email_input.clear()
            email_input.send_keys(EMAIL)
            password_input.clear()
            password_input.send_keys(PASSWORD)
            if login_button.is_enabled() and login_button.is_displayed():
                self.driver.execute_script(
                    "document.getElementById('loading-spinner').style.display = 'none';"
                )
                login_button.click()
            else:
                raise RuntimeError("button is not clickable")

            return True
        except Exception as e:
            print("error: ", e)
            self.driver.close()
            return False

    def choose_user(self) -> bool:
        try:
            user_radio = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="ParticipantsFamily_FamilyMembers_0__IsParticipating"]',
                    )
                )
            )
            next_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div[2]/div/div/div[1]/form/div[2]/section/div[3]/div[2]/div/a",
                    )
                )
            )
            if user_radio.is_enabled() and user_radio.is_displayed():
                self.driver.execute_script(
                    "document.getElementById('ajaxRequestStatus_attendance').style.display = 'none';"
                )
                user_radio.click()
            else:
                raise RuntimeError("button is not clickable")
            if next_button.is_enabled() and next_button.is_displayed():
                time.sleep(random.randint(1, 3))
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
            membership_option = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div[2]/div/div/div/div[4]/div[1]/div/ul/li[1]/div/table/tbody/tr[2]",
                    )
                )
            )
            radio_button = WebDriverWait(membership_option, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "holiday-radio-btn"))
            )
            next_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div[5]/a")
                )
            )
            html = radio_button.get_attribute("outerHTML")
            radio_button.click()

            if next_button.is_enabled() and next_button.is_displayed():
                time.sleep(random.randint(1, 5))
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
            time.sleep(random.randint(3, 6))
            WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.CSS_SELECTOR, "iframe.online-store")
                )
            )

            place_order_parent = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/ko-components.checkout.checkout/div[1]",
                    )
                )
            )

            place_order_button = WebDriverWait(place_order_parent, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "process-now"))
            )
            if place_order_button.is_enabled() and place_order_button.is_displayed():
                time.sleep(random.randint(1, 5))
                print(4)
                retries = 0
                place_order_button.click()
                while retries < 100:
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//*[@id="checkout-errors"]')
                            )
                        )
                        print("error detected")
                        time.sleep(random.randint(1, 3))
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
