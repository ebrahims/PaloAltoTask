FROM python

WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY . /app
RUN chmod +x ./twtask

CMD ["pytest", "-v","--color=yes","test_rest_api.py"]
