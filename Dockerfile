FROM continuumio/miniconda3

WORKDIR /work

RUN apt-get update && apt-get -y upgrade && \ 
    apt-get install -y --no-install-recommends \
    git && \
    rm -rf /var/lib/apt/lists/* 

RUN conda create -n av python=3.10

# Make RUN commands use the new environment:
RUN echo "conda activate av" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

COPY . .
RUN pip install -e '.[dev]' # dev reqs needed for tests

# Check if installation was succesful
RUN auto-verify --version
RUN auto-verify install nnenum
RUN auto-verify install abcrown

RUN echo $'set +euo pipefail \n\
conda activate av \n\
set -euo pipefail' > ./entrypoint.sh
RUN chmod +x entrypoint.sh

# Integration tests, should fail if installing went wrong. 
# No GPU on gh-actions
RUN if ! python -m pytest -v -m "not gpu_only"; then exit 1; fi

ENTRYPOINT ["./entrypoint.sh"]
# Clean up all images: docker rmi -f $(docker images -aq)
