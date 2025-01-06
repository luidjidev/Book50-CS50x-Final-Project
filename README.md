# Book50 - CS50 Final Project
#### Video Demo: https://youtu.be/PHPOESVm94o
#### Description: Book50 is a web application that helps users manage their reading lists. Users can search for books, organize them into different shelves (Reading, To Read, Read, and Dropped), and keep track of their reading progress.


## Features 📚

* User Authentication
  - Register new accounts
  - Login/Logout functionality
  - Secure password hashing

* Book Search
  - Search by title or author
  - Integration with Google Books API
  - Detailed book information display

* Book Management
  - Add books to different shelves:
    - Currently Reading
    - To Read
    - Already Read
    - Dropped
  - Update book status
  - Remove books from shelves

## Technical Details 🛠️

### Technologies Used
* Python/Flask
* SQLite (with CS50 library)
* HTML/CSS
* Bootstrap
* Google Books API

### Project Structure
project/
├── app.py # Main application file
├── books.db # SQLite database
├── requirements.txt # Project dependencies
├── helpers.py # Helper functions
└── templates/
├── layout.html # Base template
├── index.html # Homepage
├── login.html # Login page
├── register.html # Registration page
├── results.html # Search results
├── shelfs.html # User's bookshelves
└── book.html # Individual book details

## Database Schema 📊
sql
CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL,
hash TEXT NOT NULL
);
CREATE TABLE user_shelves (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
book_id TEXT NOT NULL,
status TEXT NOT NULL,
added_at DATETIME NOT NULL,
FOREIGN KEY(user_id) REFERENCES users(id)
);


## AI Assistance Disclosure 🤖

In the development of this project, I utilized AI assistance (Claude) in the following ways:

1. Code Review and Debugging
   - AI helped identify and fix bugs in the routing logic
   - Assisted with error handling improvements
   - Helped implement proper redirect functionality

2. Feature Implementation
   - Guidance on implementing the Google Books API integration
   - Help with session management
   - Support in creating the shelf management system

3. Code Organization
   - Suggestions for project structure
   - Help with code readability
   - Assistance with best practices

All code was reviewed, understood, and modified by me to ensure complete comprehension of the implementation. The core project idea, design decisions, and final implementation choices were made by me.

## Installation and Setup 🚀

1. Clone the repository
2. Create a virtual environment:
bash
python -m venv .venv
3. Activate the virtual environment:
bash
Windows
.venv\Scripts\activate
macOS/Linux
source .venv/bin/activate
4. Install dependencies:
bash
pip install -r requirements.txt
5. Set up the database:
bash
sqlite3 books.db < schema.sql
6. Run the application:
bash
flask run


## Usage Guide 📖

1. Register a new account or login
2. Use the search function to find books by title or author
3. Add books to your shelves using the dropdown menu
4. Manage your books in different shelves:
   - Track currently reading books
   - Save books for later
   - Mark books as read
   - Move books between shelves

## Future Improvements 🔮

* Add reading progress tracking
* Implement book ratings and reviews
* Add social features (sharing shelves, recommendations)
* Create reading statistics and analytics
* Add book categories and tags

## Credits and Acknowledgments 🙏

* CS50 team for the educational foundation
* Google Books API for book data
* Bootstrap for UI components
* Claude AI for development assistance

## Personal Touch 🎨

[Describe any unique features or personal modifications you added to make the project your own]

## License 📄

This project is part of CS50's Final Project and follows their academic honesty guidelines.