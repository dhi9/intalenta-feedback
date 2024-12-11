FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
COPY .env.example .env
COPY . /app/


EXPOSE 8000
CMD ["python", "manage.py", "runserver"]
