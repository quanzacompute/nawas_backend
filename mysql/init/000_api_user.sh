#!/usr/bin/env sh

mysql -u "root" -p$(cat /run/secrets/db_root_password) <<EOF

CREATE DATABASE IF NOT EXISTS nawas;

CREATE USER IF NOT EXISTS api@'172.16.238.2' IDENTIFIED by '$(cat /run/secrets/db_password)';
GRANT ALL PRIVILEGES ON nawas.* to api@'172.16.238.2';
EOF
