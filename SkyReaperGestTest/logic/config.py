import os
from pathlib import Path


APPDATA_PATH = Path(os.getenv("APPDATA") or "system")
SKYREAPER_FOLDER = APPDATA_PATH / "SkyReaperGest"
SKYREAPER_FOLDER.mkdir(parents=True, exist_ok=True)


HASH_PATH = SKYREAPER_FOLDER / "master.hash"
VAULT_PATH = SKYREAPER_FOLDER / "vault.enc"