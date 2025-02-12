FROM hashicorp/vault:latest

COPY vault.hcl /vault/config/vault.hcl
COPY toransit-policy.hcl /vault/config/transit-policy.hcl

COPY ./create_cert/client.crt /vault/certs/client.crt
COPY ./create_cert/client.key /vault/certs/client.key
COPY ./create_cert/vault.crt /vault/certs/vault.crt
COPY ./create_cert/vault.key /vault/certs/vault.key
COPY ./create_cert/ca.crt /vault/certs/ca.crt

COPY ./init_vault.sh /usr/local/bin/init_vault.sh
RUN chmod +x /usr/local/bin/init_vault.sh

ENTRYPOINT ["/usr/local/bin/init_vault.sh"]
