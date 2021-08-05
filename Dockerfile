ARG launch_mode=release
ARG build_version="golang:1.16-stretch"
ARG version=0.1.1

# ******* Stage: builder ******* #
FROM ${build_version} as builder

ARG geth_version=v1.10.6

RUN apt update && apt install --yes --no-install-recommends gcc git make

WORKDIR /tmp
RUN git clone https://github.com/ethereum/go-ethereum.git
RUN cd go-ethereum && git checkout ${geth_version} && make geth

WORKDIR /tmp/go-ethereum

# ******* Stage: base ******* #
FROM ubuntu:21.04 as base

RUN apt update && apt install --yes --no-install-recommends \
    ca-certificates \
    cron \
    curl \
    pip \
    tini \
    zip unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /docker-entrypoint.d
COPY entrypoints /docker-entrypoint.d
COPY scripts/entrypoint.sh /usr/local/bin/geth-entrypoint

COPY scripts/geth-helper.py /usr/local/bin/geth-helper
RUN chmod ug+x /usr/local/bin/geth-helper

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

LABEL version="${version}"

COPY --from=builder /tmp/go-ethereum/build/bin/geth /usr/local/bin/

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

# ******* Set resultant image state based on launch mode ******* #

FROM ${launch_mode} AS after-condition

FROM after-condition
