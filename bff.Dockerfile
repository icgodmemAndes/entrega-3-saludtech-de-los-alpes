FROM python:3.10.7

EXPOSE 8003/tcp

COPY bff_requirements.txt ./
RUN pip install pip==22.2.2
RUN pip install --no-cache-dir -r bff_requirements.txt

COPY . .

WORKDIR "/src"

CMD [ "uvicorn", "bff_web.main:app", "--host", "localhost", "--port", "8003", "--reload"]