FROM continuumio/miniconda3

WORKDIR /work

RUN apt-get update && apt-get -y upgrade \
  && apt-get install -y --no-install-recommends \
    git \
    wget \
    g++ \
    gcc \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* 

# Create the environment:
RUN conda create -n myenv python=3.10

# Make RUN commands use the new environment:
RUN echo "conda activate myenv" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

RUN git clone -b develop https://github.com/ADA-research/auto-verify.git && \
    cd auto-verify && \
    pip install -e .

RUN auto-verify --version
RUN auto-verify --install nnenum

RUN echo $'set +euo pipefail \n\
conda activate myenv \n\
set -euo pipefail' > ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
