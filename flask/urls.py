
from .models.tenant import TenantRoot, TenantByID, TenantByName
from .models.asn import ASNRoot, ASNByASN
from .models.prefix import PrefixRoot, PrefixByID 


## Register resources into the api
def initUrls(api):
    #tenant
    api.add_resource(TenantRoot, "/tenant/")
    api.add_resource(TenantByID, "/tenant/<int:id>")
    api.add_resource(TenantByName, "/tenant/name/<string:name>")
    
    #asn
    api.add_resource(ASNRoot, "/asn/")
    api.add_resource(ASNByASN, "/asn/<int:asn>")
    
    #prefix
    api.add_resource(PrefixRoot, "/prefix/")
    api.add_resource(PrefixByID, "/prefix/<int:id>")
