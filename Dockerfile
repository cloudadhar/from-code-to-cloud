# Dockerfile: the recipe Docker follows to build our image, top to bottom.
# Each instruction creates a layer. Docker caches layers, so rebuilds are fast.

# 1. FROM: the base image to start from.
#    A small official Python image (Alpine Linux), pulled from Amazon ECR Public
#    so we don't hit Docker Hub download limits.
FROM public.ecr.aws/docker/library/python:3.12-alpine

# 2. LABEL: information about the image (shown by `docker inspect`).
LABEL org.opencontainers.image.title="Deploy Your First App on Amazon ECS Fargate" \
      org.opencontainers.image.description="AWS Student Builder Group, Siddhant College of Engineering workshop app"

# 3. WORKDIR: the folder inside the container where our app lives.
#    Every command after this runs inside /app.
WORKDIR /app

# 4. RUN: execute a command while BUILDING the image.
#    Create a normal user so the app doesn't run as root (security best practice).
RUN addgroup -S appuser && adduser -S appuser -G appuser

# 5. COPY: copy files from your computer (the build context) into the image.
#    Only the two files the app needs. .dockerignore keeps everything else out.
COPY app.py index.html ./

# 6. USER: from here on, run as the normal user, not root.
USER appuser

# 7. ARG: a value you can pass at BUILD time:
#      docker build --build-arg APP_VERSION=v2 -t myapp:v2 .
ARG APP_VERSION=v1

# 8. ENV: environment variables available to the app at RUN time.
#    ECS can override these in the task definition (we set PLATFORM there).
ENV PORT=8080 \
    APP_VERSION=${APP_VERSION} \
    PLATFORM="Local container"

# 9. EXPOSE: documents the port the app listens on.
#    It doesn't open anything by itself: `docker run -p` or the ECS port mapping does.
EXPOSE 8080

# 10. HEALTHCHECK: how Docker checks the app is alive (calls /health every 30s).
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2)" || exit 1

# 11. CMD: the command that runs when a container STARTS from this image.
CMD ["python", "app.py"]
