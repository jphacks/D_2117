FROM nvidia/cuda:11.2.1-devel-ubuntu20.04

RUN apt-get update && apt-get install -y \
    sudo \
    wget \
    vim \
    git \
    libgl1-mesa-dev

WORKDIR /opt

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    sh Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda3 && \
    rm -r Miniconda3-latest-Linux-x86_64.sh

ENV PATH /opt/miniconda3/bin:$PATH

RUN pip install --upgrade pip && \
    conda update -n base -c defaults conda && \
    conda create -n torch && \
    conda init
ENV CONDA_DEFAULT_ENV torch
RUN echo "conda activate torch" >> ~/.bashrc
ENV PATH /opt/conda/envs/torch/bin:$PATH

RUN conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -c nvidia -y
RUN conda install -c anaconda numpy pandas pillow scipy -y && \
    conda install -c conda-forge matplotlib tqdm jupyterlab python-box ipywidgets -y && \
    pip install opencv-python

WORKDIR /workspace

CMD ["/bin/bash"]