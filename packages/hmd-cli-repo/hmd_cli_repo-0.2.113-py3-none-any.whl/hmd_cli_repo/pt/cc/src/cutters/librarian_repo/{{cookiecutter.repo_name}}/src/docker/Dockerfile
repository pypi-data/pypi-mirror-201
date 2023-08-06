# syntax = docker/dockerfile:1.0-experimental

FROM ghcr.io/hmdlabs/hmd-ms-librarian:0.1.<number>

COPY requirements.txt ${FUNCTION_DIR}

COPY ./schemas/ /schemas

RUN --mount=type=secret,id=pipconfig,dst=/etc/pip.conf \
    pip install -r requirements.txt

