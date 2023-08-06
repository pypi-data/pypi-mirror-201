from arkdriver import Driver
from arklibrary.admin import Admin, Bundle
from arklibrary.blueprints import Island
from time import sleep
from itertools import cycle
import json
import numpy as np
from random import choices
import arkdriver
import os
from pathlib import Path


spectator_ids = []
admin_id = ''
admin: Admin = None
bundle: Bundle = None


def start_admin(driver: Driver, password: str, player_id: str):
    global admin_id
    global admin
    global bundle
    admin_id = player_id
    admin = Admin(driver=driver, password=password, player_id=player_id)
    admin.enable_admin().execute()
    bundle = Bundle(admin)
    return admin


def add_spectator(player_id: str):
    global spectator_ids
    spectator_ids.append(player_id)


def give_spectators_armour():
    armours = [bundle.flak_armour, bundle.desert_armour, bundle.fur_armour, bundle.hazard_armour, bundle.tek_armour]
    bundle.tek_armour(admin_id)
    bundle.execute()
    for spectator, armour in zip(spectator_ids, cycle(armours)):
        armour(spectator, quality=6)
        bundle.execute()


def give_spectators_weapons():
    weapons = [bundle.shotgun_set, bundle.sniper_set, bundle.flame_arrow_set, bundle.compound_set, bundle.rifle_set, bundle.rocket_set]
    bundle.shotgun_set(admin_id)
    bundle.execute()
    for spectator, weapon in zip(spectator_ids, cycle(weapons)):
        weapon(spectator, quality=6)
        bundle.execute()


def give_spectators_fob_set():
    bundle.fob_set(admin_id)
    bundle.execute()
    for spectator in spectator_ids:
        bundle.fob_set(spectator)
        bundle.execute()


def spawn_dinos(blueprint_path, tamed=True, level=150):
    global admin
    global spectator_ids
    for spectator in spectator_ids:
        admin.teleport_to_playerid(spectator)
        admin.spawn_dino(blueprint_path, tamed=tamed, level=level)
    admin.execute()


def teleport_red():
    admin.teleport_red_obelisk()
    for spectator in spectator_ids:
        admin.teleport_player_id_to_me(spectator)
    admin.execute()


def teleport_blue():
    admin.teleport_blue_obelisk()
    for spectator in spectator_ids:
        admin.teleport_player_id_to_me(spectator)
    admin.execute()


def teleport_green():
    admin.teleport_green_obelisk()
    for spectator in spectator_ids:
        admin.teleport_player_id_to_me(spectator)
    admin.execute()



def save_current_coordinates(map, name, num_drops, coords):
    """ Stores the coordinates into file with a name
    :param name: str, name for the coordinates
    """
    data = {"center": {}, "gen1": {}, "gen2": {}, "island": {},
            "scortched": {}, "ragnarok": {}, "extinction": {}, "aberration": {}}
    if map not in data:
        raise NotImplemented("'{}' isn't part of the map list: {}".format(map, data.keys()))
    file_path = Path(os.path.dirname(arkdriver.__file__)) / Path('presentation/saved_coordinates.json')
    if file_path.exists():
        with open(file_path, 'r') as r:
            data = json.load(r)
    if str(num_drops) not in data[map][name]:
        data[map][name][str(num_drops)] = coords
    with open(file_path, "w") as w:
        json.dump(data, w)


def generate_obelisk_drop_coords(admin, map: str, color: str, number_of_drops: int):
    file = Path(os.path.dirname(arkdriver.__file__)) / Path('presentation/saved_coordinates.json')
    with open(file, 'r') as r:
        data = json.load(r)
    coords = None
    name = None
    if color.lower() == 'blue':
        coords = data[map]['blue_obelisk']
        name = 'blue_obelisk_drops'
    elif color.lower() == 'green':
        coords = data[map]['green_obelisk']
        name = 'green_obelisk_drops'
    elif color.lower() == 'red':
        coords = data[map]['red_obelisk']
        name = 'red_obelisk_drops'
    x, y, z, _, _ = coords.values()
    circumference_coords = obelisk_circle_coords([x, y, z], spokes=number_of_drops)
    coordinates = []
    finished = False
    while not finished:
        try:
            coordinates.clear()
            for i, ccc in enumerate(circumference_coords):
                admin.teleport_xyz(*ccc).execute()
                sleep(8)
                admin.driver.copy_coords()
                new_ccc_str = admin.driver.app.get_from_clipboard()
                coordinates.append([float(c) for c in new_ccc_str.split()][:3])
                if len(coordinates) == number_of_drops:
                    finished = True
                elif i + 1 != len(coordinates):
                    break
        except Exception:
            pass
        except KeyboardInterrupt:
            finished = True
    save_current_coordinates(map, name, number_of_drops, coordinates)


def obelisk_circle_coords(obelisk_center_coord, spokes=10):
    x_center, y_center, _ = obelisk_center_coord
    radius = 1763.2620338452252
    offsets = np.linspace(0, 360, spokes)
    coords = []
    for offset in offsets:
        x = radius * np.cos(offset)
        y = radius * np.sin(offset)
        coords.append((x_center + x, y + y_center, 0))
    return coords


def drop_the_supplies(admin, map, quantity=8, quality=0, only=False):
    supply_drops = [
        Island.WHITE_BEACON,
        Island.WHITE_BEACON_DOUBLE_ITEMS,
        Island.GREEN_BEACON,
        Island.GREEN_BEACON_DOUBLE_ITEMS,
        Island.BLUE_BEACON,
        Island.BLUE_BEACON_DOUBLE_ITEMS,
        Island.PURPLE_BEACON,
        Island.PURPLE_BEACON_DOUBLE_ITEMS,
        Island.YELLOW_BEACON,
        Island.YELLOW_BEACON_DOUBLE_ITEMS,
        Island.RED_BEACON,
        Island.RED_BEACON_DOUBLE_ITEMS
    ]
    quality = min(quality, len(supply_drops) - 1)
    drops = supply_drops[quality:]

    file = Path(os.path.dirname(arkdriver.__file__)) / Path('presentation/saved_coordinates.json')
    with open(file, 'r') as r:
        data = json.load(r)
    red = data[map]['red_obelisk_drops'][str(quantity)]
    green = data[map]['green_obelisk_drops'][str(quantity)]
    blue = data[map]['blue_obelisk_drops'][str(quantity)]

    if only:
        for ob_coords in [red, green, blue]:
            for coords in ob_coords:
                x, y, z = coords
                admin.teleport_xyz(x, y, z)
                admin.spawn_beacon(drops[0])
    else:
        weights = (100, 90, 80, 70, 60, 50, 30, 25, 20, 15, 10, 5)[quality:]
        for ob_coords in [red, green, blue]:
            shuffled_drops = choices(drops, weights=weights, k=len(ob_coords))
            for pair in zip(ob_coords, shuffled_drops):
                coords, drop = pair
                x, y, z = coords
                admin.teleport_xyz(x, y, z)
                admin.spawn_beacon(drop)
    admin.execute()


def event_supply_drops(admin, map, quantity=4, quality=4):
    message = ''
    if quality < 4:
        message = "Gamma Supply Drop: Event in {} seconds. Random drops will spawn at every obelisks. PVP is allowed."
    if 4 <= quality < 8:
        message = "Beta Supply Drop: Event in {} seconds. Random drops will spawn at every obelisks. PVP is allowed."
    if 8 <= quality:
        message = "Alpha supply: drop Event in {} seconds. Random drops will spawn at every obelisks. PVP is allowed."
    admin.broadcast(message.format(60))
    admin.execute()
    sleep(30)
    admin.broadcast(message.format(30))
    admin.execute()
    sleep(20)
    admin.broadcast(message.format(5))
    admin.execute()

    drop_the_supplies(admin, map, quantity, quality)



def initial():
    driver = Driver()
    print("Request the map to be Ragnarok.")
    input("Press enter to continue...")
    print()

    print("Request for the ADMIN password.")
    input("Press enter to continue...")
    print()

    print("Join the server and make sure you have a character already created.")
    input("Press enter to continue...")
    print()

    password = input("What is the server's ADMIN PASSWORD: ")
    while len(password) == 0:
        print("ERROR: The admin's server password must be longer than 0 characters.")
        password = input("What is the server's ADMIN PASSWORD: ")
    print()

    admin_id = input("What is the ADMIN specimen implant id: ")
    while len(admin_id) != 9 or not admin_id.isnumeric():
        print("ERROR: The specimen implant id must be length 9 and all numbers.")
        admin_id = input("What is the ADMIN specimen implant id: ")
    print()

    start_admin(driver=driver, password=password, player_id=admin_id)


def present_spectators():
    for i in range(10):
        admin.broadcast("Each player must send Zed3kiah (a.k.a Zed) their specimen implant id in a message. Open your inventory and hover over the diamond. The diamond has a number called your specimen implant id.")
        admin.execute()
        sleep(2)
    spectator = input("What is the SPECTATOR specimen implant id? (Enter 'stop' to proceed): ")
    while spectator != 'stop':
        if len(spectator) != 9 or not spectator.isnumeric():
            print("ERROR: The specimen implant id must be length 9 and all numbers.")
        else:
            spectator_ids.append(spectator)
        spectator = input("What is the SPECTATOR specimen implant id? (Enter 'stop' to proceed): ")
    print()



def present_teleportation():
    for i in range(6):
        admin.broadcast("As an example, I'll teleport you all to each obelisk every 3 seconds. Just to prove a point.")
        admin.execute()
        sleep(2)
    sleep(3)
    teleport_red()
    sleep(3)
    teleport_green()
    sleep(3)
    teleport_blue()
    sleep(3)
    teleport_red()
    sleep(3)
    teleport_green()
    sleep(3)
    teleport_blue()
    sleep(3)


def present_item_giving():
    for i in range(6):
        admin.broadcast("I will now present you with item spawning. Each one of you will receive armour of a different kind.")
        admin.execute()
        sleep(2)
    give_spectators_armour()
    sleep(20)

    for i in range(4):
        admin.broadcast("Each one of you will receive weapons of a different kind.")
        admin.execute()
        sleep(2)
    give_spectators_weapons()
    sleep(20)

    for i in range(4):
        admin.broadcast("Each one of you will receive a fob set.")
        admin.execute()
        sleep(2)
    give_spectators_fob_set()
    sleep(20)


def present_drop_party():
    admin.broadcast("ALERT: A major drop event is about to commence")
    admin.execute()
    sleep(4)

    admin.broadcast("ALERT: Everyone head to an obelisk")
    admin.execute()
    sleep(2)

    admin.broadcast("ALERT: Everyone head to an obelisk")
    admin.execute()
    sleep(2)

    obelisks = [admin.teleport_red_obelisk, admin.teleport_green_obelisk, admin.teleport_blue_obelisk]
    for spectator, obelisk in zip(spectator_ids, cycle(obelisks)):
        obelisk()
        admin.teleport_player_id_to_me(spectator)
    admin.execute()
    drop_the_supplies(admin, 'ragnarok', quantity=8, quality=99, only=False)
    print("\n\n\n\n\n\n\n\n\n")
    print("Please wait until the drop party is finished before you continue.")
    print("\n\n")


def present_ending():
    teleport_blue()

    admin.broadcast("This concludes the presentation")
    admin.execute()
    sleep(5)

    admin.broadcast("I hope you've enjoyed it. Please, now is the time to ask questions.")
    admin.execute()
    sleep(5)



def main():
    initial()
    print()
    input("Press enter to continue...")

    present_spectators()
    print()
    input("Press enter to continue...")

    present_teleportation()
    print()
    input("Press enter to continue...")

    present_item_giving()
    print()
    input("Press enter to continue...")

    present_drop_party()
    print()
    input("Press enter to continue...")

    present_ending()


if __name__ == '__main__':
    main()
