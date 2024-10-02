# accounts/tasks.py

from celery import shared_task
import time
from core.instagram import Instagram
from .models import InstagramAccount
from .functions import *

@shared_task
def long_running_task():

    loggedin_accounts = []
    accounts = InstagramAccount.objects.all()
    pks = []
    for account in accounts:
        print(f"Username: {account.username}, Password: {account.password}")
        loggedin_accounts.append(Instagram(account.username, account.password))
        res = loggedin_accounts[-1].login()
        if not res:
            print('cant login account. please double check accounts and the retry')
            return
        pks.append(loggedin_accounts[-1].get_last_json()["logged_in_user"]["pk"])

    flag = False
    while (not flag):
        flag = True
        for loggedin_account in loggedin_accounts:
            result = loggedin_account.unlink()
            if "status" not in result or result["status"] != "ok":
                flag = False
                print("An account is in unlink process.... retrying aproximately 1 hour")
        if not flag:
            total_seconds = 3600  # 1 hour = 3600 seconds
            interval = 30  # Countdown display interval (in seconds)

            # Loop through intervals of 30 seconds
            while total_seconds > 0:
                minutes, seconds = divmod(total_seconds, 60)
                print(f"Time remaining: {minutes} minutes, {seconds} seconds")
                time.sleep(interval)
                total_seconds -= interval

            print("Countdown completed. Executing the main task 1 more time...")




    numbers, tmp = get_last_32_contacts()
    print("Querying at most 32 pending numbers.... please wait. this might take several hours.")
    print(numbers)
    dist_numbers = distribute_strings(numbers)
    print("Distributed numbers:")
    print(dist_numbers)
    for i in range(5):
        loggedin_accounts[i].syncFromAdressBook(dist_numbers[i])

    time.sleep(300) # sleep 5 minutes before getting the result
    results = []
    flag = False
    while not flag:
        flag = True
        for i in range(5):
            if loggedin_accounts[i].retriveFromAdressBook(pks[i]):
                result.append(loggedin_accounts[i].get_last_json())
            else:
                flag = False
                print('Failed to get result from 1 account. retrying in 5 minutes...')
                time.sleep(300)
                break


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
