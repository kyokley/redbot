build:
	docker build --target final -t kyokley/redbot .

build-dev:
	docker build --target dev -t kyokley/redbot .

shell: build-dev
	docker run --rm -it --entrypoint /bin/sh kyokley/redbot
