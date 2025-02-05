# accounts/tasks.py

from celery import shared_task
import time
from .core.instagram import Instagram
from .models import InstagramAccount
from .core.functions import *
from datetime import datetime

@shared_task
def long_running_task():

    loggedin_accounts = []
    accounts = InstagramAccount.objects.all().order_by('lru').values()
    accounts = accounts[:5]
    pks = []
    for account in accounts:
        print(f"Username: {account.username}, Password: {account.password}")
        loggedin_accounts.append(Instagram(account.username, account.password))
        res = loggedin_accounts[-1].login()
        if not res:
            print(f"cant login account. please double check accounts and the retry")
            return
        pks.append(loggedin_accounts[-1].get_last_json()["logged_in_user"]["pk"])

    repeat_read_numbers = False
    while (not repeat_read_numbers):
        repeat_read_numbers = True
        for loggedin_account in loggedin_accounts:
            result = loggedin_account.unlink()
            if "status" not in result or result["status"] != "ok":
                repeat_read_numbers = False
                print("An account is in unlink process.... retrying approximately 1 hour")
        if not repeat_read_numbers:
            total_seconds = 3600  # 1 hour = 3600 seconds
            interval = 30  # Countdown display interval (in seconds)

            # Loop through intervals of 30 seconds
            while total_seconds > 0:
                minutes, seconds = divmod(total_seconds, 60)
                print(f"Time remaining: {minutes} minutes, {seconds} seconds")
                time.sleep(interval)
                total_seconds -= interval

            print("Countdown completed. Executing the main task 1 more time...")


    print("Unlink done")
    repeat_read_numbers = True
    while repeat_read_numbers:
        numbers, tmp = get_last_32_contacts()
        repeat_read_numbers = False
        for i in range(len(numbers)):
            if check_no_account(numbers[i]):
                print(f"Found number with no instagram account {numbers[i]}")
                del numbers[i]
                repeat_read_numbers = True
                set_number_no_account((numbers[i]))

    print("Querying at most 32 pending numbers.... please wait. this might take several hours.")
    print(numbers)
    dist_numbers = distribute_strings(numbers)
    print("Distributed numbers:")
    print(dist_numbers)
    repeat_sync_contact = False
    while not repeat_sync_contact:
        repeat_sync_contact = True
        for i in range(5):
            res = loggedin_accounts[i].syncFromAdressBook(dist_numbers[i])
            if not res:
                repeat_sync_contact = False
                print("Failed to get contacts [" + json.loads( loggedin_accounts[i].lastResponse.text)["message"] + "]")


    time.sleep(300) # sleep 5 minutes before getting the result
    results = []
    repeat_read_numbers = False
    while not repeat_read_numbers:
        repeat_read_numbers = True
        for i in range(5):
            if loggedin_accounts[i].retriveFromAdressBook(pks[i]):
                result.append(loggedin_accounts[i].get_last_json())
            else:
                repeat_read_numbers = False
                print('Failed to get result from 1 account. retrying in 5 minutes...')
                time.sleep(300)
                break

    accounts.bulk_update(lru=datetime.now())

    # Decode based on results
    info_dict = {}
    indices_dist = {}
    for result in results:
        for user in result["users"]:
            if user["username"] not in info_dict:
                info_dict[user["username"]] = user
            if user["username"] not in indices_dist:
                indices_dist[user["username"]] = [i]
            else:
                indices_dist[user["username"]].append(i)



    for username, indices in indices_dist.items():
        number = get_specific_string_from_indices(dist_numbers, indices)
        set_account(number, info_dict[username])


# 1     0001 => account 1
# 2     0010 => account 2
# 3     0011 => account 1 , account 2
# 4     0100 => account 3
# 5     0101 => account 3, account 1
# 6     0110 => account 3, account 2
# 7     0111 => account 3, account 2, account 3
# 8     1000 => account 4
# 9     1001 => account 4, account 1
# 10    1010 => account 4, account 2
# 11    1011 => account 4, account 2, account 1
# 12    1100 => account 4, account 3
# 13    1101 => account 4, account 3, account 1
# 14    1110 => account 4, account 3, account 2
# 15    1111 =? account 4, account 3, account 2, account 1


@shared_task
def my_scheduled_task():
    long_running_task().delay()
