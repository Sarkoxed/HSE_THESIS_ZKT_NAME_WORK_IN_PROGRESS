FROM zkt-toolchain as toolchain

FROM ubuntu:24.04 as ghdl-builder

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        git \
        gnat \
        llvm-dev \
        clang \
        zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /build
RUN git clone https://github.com/ghdl/ghdl.git
WORKDIR /build/ghdl/build
RUN ../configure --with-llvm-config=llvm-config --prefix=/opt/ghdl && \
    make -j25 && \
    make install


FROM ubuntu:24.04 as runtime

RUN apt-get update && \
    apt-get install -y \
        make \
        python3 \
        gcc \
        git \
        llvm \
        libgnat-13 \
        zlib1g-dev \
        libmpc-dev \
        libmpfr-dev \
        libgmp-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=toolchain /opt/riscv /opt/riscv
COPY --from=ghdl-builder /opt/ghdl /opt/ghdl

ENV PATH="/opt/riscv/bin:/opt/ghdl/bin:${PATH}"
ENV RISCV_PREFIX=riscv32-unknown-elf-

WORKDIR /project
RUN git clone https://github.com/stnolting/neorv32.git cores/neorv32
COPY targets/neorv32 /project/targets/neorv32

COPY docker/neorv32/entrypoint.sh /project/entrypoint.sh
ENTRYPOINT ["/project/entrypoint.sh"]
