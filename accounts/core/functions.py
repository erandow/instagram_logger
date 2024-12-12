import requests
import json
import configparser
from ..models import RetrievedAccount
import re



# خواندن تنظیمات از فایل config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# بررسی اینکه آیا باید شماره تلفن‌ها از URL دریافت شوند یا از دیتابیس
use_external_url = config.get('settings', 'use_external_url')
phone_numbers_url = config.get('settings', 'phone_numbers_url')
store_result_in_url = config.get('settings', 'store_result_in_url') 
owner_id = config.get('settings', 'owner_id')
result_no_account_url = config.get('settings', 'result_no_account_url')

def check_no_account(number):
    return False

def set_number_no_account(number):
    post = {
        "mobile": number,
        "status": 2,
        "owner_id": owner_id,
    }
    result = requests.post(result_no_account_url, data=post)
    print(result)

def get_last_32_contacts():
    try:
        if use_external_url == 'true':
            result = requests.get('https://api.saber24.ir/pending/mobile')
            result.raise_for_status()  # Check for HTTP errors
            my_dict = json.loads(result.text)

            numbers = [element.get('mobile') for element in my_dict[-32:]]
            if not numbers:
                raise ValueError("No numbers found in the response")
        else:
            numbers = RetrievedAccount.objects.order_by('-id').values_list('phone_number', flat=True)[:32]


        contacts = []
        for number in numbers:
            if not number.startswith("+98"):
                number = "+98" + number[1:]
            contact = dict()
            contact["phone_numbers"] = [number]
            contact["first_name"] = number
            contact["last_name"] = number
            contact["email_addresses"] = []
            contacts.append(contact)

        return contacts, len(my_dict)

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return [], 0

def distribute_strings(strings):
    try:
        if not isinstance(strings, list):
            raise ValueError("Input must be a list of strings")
        
        # Initialize 5 empty lists
        lists = [[] for _ in range(5)]

        # Iterate through the strings with their index
        for index, string in enumerate(strings):
            # Convert the index to binary and pad with zeros to ensure it's at least 5 bits
            binary_rep = f"{index:05b}"

            # Add the string to the appropriate lists based on the binary representation
            for i in range(5):
                if binary_rep[4 - i] == '1':
                    lists[i].append(string)

        return lists
    except Exception as e:
        print(f"Error distributing strings: {e}")
        return [[] for _ in range(5)]



def update_username_by_core(phone_number, username):
    try:
        # جستجو برای یافتن حساب با استفاده از شماره تلفن
        account = RetrievedAccount.objects.get(phone_number=phone_number)
        # به‌روزرسانی نام کاربری
        account.username = username
        account.save()  # ذخیره تغییرات
        return f"Username updated for account with phone number {phone_number}"

    except RetrievedAccount.DoesNotExist:
        # در صورت عدم وجود حساب با شماره تلفن وارد شده
        return f"Account with phone number {phone_number} does not exist."


def set_account(number, username):
    if store_result_in_url == 'false':
        update_username_by_core(number, username)
    else:
        post = {
            "username": username['username'],
            "user_id": username['pk_id'],
            "mobile": number,
            "name": username['full_name'],
            "profile_image": username['profile_pic_url'].split('?')[0],
            "follower_count": re.search('"edge_followed_by":{"count":([0-9]+)}',requests.get("https://www.instagram.com/" + username['username']).text).group(1),
            "following_count": re.search('"edge_follow":{"count":([0-9]+)}',requests.get("https://www.instagram.com/" + username['username']).text).group(1),
            "owner_id": owner_id,
        }
        result = requests.post(store_result_in_url, data=post)
        print(result)
        pass


def get_specific_string_from_indices(dist_numbers, indices):
    index = sum([int(2**k * x) for x, k in zip(indices, range(1, len(indices) + 1))])
    return dist_numbers[index]