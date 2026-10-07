# BASE_IMAGE must be resolved to a registry digest by the workflow.
ARG BASE_IMAGE
FROM ${BASE_IMAGE}
ARG SOURCE_REVISION
ARG BASE_IMAGE
USER root
RUN mkdir -p /opt/olivine && chown vscode:vscode /opt/olivine
USER vscode
WORKDIR /opt/olivine
COPY --chown=vscode:vscode moose_app/ moose_app/
RUN with-moose make -C moose_app -j2
COPY --chown=vscode:vscode . .
RUN test -n "${SOURCE_REVISION}" \
    && python3 scripts/prebuilt_app.py record --revision "${SOURCE_REVISION}" --base-image "${BASE_IMAGE}" \
    && with-moose python3 scripts/check_implementation.py
ENV OLIVINE_IMAGE_ROOT=/opt/olivine
LABEL org.opencontainers.image.source="https://github.com/johntfoster/olivine-carbonation-theory"
LABEL org.opencontainers.image.revision="${SOURCE_REVISION}"
LABEL org.opencontainers.image.base.name="${BASE_IMAGE}"
