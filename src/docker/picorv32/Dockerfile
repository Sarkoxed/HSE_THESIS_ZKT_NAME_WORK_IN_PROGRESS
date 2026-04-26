FROM zkt-toolchain as toolchain

FROM ubuntu:24.04 as runtime

RUN apt-get update && \
    apt-get install -y \
        make \
        python3 \
        gcc \
        git \
        iverilog \
        libmpc-dev \
        libmpfr-dev \
        libgmp-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=toolchain /opt/riscv /opt/riscv

ENV PATH="/opt/riscv/bin:${PATH}"
ENV RISCV_PREFIX=riscv32-unknown-elf-

WORKDIR /project
RUN git clone https://github.com/YosysHQ/picorv32.git cores/picorv32
COPY targets/picorv32 /project/targets/picorv32

COPY docker/picorv32/entrypoint.sh /project/entrypoint.sh
ENTRYPOINT ["/project/entrypoint.sh"]
