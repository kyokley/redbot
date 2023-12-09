DOCKER_LOCALHOST ?= localhost

build:
	docker build -t kyokley/redbot .

proxy-shell: build
	docker run --rm -it -v $$(pwd):/workspace -v $$HOME/.config/redmine:/root/.config/redmine -e KEY_PATH=/root/.config/redmine/key -e ALL_PROXY="socks5://${DOCKER_LOCALHOST}:8081" --net host --entrypoint /bin/sh kyokley/redbot

proxy-shell: build
	docker run --rm -it -v $$(pwd):/workspace -v $$HOME/.config/redmine:/root/.config/redmine -e KEY_PATH=/root/.config/redmine/key --entrypoint /bin/sh kyokley/redbot
