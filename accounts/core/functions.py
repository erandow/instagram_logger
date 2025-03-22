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
            result = requests.get(phone_numbers_url)
            result.raise_for_status()  # Check for HTTP errors
            my_dict = json.loads(result.text)

            numbers = [element.get('mobile') for element in my_dict[-32:]]
            if not numbers:
                raise ValueError("No numbers found in the response")
            
            contacts_count = len(my_dict)
        else:
            numbers = RetrievedAccount.objects.order_by('-id').values_list('phone_number', flat=True)[:32]
            contacts_count = len(numbers)


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

        return contacts, contacts_count

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
    try:
        if not number or not username:
            print(f"Warning: Missing data - number: {number}, username: {username}")
            return
            
        if store_result_in_url == 'false':
            update_username_by_core(number, username)
        else:
            # Prepare the post data with error handling for missing fields
            post = {
                "username": username.get('username', ''),
                "user_id": username.get('pk_id', ''),
                "mobile": number,
                "name": username.get('full_name', ''),
                "owner_id": owner_id,
            }
            
            # Add profile image if available
            if 'profile_pic_url' in username:
                profile_pic = username['profile_pic_url'].split('?')[0]
                post["profile_image"] = profile_pic
            
            # Try to get follower and following counts
            try:
                profile_response = requests.get(f"https://www.instagram.com/{username.get('username', '')}")
                profile_text = profile_response.text
                
                follower_match = re.search('"edge_followed_by":{"count":([0-9]+)}', profile_text)
                if follower_match:
                    post["follower_count"] = follower_match.group(1)
                
                following_match = re.search('"edge_follow":{"count":([0-9]+)}', profile_text)
                if following_match:
                    post["following_count"] = following_match.group(1)
            except Exception as e:
                print(f"Error getting follower/following counts: {e}")
            
            # Send the data
            result = requests.post(store_result_in_url, data=post)
            print(f"API response: {result.status_code} - {result.text}")
    except Exception as e:
        print(f"Error in set_account: {e}")


def get_specific_string_from_indices(dist_numbers, indices):
    try:
        # Calculate the index based on the binary representation
        index = 0
        for i, idx in enumerate(indices):
            index += 2**i * (1 if idx in [0, 1, 2, 3, 4] else 0)
        
        # Ensure the index is within the valid range
        if index < 0 or index >= len(dist_numbers):
            print(f"Warning: Calculated index {index} is out of range for dist_numbers of length {len(dist_numbers)}")
            return None
        
        return dist_numbers[index]
    except Exception as e:
        print(f"Error in get_specific_string_from_indices: {e}")
        return None