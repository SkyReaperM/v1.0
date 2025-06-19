from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Input, Button
from logic.auth import verify_password, load_master_hash, save_master_password

#STORED_HASH = "3b3d903b8156ab23efcf54af308a4a29e8079f03e6dc89893bac2b361d1879ac" # es admin123

class AuthScreen(Screen):
    def __init__(self, stored_hash=None):
        super().__init__()
        self.stored_hash = stored_hash
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Introduce tu contraseña", classes="title"),
            Input(password=True, placeholder="Contraseña", id="password_input"),
            
            Button("Mostrar contraseña", id="toggle_password"),
            Button("Entrar", id="login_button"),
            Static("", id="auth_message")
        )
        
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        password_input = self.query_one("#password_input", Input)
        msg = self.query_one("#auth_message", Static)
        
        #Mostrar contraseña
        if event.button.id == "toggle_password":
            new_state = not password_input.password
            password_input.password = new_state
            
            event.button.label = "Ocultar" if not new_state else "Mostrar"
        #Boton Entrar/ Guardar contraseña maestra
        elif event.button.id == "login_button":
            password = password_input.value
            
            stored_hash = load_master_hash()
            
            if stored_hash:
                #Existe Login normal
                if verify_password(password, stored_hash):
                    self.app.master_password = password #guardar contraseña maestra para cifrado
                    self.app.push_screen("main_menu")
                else:
                    msg.update("Contraseña Incorrecta")
                    msg.set_classes("error")
                    
                    
            
                #primera vez confirmar y guardar
                
                
                    
            else:
                save_master_password(password)
                msg.update("Contraseña establecida correctamente")
                msg.remove_class("error")
                self.app.master_password = password
                self.app.push_screen("main_menu")