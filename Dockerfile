FROM python:3.9-alpine

RUN mkdir -p /opt/services/shipping-backend

WORKDIR /opt/services/shipping-backend

ADD requirements.txt /opt/services/shipping-backend/

ADD . /opt/services/shipping-backend/

RUN apk add --no-cache gcc curl musl-dev linux-headers && \
        chmod 755 /opt/services/shipping-backend/entrypoints/* && \
            chmod +x /opt/services/shipping-backend/entrypoints/* && \
                pip install -r requirements.txt