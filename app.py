import json
from flask import Flask, render_template, request
from library import view_books, add_book, borrow_book, return_book, delete_book
from library import search_books
from library import get_dashboard_data
app = Flask(__name__)

@app.route("/")
def home():
    dashboard = get_dashboard_data()
    return render_template("index.html",books=view_books(), dashboard=dashboard)

@app.route("/search")
def search():
    query = request.args.get("query", "")
    results = search_books(query)
    dashboard = get_dashboard_data()
    
    return render_template("index.html",books=results,dashboard = dashboard)
@app.route("/add", methods=["POST"])
def add_book_route():
    title = request.form["title"]
    author = request.form["author"]
    add_book(title, author)
    dashboard = get_dashboard_data()

    return render_template(
        "index.html",
        books = veiw_books(),
        daashboard = dashboard
    )
@app.route("/borrow/<int:book_id>")
def borrow(book_id):
    borrow_book(book_id)
    dashboard = get_dashboard_data()
    return render_template("index.html", books=view_books(), dashboard=dashboard)


@app.route("/return/<int:book_id>")
def return_b(book_id):
    return_book(book_id)
    dashboard = get_dashboard_data()
    return render_template("index.html", books=view_books(), dashboard=dashboard)


@app.route("/delete/<int:book_id>")
def delete(book_id):
    delete_book(book_id)
    dashboard = get_dashboard_data()
    return render_template("index.html", books=view_books(), dashboard=dashboard)
if __name__ == "__main__":
    app.run(debug=True)
