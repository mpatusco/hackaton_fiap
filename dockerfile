FROM python:3.8.3-slim
WORKDIR /src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /src
EXPOSE 5001
CMD cd /src && python ./register/app.py

