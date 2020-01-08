FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --trusted-host pypi.org --no-cache-dir -r requirements.txt

LABEL org.opencontainers.image.title="cloud-native-demo"

COPY . .

CMD [ "python", "./app.py" ]
