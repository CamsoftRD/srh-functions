from mcp.server.fastmcp import FastMCP
import requests as r
from models.employee_model import EmployeeModel
import os



mcp = FastMCP("Cam-Functions", dependencies=["requests"])

header = {'Content-type': 'application/json',
            'x-api-key': '002002032323232320002SSS',
            'x-ui-culture': 'es-DO',
            }

RRHH_BASE_URL = os.getenv("RRHH_BASE_URL", "http://rrhh.administracionapi.camsoft.com.do:8086")
RRHH_PERSONAL_ACCESS_TOKEN = os.getenv("RRHH_PERSONAL_ACCESS_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiJlc21lcmxpbmVwIiwidW5pcXVlX25hbWUiOiJlc21lcmxpbmVwIiwicm9sZSI6IlVzZXIiLCJVc2VySUQiOiIzMjQ2IiwiRnVsbFVzZXJOYW1lIjoiRXNtZXJsaW4gUGFuaWFndWEiLCJEYXRlVXRsQWNjZXNzIjoiIiwiQ29tcGFueUlkIjoiMiIsIkNvbXBhbnlHcm91cElkIjoiMSIsIkNsaWVudElkIjoiIiwiQnJhbmNoT2ZmaWNlSWQiOiIiLCJDb21wYW55TmFtZSI6IkRyZXMuIE1hbGzDqW4gR3VlcnJhIiwiT2ZmaWNlTmFtZSI6IiIsIkVtYWlsIjoiZXNtZXJsaW5lcEBnbWFpbC5jb20iLCJpc2FkbWluIjoiVHJ1ZSIsIm5iZiI6MTc0NjczNzczMSwiZXhwIjoxNzQ4ODk3NzMxLCJpYXQiOjE3NDY3Mzc3MzF9.wiaNUYisJBRY8HU5gcCp2vScVj_j2WsVUMq34tORbIU")
header["Authorization"] = f"bearer {RRHH_PERSONAL_ACCESS_TOKEN}"


@mcp.tool()
def employee(name:str)-> list[EmployeeModel] | None:
    """
        Busca empleados por nombre y devuelve una lista de objetos EmployeeModel.

        Parámetros:
            name (str): El nombre del empleado a buscar.

        Retorna:
                - Una lista de instancias de EmployeeModel que coinciden con el nombre proporcionado.
    """

    
   
    response = r.get(url=f"{RRHH_BASE_URL}/empleados/empleados/nombre/{name}", headers=header)  
    
    employees = []  
    if response.status_code == 200:
        empleado_list = response.json()['result']
        for data in empleado_list:
            e =  EmployeeModel(
                id=data["idEmpleado"],
                full_name=data["nombreCompletoEmpleado"],
                first_name=data.get("primerNombreEmpleado"),
                last_name=data.get("primerApellidoEmpleado"),
                department_name=data.get("nombre_Departamento"),
                position_name=data.get("nombre_Puesto"),
                company_id=data.get("idcompania"),
                company_name=data.get("nombre_Compania"),
                email=data.get("email"),
                work_email=data.get("email_trabajo"),
                phone=data.get("telefonoPersonal"),
                hire_date=data.get("fechaIngreso"),
                status_id = data.get("estadoEmpleado"),
                status=data.get("nombre_EstadoEmpleado"),
                supervisor_id=data.get("user_id_supervisor"),
                supervisor_name=data.get("nombre_Supervisor"),
                coworkers=data.get("colaboradores"),
                work_schedule=data.get("horario_trabajo"),
                absences = data.get("ausencias")
                
            )
            employees.append(e)
            
    return employees




@mcp.tool()
def fetch_employee_by_user_id(user_id: int)-> EmployeeModel | None:
    """
        Busca un empleado por su ID de usuario y devuelve una instancia de EmployeeModel.

        Parámetros:
            user_id (int): El ID de usuario del empleado a buscar.

        Retorna:
            - Una instancia de EmployeeModel que representa al empleado encontrado.
    """
    try:

        response = r.get(url=f"{RRHH_BASE_URL}/empleados/empleados/usuarios/{user_id}", headers=header)  
        #data = employee.get("result", None)
        
        if response.status_code == 200:
            data = response.json()['result']
        
            if data:
                # Transformar los datos en una instancia de EmployeeModel
                return EmployeeModel(
                    id=data["idEmpleado"],
                    user_id=data.get("idUsuario"),
                    full_name=data["nombreCompletoEmpleado"],
                    first_name=data.get("primerNombreEmpleado"),
                    last_name=data.get("primerApellidoEmpleado"),
                    image_url=data.get("imageUrl"),
                    department_id=data.get("idDepartamento"),
                    department_name=data.get("nombre_Departamento"),
                    position_name=data.get("nombre_Puesto"),
                    company_id=data.get("idcompania"),
                    company_name=data.get("nombre_Compania"),
                    email=data.get("email"),
                    work_email=data.get("email_trabajo"),
                    phone=data.get("telefonoPersonal"),
                    hire_date=data.get("fechaIngreso"),
                    status_id = data.get("estadoEmpleado"),
                    status=data.get("nombre_EstadoEmpleado"),
                    supervisor_id=data.get("user_id_supervisor"),
                    supervisor_name=data.get("nombre_Supervisor"),
                    coworkers=data.get("colaboradores"),
                    work_schedule=data.get("horario_trabajo"),
                    # loans=fetch_employee_loans(data["idEmpleado"]),
                    # payments=fetch_employee_payments(data["idEmpleado"]),
                    absences = data.get("ausencias")
                    
                )
            else:
                return "\n No se encontraron datos para el usuario especificado."
        else:
            return "\n No se encontraron datos para el usuario especificado."
        
    except Exception as e:
        return {"error": str(e)}
    
# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"



if __name__ == "__main__":
    result = employee("michelle")
    print(result)        