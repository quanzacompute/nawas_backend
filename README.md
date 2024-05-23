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

![NBIP Stack - Data model(1)](https://github.com/RSloeserwij/nawas_stack/assets/20596929/7b0fbd22-ca2b-4615-94eb-5c738d6df8ab)

### Tenant
Tenant represents the member which owns the different ASN and prefixes. This is a top level object used to aggregate all the different object belonging to it.

### ASN
### Prefix
### PrefixChange
