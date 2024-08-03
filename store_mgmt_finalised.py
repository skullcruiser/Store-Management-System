import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to MySQL server (without specifying a database initially)
def connect_db(server_only=False):
    if server_only:
        return mysql.connector.connect(
            host="localhost",
            user="root",  # replace with your MySQL username
            password="admin"  # replace with your MySQL password
        )
    return mysql.connector.connect(
        host="localhost",
        user="root",  # replace with your MySQL username
        password="admin",  # replace with your MySQL password
        database="store_management"
    )

# Function to create the database if it doesn't exist
def create_database():
    db = connect_db(server_only=True)
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS store_management")
    db.commit()
    db.close()

# Function to initialize the database and create tables if they don't exist
def init_db():
    create_database()
    db = connect_db()
    cursor = db.cursor()

    # Create tables if they don't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        item_name VARCHAR(255) PRIMARY KEY,
        item_price DECIMAL(10, 2),
        item_quantity INT,
        item_category VARCHAR(255),
        item_date DATE,
        item_remarks TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users 
    (username VARCHAR(255) PRIMARY KEY)
    """)

    # Check if 'admin' user exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        # Insert 'admin' user if it doesn't exist
        cursor.execute("INSERT INTO users (username) VALUES ('admin')")
        db.commit()

    db.close()

# Function to load users from the database
def load_users():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT username FROM users")
    users = set(row[0] for row in cursor.fetchall())
    db.close()
    return users

# Function to save a new user to the database
def save_user(username):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
    db.commit()
    db.close()

# Function to display the admin menu
def admin_menu():
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Menu")
    admin_window.geometry("650x500")
    admin_window.config(bg="#f0f0f0")

    def add_item():
        item_name = entry_item_name.get()
        item_price = entry_item_price.get()
        item_quantity = entry_item_quantity.get()
        item_category = entry_item_category.get()
        item_date = entry_date.get()
        item_remarks = entry_remarks.get()

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO items (item_name, item_price, item_quantity, item_category, item_date, item_remarks) VALUES (%s, %s, %s, %s, %s, %s)",
                       (item_name, item_price, item_quantity, item_category, item_date, item_remarks))
        db.commit()
        db.close()

        messagebox.showinfo("Add Item", "Item added successfully!")
        clear_entries()

    def delete_item():
        item_name = entry_item_name.get()

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM items WHERE item_name = %s", (item_name,))
        db.commit()
        db.close()

        if cursor.rowcount > 0:
            messagebox.showinfo("Delete Item", "Item deleted successfully!")
        else:
            messagebox.showinfo("Delete Item", "Item not found!")
        clear_entries()

    def update_item():
        item_name = entry_item_name.get()

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
        UPDATE items SET
        item_price = %s,
        item_quantity = %s,
        item_category = %s,
        item_date = %s,
        item_remarks = %s
        WHERE item_name = %s
        """, (entry_item_price.get(), entry_item_quantity.get(), entry_item_category.get(), entry_date.get(), entry_remarks.get(), item_name))
        db.commit()
        db.close()

        if cursor.rowcount > 0:
            messagebox.showinfo("Update Item", "Item updated successfully!")
        else:
            messagebox.showinfo("Update Item", "Item not found!")
        clear_entries()

    def list_items():
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        db.close()

        if items:
            items_str = "\n".join([f"Name: {row[0]}, Price: {row[1]}, Quantity: {row[2]}, Category: {row[3]}, Date: {row[4]}, Remarks: {row[5]}" for row in items])
            messagebox.showinfo("Items List", items_str)
        else:
            messagebox.showinfo("Items List", "No items found!")

    def add_user():
        new_user = entry_new_user.get()
        if new_user:
            save_user(new_user)
            messagebox.showinfo("Add User", "User added successfully!")
            entry_new_user.delete(0, tk.END)
        else:
            messagebox.showerror("Add User", "Please enter a username")

    def clear_entries():
        entry_item_name.delete(0, tk.END)
        entry_item_price.delete(0, tk.END)
        entry_item_quantity.delete(0, tk.END)
        entry_item_category.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        entry_remarks.delete(0, tk.END)

    # Create and place labels and entries in grid
    labels = ["Item Name", "Item Price", "Item Quantity", "Item Category", "Date (YYYY-MM-DD)", "Remarks"]
    entries = {}
    for i, label in enumerate(labels):
        tk.Label(admin_window, text=label, bg="#f0f0f0").grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
        entry = tk.Entry(admin_window)
        entry.grid(row=i, column=1, padx=10, pady=5, sticky=tk.W)
        entries[label] = entry

    entry_item_name = entries["Item Name"]
    entry_item_price = entries["Item Price"]
    entry_item_quantity = entries["Item Quantity"]
    entry_item_category = entries["Item Category"]
    entry_date = entries["Date (YYYY-MM-DD)"]
    entry_remarks = entries["Remarks"]

    tk.Button(admin_window, text="Add Item", command=add_item, bg="#4CAF50", fg="white", relief=tk.RAISED).grid(row=len(labels), column=0, padx=10, pady=5)
    tk.Button(admin_window, text="Delete Item", command=delete_item, bg="#F44336", fg="white", relief=tk.RAISED).grid(row=len(labels), column=1, padx=10, pady=5)
    tk.Button(admin_window, text="Update Item", command=update_item, bg="#FFC107", fg="black", relief=tk.RAISED).grid(row=len(labels)+1, column=0, padx=10, pady=5)
    tk.Button(admin_window, text="List Items", command=list_items, bg="#2196F3", fg="white", relief=tk.RAISED).grid(row=len(labels)+1, column=1, padx=10, pady=5)
    tk.Button(admin_window, text="Clear", command=clear_entries, bg="#9E9E9E", fg="white", relief=tk.RAISED).grid(row=len(labels)+2, column=0, columnspan=2, padx=10, pady=5)

    tk.Label(admin_window, text="New Username", bg="#f0f0f0").grid(row=len(labels)+3, column=0, padx=10, pady=5, sticky=tk.W)
    entry_new_user = tk.Entry(admin_window)
    entry_new_user.grid(row=len(labels)+3, column=1, padx=10, pady=5, sticky=tk.W)
    tk.Button(admin_window, text="Add User", command=add_user, bg="#4CAF50", fg="white", relief=tk.RAISED).grid(row=len(labels)+4, column=0, columnspan=2, padx=10, pady=5)

# Function to display the employee menu
def employee_menu(username):
    employee_window = tk.Toplevel(root)
    employee_window.title(f"Employee Menu - {username}")
    employee_window.geometry("650x400")
    employee_window.config(bg="#f0f0f0")

    def search_item():
        item_name = entry_item_name.get()

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM items WHERE item_name = %s", (item_name,))
        item = cursor.fetchone()
        db.close()

        if item:
            item_str = f"Name: {item[0]}, Price: {item[1]}, Quantity: {item[2]}, Category: {item[3]}, Date: {item[4]}, Remarks: {item[5]}"
            messagebox.showinfo("Item Found", item_str)
        else:
            messagebox.showinfo("Search Item", "Item not found!")
        entry_item_name.delete(0, tk.END)

    def submit_item():
        item_name = entry_item_name.get()
        item_quantity = int(entry_item_quantity.get())
        item_date = entry_date.get()
        item_remarks = entry_remarks.get()

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT item_quantity FROM items WHERE item_name = %s", (item_name,))
        item = cursor.fetchone()

        if item:
            new_quantity = item[0] + item_quantity
            cursor.execute("UPDATE items SET item_quantity = %s, item_date = %s, item_remarks = %s WHERE item_name = %s",
                           (new_quantity, item_date, item_remarks, item_name))
            db.commit()
        else:
            cursor.execute("INSERT INTO items (item_name, item_quantity, item_date, item_remarks) VALUES (%s, %s, %s, %s)",
                           (item_name, item_quantity, item_date, item_remarks))
            db.commit()

        db.close()
        messagebox.showinfo("Submit Item", "Item submitted successfully!")
        clear_entries()

    def clear_entries():
        entry_item_name.delete(0, tk.END)
        entry_item_quantity.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        entry_remarks.delete(0, tk.END)

    # Create and place labels and entries in grid
    labels = ["Item Name", "Item Quantity", "Date (YYYY-MM-DD)", "Remarks"]
    entries = {}
    for i, label in enumerate(labels):
        tk.Label(employee_window, text=label, bg="#f0f0f0").grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
        entry = tk.Entry(employee_window)
        entry.grid(row=i, column=1, padx=10, pady=5, sticky=tk.W)
        entries[label] = entry

    entry_item_name = entries["Item Name"]
    entry_item_quantity = entries["Item Quantity"]
    entry_date = entries["Date (YYYY-MM-DD)"]
    entry_remarks = entries["Remarks"]

    tk.Button(employee_window, text="Search Item", command=search_item, bg="#4CAF50", fg="white", relief=tk.RAISED).grid(row=len(labels), column=0, padx=10, pady=5)
    tk.Button(employee_window, text="Submit Item", command=submit_item, bg="#2196F3", fg="white", relief=tk.RAISED).grid(row=len(labels), column=1, padx=10, pady=5)
    tk.Button(employee_window, text="Clear", command=clear_entries, bg="#9E9E9E", fg="white", relief=tk.RAISED).grid(row=len(labels)+1, column=0, columnspan=2, padx=10, pady=5)

# Main login function
def login():
    username = entry_username.get()

    if username in load_users():
        if username == "admin":
            admin_menu()
        else:
            employee_menu(username)
        login_window.withdraw()
    else:
        messagebox.showerror("Login Failed", "Invalid username")

# Initialize the database
init_db()

# Main application window
root = tk.Tk()
root.title("Store Management System")
root.geometry("300x150")
root.config(bg="#e0e0e0")

login_window = tk.Frame(root, bg="#e0e0e0")
login_window.pack(padx=20, pady=20)

tk.Label(login_window, text="Username", bg="#e0e0e0").pack(pady=(0, 10))
entry_username = tk.Entry(login_window)
entry_username.pack(pady=(0, 10))

tk.Button(login_window, text="Login", command=login, width=20, bg="#4CAF50", fg="white", relief=tk.RAISED).pack(pady=10)

root.mainloop()
