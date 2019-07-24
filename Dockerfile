# HIS HydroServer 1.0.0
# Django 2.1.5


FROM ubuntu:18.04


MAINTAINER Kenneth Lippold kjlippold@gmail.com


# Apt Setup ----------------------------------------------------------------------------------------------#

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install wget emacs vim sudo bzip2 nginx supervisor -y


# Create hsapp user --------------------------------------------------------------------------------------#

RUN adduser --disabled-password --gecos '' hsapp
RUN adduser hsapp sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER hsapp

ENV HYDROSERVER_HOME /home/hsapp
WORKDIR $HYDROSERVER_HOME
RUN chmod a+rwx $HYDROSERVER_HOME


# Place Application Files --------------------------------------------------------------------------------#

RUN mkdir hydroserver

COPY environment.yml $HYDROSERVER_HOME
COPY hydroserver/ $HYDROSERVER_HOME/hydroserver
COPY startup.sh $HYDROSERVER_HOME
COPY his_hydroserver.conf /etc/nginx/conf.d/

RUN sudo chown -R hsapp $HYDROSERVER_HOME/hydroserver


# Setup Conda Environment --------------------------------------------------------------------------------#

RUN wget https://repo.continuum.io/miniconda/Miniconda2-4.5.12-Linux-x86_64.sh
RUN bash Miniconda2-4.5.12-Linux-x86_64.sh -b
RUN rm Miniconda2-4.5.12-Linux-x86_64.sh

ENV PATH /home/hsapp/miniconda2/bin:$PATH

RUN conda update conda

RUN conda env create -f environment.yml
RUN echo "source activate hydroserver" > ~/.bashrc


# Expose Ports -------------------------------------------------------------------------------------------#

EXPOSE 8090


# Run HydroServer ----------------------------------------------------------------------------------------#

RUN sudo chmod +x startup.sh
USER root
CMD ["./startup.sh"]
