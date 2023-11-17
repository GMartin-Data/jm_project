##########################################################
# Dockerfile for the job markets project for datascientest

FROM jupyter/datascience-notebook

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

