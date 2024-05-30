#!/usr/bin/env bash

curl --header 'Content-Type: application/json' -X POST -d '{}' http://localhost:8000/tenant/name/quanza &&\
	curl --header 'Content-Type: application/json' -X POST -d '{"tenant_id":1, "name":"QUANZA-CONNECT"}' http://localhost:8000/asn/202932 &&\
	curl --header 'Content-Type: application/json' -X GET http://localhost:8000/asn/202932/sync &&\
	curl --header 'Content-Type: application/json' -X GET http://localhost:8000/asn/202932
