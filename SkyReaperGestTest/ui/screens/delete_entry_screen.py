from textual.screen import Screen
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.widgets import Static, Button
from textual.app import ComposeResult
from textual.timer import Timer

from logic.vault import load_entries
from logic.delete import delete_entry

class DeleteEntryScreen(Screen):
    timer: Timer | None = None

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Eliminar Contraseñas", classes="title"),
            ScrollableContainer(id="delete_container"),
            Vertical(id="confirmation_box"),
            Button("Volver al menu", id="back_button")
        )




    def on_mount(self) -> None:
        self.timer = self.set_interval(5, self.load_entries)
        self.load_entries()
        
    def on_show(self) -> None:
        self.load_entries()
    def on_hide(self) -> None:
        if self.timer:
            self.timer.stop()
            
    def load_entries(self):
        container = self.query_one("#delete_container", ScrollableContainer)
        container.remove_children()

        master_password = getattr(self.app, "master_password", None)
        entries = load_entries(master_password) if master_password else []

        if not entries:
            container.mount(Static("No hay entradas guardadas o error al cargar.", classes="error"))
            return

        for entry in entries:
            servicio = entry["servicio"]
            usuario = entry["usuario"]
            #debug temporal
            print(f"[DEBUG] Añadiendo botón para {servicio} - {usuario}")

            
            row = Horizontal(
                Vertical(
                    Static(f"Servicio: {servicio}", classes="entry_service", expand=True),
                    Static(f"Usuario: {usuario}", classes="entry_user", expand=True),
                    id="entry_info"
                ),
                Button("Eliminar", id=f"delete_{servicio}__{usuario}", classes="delete_button"),
                classes="entry_row"
                
            )
            container.mount(row)

    def show_confirmation(self, servicio: str, usuario: str):
        confirm_box = self.query_one("#confirmation_box", Vertical)
        confirm_box.remove_children()

        confirm_box.mount(
            Vertical(
                Static(f"¿Eliminar \"{servicio}\"?", classes="confirm_text"),
                Horizontal(
                    Button("Sí", id=f"confirm_delete_{servicio}__{usuario}", classes="confirm_yes"),
                    Button("No", id="cancel_delete", classes="confirm_no")
                )
            )
        )

    def clear_confirmation(self):
        confirm_box = self.query_one("#confirmation_box", Vertical).remove_children()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        print(f"[DEBUG] Botón presionado: {btn_id}")  # Depuración


        if btn_id == "back_button":
            self.app.pop_screen()
            return

        if btn_id.startswith("delete_"):
            raw = btn_id.replace("delete_", "")
            if "__" in raw:
                servicio, usuario = raw.split("__", 1)
                self.show_confirmation(servicio, usuario)
            return

        if btn_id.startswith("confirm_delete_"):
            raw = btn_id.replace("confirm_delete_", "")
            if "__" in raw:
                servicio, usuario = raw.split("__", 1)
                master_password = getattr(self.app, "master_password", None)

                if delete_entry(master_password, servicio, usuario):
                    self.clear_confirmation()
                    self.load_entries()
                else:
                    self.query_one("#confirmation_box", Vertical).mount(
                        Static("❌ Error al eliminar", classes="error")
                    )
            return

        if btn_id == "cancel_delete":
            self.clear_confirmation()
