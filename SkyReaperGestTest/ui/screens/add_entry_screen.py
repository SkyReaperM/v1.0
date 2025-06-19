from textual.screen import Screen
from textual.containers import Vertical
from textual.widgets import Static, Input, Button
from textual.app import ComposeResult

from logic.save import save_entry
#from logic.vault import save_entry

class AddEntryScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Añadir Nuevo Servicio", classes="title"),
            Input(placeholder="Nombre del Servicio", id="service_input"),
            Input(placeholder="Usuario o email", id="user_input"),
            Input(password=True, placeholder="Contraseña del servicio", id="password_input"),
            Button("Guardar", id="save_button"),
            Button("Volver al menú", id="back_button"),
            Static("", id="message")
        )
        
        
        
        
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        service = self.query_one("#service_input", Input).value
        username = self.query_one("#user_input", Input).value
        service_password = self.query_one("#password_input", Input).value
        msg = self.query_one("#message", Static)
        
        
        if event.button.id == "save_button":
            master_password = self.app.master_password if hasattr(self.app, "master_password") else None
            
            if not master_password:
                msg.update("Contraseña maestra no establecida")
                return
                
            success = save_entry(master_password, {
                "servicio": service,
                "usuario": username,
                "contraseña": service_password
            })
            
            if  success:
                msg.update("Guardado correctamente")
            else:
                msg.update("Error al guardar")
                
        elif event.button.id == "back_button":
            self.app.pop_screen()