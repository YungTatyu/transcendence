DCCOMPOSE := docker compose
TOOL_DIR := tools
LINTER_IMG_NAME := linter-formatter
DOCKER_MNT_DIR := /app

.PHONY: all
all: up

.PHONY: up
up:
	./certs/create_all_certs.sh
	${DCCOMPOSE} up -d --build

.PHONY: down
down:
	${DCCOMPOSE} down --rmi all --volumes --remove-orphans

.PHONY: re
re: down up

# サービス単位でコンテナを起動するターゲット
# 使い方:
#   make service <サービス名>
# 例:
#   make service vault -> vaultサービスのみを起動
#   make service vault match -> vaultとmatchサービスのみを起動
.PHONY: service
service:
	docker compose up $(filter-out $@,$(MAKECMDGOALS)) -d --build

# 余計なターゲット扱いを防ぐ
%:
	@:

.PHONY: build-linter
build-linter:
	docker build -t ${LINTER_IMG_NAME} -f ${TOOL_DIR}/Dockerfile .

.PHONY: lint
lint: build-linter
	# make lint ARG=py もしくは make lint ARG=js で言語を選択可
	docker run -t --rm -v $(shell pwd):${DOCKER_MNT_DIR} ${LINTER_IMG_NAME} lint ${ARG}

.PHONY: fmt
fmt: build-linter
	# make fmt ARG=py もしくは make fmt ARG=js で言語を選択可
	docker run -t --rm -v $(shell pwd):${DOCKER_MNT_DIR} ${LINTER_IMG_NAME} fmt ${ARG}

.PHONY: check
check: build-linter
	docker run --rm -v $(shell pwd):${DOCKER_MNT_DIR} ${LINTER_IMG_NAME}
