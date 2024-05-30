
from app.models.tenant import TenantRoot, TenantById, TenantByName
from app.models.asn import ASNRoot, ASNByASN, SyncByASN
from app.models.prefix import PrefixRoot, PrefixById
from app.models.prefix_change import PrefixChangeById, PrefixChangeByASN, PrefixChangeByTenant


## Register resources into the api
def loadUrls(api):
    #tenant
    api.add_resource(TenantRoot, "/tenant", "/tenant/")
    api.add_resource(TenantById, "/tenant/<int:id>")
    api.add_resource(TenantByName, "/tenant/name/<string:name>")
    
    #asn
    api.add_resource(ASNRoot, "/asn", "/asn/")
    api.add_resource(ASNByASN, "/asn/<int:asn>")
    api.add_resource(SyncByASN, "/asn/<int:asn>/sync")
    
    #prefix
    api.add_resource(PrefixRoot, "/prefix", "/prefix/")
    api.add_resource(PrefixById, "/prefix/<int:id>")

    #prefix changes
    api.add_resource(PrefixChangeById, "/prefix/change/<int:id>")
    api.add_resource(PrefixChangeByASN, "/asn/change/<int:asn>")
    api.add_resource(PrefixChangeByTenant, "/tenant/change/<int:id>")
