FROM hashicorp/vault:latest

COPY vault.hcl /vault/config/vault.hcl
COPY toransit-policy.hcl /vault/config/transit-policy.hcl

COPY certs/client.crt \
	certs/client.key \
	certs/server.crt \
	certs/server.key \
	certs/ca.crt \
	/vault/certs/

COPY ./init_vault.sh /usr/local/bin/init_vault.sh
RUN chmod +x /usr/local/bin/init_vault.sh

ENTRYPOINT ["/usr/local/bin/init_vault.sh"]
