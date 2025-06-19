from textual.screen import Screen
from textual.containers import Vertical
from textual.widgets import Static, Input, Button
from textual.app import ComposeResult

from logic.setup import setup_master_password, save_master_password, load_master_hash


class FirstLoginScreen(Screen):
    
    
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Escribe tu contraseña", classes="title"),
            Input(password=True, placeholder="contraseña", id="password_input"),
            Input(password=True, placeholder="Confirmar contraseña", id="confirm_input"),
            Button("Mostrar Contraseña", id="toggle_password"),
            Button("Guardar", id="save_button"),
            Static("", id="message")
        )
        
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        password_input = self.query_one("#password_input", Input)
        confirm_input = self.query_one("#confirm_input", Input)
        msg = self.query_one("#message", Static)
        
        if event.button.id == "toggle_password":
            new_state = not password_input.password
            password_input.password = new_state
            confirm_input.password = new_state
            event.button.label = "Ocultar" if not new_state else "Mostrar"
            
        if event.button.id == "save_button":
            password = password_input.value
            confirm = confirm_input.value
            
            
            
            
            if setup_master_password(password, confirm):
                msg.update("Contraseña establecida correctamente.")
                self.app.master_password = password
                self.app.push_screen("main_menu") # o main_menu
                
            else:
                msg.update("Las contraseñas no coinciden o están vacias.")