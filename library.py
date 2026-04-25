from datetime import datetime, timedelta
import json 
from datetime import datetime
#print("welcome to the library!")

from datetime import datetime
import os
import json
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, "books.json")
def get_dashboard_data():
    total = len(books)
    borrowed = 0
    available = 0
    overdue = 0

    for book in books:
        if book["status"] == "borrowed" and book.get("due_date"):
            borrowed += 1

            if book.get("due_date"):
                due_date = datetime.strptime(book["due_date"], "%Y-%m-%d")

                if datetime.now() > due_date:
                    overdue += 1
        else:
            available += 1

    return {
        "total": total,
        "borrowed": borrowed,
        "available": available,
        "overdue": overdue
    }
def save_books():
    with open("BOOOKS_JSON", "w") as file:
        json.dump(books, file)
def load_books():
    try:
      with open("BOOKS_JSON", "r") as file:
        return json.load(file)
    except FileNotFoundError:
        return []        
def view_books():
    result = ""

    for book in books:
        book.setdefault("borrow_date", None)
        book.setdefault("due_date", None)
        overdue = False
        fine = 0    
    
        if book["status"] == "borrowed" and book.get("due_date"):
           due_date = datetime.strptime(book["due_date"], "%Y-%m-%d")

           if datetime.now() > due_date:
             overdue = True
             days_late = (datetime.now() - due_date).days
             fine = days_late * 10

        status_color = "green" if book["status"] == "available" else "red"
        border_color = "red" if overdue else "#ccc"

        # ONE card per book
        result += f"""
        <div style="background:white; padding:15px; margin:10px 0; border-radius:8px; border-left:5px solid {border_color}; box-shadow:0 0 5px rgba(0,0,0,0.1);">
            
            <h3>{book['book_title']}</h3>
            <p>by {book['author']}</p>

            <p style="color:{status_color};">
                Status: {book['status']}
            </p>
        """

        # optional info
        if book["status"] == "borrowed" and book.get("due_date"):
            result += f"<p>Due: {book['due_date']}</p>"

        if book["status"] == "borrowed" and fine > 0:
            result += f"<p style='color:red;'>Fine: ₹{fine}</p>"

        # buttons ALWAYS inside same card
        result += f"""
            <a href="/borrow/{book['id']}" style="background:#2196F3; color:white; padding:5px 10px; border-radius:5px;">Borrow</a>

            <a href="/return/{book['id']}" style="background:#FFC107; color:black; padding:5px 10px; border-radius:5px;">Return</a>

            <a href="/delete/{book['id']}" style="background:red; color:white; padding:5px 10px; border-radius:5px;" onclick="return confirm('Are you sure?')">🗑️ Delete</a>

        </div>
        """

    return result
def borrow_book(book_id):
    for book in books:
        if book["id"] == book_id:
            if book["status"] == "available":
                book["status"] = "borrowed"
                today = datetime.now()
                due = today - timedelta(days=3)
                book["borrow_date"] = today.strftime("%Y-%m-%d")
                book["due_date"] = due.strftime("%Y-%m-%d")
                save_books()
                return(f"You have borrowed '{book['book_title']}' by {book['author']}.")
                return
            else:
                return(f"Sorry, '{book['book_title']}' is currently not available.")
    return("Book not found.")
def add_book(book_title, author):
    new_id = max([book["id"] for book in books], default=0) + 1#or use this new_id = len(books) + 1
    new_book = {"id": new_id, "book_title": book_title, "author": author, "status": "available"}
    books.append(new_book)
    save_books()
    return(f"'{book_title}' by {author} has been added to the library.")
def return_book(book_id):
    for book in books:
        if book["id"] == book_id:
            if book["status"] == "borrowed":
                book["status"] = "available"
                book["borrow_date"] = None
                book["due_date"] = None 
                save_books()    
                return(f"You have returned '{book['book_title']}' by {book['author']}.")
            else:
                return(f"'{book['book_title']}' is not currently borrowed.")
                return
    return("Book not found.")
def delete_book(book_id):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            save_books()
            return(f"'{book['book_title']}' by {book['author']} has been deleted from the library.")
    return("Book not found.")
def search_books(query):
    result = "<h2>Search Results:</h2>"

    found_books = [
        book for book in books
        if query.lower() in book["book_title"].lower()
        or query.lower() in book["author"].lower()
    ]

    if found_books:
        for book in found_books:
            result += f"""
            <div>
                <b>{book['book_title']}</b> by {book['author']} ({book['status']})
            </div><br>
            """
    else:
        result += "<p>No books found</p>"

    return result
books=load_books()        

