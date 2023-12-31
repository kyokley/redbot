.PHONY: build proxy-shell shell

DOCKER_LOCALHOST ?= localhost
DEFAULT_USER_INDEX ?= "275"

build:
	docker build -t kyokley/redbot .

proxy-shell: build
	docker run --rm -it -v $$(pwd):/workspace -v $$HOME/.config/redmine:/root/.config/redmine -e KEY_PATH=/root/.config/redmine/key -e ALL_PROXY="socks5://${DOCKER_LOCALHOST}:8081" --net host -e USER_INDEX=${DEFAULT_USER_INDEX} --entrypoint /bin/sh kyokley/redbot

shell: build
	docker run --rm -it -v $$(pwd):/workspace -v $$HOME/.config/redmine:/root/.config/redmine -e KEY_PATH=/root/.config/redmine/key -e USER_INDEX=${DEFAULT_USER_INDEX} --entrypoint /bin/sh kyokley/redbot
