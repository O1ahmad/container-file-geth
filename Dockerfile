ARG base_version="golang:1.16-alpine"
ARG geth_version=v1.10.6
ARG version=0.1.1

# ******* Stage: builder ******* #
FROM ${base_version} as builder

RUN apk update && apk add --no-cache gcc musl-dev linux-headers git ca-certificates

WORKDIR /tmp
RUN git clone https://github.com/ethereum/go-ethereum.git && cd go-ethereum && git checkout ${geth_version}

RUN cd go-ethereum && make geth

# ******* Stage: base ******* #
FROM ubuntu:21.04 as base

WORKDIR /docker-entrypoint.d
COPY entrypoints /docker-entrypoint.d
COPY scripts/entrypoint.sh /usr/local/bin/geth-entrypoint

WORKDIR /scripts
COPY scripts /scripts

ENTRYPOINT ["geth-entrypoint"]

# ******* Stage: testing ******* #
FROM base as test

RUN apt update && apt install --yes --no-install-recommends \
    ca-certificates \
    curl \
    tini \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://goss.rocks/install | GOSS_VER=${goss_version} GOSS_DST=/usr/local/bin sh

WORKDIR /test
COPY test /test

COPY --from=builder /tmp/go-ethereum/build/bin/geth /usr/local/bin/

RUN geth &

CMD ["goss", "--gossfile", "/test/goss.yaml", "validate"]

# ******* Stage: release ******* #
FROM base as release

LABEL version="${version}"

COPY --from=builder /tmp/go-ethereum/build/bin/geth /usr/local/bin/

EXPOSE 8545 8546 30303 30303/udp

CMD ["geth"]
