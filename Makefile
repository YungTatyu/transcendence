
LINTER_IMG_NAME := linter-formatter

check:
	docker build -t ${LINTER_IMG_NAME} .
	# docker run --rm -it ${LINTER_IMG_NAME} 
	docker run --rm -it ${LINTER_IMG_NAME} 


.PHONY: check
