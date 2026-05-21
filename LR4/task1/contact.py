class PrintableMixin:
    """Mixin to print all contacts passed as an argument."""
    @staticmethod
    def print_all(contacts):
        """Print all contacts passed as a list using their __str__ method."""
        if not contacts:
            print("No data available.")
            return

        print("All contacts:\n")
        for index, contact in enumerate(contacts, 1):
            print(f"{index}.\n Lastname: {contact.last_name}\n Phone: {contact.phone}\n")


class Contact(PrintableMixin):
    """Base class for a contact with last name and phone number."""
    all_contacts = [] # static attribute

    def __init__(self, last_name: str, phone: str): # magic method
        self.last_name = last_name # dynamic attribute
        self.phone = phone # dynamic attribute
        Contact.all_contacts.append(self)

    def __str__(self): # polymorphism / magic method
        return f"{self.last_name}: {self.phone}"

    @property
    def last_name(self) -> str: # getter
        return self._last_name

    @last_name.setter
    def last_name(self, name: str): # setter
        self._last_name = name.title()

    @classmethod
    def search_by_letter(cls, letter: str) -> list:
        return [contact for contact in cls.all_contacts if contact.last_name.upper().startswith(letter.upper())]

    @classmethod
    def search_by_phone(cls, phone: str):
        for contact in cls.all_contacts:
            if contact.phone == phone:
                return contact
        return None


class BusinessContact(Contact, PrintableMixin):
    """Inherited class for business contact"""
    def __init__(self, last_name: str, phone: str, company: str): # magic method / super
        super().__init__(last_name, phone)
        self.company = company

    def __str__(self): # magic method
        return f"{self.last_name} ({self.company}): {self.phone}"