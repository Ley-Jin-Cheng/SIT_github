class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.supplier_id: str = str(supplier_id).strip()
        self.name: str = str(name).strip()
        self.contact_email: str = str(contact_email).strip()

    def display_information(self) -> None:
        """Displays supplier details."""
        print(f"Supplier ID: {self.supplier_id} | Name: {self.name} | Contact: {self.contact_email}")

    def to_dict(self) -> dict:
        """Serializes supplier data for JSON persistence."""
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_email": self.contact_email
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            supplier_id=data.get("supplier_id", ""),
            name=data.get("name", ""),
            contact_email=data.get("contact_email", "")
        )