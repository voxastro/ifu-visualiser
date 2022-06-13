FROM python:3.9
COPY ./requirements.txt /code/
RUN cd /code \
    && pip install -U pip \
    && pip install ipython \
    && pip install -r requirements.txt

WORKDIR /code