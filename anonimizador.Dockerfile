FROM python:3.10.7

EXPOSE 5001/tcp

COPY anonimizador_requirements.txt ./
RUN pip install pip==22.2.2
RUN pip install --upgrade --no-cache-dir setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r anonimizador_requirements.txt

COPY . .

CMD [ "flask", "--app", "./src/anonimizador/api", "run", "--host=0.0.0.0", "--port=5001" ]