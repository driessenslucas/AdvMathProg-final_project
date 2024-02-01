import datetime
import os
import socket
import glob

import numpy as np
import threading
import json
from matplotlib import pyplot as plt
from matplotlib import cm
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QTabWidget, QComboBox, QListWidget

class ServerGUI(QWidget):
    def __init__(self, server):
        super().__init__()

        self.server = server

        # Set window size
        self.setGeometry(50, 50, 800, 600)

        # Create tabs
        self.tab_widget = QTabWidget(self)
        self.log_tab = QWidget()
        self.users_tab = QWidget()
        self.message_tab = QWidget()
        self.stats_tab = QWidget()
        self.user_details_tab = QWidget()  # New tab for user details

        # Add tabs to tab widget and apply styles
        self.tab_widget.addTab(self.log_tab, "Logs")
        self.tab_widget.addTab(self.users_tab, "Logged in Users")
        self.tab_widget.addTab(self.message_tab, "Send Message")
        self.tab_widget.addTab(self.stats_tab, "Query Stats")
        self.tab_widget.addTab(self.user_details_tab, "User Details")  # Add new tab
        self.tab_widget.setStyleSheet(
            "QTabBar::tab:selected { background-color: #4d4d4d; }"  # selected tab background color
            "QTabWidget::pane { border: 1px solid #4d4d4d; }"  # tab border color
        )

        # Log tab
        self.log_window = QTextEdit(self.log_tab)
        self.log_window.setReadOnly(True)
        layout = QVBoxLayout()
        layout.addWidget(self.log_window)
        self.log_tab.setLayout(layout)

        # Users tab
        self.logged_in_users_label = QLabel("Logged in Users", self.users_tab)
        self.logged_in_users_label.setStyleSheet(
            "color: #4d4d4d;"
            "font-size: 20px;"
            "font-weight: bold;"
        )
        self.update_logged_in_users()
        self.user_selector = QComboBox(self.users_tab)
        self.user_selector.setMinimumWidth(200)
        layout = QHBoxLayout()
        layout.addWidget(self.logged_in_users_label)
        layout.addStretch()
        layout.addWidget(self.user_selector)
        layout.setContentsMargins(20, 20, 20, 20)
        self.users_tab.setLayout(layout)

        # Message tab
        # Message tab
        self.message_input = QLineEdit(self.message_tab)
        self.send_button = QPushButton("Send", self.message_tab)
        self.send_button.setStyleSheet("background-color: #008CBA; color: white; border: none; padding: 10px;")
        self.send_button.clicked.connect(self.send_message_to_all_users)
        message_layout = QHBoxLayout()
        message_layout.addWidget(self.user_selector)
        message_layout.addWidget(self.message_input)
        message_layout.addWidget(self.send_button)
        layout = QVBoxLayout()
        layout.addLayout(message_layout)
        self.message_tab.setLayout(layout)

        # Query stats tab
        self.query_stats_list = QListWidget(self.stats_tab)
        self.query_stats_list.setStyleSheet("background-color: #f2f2f2; border: none; padding: 10px;")
        self.update_query_stats()
        layout = QVBoxLayout()
        layout.addWidget(self.query_stats_list)
        self.stats_tab.setLayout(layout)

        # User details tab
        self.user_selector_details = QComboBox(self.user_details_tab)  # Dropdown to select user
        self.user_selector_details.currentIndexChanged.connect(self.update_user_details)
        self.user_selector_details.setStyleSheet("background-color: white; border: 1px solid #008CBA; padding: 5px; border-radius: 5px;")
        self.username_label = QLabel(self.user_details_tab)  # Label to display username
        self.username_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #008CBA; margin-top: 20px;")
        self.email_label = QLabel(self.user_details_tab)  # Label to display email address
        self.email_label.setStyleSheet("font-size: 16px; color: #666; margin-bottom: 20px;")
        layout = QVBoxLayout()
        layout.addWidget(self.user_selector_details)
        layout.addWidget(self.username_label)
        layout.addWidget(self.email_label)
        self.user_details_tab.setLayout(layout)
        self.update_user_selector()


        # Shutdown button and apply styles
        self.shutdown_button = QPushButton("Shutdown Server", self)
        self.shutdown_button.setStyleSheet(
            "background-color: #4d4d4d;"
            "color: white;"
            "padding: 10px 20px;"
            "border-radius: 5px;"
            "font-weight: bold;"
        )
        self.shutdown_button.clicked.connect(self.shutdown_server)

        # Add tab widget and shutdown button to main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.shutdown_button)

        # Set main layout and apply background color
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #f2f2f2;")
        self.setWindowTitle("Server")
        self.show()
        
    def update_query_stats(self):
        """
        Update the query stats tab with the most frequently sought after queries.
        """
        self.query_stats_list.clear()
        query_stats = self.server.get_all_queries()
        for query, frequency in sorted(query_stats.items(), key=lambda x: x[1], reverse=True):
            self.query_stats_list.addItem(f"{query}: {frequency}")

    def update_logged_in_users(self):
        users = ", ".join(self.server.logged_in_users)
        self.logged_in_users_label.setText(f"Logged in users: {users}")


    def append_message(self, message):
        self.log_window.append(message)

    def send_message_to_all_users(self):
        recipient = self.user_selector.currentText()
        message = self.message_input.text()
        if recipient == "All":
            self.server.send_message_to_all(message)
        else:
            self.server.send_message_to_user(recipient, message)
        self.message_input.clear()
        
    def update_user_details(self):
        selected_user = self.user_selector_details.currentText()

        # Find user data by username
        user_data = self.server.get_client_data(selected_user)

        # Display user data
        if user_data:
            username = user_data.get('username')
            email = user_data.get('email')
            if username:
                self.username_label.setText(f"Username: {username}")
                if email:
                    self.email_label.setText(f"Email: {email}")
                else:
                    self.email_label.setText("No email available")
            else:
                self.user_details_label.setText("No username available")
        else:
            self.user_details_label.setText("No user selected")
            
    def update_user_selector(self):
        self.user_selector.clear()
        self.user_selector.addItem("All")
        all_users = self.server.get_all_users()
        self.user_selector_details.addItems(all_users)

    def shutdown_server(self):
        self.server.shutdown_server()
        QApplication.quit()

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.login_data = self.load_login_data()
        self.logged_in_users = []
        self.logged_in_sockets = {}
        self.search_queries = {}
        self.gui = ServerGUI(self)

    def load_login_data(self):
        with open("./data/login_data.json") as f:
            login_data = json.load(f)
        return login_data

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.gui.append_message(f"Server started on {self.host}:{self.port}...")

        while True:
            client_socket, client_address = self.server_socket.accept()
            self.gui.append_message(f"New connection from {client_address[0]}:{client_address[1]}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        try:
            message = client_socket.recv(1024).decode("utf8")
            message = json.loads(message)
            if message["type"] == "login":
                username = message["username"]
                password = message["password"]
                if username in self.login_data and self.login_data[username] == password:
                    response = {"status": "success", "message": "Login successful"}
                    self.logged_in_users.append(username)
                    self.logged_in_sockets[client_socket] = username
                    self.gui.update_logged_in_users()
                   
                    self.gui.append_message(f"{username} logged in")                      
                else:
                    response = {"status": "error", "message": "Invalid username or password"}
                client_socket.send(json.dumps(response).encode("utf8"))
            elif message["type"] == "register":
                username = message["username"]
                password = message["password"]
                if username in self.login_data:
                    response = {"status": "error", "message": "Username already exists"}
                else:
                    self.login_data[username] = password
                    with open("./data/login_data.json", "w") as f:
                        json.dump(self.login_data, f, indent=4)
                    response = {"status": "success", "message": "Registration successful"}
                    self.gui.append_message(f"{username} registered")
                client_socket.send(json.dumps(response).encode("utf8"))
            else:
                response = {"status": "error", "message": "Invalid message type"}
                client_socket.send(json.dumps(response).encode("utf8"))

            #if client is closed, remove from logged in users

            self.listen_to_queries(client_socket)
        except:
            username = self.logged_in_sockets.get(client_socket)
            if username is not None:
                self.logged_in_users.remove(username)
                del self.logged_in_sockets[client_socket]
                self.gui.update_logged_in_users()
                self.gui.append_message(f"{username} disconnected")
                
    def return_age_rating(self,rating):
        # open ./data/{rating}_*.json
        with open(f'./data/age_rating_list{rating}.json') as json_file:
            json_file = json.load(json_file)
        
        return json_file

    def return_Top_anime(self,nr):
        # open ./data/top_anime_list2.json
        nr = int(nr)
        with open('./data/top_anime_list2.json') as json_file:
            json_file = json.load(json_file)
        
        # return the top nr animes
        return json_file[:nr]
    
    def return_airing(self,status):
        # get all files in ./data/ directory that match the pattern "{status}_*.json"
        file_paths = glob.glob(f"./data/{status}_*.json")
        
        
        # iterate over each file and load its contents as JSON
        for file_path in file_paths:
            with open(file_path) as f:
                json_data = json.load(f)
            
        # # limit to 50 results
        # json_data = json_data[:50]
        # return the list of all JSON data
        return json_data
    
    def create_genre_pie_chart(self,source_type=None):
        # open the ./data/Genres_Sources.json file
        with open('./data/Genres_Sources.json') as f:
            data = json.load(f)

        # filter the data by source type if specified
        if source_type:
            data = [item for item in data if item.get('Source') == source_type]

        # create a dictionary to store the count of each genre
        genre_count = {}

        # iterate over each item and count the number of occurrences of each genre
        for item in data:
            genres_str = item.get('Genres', '')
            genres = genres_str.split(',')
            for genre in genres:
                genre = genre.strip()
                if genre:
                    if genre in genre_count:
                        genre_count[genre] += 1
                    else:
                        genre_count[genre] = 1

        # create a list of genre labels and a list of corresponding counts
        labels = list(genre_count.keys())
        counts = list(genre_count.values())

        # create a pie chart
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(counts, labels=labels, startangle=90, autopct='%1.1f%%')
        ax.axis('equal')
        title = 'Pie Chart of Genres'
        if source_type:
            title += f' for {source_type}'
        ax.set_title(title)

        # move the pie chart to the right to make space for the legend
        ax.legend(wedges, labels, title="Genres", loc="center left", bbox_to_anchor=(0.75, 0, 0.5, 1))

        ax.axis('equal')
        ax.set_title(f'Pie Chart of Genres for Source: {source_type}')
        plt.savefig(f'./data/{source_type}_pie_chart.png')
        
        
    def listen_to_queries(self, client):
        client_socket = client
        try:
            resp = client_socket.recv(1024).decode("utf8")
            message = json.loads(resp)
            query = message["params"]
            self.gui.append_message(f"Search query: {query} from {client_socket}")
            
            if 'age_rating' in query:
                # get age rating
                age_rating = query['age_rating']
                # get all movies with age rating
                
                message = {"type": 'age_rating' ,"results": self.return_age_rating(f"{age_rating}")}
                client_socket.send(json.dumps(message).encode("utf8"))
            elif 'top' in query:
                # get the number of top movies
                top = query['top']
                message = {"type": 'top' ,"results": self.return_Top_anime(top)}
                self.gui.append_message(f"{message}")
                client_socket.send(json.dumps(message).encode("utf8"))
            elif "airing" in query:
                # get the status of the anime
                status = query['airing']
                message = {"type": 'airing' ,"results": self.return_airing(status)}
                client_socket.send(json.dumps(message).encode("utf8"))
            elif "type" in query:
                source = query['type']
                # self.create_genre_pie_chart(source)
                message = {"type": 'source' ,"results": f"{source}_pie_chart.png", "pic": True}
                client_socket.send(json.dumps(message).encode("utf8"))
            else:
                message = {"type": 'none' ,"results": "Invalid message type"}
                client_socket.send(json.dumps(message).encode("utf8"))
            
            try:
                new_dict = {}
                # cast query as str
                new_dict[str(query)] = 1
                self.save_queries(new_dict)
                self.gui.update_query_stats()
            except Exception as e:
                self.gui.append_message(f'error with updating queries {e}')
        except Exception as e:
            response = {"status": "error", "message": "Invalid message type"}
            client_socket.send(json.dumps(response).encode("utf8"))
            self.gui.append_message(f"Error in listening to queries {e}")
        finally:
            self.listen_to_queries(client_socket)
        
    def get_client_data(self, username):
        # get data from login_data.json
        with open('./data/login_data.json', 'r') as f:
            data = json.load(f)
        user_data = {'username': username}
        if username in data:
            user_data['password'] = data[username]
        return user_data
    
    def get_all_users(self):
        
        with open('./data/login_data.json', 'r') as f:
            data = json.load(f)
        return list(data.keys())

    def get_all_queries(self):
      # read out json file
        with open('./data/cache.json', 'r') as f:
            data = json.load(f)
        return data

  
    def send_message(self, message, client_socket=None):
        message_data = {"type": "alert", "message": f"{message}"}
        if client_socket:
            client_socket.send(json.dumps(message).encode("utf8"))
        else:
            for socket in self.logged_in_users:
                    
                    socket.send(json.dumps(message_data).encode("utf8"))
                    self.gui.append_message(f"Sending message {message_data} to {socket}")

    def send_message_to_all(self, message):
      for client_socket in self.logged_in_sockets.keys():
            message_data = {"type": "alert", "message": f"{message}"}
            self.gui.append_message(f"Sending message {message_data} to {client_socket}")
            client_socket.send(json.dumps(message_data).encode("utf8"))
            
    def save_queries(self, queries):
        data = self.get_all_queries()
        new_data = queries
        if new_data:
            for key, value in new_data.items():
                if key in data:
                    data[key] += value
                else:
                    data[key] = value

            with open('./data/cache.json', 'w') as f:
                json.dump(data, f, indent=4, sort_keys=True)

    def shutdown_server(self):
      self.server_socket.close()
      self.logged_in_users = []
      self.logged_in_sockets = {}
      self.gui.append_message("Server shut down")

if __name__ == "__main__":
    app = QApplication([])
    server = Server("127.0.0.1", 6500)
    threading.Thread(target=server.start).start()
    app.exec_()
