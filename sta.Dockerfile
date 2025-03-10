FROM python:3.10.7

EXPOSE 5000/tcp

COPY requirements.txt ./
RUN pip install pip==22.2.2
RUN pip install --upgrade --no-cache-dir setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "flask", "--app", "./src/sta/api", "run", "--host=0.0.0.0"]