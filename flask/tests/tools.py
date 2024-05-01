from models.tenant import Tenant
from models.asn import ASN
from models.prefix import Prefix

## General tools for the testcases

def create_tenant(db, tenant_id=1):
    tenant = Tenant(id=tenant_id, name="test_tenant{}".format(tenant_id))
    db.session.add(tenant)
    db.session.commit()
    return tenant

def create_asn(db, tenant, asn_id=1):
    asn = ASN(asn=asn_id, tenant_id=tenant.id)
    db.session.add(asn)
    db.session.commit()
    return asn

def create_prefix(db, asn, prefix_id=1, cidr="8.8.8.8/32"):
    prefix = Prefix(id=prefix_id, asn=asn.asn, cidr=cidr)
    db.session.add(prefix)
    db.session.commit()
    return prefix
