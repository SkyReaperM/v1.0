from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual.containers import Vertical, Horizontal
from textual.app import ComposeResult


from logic.randomizer import generate_random_password
from logic.save import save_entry 

class GeneratePasswordScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("🔐 Generador de Contraseñas", classes="title"),
            
            Input(placeholder="Servicio", id="service_input"),
            Input(placeholder="Usuario o Email", id="user_input"),
            
            
            Horizontal(
                Static("Longitud:"),
                Input(value="16", id="length_input", classes="small_input"),
            ),
            
            Button("Generar y Guardar", id="generate_button"),
            Static("", id="password_output"),
            
            Button("Volver al menu", id="back_button"),
        )
        
        
def on_button_pressed(self, event: Button.Pressed) -> None:
    print(f"[DEBUG] Botón presionado: {event.button.id}")  # 👈 Agregado para depurar
    output = self.query_one("#password_output", Static)
    
    
    if event.button.id == "generate_button":
        try:
            length = int(self.query_one("#length_input", Input).value)
            servicio = self.query_one("#service_input", Input).value
            usuario = self.query_one("#user_input", Input).value
            master_password = getattr(self.app, "master_password", None)
            
            
            if not (servicio and usuario):
                output.update("⚠️ Servicio y usuario requeridos")
                return
                
                
            password = generate_random_password(length)
            success = save_entry(master_password, {
                "servicio": servicio,
                "usuario": usuario,
                "contraseña": password
            })
            if success:
                output.update(f"✅ Generado y guardado:\n🔑 {password}")
            else:
                output.update(f"❌ Error: {e}")
                
        except Exception as e:
            output.update(f"❌ Error: {e}")
    elif event.button.id == "back_button":
        self.app.pop_screen()