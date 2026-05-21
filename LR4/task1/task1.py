from task1.contact import Contact
from task1.storage_csv import save_to_csv, load_from_csv
from task1.storage_pickle import save_to_pickle, load_from_pickle
from utils.inputValidate import input_data, input_with_validator

def display_menu():
    print("\nNotebook Menu:")
    print("1. Add contact")
    print("2. Find by last name")
    print("3. Find by phone number")
    print("4. Save to CSV")
    print("5. Load from CSV")
    print("6. Save to Pickle")
    print("7. Load from Pickle")
    print("8. Show all contacts")
    print("0. Exit\n")


def add_contact():
    last_name = input_with_validator("Enter last name: ", str.isalpha)
    phone = input_data("Enter phone: ", str)

    Contact(last_name, phone)
    print("Contact added")


def find_by_letter():
    letter = input_with_validator("Enter the first letter of the last name: ", str.isalpha)

    contacts_founded = Contact.search_by_letter(letter)
    if contacts_founded:
        for contact in contacts_founded:
            print(contact)
    else:
        print("No contacts found")


def find_by_phone():
    phone = input_data("Enter phone number: ", str)
    contact = Contact.search_by_phone(phone)

    if contact:
        print(f"Found: {contact.last_name}")
    else:
        print("Contact not found")


def input_all_contacts():
    Contact.print_all(Contact.all_contacts)


def task1():
    while True:
        display_menu()
        choice = input("Choose an option: ")
        match choice:
            case "1": add_contact()
            case "2": find_by_letter()
            case "3": find_by_phone()
            case "4": save_to_csv()
            case "5": load_from_csv()
            case "6": save_to_pickle()
            case "7": load_from_pickle()
            case "8": input_all_contacts()
            case "0": break
            case _: print("Invalid choice\n")
