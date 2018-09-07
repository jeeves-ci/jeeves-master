FROM "python:2.7"

ENV POSTGRES_HOST_PORT_ENV ""
ENV POSTGRES_USERNAME_ENV ""
ENV POSTGRES_PASSWORD_ENV ""

ENV RABBITMQ_HOST_PORT_ENV ""
ENV RABBITMQ_USERNAME_ENV ""
ENV RABBITMQ_PASSWORD_ENV ""

RUN git clone https://github.com/jeeves-ci/jeeves-master.git \
    && cd jeeves-master \
    && git checkout master \
    && pip install -r requirements.txt .

# webui port
EXPOSE 7778
# rest api port
EXPOSE 8080

WORKDIR jeeves-master/
CMD ["python", "rest_service/server.py"]