import os
import pickle
from task1.contact import Contact


def save_to_pickle():
    """Save all contacts using pickle."""
    file_path = get_path_to_file()

    with open(file_path, "wb") as pickle_file_out:
        pickle.dump(obj=Contact.all_contacts, file=pickle_file_out)


def load_from_pickle():
    """Load contacts using pickle."""
    file_path = get_path_to_file()

    Contact.all_contacts.clear()
    with open(file_path, "rb") as pickle_file_in:
        loaded = pickle.load(pickle_file_in)
        Contact.all_contacts.extend(loaded)


def get_path_to_file():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_file_dir, 'files', 'contacts.pkl')
