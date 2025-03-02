# Entrega 3

Repositorio con código base para el uso de un sistema usando el patrón CQRS y usando eventos de dominio e integración para la comunicación asíncrona entre componentes internos parte del mismo contexto acotado y sistemas externos.

## Estructura del proyecto

Este repositorio sigue en general la misma estructura del repositorio de origen. Sin embargo, hay un par de adiciones importante mencionar:

- Nuestro proyecto de STA ha cambiado de forma considerable. Los siguientes son los cambios relevantes en cada módulo:
    - **api**: En este módulo se modificó el API de `ingesta.py` el cual cuenta con dos endpoints: `/crear-ingesta-comando` y `/consulta-por-id/<id>`, los cuales por detrás de escenas usan un patrón CQRS como la base de su comunicación.
    - **modulos/../aplicacion**: Este módulo ahora considera los sub-módulos: `queries` y `comandos`. En dichos directorios pdrá ver como se desacopló las diferentes operaciones lectura y escritura. Vea en el módulo `ingesta` los archivos `crear_ingesta.py` y `obtener_ingesta.py` para ver como se logra dicho desacoplamiento.
    - **modulos/../aplicacion/handlers.py**: Estos son los handlers de aplicación que se encargan de oir y reaccionar a eventos. Si consulta el módulo de clientes podra ver que tenemos handlers para oir y reaccionar a los eventos de dominio para poder continuar con una transacción. En el modulo de vuelos encontramos handlers para eventos de integración los cuales pueden ser disparados desde la capa de infraestructura, la cual está consumiendo eventos y comandos del broker de eventos.
    - **modulos/../dominio/eventos.py**: Este archivo contiene todos los eventos de dominio que son disparados cuando una actividad de dominio es ejecutada de forma correcta.
    - **modulos/../infraestructura/consumidores.py**: Este archivo cuenta con toda la lógica en términos de infrastructura para consumir los eventos y comandos que provienen del broker de eventos. Desarrollado de una forma funcional.
    - **modulos/../infraestructura/despachadores.py**: Este archivo cuenta con toda la lógica en terminos de infrastructura para publicar los eventos y comandos de integración en el broker de eventos. Desarrollado de manera OOP.
    - **modulos/../infraestructura/schema**: En este directorio encontramos la definición de los eventos y comandos de integración. Puede ver que se usa un formato popular en la comunidad de desarrollo de software open source, en donde los directorios/módulos nos dan un indicio de las versiones `/schema/v1/...`. De esta manera podemos estar tranquilos con versiones incrementales y menores, pero listos cuando tengamos que hacer un cambio grande.
    - **seedwork/aplicacion/comandos.py**: Definición general de los comandos, handlers e interface del despachador.
    - **seedwork/infraestructura/queries.py**: Definición general de los queries, handlers e interface del despachador.
    - **seedwork/infraestructura/uow.py**: La Unidad de Trabajo (UoW) mantiene una lista de objetos afectados por una transacción de negocio y coordina los cambios de escritura. Este objeto nos va ser de gran importancia, pues cuando comenzamos a usar eventos de dominio e interactuar con otros módulos, debemos ser capaces de garantizar consistencia entre los diferentes objetos y partes de nuestro sistema.

## STA
### Ejecutar Aplicación STA

Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/sta/api run
```

Siempre puede ejecutarlo en modo DEBUG:

```bash
flask --app src/sta/api --debug run
```

### Crear imagen para STA Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f sta.Dockerfile -t sta/flask
```

### Ejecutar STA contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run -p 5000:5000 -e BROKER_HOST=127.0.0.1 -e DB_HOSTNAME=127.0.0.1 -e DB_USERNAME="root" -e DB_PASSWORD="admin" -e DB_NAME="ingestas" sta/flask
```

## BFF: Web

Desde el directorio `src` ejecute el siguiente comando

```bash
uvicorn bff_web.main:app --host localhost --port 8003 --reload
```

### Crear imagen para BFF Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f bff.Dockerfile -t sta/bff
```

### Ejecutar BFF contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run -p 8003:8003 -e BROKER_HOST=127.0.0.1 -e SALUDTECH_ALPES_ADDRESS="localhost" sta/bff
```

## Docker-compose

Para desplegar toda la arquitectura en un solo comando, usamos `docker-compose`. Para ello, desde el directorio principal, ejecute el siguiente comando:

```bash
docker-compose up
```

Si desea detener el ambiente ejecute:

```bash
docker-compose stop
```

En caso de querer desplegar dicha topología en el background puede usar el parametro `-d`.

```bash
docker-compose up -d
```

## Comandos útiles

### Listar contenedoras en ejecución
```bash
docker ps
```

### Listar todas las contenedoras
```bash
docker ps -a
```

### Parar contenedora
```bash
docker stop <id_contenedora>
```

### Eliminar contenedora
```bash
docker rm <id_contenedora>
```

### Listar imágenes
```bash
docker images
```

### Eliminar imágenes
```bash
docker images rm <id_imagen>
```

### Acceder a una contendora
```bash
docker exec -it <id_contenedora> sh
```

### Kill proceso que esta usando un puerto
```bash
fuser -k <puerto>/tcp
```

### Correr docker-compose usando profiles
```bash
docker-compose --profile <pulsar|resource|all> up
```

## Despliegue en Nube

### Pulsar en EC2

```bash
sudo docker run -it \
-p 6650:6650 \
-p 8080:8080 \
--mount source=pulsardata,target=/pulsar/data \
--mount source=pulsarconf,target=/pulsar/conf \
-e PULSAR_STANDALONE_USE_ZOOKEEPER=1 \
apachepulsar/pulsar:4.0.3 \
bin/pulsar standalone
```
```bash
curl http://34.16.96.125:8080/admin/v2/clusters
```


### Construir imagenes

los comandos acontinuación deben ejecutarse desde la carpeta raíz del proyecto.

##### Pre-Comandos
```bash
gcloud auth configure-docker us-central1-docker.pkg.dev && \
gcloud config set project nomoniliticasmiso2025
```

#### STA para Deploy
```bash
docker build -t us-central1-docker.pkg.dev/nomoniliticasmiso2025/no-monoliticas/sta-service:1.0.2 -f sta.Dockerfile . && \
docker push us-central1-docker.pkg.dev/nomoniliticasmiso2025/no-monoliticas/sta-service:1.0.2
```

#### BFF para Deploy
```bash
docker build -t us-central1-docker.pkg.dev/nomoniliticasmiso2025/no-monoliticas/bff-service:1.0.2 -f bff.Dockerfile . && \
docker push us-central1-docker.pkg.dev/nomoniliticasmiso2025/no-monoliticas/bff-service:1.0.2
```

### Desplegar en GCP

Los siguientes comandos deben ejecutarse desde la carpeta `deployment`.<br>
Antes de ejecutar los comandos, asegúrese de tener configurado el `kubectl` para el cluster de GCP.

##### Comandos previos para configurar el cluster

Estos comandos se deben correr directos en la consola de GCP.

```bash
gcloud compute networks create vpn-no-monoliticas --project=nomoniliticasmiso2025 --subnet-mode=custom --mtu=1460 --bgp-routing-mode=regional && \
gcloud compute networks subnets create red-k8s-nomoniliticasmiso2025 --range=192.168.32.0/19 --network=vpn-no-monoliticas --region=us-central1 --project=nomoniliticasmiso2025 && \
gcloud compute addresses create red-dbs-nomoniliticasmiso2025 --global --purpose=VPC_PEERING --addresses=192.168.0.0 --prefix-length=24 --network=vpn-no-monoliticas --project=nomoniliticasmiso2025 && \
gcloud services vpc-peerings connect --service=servicenetworking.googleapis.com --ranges=red-dbs-nomoniliticasmiso2025 --network=vpn-no-monoliticas --project=nomoniliticasmiso2025 && \
gcloud compute firewall-rules create allow-db-ingress --direction=INGRESS --priority=1000 --network=vpn-no-monoliticas --action=ALLOW --rules=tcp:3306 --source-ranges=192.168.1.0/24 --target-tags=basesdedatos --project=nomoniliticasmiso2025
```

Los siguientes comandos se vuelven a correr en la consola local; Pero antes debes contar con un cluster ya creado en GCP.

```bash
gcloud container clusters get-credentials no-monoliticas-cluster --region us-central1 --project nomoniliticasmiso2025
```

Por último el deploy de los servicios usando los siguientes comandos en la consola local. <br>
Estos comandos se deben correr desde la carpeta `deployment`.

```bash
kubectl apply -f secrets.yaml && \
kubectl apply -f k8s-base-layer-deployment.yaml && \
kubectl apply -f k8s-ingress-deloyment.yaml && \
cd ..
```