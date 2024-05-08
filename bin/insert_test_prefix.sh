#!/usr/bin/env bash

curl --header 'Content-Type: application/json' -X POST -d '{}' http://localhost:8000/tenant/name/roy &&\
	curl --header 'Content-Type: application/json' -X POST -d '{"tenant_id":1}' http://localhost:8000/asn/1 &&\
	curl --header 'Content-Type: application/json' -X POST -d '{"asn":1,"cidr":"0.0.0.0/0"}' http://localhost:8000/prefix
