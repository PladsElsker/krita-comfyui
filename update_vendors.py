import shutil
import sys
from pathlib import Path


def _update_vendors_func(venv_dir: str = "venv", plugin_dir: str = str(Path("pykrita") / "comfyui"), clean: bool = True, ignore_list=[]):
    base = Path(__file__).resolve().parent
    venv_site = base / venv_dir / "Lib" / "site-packages"

    if not venv_site or not venv_site.exists():
        print(f"[!] Could not locate site-packages inside {venv_dir}")
        sys.exit(1)

    vendor_dir = base / plugin_dir / "vendor"

    if clean and vendor_dir.exists():
        shutil.rmtree(vendor_dir)

    vendor_dir.mkdir(parents=True, exist_ok=True)

    print(f"Copying from {venv_site}")
    for item in venv_site.iterdir():
        name = item.name
        
        if any(
            name.startswith(prefix.rstrip("*")) or name.endswith(suffix.lstrip("*"))
            for prefix in ignore_list 
            for suffix in ignore_list
        ):
            continue

        if name.endswith((".dist-info", ".data", "__pycache__")):
            continue

        dest = vendor_dir / name

        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)

    print(f"Vendor folder updated: {vendor_dir}")


def update_vendors():
    _update_vendors_func(ignore_list=["pip", "watchdog", "PyQt5"])


if __name__ == "__main__":
    update_vendors()
