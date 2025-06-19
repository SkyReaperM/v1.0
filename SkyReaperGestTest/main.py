from textual.app import App

from logic.setup import is_first_time_setup
from ui.screens.auth_screen import AuthScreen
from ui.screens.first_login_screen import FirstLoginScreen
from ui.screens.main_menu_screen import MainMenuScreen
from ui.screens.add_entry_screen import AddEntryScreen
from ui.screens.view_entries_screen import ViewEntriesScreen
from ui.screens.delete_entry_screen import DeleteEntryScreen
from ui.screens.generate_password_screen import GeneratePasswordScreen

class SkyReaperApp(App):
    CSS_PATH = "ui/styles/default.css"
    
    def on_ready(self):
        #registrar pantallas
        self.install_screen(FirstLoginScreen(), name="first_login")
        self.install_screen(AuthScreen(), name="auth")
        self.install_screen(MainMenuScreen(), name="main_menu")
        self.install_screen(AddEntryScreen(), name="add_entry")
        self.install_screen(ViewEntriesScreen(), name="view_entries")
        self.install_screen(DeleteEntryScreen(), name="delete_entry")
        self.install_screen(GeneratePasswordScreen(), name="generate_password")
        #Decidir que pantalla mostrar primero
        if is_first_time_setup():
            self.push_screen("first_login")
        else:
            self.push_screen("auth")
    
        
if __name__ == "__main__":
    app = SkyReaperApp()
    app.run()