FROM ubuntu:18.10

RUN apt-get -y -m update && apt-get install -y cmake g++ zip curl apparmor apparmor-utils

RUN curl -LO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    chmod +x Miniconda3-latest-Linux-x86_64.sh && \
    ./Miniconda3-latest-Linux-x86_64.sh -b -p /miniconda3

ENV PATH="/miniconda3/bin:${PATH}"

RUN groupadd -g 629 prole && \
    useradd -r -u 629 -g prole prole

RUN mkdir /run_home

# Construct the conda environment
COPY cog_environment.yml .
RUN conda update -n base -c defaults conda && \
    conda env update --name base --file /cog_environment.yml && \
	rm /cog_environment.yml

# Copy files for the flask server
COPY templates /run_home/templates
COPY static /run_home/static
COPY flask_main.py /run_home

RUN mkdir /scratch && \
    chown prole /scratch && \
    chown prole run_home && \
    chown prole /run_home/flask_main.py

# Switch to our user for the rest
USER prole
CMD ["python","-u","/run_home/flask_main.py"]