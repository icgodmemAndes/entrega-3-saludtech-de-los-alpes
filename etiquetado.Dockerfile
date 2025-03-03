FROM python:3.10.7

EXPOSE 5002/tcp

COPY etiquetado_requirements.txt ./
RUN pip install pip==22.2.2
RUN pip install --upgrade --no-cache-dir setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r etiquetado_requirements.txt

COPY . .

CMD [ "flask", "--app", "./src/etiquetado/api", "run", "--host=0.0.0.0", "--port=5002"]