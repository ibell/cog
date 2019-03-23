FROM continuumio/miniconda3

RUN groupadd -g 629 prole && \
    useradd -r -u 629 -g prole prole

RUN mkdir /run_home

ADD cog_environment.yml .
RUN conda env create -f /cog_environment.yml

COPY templates templates
COPY static static
COPY start.sh .

RUN mkdir /scratch && \
    chown prole /scratch && \
    chown prole start.sh
COPY flask_main.py .

# Switch to our user for the rest
USER prole
RUN chmod +x start.sh
CMD ["./start.sh"]