FROM continuumio/miniconda3:latest as conda-sagemath-coinor
ADD environment.yml /tmp/environment.yml
# https://jcrist.github.io/conda-docker-tips.html: it's best to have RUN commands that install things using a package manager (like conda) also cleanup extraneous files after the install.
RUN conda env create -f /tmp/environment.yml && conda clean -afy
