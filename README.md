# Anime Data Server-Client Application

This project is a server-client application developed as part of the Advanced Mathematics and Programming course. It provides an interface for users to query anime data based on various criteria such as top trending, age rating, airing status, and type. The server handles client connections, authentication, and data serving, while the client offers a graphical interface for user interaction.

## Project Structure

```
project-root
│
├── client
│   └── client.py          # Client application with GUI for user interaction
│
├── data                   # Data files including JSON and images for the application
│   ├── *.json             # JSON files for anime data, login credentials, and query cache
│   ├── *.png              # Pie chart images for different anime sources and genres
│   └── *.csv, *.ipynb     # Additional data analysis notebooks and CSV files
│
├── README.md              # This README file
│
├── server
│   └── server.py          # Server application handling data serving and client management
│
└── test.py                # Test script for additional testing (if applicable)
```

## Features

- **User Authentication:** Login and registration functionality for users.
- **Anime Queries:** Users can search for anime based on top trends, age rating, airing status, and type.
- **Data Visualization:** Pie charts representing distributions of anime by source and genre.
- **Server Management GUI:** Real-time monitoring and management of server operations and client connections.
- **Client GUI:** User-friendly interface for performing searches and viewing results.

## Requirements

- Python 3.x
- PyQt5 for the graphical user interface
- Socket programming for network communication
- Threading for concurrent operations

## Setup and Running

1. **Server Setup:**

   - Navigate to the `server` directory.
   - Run `server.py` to start the server:

     ```
     python server.py
     ```

   - The server GUI will launch, displaying real-time logs and allowing for server management.

2. **Client Setup:**

   - Navigate to the `client` directory.
   - Run `client.py` to start the client application:

     ```
     python client.py
     ```

   - The client GUI will launch, prompting for login or registration before allowing access to search functionalities.

## Data Management

- Data is stored in JSON format in the `data` directory for easy access and manipulation.
