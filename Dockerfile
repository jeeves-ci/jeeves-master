FROM "python:2.7"

ENV POSTGRES_HOST_PORT_ENV=${UNSET}
ENV POSTGRES_USERNAME_ENV=${UNSET}
ENV POSTGRES_PASSWORD_ENV=${UNSET}

ENV RABBITMQ_HOST_PORT_ENV=${UNSET}
ENV RABBITMQ_USERNAME_ENV=${UNSET}
ENV RABBITMQ_PASSWORD_ENV=${UNSET}

RUN git clone https://github.com/jeeves-ci/jeeves-master.git \
    && cd jeeves-master \
    && git checkout 0.1 \
    && pip install -r requirements.txt .

# webui port
EXPOSE 7778
# rest api port
EXPOSE 8080

WORKDIR jeeves-master/
CMD ["python", "-m", "rest_service", "rest_service/server.py"]