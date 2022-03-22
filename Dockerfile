FROM python:3.8-alpine
RUN apk update
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
EXPOSE 8888
CMD python /app/app.py