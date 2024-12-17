FROM odoo:17.0

ARG LOCALE=en_US.UTF-8

ENV LANGUAGE=${LOCALE}
ENV LC_ALL=${LOCALE}
ENV LANG=${LOCALE}
ENV ODOO_CUSTOM_ADDONS=/mnt/custom_addons

COPY custom_addons/ $ODOO_CUSTOM_ADDONS

RUN chown -R odoo:odoo $ODOO_CUSTOM_ADDONS



USER 0

RUN apt-get -y update && apt-get install -y --no-install-recommends locales netcat-openbsd \
    && locale-gen ${LOCALE}

WORKDIR /app

COPY --chmod=755 entrypoint.sh ./

ENTRYPOINT ["/bin/sh"]

CMD ["entrypoint.sh"]
