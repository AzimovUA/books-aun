FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install waitress

COPY . /app/

EXPOSE 8080

RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["waitress-serve", "--port=8080", "books.wsgi:application"]
