FROM hashicorp/vault:latest

COPY vault_service/config/ /vault/config/

COPY certs/client.crt \
	certs/client.key \
	certs/server.crt \
	certs/server.key \
	certs/ca.crt \
	/vault/certs/

COPY vault_service/init_vault.sh /usr/local/bin/init_vault.sh
RUN chmod +x /usr/local/bin/init_vault.sh

ENTRYPOINT ["/usr/local/bin/init_vault.sh"]
