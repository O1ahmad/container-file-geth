filepath        :=      $(PWD)
versionfile     :=      $(filepath)/version.txt
version         :=      $(shell cat $(versionfile))
image_repo      :=      0labs/geth

build:
	docker build -t $(image_repo):$(version) --build-arg geth_version=$(version) .

test:
	docker build --target test --build-arg geth_version=$(version) -t geth:test . && docker run --env-file test/test.env geth:test

release:
	docker build --no-cache -t $(image_repo):$(version) --build-arg geth_version=$(version) .
	docker push $(image_repo):$(version)

latest:
	docker tag $(image_repo):$(version) $(image_repo):latest
	docker push $(image_repo):latest

tools:
	docker build -t $(image_repo):$(version)-tools --build-arg geth_version=$(version) --build-arg launch_mode=tools .
	docker push ${image_repo}:$(version)-tools

.PHONY: test
