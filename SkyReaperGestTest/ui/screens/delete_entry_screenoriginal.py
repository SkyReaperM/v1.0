from textual.screen import Screen
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.widgets import Static, Button
from textual.app import ComposeResult


from logic.vault import load_entries, delete_entry



class DeleteEntryScreen(Screen):
    
    
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Eliminar Contraseñas", classes="title"),
            ScrollableContainer(id="delete_container"),
             #Mostramos confirmación
            Vertical(id="confirmation_box"),
            Button("Volver al menu", id="back_button")
        )
        
        
        
        
    def on_show(self) -> None:
        self.load_entries()
        
        
        
    def load_entries(self):
        container = self.query_one("#delete_container", ScrollableContainer)
        container.remove_children()
        
        
        master_password = getattr(self.app, "master_password", None)
        entries = load_entries(master_password) if master_password else []
        
        if not entries:
            container.mount(Static("No hay entradas guardadas o error al cargar. ", classes="error"))
            return
            
            
        for entry in entries:
            servicio = entry["servicio"]
            usuario = entry["usuario"]
            #id con combinacion unica
            btn_id = f"delete_{servicio}__{usuario}"
            container.mount(
                Horizontal(
                    Static(f"{'servicio'}", classes="entry_service", expand=True),
                    Static(f"{'usuario'}", classes="entry_user", expand=True),
                    Button("Eliminar", id=btn_id, classes="delete_button"),
                    classes="entry_row"
                )
            )
            
            
            
    def show_confirmation(self, servicio: str, usuario: str):
        confirm_box = self.query_one("#confirmation_box", Vertical)
        confirm_box.remove_children()
        
        confirm_box.mount(
            Vertical(
                Static(f"¿Eliminar \"{servicio}\"?", classes="confirm_text"),
                Horizontal(
                    Button("Si", id=f"confirm_delete_{servicio}__{usuario}", classes="confirm_yes"),
                    Button("No", id=f"cancel_delete", classes="confirm_no")
                )
            )
        )
        
    def clear_confirmation(self):
        self.query_one("#confirmation_box", Vertical).remove_children()
        
        
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        
        if btn_id == "back_button":
            self.app.pop_screen()
            return
            
            
        if btn_id.startswith("delete_"):
            raw = btn_id.replace("delete_", "")
            servicio, usuario = raw.split("__", 1)
            self.show_confirmation(servicio, usuario)
            return
            
        if btn_id.startswith("confirm_delete_"):
            raw = btn_id.replace("confirm_delete_", "")
            servicio, usuario = raw.split("__", 1)
            master_password = getattr(self.app, "master_password", None)
            
            if delete_entry(master_password, servicio):
                self.clear_confirmation()
                self.load_entries()
            else:
                self.query_one("#confirmation_box", Vertical).mount(
                    Static("❌ Error al eliminar", classes="error")
                )
            
        if btn_id == "cancel_delete":
            self.clear_confirmation()