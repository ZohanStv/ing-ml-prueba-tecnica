FROM python:3.11.10-slim-bookworm
WORKDIR /app
COPY ./digits_model ./digits_model
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
WORKDIR /app/digits_model
CMD ["python", "-u", "manage.py", "runserver", "0.0.0.0:8000"]



