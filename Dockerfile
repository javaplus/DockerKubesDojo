FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

LABEL org.opencontainers.image.title="cloud-native-demo"

COPY . .

CMD [ "python", "./app.py" ]
