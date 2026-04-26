FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        autoconf \
        automake \
        git \
        curl \
        texinfo \
        bison \
        flex \
        gawk \
        libgmp-dev \
        libmpfr-dev \
        libmpc-dev \
        zlib1g-dev \
        libexpat1-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /build
RUN git clone https://github.com/riscv/riscv-gnu-toolchain.git
WORKDIR /build/riscv-gnu-toolchain
RUN ./configure --prefix=/opt/riscv --with-arch=rv32i --with-abi=ilp32
RUN make -j25
