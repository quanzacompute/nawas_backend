
from models.tenant import TenantRoot, TenantById, TenantByName
from models.asn import ASNRoot, ASNByASN
from models.prefix import PrefixRoot, PrefixById


## Register resources into the api
def loadUrls(api):
    #tenant
    api.add_resource(TenantRoot, "/tenant/")
    api.add_resource(TenantById, "/tenant/<int:id>")
    api.add_resource(TenantByName, "/tenant/name/<string:name>")
    
    #asn
    api.add_resource(ASNRoot, "/asn/")
    api.add_resource(ASNByASN, "/asn/<int:asn>")
    
    #prefix
    api.add_resource(PrefixRoot, "/prefix/")
    api.add_resource(PrefixById, "/prefix/<int:id>")
