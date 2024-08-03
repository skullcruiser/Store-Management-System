Store Management System
Overview
The Store Management System is a simple desktop application designed for managing inventory in a store. Built using Python with a MySQL database backend and Tkinter for the graphical user interface (GUI), this system provides functionalities for both administrators and employees to interact with store data efficiently.

Features
User Management: Allows administrators to add new users, including creating a default 'admin' user.
Inventory Management: Supports adding, updating, deleting, and listing items in the inventory.
Employee Functionality: Enables employees to search for items and submit item entries with updated quantities.
Date Format Guidance: Provides clear instructions for date entry to ensure data consistency.

Technologies Used
Python: Main programming language.
MySQL: Database management system for storing and retrieving data.
Tkinter: GUI toolkit used for creating the desktop application interface.
mysql-connector-python: Python library for connecting to the MySQL database.

Installation
Clone the Repository:
  git clone https://github.com/yourusername/store-management-system.git
  cd store-management-system
Install Dependencies:
  Ensure you have Python 3.x installed.
  Install the required Python packages:
    pip install mysql-connector-python
Setup MySQL:
  Make sure you have MySQL installed and running.
  Update the connect_db() function in tempCodeRunnerFile.py with your MySQL credentials if necessary.
Run the Application:
  python tempCodeRunnerFile.py
Usage
  Login: Enter a username to log in. The default username admin will provide administrative access.
  Admin Menu: Manage inventory by adding, updating, deleting, or listing items. Add new users as needed.
  Employee Menu: Search for items and submit new inventory entries.

Contributing
Contributions are welcome! If you would like to contribute to this project, please fork the repository and submit a pull request with your changes.

License
This project is licensed under the MIT License - see the LICENSE file for details.
