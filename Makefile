
LINTER_DIR := linters
LINTER_IMG_NAME := linter-formatter
DOCKER_MNT_DIR := /app

.PHONY: build-linter
build-linter:
	docker build -t ${LINTER_IMG_NAME} -f ${LINTER_DIR}/Dockerfile .

.PHONY: lint
lint: build-linter
	# make lint ARG=py もしくは make lint ARG=js で言語を選択可
	docker run -it --rm -v .:${DOCKER_MNT_DIR} ${LINTER_IMG_NAME} lint ${ARG}

.PHONY: fmt
fmt: build-linter
	# make fmt ARG=py もしくは make fmt ARG=js で言語を選択可
	docker run -it --rm -v .:${DOCKER_MNT_DIR} ${LINTER_IMG_NAME} fmt ${ARG}

.PHONY: check
check: build-linter
	docker run -it --rm -v .:${DOCKER_MNT_DIR} ${LINTER_IMG_NAME}
