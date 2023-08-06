"""
This program controls the admin commands in the game.
Also any menu navigations.


Note: SpecimenImplant has a player's ID called "Sample #: 34225234"
Can have user input their sample #


"""

from time import sleep
from arkdriver.driver.application import Application


class Driver:
    def __init__(self, application=None):
        if application is None:
            application = Application()
            application.start()
        self.app = application
        self.pane = application.pane

    def open_players_list(self):
        """ In spectator mode, lists all current players """
        self.app.set_focus()
        sleep(1)
        self.app.send_key_ctrl_n()

    def close_players_list(self):
        """ Closes the players list window """
        coords = self.app.locate_button_by_image('player_list', 'close_template')
        self.app.click(coords=coords)

    def save_players_list(self):
        """ Stores the list of all players """
        # TODO: Machine learning and OCR to get the text list
        pass

    def close_admin_menu(self):
        """ Closes the admin menu window """
        coords = self.app.locate_button_by_image('admin_menu', 'close_template')
        self.app.click(coords=coords)

    def resume_pause_menu(self):
        """ Closes the pause menu window """
        coords = self.app.locate_button_by_image('pause_menu', 'close_template')
        self.app.click(coords=coords)

    def close_pause_menu(self):
        """ Closes the pause menu window """
        coords = self.app.locate_button_by_image('pause_menu', 'resume_template')
        self.app.click(coords=coords)

    def exit_to_main_menu(self):
        """ Exits to the main menu """
        coords = self.app.locate_button_by_image('pause_menu', 'exit_to_main_menu_template')
        self.app.click(coords=coords)

    def get_from_clipboard(self):
        """ Get the text from what is copied. """
        return self.app.get_from_clipboard()

    def write_console(self, *commands):
        self.app.set_focus()
        sleep(1)
        self.app.set_focus()
        self.app.save_to_clipboard_text("|".join(["{}".format(command) for command in commands]) + '|')
        self.app.send_key_tab()
        sleep(0.2)
        self.app.send_key_paste()
        sleep(1)
        self.app.send_key_enter()

    def write_console_args(self, args: list, *command_formats):
        """ player_ids is a list of player ids
            command_formats are commands in format form: "cheat GiveItemTO {} Pickaxe 1 1"
                where there is a '{}' in the string
         """
        commands = []
        for str_format in command_formats:
            commands.append(str_format.format(*args))
        self.write_console(*commands)

