FROM m.daocloud.io/docker.io/continuumio/miniconda3:latest

ENV DEBIAN_FRONTEND=noninteractive

COPY sources.list /etc/apt/
RUN mv /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list.d/debian.sources.bak && \
    apt update && \
    apt upgrade -y && \
    apt-get install -y --allow-downgrades --no-install-recommends \
        ca-certificates \
        ncurses-base=6.3-2ubuntu0.1 \
        curl \
        make \
        vim \
        libfreetype6 \
        libfontconfig1 \
        net-tools \
        supervisor && \
    mkdir -p /opt/PyChemKit/log && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# Setup chem_runner
COPY conf/chem_runner.conf /etc/supervisor/conf.d/
# Setup classify_runner
COPY conf/classify_runner.conf /etc/supervisor/conf.d/
# eln apis
COPY conf/eln_runner.conf /etc/supervisor/conf.d/

COPY . /opt/PyChemKit/

# Install python dependencies using pip
COPY environment.yaml /opt/PyChemKit/
RUN cd /opt/PyChemKit/ && chmod +x ./start.sh && conda env create -f environment.yaml

# chem_runner
EXPOSE 6010
# classify_runner
EXPOSE 6020
# eln_runner
EXPOSE 6030

WORKDIR /opt/PyChemKit/
# CMD
CMD ["./start.sh"]
