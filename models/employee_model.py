from dataclasses import dataclass
from typing import Optional, List, Dict



@dataclass
class EmployeeModel:
    id: Optional[int] = None
    user_id: Optional[int] = None
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    last_name: Optional[str] = None
    sur_name: Optional[str] = None
    birthday: Optional[str] = None
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    company_name: Optional[str] = None
    company_id: Optional[int] = None
    position_name: Optional[str] = None
    email: Optional[str] = None
    work_email: Optional[str] = None
    phone: Optional[str] = None
    hire_date: Optional[str] = None
    status_id: Optional[int] = None
    status: Optional[str] = None
    supervisor_id: Optional[int] = None
    supervisor_name: Optional[str] = None
    image_url: Optional[str] = None
    coworkers: Optional[Dict[str, Optional[any]]] = None
    work_schedule: Optional[Dict[str, Optional[str]]] = None  # Added work schedule
    loans: Optional[List[Dict[str, Optional[str]]]] = None  # New parameter for loans
    payments: Optional[List[Dict[str, Optional[str]]]] = None  # New parameter for loans
    absences: Optional[List[Dict[str, Optional[str]]]] = None  # New parameter for loans
    
    identification_type: Optional[int] = None  # idTipoIdentificacion
    identification_data: Optional[str] = None  # datoIdentificacion
    personal_phone: Optional[str] = None       # telefonoPersonal
    academic_degree_id: Optional[int] = None   # idGradoAcademico