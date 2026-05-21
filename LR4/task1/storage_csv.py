import csv
import os
from task1.contact import Contact

def save_to_csv():
    """Save all contacts to a CSV file."""
    file_path = get_path_to_file()

    with open(file_path, "w", newline='') as file_csv_out:
        writer = csv.writer(file_csv_out)

        for contact in Contact.all_contacts:
            writer.writerow([contact.last_name, contact.phone])


def load_from_csv():
    """Load contacts from a CSV file."""
    file_path = get_path_to_file()

    Contact.all_contacts.clear()
    with open(file_path, newline='') as file_csv_in:
        reader_csv = csv.reader(file_csv_in)

        for row in reader_csv:
            if row:
                Contact(row[0], row[1])

def get_path_to_file():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_file_dir, 'files', 'contacts.csv')
