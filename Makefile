filepath        :=      $(PWD)
versionfile     :=      $(filepath)/version.txt
version         :=      $(shell cat $(versionfile))
image_repo      :=      0labs/geth

build:
	docker build --tag $(image_repo):$(version) --build-arg geth_version=$(version) .

test:
	docker build --target test --build-arg geth_version=$(version) --tag geth:test . && docker run --env-file test/test.env geth:test

test-compose:
	echo "image=${image_repo}:${version}" > compose/.env-test
	cd compose && docker-compose config && docker-compose --env-file .env-test up -d && \
	sleep 5 && docker-compose logs 2>&1 | grep "Starting Geth on Rinkeby" && \
	docker-compose down && rm .env-test

release:
	docker build --target release --tag $(image_repo):$(version) --build-arg geth_version=$(version) .
	docker push $(image_repo):$(version)

latest:
	docker tag $(image_repo):$(version) $(image_repo):latest
	docker push $(image_repo):latest

tools:
	docker build --target tools --tag $(image_repo):$(version)-tools --build-arg geth_version=$(version) .
	docker push ${image_repo}:$(version)-tools

.PHONY: test
