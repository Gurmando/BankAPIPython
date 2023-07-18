class Address:
    def __init__(self, id, street_number, street_name, city, state, zip):
        self.id = int(id)
        self.street_number = str(street_number)
        self.street_name = str(street_name)
        self.city = str(city)
        self.state = str(state)
        self.zip = str(zip)