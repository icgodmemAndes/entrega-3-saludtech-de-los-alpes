from anonimizador.seedwork.aplicacion.comandos import Comando, ComandoHandler
from anonimizador.seedwork.aplicacion.comandos import ejecutar_commando as comando
from anonimizador.modulos.dominio.entidades import  Imagen
from dataclasses import dataclass
import base64

@dataclass
class ComandoAnonimizarImagen(Comando):
    id_ingesta: str
    url_path: str

class AnonimizarImagenHandler(ComandoHandler):

    def a_entidad(self, comando: ComandoAnonimizarImagen) -> Imagen:
        encoded_url_path = base64.b64encode(comando.url_path.encode()).decode()
        
        params = dict(
            id_ingesta=comando.id_ingesta,
            url_path=encoded_url_path,        
        )

        anonimizador = Imagen(**params)
        return anonimizador
        

    def handle(self, comando: ComandoAnonimizarImagen):
        imagen_anonimizada = self.a_entidad(comando)
        
        


@comando.register(ComandoAnonimizarImagen)
def ejecutar_comando_crear_reserva(comando: ComandoAnonimizarImagen):
    handler = AnonimizarImagenHandler()
    handler.handle(comando)