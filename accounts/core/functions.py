import requests
import json

def get_last_32_contacts():
    try:
        result = requests.get('https://api.saber24.ir/pending/mobile')
        result.raise_for_status()  # Check for HTTP errors
        my_dict = json.loads(result.text)

        numbers = [element.get('mobile') for element in my_dict[-32:]]
        if not numbers:
            raise ValueError("No numbers found in the response")

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
