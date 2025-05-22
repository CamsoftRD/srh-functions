from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class PostModel:
    id: Optional[int] = None #id
    content: Optional[str] = None  #contenido
    entity: Optional[str] = None #entidad
    register_id: Optional[int] = None #id_Registro
    owner_id: Optional[int] = None # id_Usuario
    owner_name: Optional[str]=None #primerNombre
    owner_last_name: Optional[str] = None #primerApellido
    owner_image_url: Optional[str] = None # urlImage
    create_at: Optional[str] = None # fecha_Creacion
    update_at: Optional[str] = None #fecha_Actualizacion
    files: Optional[Dict[str, Optional[any]]] = None
    Scope: Optional[Dict[str, Optional[any]]] = None





