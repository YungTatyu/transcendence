FROM debian:bullseye

RUN apt-get update && apt-get -y install \
	curl \
	supervisor \
	tini \
	gnupg \
	lsb-release \
	jq

RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg && \
	echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
	tee /etc/apt/sources.list.d/hashicorp.list && \
	apt-get update && \
	apt-get -y install vault && \
	rm -rf /var/lib/apt/lists/*

COPY config/ /vault/config/
COPY init_vault_and_rotate_api_key.sh /usr/local/bin/init_vault_and_rotate_api_key.sh
RUN chmod +x /usr/local/bin/init_vault_and_rotate_api_key.sh

# supervisord を PID1 で起動
COPY supervisord.conf /etc/supervisord.conf
RUN mkdir -p /var/log/supervisor
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
