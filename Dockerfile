FROM python:3.11-slim

# set working directory
WORKDIR /app

# prevent python from writing pyc files and enable stdout/stderr buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install system deps needed for some packages
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc curl && rm -rf /var/lib/apt/lists/*

# copy requirements and install
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app/

# collect static files (best-effort)
RUN python manage.py collectstatic --noinput || true

# expose port commonly used by hosts
EXPOSE 8080

# default command
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "3"]
