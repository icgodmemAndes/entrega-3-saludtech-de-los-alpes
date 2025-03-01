import uuid

from etiquetado.seedwork.aplicacion.comandos import Comando, ComandoHandler
from etiquetado.seedwork.aplicacion.comandos import ejecutar_commando as comando
from etiquetado.modulos.dominio.entidades import Imagen
from dataclasses import dataclass
import datetime

from etiquetado.modulos.dominio.objetos_valor import EstadoEtiquetado, Modalidad, RegionAnatomica, Patologia, MetadatosImagen, Demografia


@dataclass
class ComandoTagearImagen(Comando):
    id_proveedor: uuid.UUID
    id_paciente: uuid.UUID
    url_path: str
    estado: str
    modalidad: str
    region_anatomica: str
    patologia: str
    resolucion: str
    contraste: str
    tipo: str
    fase: str
    grupo_edad: str
    sexo: str
    etnicidad: str

class TagearImagenHandler(ComandoHandler):

    def a_entidad(self, comando: ComandoTagearImagen) -> Imagen:
        imagen = Imagen(
            id_proveedor = comando.id_proveedor,
            id_paciente = comando.id_paciente,
            url_path = comando.url_path,
            estado = EstadoEtiquetado.CREADA,
            modalidad = Modalidad(nombre = comando.modalidad),
            region = RegionAnatomica(nombre = comando.region_anatomica),
            patologia = Patologia(nombre = comando.patologia),
            metadatos = MetadatosImagen(resolucion = comando.resolucion, contraste = comando.contraste, tipo = comando.tipo, fase= comando.fase),
            demografia = Demografia(grupo_edad = comando.grupo_edad,sexo= comando.sexo,etnicidad= comando.etnicidad),
            fecha_creacion = datetime.datetime.now(),
            fecha_actualizacion = datetime.datetime.now()
        )

        return imagen
        

    def handle(self, comando: ComandoTagearImagen):

        imagen = self.a_entidad(comando)


@comando.register(ComandoTagearImagen)
def ejecutar_comando_tagear_imagen(comando: ComandoTagearImagen):
    handler = TagearImagenHandler()
    handler.handle(comando)