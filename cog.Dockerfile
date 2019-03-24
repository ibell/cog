FROM continuumio/miniconda3

RUN groupadd -g 629 prole && \
    useradd -r -u 629 -g prole prole

RUN mkdir /run_home

COPY cog_environment.yml .
RUN conda env create -f /cog_environment.yml
RUN rm cog_environment.yml

COPY templates /run_home/templates
COPY static /run_home/static
COPY start.sh .
COPY flask_main.py /run_home

RUN mkdir /scratch && \
    chown prole /scratch && \
    chown prole start.sh && \
    chown prole run_home && \
    chown prole /run_home/flask_main.py

# Switch to our user for the rest
USER prole
RUN chmod +x start.sh
CMD ["./start.sh"]