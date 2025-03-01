FROM python:3.10-slim

EXPOSE 5000/tcp

COPY etiquetado-requirements.txt ./
RUN pip install --upgrade --no-cache-dir pip setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r etiquetado-requirements.txt

COPY . .

WORKDIR "/src"

CMD [ "uvicorn", "etiquetado.main:app", "--host", "localhost", "--port", "8000", "--reload"]