from textual.screen import Screen
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.widgets import Static, Button, Input
from textual.app import ComposeResult
from textual.timer import Timer
from logic.vault import load_entries

class ViewEntriesScreen(Screen):
    timer: Timer | None = None
    
    def compose(self) -> ComposeResult:
        
        yield Vertical(
            Static("Contraseñas Guardadas", classes="title", id="title"),
            ScrollableContainer(id="entries_container"),
            Button("Volver al Menu", id="back_button")
            
            )
            
        
        
    def on_mount(self) -> None:
        #Refresca cada 5 secs
        self.timer = self.set_interval(5, self.load_entries)
        self.load_entries()
        
        
    def on_show(self) -> None:
        self.load_entries()
        
        
    def on_hide(self) -> None:
         #Se para si se oculta pantalla
         
         if self.timer:
             self.timer.stop()
        
    def load_entries(self) -> None:
        
        container = self.query_one("#entries_container", ScrollableContainer)
        container.remove_children()
        
        master_password = getattr(self.app, "master_password", None)
        
        if not master_password:
            container.mount(Static("Contraseña maestra no disponible", classes="error"))
            return
            
        entries = load_entries(master_password)
            
        if not entries:
            container.mount(Static("No se puede cargar la contraseña o esta vacia", classes="error"))
            return
            
        for entry in entries:
            container.mount(
                Static(
                    f"Servicio: {entry['servicio']}\n👤 Usuario: {entry['usuario']}\n🔑 Contraseña: {entry['contraseña']}",
                    classes="entry"
                )
            )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back_button":
            self.app.pop_screen()