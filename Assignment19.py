import sqlite3

# Database setup
def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file. """
    conn = sqlite3.connect(db_file)
    return conn

def create_tables(conn):
    """ Create tables for the BookHaven database. """
    with conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
            AuthorID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Bio TEXT
        );
        ''')

        conn.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            BookID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            AuthorID INTEGER,
            Genre TEXT,
            PublicationDate DATE,
            Price REAL NOT NULL,
            StockQuantity INTEGER DEFAULT 0,
            FOREIGN KEY (AuthorID) REFERENCES Authors (AuthorID)
        );
        ''')

        conn.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            Phone TEXT
        );
        ''')

        conn.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
            TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID INTEGER,
            BookID INTEGER,
            TransactionDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            Quantity INTEGER NOT NULL,
            FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID),
            FOREIGN KEY (BookID) REFERENCES Books (BookID)
        );
        ''')

# CRUD operations
def add_author(conn, name, bio):
    """ Add a new author to the database. """
    with conn:
        conn.execute('INSERT INTO Authors (Name, Bio) VALUES (?, ?)', (name, bio))

def add_book(conn, title, author_id, genre, publication_date, price, stock_quantity):
    """ Add a new book to the database. """
    with conn:
        conn.execute('INSERT INTO Books (Title, AuthorID, Genre, PublicationDate, Price, StockQuantity) VALUES (?, ?, ?, ?, ?, ?)', 
                     (title, author_id, genre, publication_date, price, stock_quantity))

def add_customer(conn, name, email, phone):
    """ Add a new customer to the database. """
    with conn:
        conn.execute('INSERT INTO Customers (Name, Email, Phone) VALUES (?, ?, ?)', (name, email, phone))

def add_transaction(conn, customer_id, book_id, quantity):
    """ Record a new transaction. """
    with conn:
        conn.execute('INSERT INTO Transactions (CustomerID, BookID, Quantity) VALUES (?, ?, ?)', 
                     (customer_id, book_id, quantity))

def view_authors(conn):
    """ Retrieve all authors. """
    cursor = conn.execute('SELECT * FROM Authors')
    for row in cursor:
        print(row)

def view_books(conn):
    """ Retrieve all books. """
    cursor = conn.execute('SELECT * FROM Books')
    for row in cursor:
        print(row)

def view_customers(conn):
    """ Retrieve all customers. """
    cursor = conn.execute('SELECT * FROM Customers')
    for row in cursor:
        print(row)

def view_transactions(conn):
    """ Retrieve all transactions. """
    cursor = conn.execute('SELECT * FROM Transactions')
    for row in cursor:
        print(row)

# Main menu for the Library Management System
def main():
    conn = create_connection('bookhaven.db')
    create_tables(conn)

    while True:
        print("\nWelcome to the Library Management System!")
        print("Main Menu:")
        print("1. Author Operations")
        print("2. Book Operations")
        print("3. Customer Operations")
        print("4. Transaction Operations")
        print("5. Quit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            print("\nAuthor Operations:")
            name = input("Enter author's name: ")
            bio = input("Enter author's biography: ")
            add_author(conn, name, bio)
            print("Author added.")

        elif choice == '2':
            print("\nBook Operations:")
            title = input("Enter book title: ")
            author_id = input("Enter author ID: ")
            genre = input("Enter book genre: ")
            publication_date = input("Enter publication date (YYYY-MM-DD): ")
            price = float(input("Enter book price: "))
            stock_quantity = int(input("Enter stock quantity: "))
            add_book(conn, title, author_id, genre, publication_date, price, stock_quantity)
            print("Book added.")

        elif choice == '3':
            print("\nCustomer Operations:")
            name = input("Enter customer's name: ")
            email = input("Enter customer's email: ")
            phone = input("Enter customer's phone: ")
            add_customer(conn, name, email, phone)
            print("Customer added.")

        elif choice == '4':
            print("\nTransaction Operations:")
            customer_id = input("Enter customer ID: ")
            book_id = input("Enter book ID: ")
            quantity = int(input("Enter quantity: "))
            add_transaction(conn, customer_id, book_id, quantity)
            print("Transaction recorded.")

        elif choice == '5':
            break

        else:
            print("Invalid choice. Please try again.")

        # View current records
        print("\nCurrent Records:")
        print("\nAuthors:")
        view_authors(conn)
        print("\nBooks:")
        view_books(conn)
        print("\nCustomers:")
        view_customers(conn)
        print("\nTransactions:")
        view_transactions(conn)

    conn.close()

if __name__ == "__main__":
    main()
