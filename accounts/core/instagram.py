import hashlib
import requests
import json
import uuid
import hmac
import urllib
from urllib.parse import quote


class Instagram:
    API_URL = 'https://i.instagram.com/api/v1/'
    USER_AGENT = 'Instagram 130.0.0.30.110 Android (33/13.0; 480dpi; 1080x1920; XIAOMI; 23122PCD1G; Poco X6 5G; qcom)'
    IG_SIG_KEY = '109513c04303341a7daf27bb41b268e633b30dcc65a3fe14503f743176113869'
    SIG_KEY_VERSION = '4'

    def __init__(self, username, password):
        try:
            if not username or not password:
                raise ValueError("Username and password must not be empty")

            m = hashlib.md5()
            m.update(username.encode('utf-8') + password.encode('utf-8'))
            self.device_id = self.generateDeviceId(m.hexdigest())
            self.setUser(username, password)
            self.isLoggedIn = False
            self.lastResponse = None
        except Exception as e:
            print(f"Error during initialization: {e}")

    def setUser(self, username, password):
        self.username = username
        self.password = password
        self.uuid = self.generateUUID(True)

    def login(self, force=False):
        try:
            if not self.isLoggedIn or force:
                self.s = requests.Session()

                if self.sendRequest('si/fetch_headers/?challenge_type=signup&guid=' + self.generateUUID(False), None, True):
                    print(self.lastResponse.cookies)

                    data = {
                        'phone_id': self.generateUUID(True),
                        '_csrftoken': self.lastResponse.cookies['csrftoken'],
                        'username': self.username,
                        'guid': self.uuid,
                        'device_id': self.device_id,
                        'password': self.password,
                        'login_attempt_count': '0'
                    }

                    if self.sendRequest('accounts/login/', self.generateSignature(json.dumps(data)), True):
                        self.isLoggedIn = True
                        self.username_id = self.lastJson["logged_in_user"]["pk"]
                        self.rank_token = f"{self.username_id}_{self.uuid}"
                        self.token = self.lastResponse.cookies["csrftoken"]

                        return True
        except requests.exceptions.RequestException as e:
            print(f"Network error during login: {e}")
        except KeyError as e:
            print(f"KeyError during login - missing key: {e}")
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON during login: {e}")
        except Exception as e:
            print(f"Unexpected error during login: {e}")

        return False

    def generateDeviceId(self, seed):
        try:
            volatile_seed = "12345"
            m = hashlib.md5()
            m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
            return 'android-' + m.hexdigest()[:16]
        except Exception as e:
            print(f"Error generating device ID: {e}")
            return None

    def generateUUID(self, type):
        try:
            generated_uuid = str(uuid.uuid4())
            return generated_uuid if type else generated_uuid.replace('-', '')
        except Exception as e:
            print(f"Error generating UUID: {e}")
            return None

    def set_session(self, session):
        if not self.isLoggedIn:
            self.s = session

    def get_session(self):
        return self.s

    def generateSignature(self, data):
        try:
            return 'ig_sig_key_version=' + self.SIG_KEY_VERSION + '&signed_body=' + hmac.new(
                self.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'),
                hashlib.sha256).hexdigest() + '.' + urllib.parse.quote_plus(data)
        except Exception as e:
            print(f"Error generating signature: {e}")
            return None

    def retriveFromAdressBook(self, target_id = 0):
        return self.sendRequest(f'discover/chaining/?target_id={target_id}')

    def sendRequest(self, endpoint, post=None, login=False):
        try:
            if not self.isLoggedIn and not login:
                raise Exception("Not logged in!\n")

            self.s.headers.update({
                'Connection': 'close',
                'Accept': '*/*',
                'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie2': '$Version=1',
                'Accept-Language': 'en-US',
                'User-Agent': self.USER_AGENT
            })

            if post:
                response = self.s.post(self.API_URL + endpoint, data=post)
            else:
                response = self.s.get(self.API_URL + endpoint)

            self.lastResponse = response

            if response.status_code == 200:
                self.lastJson = response.json()  # Uses .json() to parse
                return True
            else:
                print(f"Error {response.status_code}: {response.text}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"Network error while sending request: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON parsing error in response: {e}")
        except Exception as e:
            print(f"Unexpected error in sendRequest: {e}")
        return False

    def syncFromAdressBook(self, contacts):
        try:
            post = {
                "include": "extra_display_name",
                "phone_id": self.generateUUID(True),
                "module": "find_friends_contacts",
                "contacts": json.dumps(contacts),
                "source": "user_setting",
                "_csrftoken": self.lastResponse.cookies['csrftoken'],
                "device_id": self.device_id,
                "_uuid": self.uuid,
            }
            return self.sendRequest('address_book/link/', post=post)
        except Exception as e:
            print(f"Error syncing from address book: {e}")
            return False

    def unlink(self):
        try:
            post = {
                "user_initiated": "true",
                "phone_id": self.generateUUID(True),
                "device_id": self.device_id,
                "_uuid": self.uuid,
            }
            return self.sendRequest('address_book/unlink/', post=post)
        except Exception as e:
            print(f"Error unlinking address book: {e}")
            return False

    def get_last_json(self):
        try:
            return self.lastJson
        except AttributeError:
            print("Error: No last JSON available")
            return None

    def accuire(self):
        try:
            post = {
                "phone_id": self.generateUUID(True),
                "_csrftoken": self.lastResponse.cookies['csrftoken'],
                "module": "acquire_owner_contacts",
                "me": str(self.s),
                "_uuid": self.uuid,
            }
            return self.sendRequest('address_book/link/acquire_owner_contacts', post=post)
        except Exception as e:
            print(f"Error acquiring owner contacts: {e}")
            return False
