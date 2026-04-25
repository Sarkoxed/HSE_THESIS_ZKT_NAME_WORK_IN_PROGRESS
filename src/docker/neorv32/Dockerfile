FROM ubuntu:24.04 as builder

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
        libexpat1-dev \
        gnat \
        llvm-dev \
        clang && \
    apt-get -y autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /project/deps
RUN git clone https://github.com/riscv/riscv-gnu-toolchain.git
RUN git clone https://github.com/ghdl/ghdl.git

WORKDIR /project/deps/riscv-gnu-toolchain
RUN ./configure --prefix=/opt/riscv --with-arch=rv32i --with-abi=ilp32
RUN make -j25
RUN make install

WORKDIR /project/deps/ghdl
RUN mkdir build && \
    cd build && \ 
    ../configure --with-llvm-config=llvm-config --prefix=/opt/ghdl && \
    make -j25 && \
    make install


FROM ubuntu:24.04 as runtime

RUN apt-get update && \
    apt-get install -y \
        make \
        python3 \
        llvm \
        git && \
    apt-get -y autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=builder /opt/riscv /opt/riscv
COPY --from=builder /opt/ghdl /opt/ghdl

WORKDIR /project/cores
RUN git clone https://github.com/stnolting/neorv32.git

ENV PATH="/opt/riscv/bin:/opt/ghdl/bin:${PATH}"
ENV RISCV_PREFIX=riscv32-unknown-elf-

# refactor later

RUN apt-get update && \
    apt-get install -y \
        make \
        python3 \
        llvm \
        libmpc-dev \
        libmpfr-dev \
        libgmp-dev \
        gcc

RUN apt-get install libgnat-13 zlib1g-dev

WORKDIR /project
COPY ./entrypoint.sh ./entrypoint.sh
ENTRYPOINT ["/project/entrypoint.sh"]
