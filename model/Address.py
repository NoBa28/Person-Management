class Address:

    def __init__(self, street, house_num, zip_code, city, country, address_id=None):
        self.address_id = address_id
        self.street = street
        self.house_num = house_num
        self.zip_code = zip_code
        self.city = city
        self.country = country

    def __str__(self):
        return (f"Strasse: {self.street}\n"
                f"Hausnummer: {self.house_num}\n"
                f"Postleitzahl: {self.zip_code}\n"
                f"Stadt: {self.city},\n"
                f"Land: {self.country}\n")

    def __eq__(self, other):
        if not isinstance(other, Address):
            return False
        return (self.street == other.street and
                self.house_num == other.house_num and
                self.zip_code == other.zip_code and
                self.city == other.city and
                self.country == other.country)

    def __hash__(self):
        return hash((self.street,
                     self.house_num,
                     self.zip_code,
                     self.city,
                     self.country))
