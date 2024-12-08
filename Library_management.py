import sqlite3

# Connect to SQLite database (it will create if doesn't exist)
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create tables for books, members, and transactions
def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        book_id INTEGER PRIMARY KEY,
                        title TEXT,
                        author TEXT,
                        isbn TEXT,
                        quantity INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                        member_id INTEGER PRIMARY KEY,
                        name TEXT,
                        email TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        transaction_id INTEGER PRIMARY KEY,
                        member_id INTEGER,
                        book_id INTEGER,
                        issue_date TEXT,
                        return_date TEXT,
                        FOREIGN KEY (member_id) REFERENCES members (member_id),
                        FOREIGN KEY (book_id) REFERENCES books (book_id))''')

# Function to add a book to the library
def add_book(title, author, isbn, quantity):
    cursor.execute('''INSERT INTO books (title, author, isbn, quantity) 
                      VALUES (?, ?, ?, ?)''', (title, author, isbn, quantity))
    conn.commit()

# Function to add a member to the library
def add_member(name, email):
    cursor.execute('''INSERT INTO members (name, email) 
                      VALUES (?, ?)''', (name, email))
    conn.commit()

# Function to issue a book to a member
def issue_book(member_id, book_id, issue_date):
    cursor.execute('SELECT quantity FROM books WHERE book_id = ?', (book_id,))
    book = cursor.fetchone()
    
    if book and book[0] > 0:
        cursor.execute('''INSERT INTO transactions (member_id, book_id, issue_date, return_date) 
                          VALUES (?, ?, ?, ?)''', (member_id, book_id, issue_date, None))
        cursor.execute('UPDATE books SET quantity = quantity - 1 WHERE book_id = ?', (book_id,))
        conn.commit()
        print(f"Book {book_id} issued successfully!")
    else:
        print("Book is not available!")

# Function to return a book
def return_book(transaction_id, return_date):
    cursor.execute('''SELECT book_id FROM transactions WHERE transaction_id = ? AND return_date IS NULL''', (transaction_id,))
    transaction = cursor.fetchone()

    if transaction:
        cursor.execute('''UPDATE transactions SET return_date = ? WHERE transaction_id = ?''', (return_date, transaction_id))
        cursor.execute('UPDATE books SET quantity = quantity + 1 WHERE book_id = ?', (transaction[0],))
        conn.commit()
        print("Book returned successfully!")
    else:
        print("Invalid transaction or the book was already returned.")

# Function to display all books in the library
def display_books():
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    
    print("Books in Library:")
    for book in books:
        print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, ISBN: {book[3]}, Quantity: {book[4]}")

# Function to display all members
def display_members():
    cursor.execute('SELECT * FROM members')
    members = cursor.fetchall()
    
    print("Library Members:")
    for member in members:
        print(f"ID: {member[0]}, Name: {member[1]}, Email: {member[2]}")

# Main function to interact with the user
def main():
    create_tables()

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Add Member")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Display Books")
        print("6. Display Members")
        print("7. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            quantity = int(input("Enter book quantity: "))
            add_book(title, author, isbn, quantity)
        
        elif choice == '2':
            name = input("Enter member name: ")
            email = input("Enter member email: ")
            add_member(name, email)
        
        elif choice == '3':
            member_id = int(input("Enter member ID: "))
            book_id = int(input("Enter book ID to issue: "))
            issue_date = input("Enter issue date (YYYY-MM-DD): ")
            issue_book(member_id, book_id, issue_date)
        
        elif choice == '4':
            transaction_id = int(input("Enter transaction ID to return: "))
            return_date = input("Enter return date (YYYY-MM-DD): ")
            return_book(transaction_id, return_date)
        
        elif choice == '5':
            display_books()
        
        elif choice == '6':
            display_members()
        
        elif choice == '7':
            print("Exiting system...")
            break
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()

# Close the database connection when done
conn.close()
