
LINTER_DIR := linters
LINTER_IMG_NAME := linter-formatter
DOCKER_MNT_DIR := /app

.PHONY: build-linter
build-linter:
	docker build -t ${LINTER_IMG_NAME} -f ${LINTER_DIR}/Dockerfile .

.PHONY: lint
lint: build-linter
	docker run -it --rm -v .:${DOCKER_MNT_DIR} ${LINTER_IMG_NAME} lint

.PHONY: fmt
fmt: build-linter
	docker run -it --rm -v .:${DOCKER_MNT_DIR} ${LINTER_IMG_NAME} fmt

.PHONY: check
check: build-linter
	docker run -it --rm -v .:${DOCKER_MNT_DIR} ${LINTER_IMG_NAME}
