
from src.model.tenant import TenantList, TenantByID, TenantByName
from src.model.asn import ASNList, ASNListByTenant, ASNByASN
from src.model.prefix import PrefixList, PrefixByASN, PrefixByID 


## Register resources into the api
def initUrls(api):
    #tenant
    api.add_resource(TenantList, "/tenant/")
    api.add_resource(TenantByID, "/tenant/<int:id>")
    api.add_resource(TenantByName, "/tenant/name/<string:name>")
    
    #asn
    api.add_resource(ASNList, "/asn/")
    api.add_resource(ASNByASN, "/asn/<int:asn>")
    
    #prefix
    api.add_resource(PrefixList, "/prefix/")
    api.add_resource(PrefixByID, "/prefix/<int:id>")
