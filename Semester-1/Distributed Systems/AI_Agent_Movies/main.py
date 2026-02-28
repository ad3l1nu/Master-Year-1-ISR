import sys
import os
from PyQt6.QtWidgets import QApplication
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Încarcă variabilele de mediu din fișierul .env
load_dotenv(os.path.join(current_dir, '.env'))

try:
    from ui.app_gui import AppWindow
except ImportError:
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("app_gui", os.path.join(current_dir, "app_gui.py"))
        if spec and spec.loader:
            app_gui = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(app_gui)
            AppWindow = app_gui.AppWindow
        else:
            raise ImportError("app_gui.py not found")
    except ImportError as e:
        print("❌ EROARE CRITICĂ: Nu pot găsi fișierul 'app_gui.py'!")
        print(f"Detalii eroare: {e}")
        sys.exit(1)

def validate_env_vars():
    """Validează că cheile API necesare sunt setate."""
    
    if "GEMINI_API_KEY" not in os.environ:
        print("❌ EROARE: Cheia GEMINI_API_KEY nu este setată. Configurează fișierul .env")
        sys.exit(1)
    
    if "TMDB_API_KEY" not in os.environ:
        print("❌ EROARE: Cheia TMDB_API_KEY nu este setată. Configurează fișierul .env")
        sys.exit(1)

if __name__ == "__main__":
    validate_env_vars()
    
    app = QApplication(sys.argv)
    
    try:
        window = AppWindow()
        window.show()
        print("✅ Aplicația a pornit cu succes!")
        sys.exit(app.exec())
    except Exception as e:
        print(f"❌ Eroare fatală la pornire: {e}")