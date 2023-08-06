from arkdriver.presentation.presentation import main as presentation
from arkdriver.driver import Driver
from arklibrary.admin import Admin
from pathlib import Path
from arklibrary import Ini
from time import sleep
import requests


URL = 'http://api.loadingproductions.com'
TEST_URL = 'http://127.0.0.1:5000'
TEST_CLOUD_URL = 'http://3.137.160.113'


def ping(url: str):
    count = 0
    received = False
    while not received and count < 10:
        try:
            res = requests.get(url)
            assert res.status_code == 200, f"Url returned status code: {res.status_code}"
            assert res.json()['connection'] == "successful", "Connection was not successful"
            received = True
        except Exception as e:
            print(e)
        count += 1


def get_commands(url: str):
    count = 0
    while count < 10:
        try:
            return requests.get(url)
        except Exception as e:
            print(e)
        count += 1


def set_command_as_executed(url: str, command_id):
    count = 0
    sent = False
    while not sent and count < 10:
        try:
            res = requests.patch(url + f'/command/{command_id}', data={'executed': True})
            if res.status_code != 200:
                raise Exception("failed to update command as executed [command_id]:", command_id)
            sent = True
        except Exception as e:
            print(e)
        count += 1


def config():
    path = Path.cwd() / Path('config.ini')
    if not path.exists():
        return
    config = Ini(path)
    if not 'ADMIN' in config:
        return
    admin_password = config['ADMIN']['password']
    admin_player_id = config['ADMIN']['player_id']
    return {'admin_password': admin_password, 'admin_player_id': admin_player_id}


def fetch_commands(url: str, interval=10, wait=5):
    while True:
        res = get_commands(url)
        data = []
        try:
            data = [c for c in res.json() if not c['executed']]
            print(f"FETCHED: {len(data)}")
        except:
            print(f"[Error] Request to api crashed, response: {res = }")
        if len(data) == 0:
            sleep(wait)
            continue
        i = 0
        while i < len(data):
            print(f"DATA[{i}: {min(i+interval, len(data))}]: {data}")
            yield data[i:i+interval]
            i += interval


def run(url: str, interval=10, wait=5):
    print("Sign into the server.")
    input("Press enter to continue...")
    print()

    print("Create your character and spawn without dying.")
    input("Press enter to continue...")
    print()
    admin_credentials = config()
    if admin_credentials is None:
        print(admin_credentials)
        password = input("What is the server ADMIN PASSWORD: ")
        while len(password) == 0:
            print("ERROR: The admin password must be longer than 0 characters.")
            password = input("What is the server's ADMIN PASSWORD: ")
        print()

        admin_id = input("What is the ADMIN specimen implant id: ")
        while len(admin_id) != 9 or not admin_id.isnumeric():
            print("ERROR: The specimen implant id must be length 9 and all numbers.")
            admin_id = input("What is the ADMIN specimen implant id: ")
        print()
    else:
        password = admin_credentials['admin_password'].upper()
        admin_id = admin_credentials['admin_player_id']
    print("Close any menu on the screen and make sure your character's inventory is closed.")
    input("Press enter to continue...")

    driver = Driver()
    admin = Admin(driver=driver, password=password, player_id=admin_id)
    admin.enable_admin()
    admin.execute()
    for commands in fetch_commands(url + '/command', interval=interval, wait=wait):
        for command in commands:
            admin.command_list.append(command['code'])
            command['executed'] = True
            set_command_as_executed(url, command['id'])
        admin.execute()


def executable():
    ping(URL)
    run(URL, interval=10, wait=5)


def main():
    print("[1] Run driver with official API")
    print("[2] Test driver with local API")
    print("[3] Test driver with cloud API")
    print("[4] presentation")
    response = input("What would you like to run? ")
    choices = ['1', '2', '3', '4']
    while response not in choices:
        print(f"ERROR: your response should be a choice of: {choices}")
        print("[1] Run driver with official API")
        print("[2] Test driver with local API")
        print("[3] Test driver with cloud API")
        print("[4] presentation")
        response = input("What would you like to run? ")

    if response == '1':
        ping(URL + '/ping')
        run(URL, interval=10, wait=5)
    elif response == '2':
        ping(TEST_URL + '/ping')
        run(TEST_URL, interval=10, wait=5)
    elif response == '3':
        ping(TEST_CLOUD_URL + '/ping')
        run(TEST_CLOUD_URL, interval=10, wait=5)
    elif response == '4':
        presentation()


if __name__ == "__main__":
    main()
