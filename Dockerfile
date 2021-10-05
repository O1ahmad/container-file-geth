ARG build_version="golang:1.17-stretch"

# ******* Stage: builder ******* #
FROM ${build_version} as builder

ARG geth_version=v1.10.9

RUN apt update && apt install --yes --no-install-recommends gcc git make

WORKDIR /tmp
RUN git clone --depth 1 --branch ${geth_version} https://github.com/ethereum/go-ethereum.git
RUN cd go-ethereum && make geth

WORKDIR /tmp/go-ethereum

# ******* Stage: base ******* #
FROM ubuntu:20.04 as base

RUN apt update && apt install --yes --no-install-recommends \
    ca-certificates \
    cron \
    curl \
    pip \
    tini \
    zip unzip \
    # apt cleanup
	&& apt-get autoremove -y; \
	apt-get clean; \
	update-ca-certificates; \
	rm -rf /tmp/* /var/tmp/* /var/lib/apt/lists/*

WORKDIR /docker-entrypoint.d
COPY entrypoints /docker-entrypoint.d
COPY scripts/entrypoint.sh /usr/local/bin/geth-entrypoint

COPY scripts/geth-helper.py /usr/local/bin/geth-helper
RUN chmod 775 /usr/local/bin/geth-helper

RUN pip install click requests toml

ENTRYPOINT ["geth-entrypoint"]

# ******* Stage: testing ******* #
FROM base as test

ARG goss_version=v0.3.16

RUN curl -fsSL https://goss.rocks/install | GOSS_VER=${goss_version} GOSS_DST=/usr/local/bin sh

WORKDIR /test

COPY test /test
COPY --from=builder /tmp/go-ethereum/build/bin/geth /usr/local/bin/

CMD ["goss", "--gossfile", "/test/goss.yaml", "validate"]

# ******* Stage: release ******* #
FROM base as release

ARG version=0.2.2

LABEL 01labs.image.authors="zer0ne.io.x@gmail.com" \
	01labs.image.vendor="O1 Labs" \
	01labs.image.title="0labs/geth" \
	01labs.image.description="Official Golang implementation of the Ethereum protocol." \
	01labs.image.source="https://github.com/0x0I/container-file-geth/blob/${version}/Dockerfile" \
	01labs.image.documentation="https://github.com/0x0I/container-file-geth/blob/${version}/README.md" \
	01labs.image.version="${version}"

COPY --from=builder /tmp/go-ethereum/build/bin/geth /usr/local/bin/

#      rpc   ws   p2p   discovery
#       ↓    ↓     ↓        ↓
EXPOSE 8545 8546 30303 30303/udp

CMD ["geth"]

# ******* Stage: tools ******* #

FROM builder as build-tools

RUN cd /tmp/go-ethereum && make all

# ------- #

FROM base as tools

COPY --from=build-tools /tmp/go-ethereum/build/bin/* /usr/local/bin/

WORKDIR /root/.ethereum

CMD ["/bin/bash"]
