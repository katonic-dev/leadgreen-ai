# Production image for the site: the committed, already-built folder served by unprivileged nginx.
# Build from the repository root:  docker build -t leadgreen-site .
# Runs as UID 101 on port 8080 and writes only to /tmp; docker/nginx.conf has the server config.

# Pinned by digest; bump tag and digest together. Override to pull through a registry mirror.
ARG NGINX_IMAGE=nginxinc/nginx-unprivileged:1.30.5-alpine-slim@sha256:7f79f463c6eb0d0bf8782992bb9636434398e3e5848398805aef2c9b025d8609

# Stage the site (.dockerignore keeps out the sources, drafts and repo files), drop the image's own config folder,
# and make every file root-owned and world-readable, so nginx can serve the content but not change it.
FROM ${NGINX_IMAGE} AS site
USER root
COPY . /site
RUN rm -rf /site/docker && chmod -R u=rwX,go=rX /site

FROM ${NGINX_IMAGE}
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY --from=site /site /srv/site
USER 101
EXPOSE 8080
# nginx as PID 1, skipping the base image's entrypoint scripts: they rewrite config at start, which a read-only root
# filesystem refuses, and none of them applies here. The inherited STOPSIGNAL SIGQUIT is a graceful shutdown.
ENTRYPOINT ["nginx", "-g", "daemon off;"]
