FROM hashicorp/vault:latest

COPY vault.hcl /vault/config/vault.hcl
COPY ./init_vault.sh /usr/local/bin/init_vault.sh
RUN chmod +x /usr/local/bin/init_vault.sh

ENTRYPOINT ["/usr/local/bin/init_vault.sh"]
