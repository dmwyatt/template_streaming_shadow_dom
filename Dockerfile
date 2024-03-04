FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV /usr/local/

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl

# Set work directory
WORKDIR /code

# Copy the current directory contents into the container at /code/
COPY . /code/

RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && . $HOME/.cargo/env \
    && uv pip compile requirements.in -o requirements.txt \
    && uv pip sync requirements.txt

EXPOSE 8000

# gunicorn
CMD ["gunicorn", "template_streaming_shadow_dom.wsgi:application", "--bind", "0.0.0.0:8000"]
