FROM debian:bullseye

RUN apt-get update && apt-get -y install \
	curl \
	systemd \
	gnupg \
	lsb-release

RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg && \
	echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
	tee /etc/apt/sources.list.d/hashicorp.list && \
	apt-get update && \
	apt-get -y install vault && \
	rm -rf /var/lib/apt/lists/*

COPY config/ /vault/config/
COPY init_vault_and_rotate_api_key.sh /usr/local/bin/init_vault_and_rotate_api_key.sh
RUN chmod +x /usr/local/bin/init_vault_and_rotate_api_key.sh

COPY service_files/*.service /etc/systemd/system/
RUN systemctl enable vault
RUN systemctl enable init_vault_and_rotate_api_key
ENTRYPOINT ["/bin/systemd"]
