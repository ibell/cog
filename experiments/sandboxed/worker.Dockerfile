FROM continuumio/miniconda3

# Construct the conda environment
COPY worker_environment.yml .
RUN conda update -n base -c defaults conda && \
    conda env update --name base --file /worker_environment.yml && \
	rm /worker_environment.yml

COPY worker_main.py .

# Switch to our user for the rest
CMD ["python","-u","worker_main.py"]