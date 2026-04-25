import json
from flask import Flask, render_template, request, redirect
from library import (
    view_books,
    add_book,
    borrow_book,
    return_book,
    delete_book,
    search_books,
    get_dashboard_data
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template(
        "index.html",
        books=view_books(),
        dashboard=get_dashboard_data()
    )


@app.route("/search")
def search():
    query = request.args.get("query", "")
    results = search_books(query)

    return render_template(
        "index.html",
        books=results,
        dashboard=get_dashboard_data()
    )


@app.route("/add", methods=["POST"])
def add_book_route():
    title = request.form["title"]
    author = request.form["author"]

    add_book(title, author)

    return redirect("/")


@app.route("/borrow/<int:book_id>")
def borrow(book_id):
    borrow_book(book_id)
    return redirect("/")


@app.route("/return/<int:book_id>")
def return_b(book_id):
    return_book(book_id)
    return redirect("/")


@app.route("/delete/<int:book_id>")
def delete(book_id):
    delete_book(book_id)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
