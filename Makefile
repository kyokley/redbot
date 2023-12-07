build:
	docker build --target final -t kyokley/redbot .

build-dev:
	docker build --target dev -t kyokley/redbot .

shell: build-dev
	docker run --rm -it -v $$(pwd):/workspace -v $$HOME/.config/redmine:/root/.config/redmine -e KEY_PATH=/root/.config/redmine/key --entrypoint /bin/sh kyokley/redbot
