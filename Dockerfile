FROM "python:2.7"

ENV POSTGRES_HOST_PORT_ENV ""
ENV POSTGRES_USERNAME_ENV ""
ENV POSTGRES_PASSWORD_ENV ""

ENV RABBITMQ_HOST_PORT_ENV ""
ENV RABBITMQ_USERNAME_ENV ""
ENV RABBITMQ_PASSWORD_ENV ""

ENV JEEVES_JWT_SECRET_KEY_ENV "change-me"
ENV JEEVES_ADMIN_EMAIL_ENV "admin@jeeves.com"
ENV JEEVES_ADMIN_PASSWORD_ENV "Password1"
ENV JEEVES_ORG_NAME_ENV "default"

RUN git clone https://github.com/jeeves-ci/jeeves-master.git \
    && cd jeeves-master \
    && git checkout master \
    && pip install -r requirements.txt -e .

# webui port
EXPOSE 7778
# rest api port
EXPOSE 8080

WORKDIR jeeves-master/
CMD ["python", "rest_service/server.py"]