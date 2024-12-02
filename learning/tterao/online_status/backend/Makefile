
all: build

build:
	python manage.py runserver 

build-redis-server:
	docker run --rm -p 6379:6379 redis:7

test:
	./manage.py test test/

.PHONY: all build test build-redis-server
