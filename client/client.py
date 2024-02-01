import sys
import json
import socket
import threading
import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QHBoxLayout, QLabel, QApplication, QMainWindow, QPushButton, QLineEdit, QMessageBox, QTableView, QTableWidget, QHeaderView, QAbstractItemView, QTextEdit, QTabWidget, QComboBox
from PyQt5.QtCore import Qt , QByteArray

class LoginWindow(QMainWindow):
    def __init__(self, client_socket):
        super().__init__()
        self.username = None

        # Set window title and size
        self.setWindowTitle("Login")
        self.setGeometry(400, 200, 600, 400)

        # Set background color
        self.setStyleSheet("background-color: #f2f2f2;")

        # Add login label
        self.label = QLabel("Login", self)
        self.label.setGeometry(250, 50, 100, 30)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Add username label and textbox
        self.username_label = QLabel("Username:", self)
        self.username_label.setGeometry(150, 100, 80, 30)
        self.username_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.username_textbox = QLineEdit(self)
        self.username_textbox.setGeometry(250, 100, 200, 30)
        self.username_textbox.setStyleSheet("font-size: 16px; padding: 5px; border-radius: 5px; border: 1px solid #ccc;")

        # Add password label and textbox
        self.password_label = QLabel("Password:", self)
        self.password_label.setGeometry(150, 150, 80, 30)
        self.password_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.password_textbox = QLineEdit(self)
        self.password_textbox.setGeometry(250, 150, 200, 30)
        self.password_textbox.setStyleSheet("font-size: 16px; padding: 5px; border-radius: 5px; border: 1px solid #ccc;")
        self.password_textbox.setEchoMode(QLineEdit.Password)

        # Add login and register buttons
        self.login_button = QPushButton("Login", self)
        self.login_button.setGeometry(200, 220, 100, 40)
        self.login_button.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px; border-radius: 5px; background-color: #4CAF50; color: #fff;")
        self.login_button.clicked.connect(lambda: self.login(client_socket))

        self.register_label = QLabel("Don't have an account?", self)
        self.register_label.setGeometry(190, 280, 160, 30)
        self.register_label.setStyleSheet("font-size: 14px;")

        self.register_button = QPushButton("Register", self)
        self.register_button.setGeometry(360, 280, 80, 40)
        self.register_button.setStyleSheet("font-size: 14px; padding: 5px; border-radius: 5px;background-color: #2196F3; color: #fff;")
        self.register_button.clicked.connect(lambda: self.open_register_window( client_socket))

    def login(self, client_socket):
        username = self.username_textbox.text()
        password = self.password_textbox.text()
        message = {"type": "login", "username": username, "password": password}
        client_socket.send(json.dumps(message).encode())
        response = client_socket.recv(1024).decode("utf8")
        message = json.loads(response)
        if message["status"] == "success":
            # Login successful, show message and open search window
            # QMessageBox.information(self, "Login", "Login successful!")
            self.username = username
            self.search_window = SearchWindow(client_socket, username)
            self.search_window.show()
            self.close()
        else:
            # Login failed, show error message
            QMessageBox.warning(self, "Login", "Invalid username or password.")
            self.username_textbox.setText("")

    def open_register_window(self, client_socket):
        self.register_window = RegisterWindow(client_socket)
        self.register_window.show()
        self.close()

class RegisterWindow(QMainWindow):
    def __init__(self, client_socket):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Register")
        self.setGeometry(400, 200, 600, 400)

        # Set background color
        self.setStyleSheet("background-color: #f2f2f2;")

        # Add registration label
        self.label = QLabel("Registration", self)
        self.label.setGeometry(250, 50, 200, 30)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Add username label and textbox
        self.username_label = QLabel("Username:", self)
        self.username_label.setGeometry(150, 100, 80, 30)
        self.username_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.username_textbox = QLineEdit(self)
        self.username_textbox.setGeometry(250, 100, 200, 30)
        self.username_textbox.setStyleSheet("font-size: 16px; padding: 5px; border-radius: 5px; border: 1px solid #ccc;")

        # Add password label and textbox
        self.password_label = QLabel("Password:", self)
        self.password_label.setGeometry(150, 150, 80, 30)
        self.password_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.password_textbox = QLineEdit(self)
        self.password_textbox.setGeometry(250, 150, 200, 30)
        self.password_textbox.setStyleSheet("font-size: 16px; padding: 5px; border-radius: 5px; border: 1px solid #ccc;")
        self.password_textbox.setEchoMode(QLineEdit.Password)

        # Add register and back buttons
        self.register_button = QPushButton("Register", self)
        self.register_button.setGeometry(200, 220, 100, 40)
        self.register_button.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px; border-radius: 5px; background-color: #2196F3; color: #fff;")
        self.register_button.clicked.connect(lambda: self.register(client_socket))

        self.back_button = QPushButton("Back", self)
        self.back_button.setGeometry(360, 220, 100, 40)
        self.back_button.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px; border-radius: 5px; background-color: #ccc; color: #000;")
        self.back_button.clicked.connect(lambda: self.back(client_socket))


    def register(self, client_socket):
        username = self.username_textbox.text()
        password = self.password_textbox.text()
        message = {"type": "register", "username": username, "password": password}
        client_socket.send(json.dumps(message).encode())
        response = client_socket.recv(1024).decode()
        message = json.loads(response)
        if message["status"] == "success":
            QMessageBox.information(self, "Registration", "Registration successful!")
            # show search window
            self.search_window = SearchWindow(client_socket, username)
            self.search_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Registration", "Username already exists.")
            self.username_textbox.setText("")

    def back(self, client_socket):
        # show login window
        self.login_window = LoginWindow(client_socket)
        self.login_window.show()
        self.close()


class SearchWindow(QMainWindow):
    def __init__(self, client_socket, username):
        super().__init__()
        self.username = username
        self.client_socket = client_socket

        # Set window title and size
        self.setWindowTitle("Anime Search")
        self.setGeometry(400, 200, 800, 900)

        # Set background color
        self.setStyleSheet("background-color: #f2f2f2;")

        # Create tabs
        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(0, 0, 800, 1000)
        self.tabs.setStyleSheet("font-size: 16px;")

        # Create search tab
        self.search_tab = QWidget()
        self.tabs.addTab(self.search_tab, "Search")

        # Add widgets to search tab
        self.search_label = QLabel("Search Anime", self.search_tab)
        self.search_label.setGeometry(50, 50, 200, 30)
        self.search_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Search dropdowns
        self.search_combo = QComboBox(self.search_tab)
        self.search_combo.setGeometry(50, 100, 200, 30)
        self.search_combo.addItems(["Top X trending anime", "Age rating", "Currently airing/finished/not aired yet", "Type"])

        # Top X dropdown
        self.top_combo = QComboBox(self.search_tab)
        self.top_combo.setGeometry(300, 100, 100, 30)
        self.top_combo.addItems(["5", "10", "15", "25"])
        self.top_combo.show()

        # Age rating dropdown
        self.age_combo = QComboBox(self.search_tab)
        self.age_combo.setGeometry(300, 100, 100, 30)
        self.age_combo.addItems(["all_ages","teens", "children","violence", "R+", "none", "hentai"])
        self.age_combo.hide()

        # Currently airing/finished/not aired yet dropdown
        self.airing_combo = QComboBox(self.search_tab)
        self.airing_combo.setGeometry(250, 100, 170, 30)
        self.airing_combo.addItems(["currently_airing", "finished_airing", "not_yet_aired"])
        self.airing_combo.hide()

        # Genre lineedit
        self.genre_lineedit = QLineEdit(self.search_tab)
        self.genre_lineedit.setGeometry(460, 100, 200, 30)
        self.genre_lineedit.hide()

        # Type dropdown
        self.type_combo = QComboBox(self.search_tab)
        self.type_combo.setGeometry(300, 100, 150, 30)
        self.type_combo.addItems(['Manga', 'Visual novel', 'Novel' ,'4-koma manga', 'Original', 'Light novel',
'Web manga' ,'Web novel' ,'Game', 'Music', 'Book' ,'Other' ,'Unknown',
'Picture book', 'Mixed media'])
        self.type_combo.hide()

        # Search button
        self.search_button = QPushButton("Search", self.search_tab)
        self.search_button.setGeometry(680, 100, 100, 30)
        self.search_button.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px; border-radius: 5px; background-color: #4CAF50; color: #fff;")
        self.search_button.clicked.connect(self.search_anime)

        self.result_label = QLabel("Results", self.search_tab)
        self.result_label.setGeometry(50, 150, 100, 30)
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        
        self.result_table = QTableWidget(self.search_tab)
        self.result_table.setGeometry(50, 200, 700, 600)
        #enable scrolling
        # self.result_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.result_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        # Connect search combo to dropdown visibility
        self.search_combo.currentIndexChanged.connect(self.update_dropdown_visibility)
                
        
        # Create profile tab
        self.profile_tab = QWidget()
        self.tabs.addTab(self.profile_tab, "Profile")
        # Add widgets to profile tab
        # username label and a logout button
        self.username_label = QLabel("Hello,\t" + username, self.profile_tab)
        self.username_label.setGeometry(50, 50, 200, 30)
        self.username_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.logout_button = QPushButton("Logout", self.profile_tab)
        self.logout_button.setGeometry(680, 50, 100, 30)
        self.logout_button.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px; border-radius: 5px; background-color: #4CAF50; color: #fff;")
        self.logout_button.clicked.connect(lambda: self.logout(client_socket))


        # Create logs tab
        self.logs_tab = QWidget()
        self.tabs.addTab(self.logs_tab, "server messages")

        # Add widgets to logs tab
        self.logs_label = QLabel("server messages", self.logs_tab)
        self.logs_label.setGeometry(50, 50, 200, 30)
        self.logs_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.logs_text = QTextEdit(self.logs_tab)
        self.logs_text.setGeometry(50, 100, 700, 400)
        self.logs_text.setReadOnly(True)
        
        # Create a thread for listening and alerts
        self.thread = threading.Thread(target=self.listen_and_alert)
        # Set the thread as a daemon so it will automatically be terminated when the main thread exits
        self.thread.daemon = True
        # Start the thread
        self.thread.start()
        
    def listen_and_alert(self):
        import time
        while True:
            # Put your listening code here
            # ...
            # If an alert needs to be shown, use QMetaObject.invokeMethod to call a method on the main thread to show the alert
            
            # Wait for a short period of time before checking for new messages again
            time.sleep(1)
    
        
    def update_dropdown_visibility(self):
            current_index = self.search_combo.currentIndex()
            if current_index == 0:
                self.top_combo.show()
                self.age_combo.hide()
                self.airing_combo.hide()
                self.genre_lineedit.hide()
                self.type_combo.hide()

            elif current_index == 1:
                self.top_combo.hide()
                self.age_combo.show()
                self.airing_combo.hide()
                self.genre_lineedit.hide()
                self.type_combo.hide()

            elif current_index == 2:
                self.top_combo.hide()
                self.age_combo.hide()
                self.airing_combo.show()
                self.genre_lineedit.show()
                self.type_combo.hide()

            elif current_index == 3:
                self.top_combo.hide()
                self.age_combo.hide()
                self.airing_combo.hide()
                self.genre_lineedit.hide()
                self.type_combo.show()
        
    def search_anime(self):
        # Clear previous search results
        self.result_table.clearContents()
        self.result_table.verticalScrollBar().setValue(0)
        

        # Get selected search type
        search_type = self.search_combo.currentText()

        # Get search parameters based on selected type
        if search_type == "Top X trending anime":
            top_param = self.top_combo.currentText()
            params = {"top": top_param}

        elif search_type == "Age rating":
            age_param = self.age_combo.currentText()
            params = {"age_rating": age_param}

        elif search_type == "Currently airing/finished/not aired yet":
            airing_param = self.airing_combo.currentText()
            genre_param = self.genre_lineedit.text()
            params = {"airing": airing_param, "genre": genre_param}

        elif search_type == "Type":
            type_param = self.type_combo.currentText()
            params = {"type": type_param}

        # Send search request to server
        search_request = {"action": "search", "params": params}
        self.client_socket.send(json.dumps(search_request).encode())

      # Receive search results from server
        try:
            self.result_table.clearContents()
            self.result_table.setRowHeight(0, 20)
            self.result_table.setColumnWidth(0, 300)
            self.result_table.setColumnWidth(1, 300)
            search_results = json.loads(self.client_socket.recv(4096).decode())
            
            type = search_results['type']
            originial_search_results = search_results
            has_pictures = False
            try:
                if 'pic' in search_results:
                    has_pictures = True
            except:
                pass

            search_results = search_results["results"]
            # QMessageBox.information(self, 'alert', f'{search_results}')
        
            # QMessageBox.information(self, 'alert', f'{type}')
            if search_results and not has_pictures:
                # Populate table with search results
                
                try:
                    
                    if type == 'top':
                        self.result_table.setRowCount(len(search_results))
                        self.result_table.setColumnCount(2)
                        self.result_table.setHorizontalHeaderLabels(["Rank", "Name"])

                        for i, result in enumerate(search_results):
                            rank_item = QtWidgets.QTableWidgetItem(str(result["Rank"]))
                            name_item = QtWidgets.QTableWidgetItem(result["Name"])

                            #set column width to fit the name item
                            
                            self.result_table.setColumnWidth(1, 20)
                            self.result_table.setColumnWidth(1, 300)
                            
                            self.result_table.setItem(i, 0, rank_item)
                            self.result_table.setItem(i, 1, name_item)
                        self.result_table.verticalScrollBar().setValue(len(search_results))
                        # QMessageBox.information(self, 'alert', f'{search_results}')
                    elif type == 'airing':
                        self.result_table.setRowCount(len(search_results))
                        self.result_table.setColumnCount(2)
                        self.result_table.setHorizontalHeaderLabels(["Title", "Genres"])

                        for i, result in enumerate(search_results):
                            rank_item = QtWidgets.QTableWidgetItem(result["Title"])
                            name_item = QtWidgets.QTableWidgetItem(result["Genres"])
                            self.result_table.setColumnWidth(0, 400)
                            self.result_table.setColumnWidth(1, 300)
                            self.result_table.setItem(i, 0, rank_item)

                            self.result_table.setItem(i, 1, name_item)
                        self.result_table.verticalScrollBar().setValue(len(search_results))
                    elif type == 'age_rating':
                        self.result_table.setRowCount(len(search_results))
                        self.result_table.setColumnCount(2)
                        self.result_table.setHorizontalHeaderLabels(["Title", "Rating"])

                        for i, result in enumerate(search_results):
                            rank_item = QtWidgets.QTableWidgetItem(result["Title"])
                            name_item = QtWidgets.QTableWidgetItem(result["Age Rating"])
                            self.result_table.setColumnWidth(0, 300)
                            self.result_table.setItem(i, 0, rank_item)
                            self.result_table.setItem(i, 1, name_item)
                        self.result_table.verticalScrollBar().setValue(len(search_results))
                except Exception as e:
                    QMessageBox.information(self, 'alert', f'{e}')
                    self.result_table.setRowCount(1)
                    self.result_table.setColumnCount(1)
                    self.result_table.setHorizontalHeaderLabels(["No results found."])

            elif has_pictures:
                

                # create a table with one row and one column
                
                self.result_table.setRowCount(1)
                self.result_table.setColumnCount(1)

                # load an image from a URL
                url = f"https://projectmaths.blob.core.windows.net/pics/{search_results}"
                response = requests.get(url)
                if response.status_code == 200:
                    picture_bytes = response.content
                    pixmap = QPixmap()
                    qbytearray = QByteArray(picture_bytes)
                    pixmap.loadFromData(qbytearray)
                    #reduce the size of the image
                    # pixmap = pixmap.scaled(600, 600, QtCore.Qt.KeepAspectRatio)
                    
                    # create a label widget with the loaded image
                    picture_label = QLabel()
                    picture_label.setPixmap(pixmap)
                    picture_widget = QWidget()
                    layout = QHBoxLayout(picture_widget)
                    layout.addWidget(picture_label)
                    layout.setAlignment(picture_label, QtCore.Qt.AlignCenter)

                    # add the picture widget to the table
                    self.result_table.setRowHeight(0, 600)
                    self.result_table.setColumnWidth(0, 700)
                    self.result_table.setCellWidget(0, 0, picture_widget)


            else:
                # Display "No results found" message
                self.result_table.setRowCount(1)
                self.result_table.setColumnCount(1)
                self.result_table.setHorizontalHeaderLabels(["No results found."])
            
        except Exception as e:
                QMessageBox.information(self, 'alert', f'{e}')
                self.result_table.setRowCount(1)
                self.result_table.setColumnCount(1)
                self.result_table.setHorizontalHeaderLabels(["No results found."])
        

    def display_logs(self, message):
        self.logs_text.append(message)


    def logout(self, client_socket):
        message = {"type": "logout", "username": self.username}
        client_socket.send(json.dumps(message).encode())
        self.close()
        sys.exit(app.exec_())
        

if __name__ == '__main__':
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Get local machine name
        host = socket.gethostname()

            # Define the port on which you want to connect
        port = 6500

            # connect to the server on local computer
        client_socket.connect((host, port))
    
        app = QApplication(sys.argv)
        login_window = LoginWindow(client_socket)
        login_window.show()
        sys.exit(app.exec_())
    except:
        message = {"type": "logout", "username": f'unknown'}
        client_socket.send(json.dumps(message).encode())
        client_socket.close()
        sys.exit(app.exec_())
        
