# Sum_IN-HK-10
PROJECT NO:01
The CLI Contact Management System is a terminal-based application that simulates a real-world mini CRM (Customer Relationship Management) tool. It allows users to add, update, delete, search, and filter contacts — all without needing a database or internet connection.

Built with a clean modular architecture, the system is lightweight, beginner-friendly, and easily extendable for future features.

✨ Features
#	Feature	Description
1	➕ Add Contact	Store name, phone, email, city, category & notes
2	👁️ View All	Display all contacts in a formatted table
3	✏️ Update	Edit any field of an existing contact
4	🗑️ Delete	Remove a contact with confirmation prompt
5	🔍 Smart Search	Search across all fields simultaneously
6	🔽 Advanced Filters	Filter by category, city, or date added
7	📤 Export	Export contacts to CSV or JSON
8	📥 Import	Bulk import contacts from a CSV file
9	📊 Statistics	View contact breakdown by category
10	🔒 Duplicate Check	Warns before saving duplicate entries
🗂️ Project Structure
cli-contact-manager/
│
├── main.py              # App entry point & main menu
├── contacts.py          # CRUD operations
├── search.py            # Search & filter logic
├── storage.py           # File read/write (JSON)
├── export.py            # CSV & JSON export
├── utils.py             # Validators & helpers
├── display.py           # Terminal UI formatting
│
├── data/
│   └── contacts.json    # Auto-generated local database
│
├── exports/             # Exported files go here
├── tests/               # Unit tests
├── requirements.txt
└── README.md
