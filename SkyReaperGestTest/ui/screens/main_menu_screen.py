from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical
from textual.app import ComposeResult

class MainMenuScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(" Menu Principal - SkyReaper V1.2", classes="title"),
            Button("Randomizar Contraseñas", id="generate_random"),
            Button("Guardar Contraseña", id="save_password"),
            Button("Ver Contraseñas", id="view_password"),
            Button("Eliminar Contraseñas", id="delete_password"),
            Button("Salir", id="exit_app")
        )
        
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "save_password":
            self.app.push_screen("add_entry")
            
        elif btn_id == "view_password":
            self.app.push_screen("view_entries")
        
        elif btn_id == "delete_password":
            self.app.push_screen("delete_entry")
            
        elif btn_id == "exit_app":
            self.app.exit()
            
        elif btn_id == "generate_random": # Aquí puedes redirigir a la pantalla de generación si existe
            self.app.push_screen("generate_password")
            
        else:
            # Botones con pantalla
            
            pass