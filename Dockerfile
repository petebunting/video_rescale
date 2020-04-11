FROM ubuntu:latest 

LABEL authors="Pete Bunting"
LABEL maintainer="petebunting@mac.com" 

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing && \
    apt-get install -y apt-utils wget bzip2 curl git binutils vim imagemagick ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/miniconda && \
    rm ~/miniconda.sh && \
    /opt/miniconda/bin/conda clean -tipsy && \
    ln -s /opt/miniconda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/miniconda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

# use python 3.8 and update conda 
RUN conda install --yes -c conda-forge python=3.8 && conda update --yes -n base conda

RUN pip install ffprobe-python

COPY rescale_videos.py /usr/local/bin
RUN chmod a+x /usr/local/bin/rescale_videos.py

# Add Tini
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

CMD [ "/bin/bash" ]

