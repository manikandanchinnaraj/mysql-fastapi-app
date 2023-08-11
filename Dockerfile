FROM python:3.8
LABEL authors="mchinnaraj"


COPY books-api /opt/books-api
COPY requirements.txt /opt/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /opt/requirements.txt

WORKDIR /opt/

#CMD ["uvicorn", "books-api.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
CMD ["uvicorn", "books-api.main:app", "--host", "0.0.0.0", "--port", "8000"]

