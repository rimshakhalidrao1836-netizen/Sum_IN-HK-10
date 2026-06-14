import json
import csv
import os
import re

FILE_NAME = "contacts.json"


# =========================
# FILE HANDLING
# =========================
def load_contacts():
    try:
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as file:
                return json.load(file)
    except Exception as e:
        print("Error Loading File:", e)
    return []


def save_contacts(contacts):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(contacts, file, indent=4)
    except Exception as e:
        print("Error Saving File:", e)


# =========================
# VALIDATION
# =========================
def valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


def valid_phone(phone):
    return phone.isdigit() and len(phone) >= 10


# =========================
# ID GENERATOR
# =========================
def generate_id(contacts):
    if not contacts:
        return 1
    return max(contact["ID"] for contact in contacts) + 1


# =========================
# DISPLAY
# =========================
def display_contacts(contact_list):

    if not contact_list:
        print("\nNo Contacts Found.")
        return

    print("\n" + "=" * 120)

    print(
        f"{'ID':<5}"
        f"{'Name':<20}"
        f"{'Phone':<15}"
        f"{'Email':<30}"
        f"{'City':<15}"
        f"{'Company':<20}"
        f"{'Fav':<5}"
    )

    print("=" * 120)

    for c in contact_list:
        print(
            f"{c['ID']:<5}"
            f"{c['Name']:<20}"
            f"{c['Phone']:<15}"
            f"{c['Email']:<30}"
            f"{c['City']:<15}"
            f"{c['Company']:<20}"
            f"{str(c['Favorite']):<5}"
        )

    print("=" * 120)


# =========================
# ADD CONTACT
# =========================
def add_contact(contacts):

    print("\nADD CONTACT")

    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    city = input("City: ").strip()
    company = input("Company: ").strip()

    if not all([name, phone, email, city, company]):
        print("Fields Cannot Be Empty")
        return

    if not valid_email(email):
        print("Invalid Email")
        return

    if not valid_phone(phone):
        print("Invalid Phone")
        return

    contact = {
        "ID": generate_id(contacts),
        "Name": name,
        "Phone": phone,
        "Email": email,
        "City": city,
        "Company": company,
        "Favorite": False
    }

    contacts.append(contact)
    save_contacts(contacts)

    print("Contact Added Successfully")


# =========================
# SEARCH
# =========================
def search_contact(contacts):

    keyword = input(
        "Enter Name / Phone / Email: "
    ).lower()

    result = []

    for c in contacts:
        if (
            keyword in c["Name"].lower()
            or keyword in c["Phone"].lower()
            or keyword in c["Email"].lower()
        ):
            result.append(c)

    display_contacts(result)


# =========================
# FILTER
# =========================
def filter_contacts(contacts):

    print("\n1. City")
    print("2. Company")

    choice = input("Choose Filter: ")

    if choice == "1":

        city = input("City: ").lower()

        result = [
            c for c in contacts
            if c["City"].lower() == city
        ]

        display_contacts(result)

    elif choice == "2":

        company = input("Company: ").lower()

        result = [
            c for c in contacts
            if c["Company"].lower() == company
        ]

        display_contacts(result)

    else:
        print("Invalid Choice")


# =========================
# UPDATE
# =========================
def update_contact(contacts):

    try:
        cid = int(input("Enter ID: "))
    except:
        print("Invalid ID")
        return

    for c in contacts:

        if c["ID"] == cid:

            print("Leave Blank To Skip")

            name = input("New Name: ")
            phone = input("New Phone: ")
            email = input("New Email: ")
            city = input("New City: ")
            company = input("New Company: ")

            if name:
                c["Name"] = name

            if phone:
                if valid_phone(phone):
                    c["Phone"] = phone

            if email:
                if valid_email(email):
                    c["Email"] = email

            if city:
                c["City"] = city

            if company:
                c["Company"] = company

            save_contacts(contacts)

            print("Updated Successfully")
            return

    print("Contact Not Found")


# =========================
# DELETE
# =========================
def delete_contact(contacts):

    try:
        cid = int(input("Enter ID: "))
    except:
        print("Invalid ID")
        return

    for c in contacts:

        if c["ID"] == cid:

            contacts.remove(c)

            save_contacts(contacts)

            print("Deleted Successfully")
            return

    print("Contact Not Found")


# =========================
# FAVORITE
# =========================
def favorite_contact(contacts):

    try:
        cid = int(input("Enter ID: "))
    except:
        print("Invalid ID")
        return

    for c in contacts:

        if c["ID"] == cid:

            c["Favorite"] = not c["Favorite"]

            save_contacts(contacts)

            print("Favorite Updated")
            return

    print("Contact Not Found")


# =========================
# SORT
# =========================
def sort_contacts(contacts):

    sorted_list = sorted(
        contacts,
        key=lambda x: x["Name"].lower()
    )

    display_contacts(sorted_list)


# =========================
# EXPORT CSV
# =========================
def export_csv(contacts):

    with open(
        "contacts.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=contacts[0].keys()
        )

        writer.writeheader()
        writer.writerows(contacts)

    print("Exported To contacts.csv")


# =========================
# MAIN MENU
# =========================
def main():

    contacts = load_contacts()

    while True:

        print("\n")
        print("=" * 40)
        print("CONTACT MANAGEMENT SYSTEM")
        print("=" * 40)

        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Filter Contacts")
        print("5. Update Contact")
        print("6. Delete Contact")
        print("7. Sort A-Z")
        print("8. Favorite Contact")
        print("9. Export CSV")
        print("10. Exit")

        choice = input("\nEnter Choice: ")

        try:

            if choice == "1":
                add_contact(contacts)

            elif choice == "2":
                display_contacts(contacts)

            elif choice == "3":
                search_contact(contacts)

            elif choice == "4":
                filter_contacts(contacts)

            elif choice == "5":
                update_contact(contacts)

            elif choice == "6":
                delete_contact(contacts)

            elif choice == "7":
                sort_contacts(contacts)

            elif choice == "8":
                favorite_contact(contacts)

            elif choice == "9":

                if contacts:
                    export_csv(contacts)
                else:
                    print("No Contacts Available")

            elif choice == "10":

                save_contacts(contacts)

                print("Program Closed")

                break

            else:
                print("Invalid Choice")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()