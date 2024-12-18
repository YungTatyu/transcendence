
LINTER_DIR := linters
LINTER_IMG_NAME := linter-formatter

check:
	docker build -t ${LINTER_IMG_NAME} -f ${LINTER_DIR}/Dockerfile .
	docker run --rm -it ${LINTER_IMG_NAME} 


.PHONY: check
