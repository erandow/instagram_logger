def get_last_32_contacts():
    result = requests.get('https://api.saber24.ir/pending/mobile')
    my_dict = json.loads(result.text)
    numbers = [element.get('mobile') for element in my_dict[-32:]]
    contacts = []
    for number in numbers:
        number = "+98" + number[1:]
        contact = dict()
        contact["phone_numbers"] = [number]
        contact["first_name"] = number
        contact["last_name"] = number
        contact["email_addresses"] = []
        contacts.append(contact)
    return contacts, len(my_dict)


def distribute_strings(strings):
    # Initialize 5 empty lists
    lists = [[] for _ in range(5)]

    # Iterate through the strings with their index
    for index, string in enumerate(strings):
        # Convert the index to binary and pad with zeros to ensure it's at least 5 bits
        binary_rep = f"{index:05b}"

        # Add the string to the appropriate lists based on the binary representation
        for i in range(5):
            if binary_rep[4 - i] == '1':  # reverse the index to align with list order
                lists[i].append(string)

    return lists


def get_specific_string_from_indices(lists, indices):
    # Iterate through the indices in reverse order to prioritize higher indices
    for index in sorted(indices, reverse=True):
        if index < len(lists) and lists[index]:  # Check if the index is valid and the list is not empty
            return lists[index][-1]  # Return the last string from the valid list
    return None  # Return None if no valid index is found


def set_account(number, user):
    post = {
       "username": user["username"],
       "user_id": user["pk"],
       "mobile": number,
       "name": user["full_name"],
       "biogrraphy": "is not availible now",
       "profile_image": user["profile_pic_url"],
       "public": str(int(user["is_private"])),
       "follower_count": 1,
        "following_count": 1,
    }

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    result = requests.post('https://api.saber24.ir/set/pending/mobile')
    if result.status_code != 200:
        print(f'Account didnt set well. message: {result.message}')
