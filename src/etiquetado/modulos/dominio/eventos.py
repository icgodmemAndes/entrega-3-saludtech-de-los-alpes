
class magenTageada(Record):
    id_proveedor: String()
    id_paciente: String()
    url_path: String()
    estado: String()
    etiquetas: Array(String())
    modelo_utilizado: String()
    confianza: Float()