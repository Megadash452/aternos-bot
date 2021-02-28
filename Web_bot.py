import selenium, time
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Web_bot:
    def __init__(self, visible=False):
        self.server_active = False
        self.server_online = False
        options = selenium.webdriver.ChromeOptions()
        if not visible:
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            # OR options.add_argument("--disable-gpu")

        self.browser = selenium.webdriver.Chrome("chromedriver.exe", options=options)
        print("Web Bot Ready")

    def aternos_logIn(self):
        self.browser.get("https://aternos.org/go/")

        with open("meta.json", 'r') as f:
            data = json.load(f)
            username = data["aternos"]["username"]
            password = data["aternos"]["password"]

        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located(
                (By.ID, "user")
            )
        ).send_keys(username)

        self.browser.find_element_by_id("password").send_keys(password)
        self.browser.find_element_by_id("login").click()

    def aternos_logIn_withGoogle(self):
        self.browser.get(
            "https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAAQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin")

        with open("meta.json", 'r') as f:
            data = json.load(f)
            gmail = data["google"]["gmail"]
            gpass = data["google"]["password"]

        try:
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located(
                    (By.ID, "identifierId")
                )
            ).send_keys(gmail)

            self.browser.find_element_by_id("identifierNext") \
                .find_element_by_class_name("VfPpkd-dgl2Hf-ppHlrf-sM5MNb") \
                .find_element_by_class_name("VfPpkd-LgbsSe") \
                .send_keys(Keys.RETURN)
        except Exception as error:
            self.browser.quit()
            print(
                error,
                "Could not load Google Sign In page{}. Re-run the program."
            )

        time.sleep(1)

        try:
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located(
                    (By.ID, "password")
                )
            ).find_element_by_name("password") \
                .send_keys(gpass)

            self.browser.find_element_by_id("passwordNext") \
                .find_element_by_class_name("AjY5Oe") \
                .send_keys(Keys.RETURN)
        except Exception as error:
            self.browser.quit()
            print(
                error,
                f"Email Address <{gmail}> does not exist. Make sure you have the right email address in \"meta.json\""
            )

        try:
            WebDriverWait(self.browser, 3).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "lnXdpd")
                )
            )
        except Exception as error:
            self.browser.quit()
            print(
                error,
                "Your password is incorrect{}. Make sure your password may be correct in \"meta.json\""
            )

        self.browser.get("https://aternos.org/go/")

        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "google-button")
            )
        ).click()

        print(f"Signed in to Aternos with Google account <{gmail}>")

    def activate_server(self):
        print("Activating server")
        self.browser.get("https://aternos.org/servers/")
        try:
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "server")
                )
            ).click()

            # WebDriverWait(self.browser, 5).until(
            #     EC.presence_of_element_located(
            #         (By.CLASS_NAME, "btn-red")
            #     )
            # ).click()

            if "Online" in WebDriverWait(self.browser, 5).until(
                               EC.presence_of_element_located(
                                   (By.CLASS_NAME, "statuslabel-label")
                               )
                           ).text:
                print("Server was already online")
                self.server_online = True
                self.server_active = True

            elif "Offline" in self.browser.find_element_by_class_name("statuslabel-label").text:
                self.browser.find_element_by_id("start").click()
                print("Starting Server... (This may take a while)")
                self.server_active = True

        except Exception as e:
            print(e)

    def check_if_online(self):
        if self.server_online:
            return True
        elif "Online" in self.browser.find_element_by_class_name("statuslabel-label").text:
            return True
        else:
            return False

    def check_when_online(self):
        while True:
            if "Online" in self.browser.find_element_by_class_name("statuslabel-label").text:
                break
            else:
                time.sleep(1)
                self.check_when_online()


if __name__ == "__main__":
    web_bot = Web_bot(visible=False)
    with open("meta.json", 'r') as f:
        if json.load(f)["account type"] == "google":
            web_bot.aternos_logIn_withGoogle()
        else:
            web_bot.aternos_logIn()

    web_bot.activate_server()