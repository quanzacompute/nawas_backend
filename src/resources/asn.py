from .prefix import Prefix
from src.db.connection import DBConnection

from flask_restful import Resource


class ASN(Resource):
    pfs = []
    asn = None

    def __init(self):
        asn = self.asn


    ## checks if variable is indeed a prefix, and calls on internal verification function to check integrity
    #    pf        Prefix      prefix to check
    #  
    #  returns:    True if prefix is valid
    def check_prefix(pf):
        if isinstance (pf, Prefix):
            return pf.check()
        else:
            return False

    def add_prefix(pf):
        check_prefix(pf)
        pfs.append(pf)
    
    def remove_prefix(pf):
        check_prefix(pf)
        pfs.remove(pf)


    

