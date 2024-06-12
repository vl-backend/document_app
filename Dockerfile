FROM python:3.10.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV IS_DOCKERIZED=True

WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install -U pipenv
RUN pipenv install --system

COPY . /app

EXPOSE 8000
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]