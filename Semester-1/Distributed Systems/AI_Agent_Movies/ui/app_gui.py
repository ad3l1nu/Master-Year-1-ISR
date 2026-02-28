import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QStackedWidget, QTextBrowser, QMessageBox)
from PyQt6.QtCore import QObject, QThread, pyqtSignal, Qt
from datetime import datetime

try:
    from services.gemini_service import GeminiService
    from services.movie_service import MovieService, MovieParser
    from services.firebase_service import FirebaseService
except ImportError as e:
    print(f"❌ Eroare import servicii: {e}")
    print("Verifică dacă ai creat fișierul gol '__init__.py' în folderul '/services'!")

class ApiWorker(QObject):
    finished = pyqtSignal()
    auth_success = pyqtSignal(dict)
    auth_error = pyqtSignal(str)
    openai_result_ready = pyqtSignal(object)
    
    movie_data_ready = pyqtSignal(dict, dict)
    
    chat_error = pyqtSignal(str)

    def __init__(self, task, **kwargs):
        super().__init__()
        self.task = task
        self.kwargs = kwargs

    def run(self):
        try:
            if self.task == "sign_in":
                result = self.kwargs['service'].sign_in(self.kwargs['email'], self.kwargs['password'])
                if "error" in result: self.auth_error.emit(result["error"])
                else: self.auth_success.emit(result)
            elif self.task == "sign_up":
                result = self.kwargs['service'].sign_up(self.kwargs['email'], self.kwargs['password'])
                if "error" in result: self.auth_error.emit(result["error"])
                else: self.auth_success.emit(result)
            
            elif self.task == "chat":
                result = self.kwargs['gemini_service'].interpret_user_request(self.kwargs['user_input'])
                
                if isinstance(result, dict) and 'search_query' in result:
                    movie_data = self.kwargs['movie_service'].search_movie(result['search_query'])
                    if movie_data:
                        self.movie_data_ready.emit({'results': movie_data}, result)
                    else:
                        self.chat_error.emit("Nu am găsit niciun film potrivit.")
                else:
                    self.openai_result_ready.emit(result)

        except Exception as e:
            error_msg = f"Eroare: {e}"
            if self.task in ["sign_in", "sign_up"]: self.auth_error.emit(error_msg)
            else: self.chat_error.emit(error_msg)
        finally:
            self.finished.emit()

class LoginWidget(QWidget):
    go_to_signup = pyqtSignal()
    continue_as_guest = pyqtSignal()
    login_attempt = pyqtSignal(str, str)
    def __init__(self):
        super().__init__(); self.init_ui()
    def init_ui(self):
        self.setStyleSheet("background-color: #343541; color: white; font-size: 14px;"); layout = QVBoxLayout(self); layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.email_input = QLineEdit(); self.email_input.setPlaceholderText("Email"); self.password_input = QLineEdit(); self.password_input.setPlaceholderText("Parolă"); self.password_input.setEchoMode(QLineEdit.EchoMode.Password); login_button = QPushButton("Autentificare"); login_button.clicked.connect(self.on_login); self.error_label = QLabel(""); self.error_label.setStyleSheet("color: #ff6b6b;"); guest_button = QPushButton("Continuă ca oaspete"); guest_button.setStyleSheet("border: none; color: #ACACBE;"); guest_button.setCursor(Qt.CursorShape.PointingHandCursor); guest_button.clicked.connect(self.continue_as_guest.emit); signup_label = QLabel("Nu ai cont? <a href='signup' style='color: #19C37D; text-decoration: none;'>Înregistrează-te</a>"); signup_label.setOpenExternalLinks(False); signup_label.linkActivated.connect(lambda: self.go_to_signup.emit())
        for widget in [self.email_input, self.password_input, login_button, self.error_label, guest_button, signup_label]: widget.setFixedWidth(300); layout.addWidget(widget)
    def on_login(self):
        email = self.email_input.text().strip(); password = self.password_input.text().strip()
        if email and password: self.login_attempt.emit(email, password); self.error_label.setText("Autentificare în curs...")
        else: self.error_label.setText("Te rog completează ambele câmpuri.")

class SignUpWidget(QWidget):
    go_to_login = pyqtSignal()
    signup_attempt = pyqtSignal(str, str)
    def __init__(self):
        super().__init__(); self.init_ui()
    def init_ui(self):
        self.setStyleSheet("background-color: #343541; color: white; font-size: 14px;"); layout = QVBoxLayout(self); layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.email_input = QLineEdit(); self.email_input.setPlaceholderText("Email"); self.password_input = QLineEdit(); self.password_input.setPlaceholderText("Parolă (minim 6 caractere)"); self.password_input.setEchoMode(QLineEdit.EchoMode.Password); self.confirm_password_input = QLineEdit(); self.confirm_password_input.setPlaceholderText("Confirmă parola"); self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password); signup_button = QPushButton("Înregistrare"); signup_button.clicked.connect(self.on_signup); self.error_label = QLabel(""); self.error_label.setStyleSheet("color: #ff6b6b;"); login_label = QLabel("Ai deja cont? <a href='login' style='color: #19C37D; text-decoration: none;'>Autentifică-te</a>"); login_label.setOpenExternalLinks(False); login_label.linkActivated.connect(lambda: self.go_to_login.emit())
        for widget in [self.email_input, self.password_input, self.confirm_password_input, signup_button, self.error_label, login_label]: widget.setFixedWidth(300); layout.addWidget(widget)
    def on_signup(self):
        email = self.email_input.text().strip(); password = self.password_input.text().strip(); confirm = self.confirm_password_input.text().strip()
        if password != confirm: self.error_label.setText("Parolele nu se potrivesc."); return
        if len(password) < 6: self.error_label.setText("Parola trebuie să aibă minim 6 caractere."); return
        if email and password: self.signup_attempt.emit(email, password); self.error_label.setText("Înregistrare în curs...")
        else: self.error_label.setText("Te rog completează toate câmpurile.")

class ChatWidget(QWidget):
    conversation_updated = pyqtSignal()
    logout_requested = pyqtSignal()
    login_requested = pyqtSignal()

    def __init__(self, gemini_service, movie_service):
        super().__init__()
        self.gemini_service = gemini_service
        self.movie_service = movie_service
        self.conversation_history = []
        self.init_ui()
    
    def get_conversation_history(self): 
        return self.conversation_history
    
    def clear_history(self): 
        self.conversation_history = [] 
        self.chat_display.clear()
    
    def load_conversation_history(self, history: list):
        self.clear_history()
        # Actualizăm lista internă
        self.conversation_history = history
        
        # Reafișăm mesajele fără să le salvăm din nou
        for message in history:
            content = message.get("content", "")
            # Adăugăm direct în display fără a apela append_message cu save=True
            self.display_html_message(content)
            
        self.display_html_message("<div class='bot_message'>🤖 Bună! Istoricul conversației a fost încărcat.</div>")

    def init_ui(self):
        self.setStyleSheet("background-color: #343541;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Header
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        
        self.login_signup_button = QPushButton("Log in / Sign up")
        self.login_signup_button.setFixedWidth(120)
        self.login_signup_button.clicked.connect(self.login_requested.emit)
        header_layout.addWidget(self.login_signup_button)

        self.logout_button = QPushButton("Deconectare")
        self.logout_button.setFixedWidth(100)
        self.logout_button.clicked.connect(self.logout_requested.emit)
        header_layout.addWidget(self.logout_button)
        
        layout.addLayout(header_layout)

        # Chat Area
        self.chat_display = QTextBrowser()
        self.chat_display.setOpenExternalLinks(True)
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Input Area
        input_container = QWidget()
        input_container.setStyleSheet("background-color: #40414F; border-radius: 18px;")
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Scrie un mesaj... (ex: 'Filme de comedie 2024')")
        self.input_field.setMinimumHeight(40)
        self.input_field.setStyleSheet("QLineEdit { background-color: transparent; color: #FFFFFF; border: none; padding-left: 16px; font-size: 14px; }")
        self.input_field.returnPressed.connect(self.on_send_message)
        
        send_button = QPushButton("➤")
        send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        send_button.setFixedSize(36, 36)
        send_button.setStyleSheet("QPushButton { background-color: transparent; color: #ACACBE; border: none; font-size: 20px; font-weight: bold; } QPushButton:hover { color: #FFFFFF; }")
        send_button.clicked.connect(self.on_send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_button, 0, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(input_container)

    def on_send_message(self):
        user_text = self.input_field.text().strip()
        if not user_text: return
        
        self.append_message(f"<div class='user_message'><div class='user_message_content'>{user_text}</div></div>")
        self.input_field.clear()
        
        self.append_message("<div class='bot_message'><i>🧠 Mă gândesc...</i></div>", save=False)
        QApplication.processEvents()
        
        self.thread = QThread()
        self.worker = ApiWorker("chat", gemini_service=self.gemini_service, movie_service=self.movie_service, user_input=user_text)
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        
        # Conectăm semnalele (REPARAT flight -> movie)
        self.worker.openai_result_ready.connect(self.handle_text_result)
        self.worker.movie_data_ready.connect(self.display_movie_results)
        self.worker.chat_error.connect(self.display_error)
        
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def handle_text_result(self, result):
        self.remove_last_message() # Scoatem "Ma gandesc..."
        if isinstance(result, str): 
            self.append_message(f"<div class='bot_message'>{result}</div>")

    def display_movie_results(self, movie_data, search_params):
        self.remove_last_message()
        html_output = MovieParser.process_and_format_html(movie_data.get('results', []))
        self.append_message(f"<div class='bot_message'>{html_output}</div>")

    def display_error(self, message):
        self.remove_last_message()
        self.append_message(f"<div class='bot_message' style='color: #ff6b6b;'><b>Eroare:</b> {message}</div>")

    def append_message(self, html_content, save=True):
        # 1. Adăugăm în UI
        self.display_html_message(html_content)
        
        # 2. Salvăm în istoric și emitem semnal
        if save:
            role = "user" if "user_message" in html_content else "assistant"
            self.conversation_history.append({
                "role": role, 
                "content": html_content, 
                "timestamp": datetime.now().isoformat()
            })
            self.conversation_updated.emit()

    def display_html_message(self, html_content):
        # Stiluri CSS Inline
        full_html = f"""
        <html><head><style>
            p {{ margin: 0; padding: 0; }} 
            .user_message {{ margin-bottom: 15px; text-align: right; }} 
            .user_message_content {{ background-color: #19C37D; color: white; padding: 10px; border-radius: 15px 15px 0 15px; display: inline-block; text-align: left; max-width: 80%; }} 
            .bot_message {{ margin-bottom: 15px; background-color: #444654; padding: 10px; border-radius: 15px; }} 
            a {{ color: #19C37D; text-decoration: none; }} 
        </style></head><body>{html_content}</body></html>
        """
        self.chat_display.append(full_html)

    def remove_last_message(self):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.select(cursor.SelectionType.BlockUnderCursor)
        cursor.removeSelectedText()
        cursor.deletePreviousChar()
        self.chat_display.setTextCursor(cursor)

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Movie Assistant")
        self.resize(500, 700)
        self.current_user = None
        
        try:
            from services.firebase_service import FirebaseService
            from services.gemini_service import GeminiService
            from services.movie_service import MovieService
            
            self.firebase_service = FirebaseService()
            self.gemini_service = GeminiService()
            self.movie_service = MovieService()
        except Exception as e:
            QMessageBox.critical(self, "Eroare la Inițializare", f"Aplicația nu a putut porni:\n{e}"); sys.exit(1)
            return

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login_screen = LoginWidget()
        self.signup_screen = SignUpWidget()
        self.chat_screen = ChatWidget(self.gemini_service, self.movie_service)

        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.signup_screen)
        self.stacked_widget.addWidget(self.chat_screen)

        # Conectări
        self.login_screen.go_to_signup.connect(lambda: self.stacked_widget.setCurrentWidget(self.signup_screen))
        self.login_screen.continue_as_guest.connect(self.start_guest_session)
        self.login_screen.login_attempt.connect(lambda email, password: self.handle_auth("sign_in", email, password))
        
        self.signup_screen.go_to_login.connect(lambda: self.stacked_widget.setCurrentWidget(self.login_screen))
        self.signup_screen.signup_attempt.connect(lambda email, password: self.handle_auth("sign_up", email, password))

        self.chat_screen.conversation_updated.connect(self.save_current_conversation)
        self.chat_screen.logout_requested.connect(self.logout)
        self.chat_screen.login_requested.connect(self.go_to_login_screen)

    def handle_auth(self, task, email, password):
        self.thread = QThread()
        self.worker = ApiWorker(task, service=self.firebase_service, email=email, password=password)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        
        self.worker.auth_success.connect(self.start_user_session)
        
        error_label = self.login_screen.error_label if task == "sign_in" else self.signup_screen.error_label
        self.worker.auth_error.connect(error_label.setText)
        
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def start_user_session(self, user_data):
        self.current_user = user_data
        print(f"Autentificat: {user_data.get('email')}")
        self.stacked_widget.setCurrentWidget(self.chat_screen)
        
        self.chat_screen.logout_button.show()
        self.chat_screen.login_signup_button.hide()
        
        # Încărcare istoric
        history = self.firebase_service.load_conversation(self.current_user['localId'])
        self.chat_screen.load_conversation_history(history)

    def start_guest_session(self):
        self.current_user = None
        self.chat_screen.clear_history()
        self.stacked_widget.setCurrentWidget(self.chat_screen)
        self.chat_screen.logout_button.hide()
        self.chat_screen.login_signup_button.show()
        self.chat_screen.append_message("<div class='bot_message'><i>Sunteți în modul oaspete. Istoricul nu se salvează.</i></div>", save=False)

    def save_current_conversation(self):
        if self.current_user:
            history = self.chat_screen.get_conversation_history()
            self.firebase_service.save_conversation(self.current_user['localId'], history)

    def go_to_login_screen(self):
        self.stacked_widget.setCurrentWidget(self.login_screen)

    def logout(self):
        self.current_user = None
        self.login_screen.email_input.clear()
        self.login_screen.password_input.clear()
        self.login_screen.error_label.setText("Deconectat cu succes.")
        self.stacked_widget.setCurrentWidget(self.login_screen)