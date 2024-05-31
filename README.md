# NAWAS Stack

This project is intended as a backend for the NAWAS project by NBIP. It is intended to track changes to prefixes registered to member of the organization and in the future even trigger actions based of these changes. 
The main stack is made of a mysql database in combination with a Flask application in python, which all run in docker to ease deployment and access between the different nodes.

## Deployment

### Secrets
To deploy the stack, please make sure to create a directory in the root of this project, called secrets. 

It should contain two files:
 - db_password.txt
 - db_root_password.txt

These two passwords should be kept save by the user, in case of a backup restore you will need them.

### Test code integrity
To test the integrity of the code, the API can be started in unittest mode using the docker-compose.test.yml file as follows:

``` docker compose -f docker-compose.test.yml up && docker compose -f docker-compose.test.yml down ```

This will test the code with more than 70 different tests, making sure the code is working properly. Using the above command this will also build an image which can be used by the production stack later.

### Production deployment
After the code has been verified the stack can be deployed with a basic up command:

```docker compose up -d```

This will up both the database and the api, which should be in working order after the boot. Make sure to take not of the mysql volume, which contains all the data in the database. In case of backups, this directory, in combination with the passwords, should be backed up.

## API

### Model

The API operates with 3 diffent objects:
  - Tenant
  - ASN
  - Prefix

It also tracks changes to prefix using the PrefixChange object.

These objects interact with each other as follows:

![NBIP Stack - Data model(2)](https://github.com/quanzacompute/nawas_backend/assets/171254481/d06ed732-adca-43f7-82a3-6f472d9f5372)

### Tenant
Tenant represents the member which owns the different ASN and prefixes. This is a top level object used to aggregate all the different object belonging to it.

It can be interacted with as a list, and individually by either name or id, using the following endpoints:

- Root -> localhost:8000/tenant
- ID -> localhost:8000/tenant/<int:id>
- Name -> localhost:8000/tenant/<string:name>

These endpoints can be approached with the following methods:

#### GET
Retrieves the current information in the database. This will return a data structure containing the tenant and all its children (asns, prefixes)

#### POST / PUT
Post: Creates a new instance of this object in the database. 
Put: Updates an existing instance of the object.

This method requires a payload as follows:

```
{
  'id': 1,
  'name': 'quanza'
}
```
The id field does not have to be provided when using the POST method, this fields automatically auto increments when the object is created. 

#### DELETE
Deletes an instance of this object in the database.
WARNING: this method will return a failure if the object still has children assigned to it in the database.


### ASN

ASN is the object representing an Autonomous System Number, and is the object used to aggregate prefixes and sync them.

It can be interacted with as a list, and individually by either name or id, using the following endpoints:

- Root -> localhost:8000/asn
- ID -> localhost:8000/asn/<int:id>
- Sync -> localhost:8000/asn/<int:id>/sync

The Sync endpoint triggers a sync action which will retrieve current information from the public database, which is bgpview in this case. This will compare prefixes assigned to the ASN with the situation in the database, and alter the database accordingly

These endpoints can be approached with the following methods:

#### GET
Retrieves the current information in the database. This will return a data structure containing the tenant and all its children (asns, prefixes). A GET request on the Sync endpoint (as defined above), will trigger a sync action on the provided ASN. 

#### POST / PUT
Post: Creates a new instance of this object in the database. 
Put: Updates an existing instance of the object.

This method requires a payload as follows:

```
{
  'asn': 1,
  'tenant_id': 1,
  'name': 'quanza'
}
```


#### DELETE
Deletes an instance of this object in the database.
WARNING: this method will return a failure if the object still has children assigned to it in the database.

### Prefix



### PrefixChange
