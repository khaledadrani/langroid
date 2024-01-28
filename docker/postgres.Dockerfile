FROM bitnami/postgresql:16.1.0-debian-11-r13

USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-all \
    && rm -rf /var/lib/apt/lists/*
RUN cd /tmp \
    && git clone --branch v0.5.0 https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make \
    && make install

USER 1000