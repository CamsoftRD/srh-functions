from dataclasses import dataclass
from typing import Optional

@dataclass
class DepartmentModel:
    id_departamento: int
    id_compania: int
    nombre: str
    departamento_padre: Optional[int] = None
    gerente_departamento: Optional[int] = None
    nombre_gerente_departamento: Optional[str] = None
    nombre_departamento_padre: Optional[str] = None
    estado: Optional[str] = None
    sucursal: Optional[str] = None
    clasificacion1: Optional[str] = None
    clasificacion2: Optional[str] = None
    clasificacion3: Optional[str] = None
    centro_costos: Optional[str] = None
    custom_data: Optional[str] = None
    custom_data2: Optional[str] = None