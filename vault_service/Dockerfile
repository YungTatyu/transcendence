FROM hashicorp/vault:1.18.4

COPY config/ /vault/config/

COPY init_vault.sh /usr/local/bin/init_vault.sh
RUN chmod +x /usr/local/bin/init_vault.sh

ENTRYPOINT ["/usr/local/bin/init_vault.sh"]
