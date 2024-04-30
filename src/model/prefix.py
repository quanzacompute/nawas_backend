from src.db.connection import DBConnection

class Prefix():
    id = None
    cidr = None

    ## initialize when reading from database, with an id
    def __init(self, id, cidr):
        id = self.id
        cidr = self.cidr

    ## initialize before adding to database, so without an id
    def __init(self, cidr):
        cidr = self.cidr

    ## verify data integrity, by checking cidr
    # TODO: something with id?
    def check(self):
        return cidr is not None         

