from mcp.server.fastmcp import FastMCP
import requests as r
from models.employee_model import EmployeeModel
import os
import json
from datetime import datetime
from models.payroll_model import PayrollSummary



mcp = FastMCP("Cam-Functions", dependencies=["requests"])


header = {'Content-type': 'application/json',
            'x-api-key': '002002032323232320002SSS',
            'x-ui-culture': 'es-DO',
            }

RRHH_BASE_URL = os.getenv("RRHH_BASE_URL", "")
RRHH_PERSONAL_ACCESS_TOKEN = os.getenv("RRHH_PERSONAL_ACCESS_TOKEN", "")
header["Authorization"] = f"bearer {RRHH_PERSONAL_ACCESS_TOKEN}"






#@mcp.tool()
def get_resumen(periodoInicial="2024-01-01T00:00:00", periodoFinal="2024-09-30T09:00:00") -> list[PayrollSummary] | None:
    """
    Realiza una solicitud para obtener un reporte de nómina entre un periodo de tiempo específico.
    Parámetros:
    - periodoInicial (str): Fecha de inicio del periodo en formato ISO8601. ejemplo "2024-01-01T00:00:00".
    - periodoFinal (str): Fecha de fin del periodo en formato ISO8601. ejemplo "2024-09-30T09:00:00".

    Retorno:
    - Array PayrollSummary: instancia con los datos relevantes de la nómina.
    - None: si la solicitud falla o la respuesta no contiene datos válidos.
    
    """
    
    if not periodoInicial:
        periodoInicial = datetime(datetime.now().year, 1, 1).strftime('%Y-%m-%dT%H:%M:%S')

    if not periodoFinal:
        periodoFinal = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    body = {
        "type": 4,
        "DetalleGeneralModel": {
            "compania": 2,
            "tipoNomina": 115,
            "periodoInicial": periodoInicial,
            "periodoFinal": periodoFinal,
            "idiomaFormaPago": "es-DO",
            "idiomaTipoContrato": "es-DO"
        }, 
        "json": True
    }

    response = r.post(
        url=f"{RRHH_BASE_URL}/nomina/UtilReporteNomina/generar-reporte-nomina",
        headers=header,
        data=json.dumps(body)
    )
    payrolls = []
    if response.status_code == 200:
        try:
            response_data = response.json()
            for data in response_data:
                # Mapeo manual de claves del JSON a atributos del dataclass
                mapped_data = {
                    "company_name": data.get("nombreEmpresa"),
                    "company_address": data.get("direccionEmpresa"),
                    "current_date": data.get("fechaActual"),
                    "current_time": data.get("horaActual"),
                    "logged_user_name": data.get("nombreUsuarioLogeado"),
                    "payroll_info": data.get("infoNomina"),
                    "period_info": data.get("infoPeriodo"),
                    "department": data.get("departamento"),
                    "code": data.get("codigo"),
                    "employee": data.get("empleado"),
                    "position": data.get("puesto"),
                    "salary": data.get("salario"),
                    "salary_type": data.get("tipoSalario"),
                    "earnings": data.get("ingresos"),
                    "discounts": data.get("descuentos"),
                    "law_discounts": data.get("descuentosLey"),
                    "total_discounts": data.get("totalDescuentos"),
                    "net": data.get("neto"),
                    "salary_method": data.get("formaSalario"),
                    "salary_type_id": data.get("idTipoSalario"),
                    "salary_method_id": data.get("idFormaSalario"),
                }

                payrolls.append(PayrollSummary(**mapped_data))
            
            return payrolls

        except Exception as e:
            print(f"Error al parsear la respuesta al modelo PayrollSummary: {e}")
            return None
    else:
        print(f"Error en la solicitud: {response.status_code} - {response.text}")
        return None


@mcp.tool()
def employee(name:str)-> list[EmployeeModel] | None:
    """
        Busca empleados por nombre y devuelve una lista de objetos EmployeeModel.

        Parámetros:
            name (str): El nombre del empleado a buscar.

        Retorna:
            - Una lista de instancias de EmployeeModel que coinciden con el nombre proporcionado, incluye ausencias, horarios, colaboradores y supervisor.
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
def employees()-> list[EmployeeModel] | None:
    """
        Busca empleados devuelve una lista de objetos EmployeeModel.

        Retorna:
            - Una lista de instancias de EmployeeModel, incluye ausencias, horarios, colaboradores y supervisor.
    """

    
   
    response = r.get(url=f"{RRHH_BASE_URL}/empleados/empleados", headers=header)  
    
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
            - Una instancia de EmployeeModel que representa al empleado encontrado, incluye ausencias, horarios, colaboradores , supervisor, prestamos y volantes de pagos"""
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
    

@mcp.tool()
def add_absence(employee_id, from_date, to_date, comment, reason_code, cantidad) -> dict:
    """
    Establece una ausencia para un empleado.
    
    Parámetros:
        param employee_id: ID del empleado (int).
        param from_date: Fecha de inicio de la ausencia ejemplo: "2025-05-22T08:00:00".
        param to_date: Fecha de fin de la ausencia ejemplo: "2025-05-22T08:00:00.
        param comment: Comentario sobre la ausencia.
        param reason_code: Código de la razón de la ausencia (int).
        reason_codes:         
            "vacaciones: 1,
            "licencia": 2,
            "permiso_dias": 3,
            "permiso_horas": 4,
            "excusa": 5
        
    
    Retorna:
         - diccionario con la respuesta de la insercion.
    """
    
    
    #employee_id = st.session_state.me.id
    supervisor = 1074
    body = [{
        "Id_AccionWeb": 12,
        "Id_Registro_Relacionado": employee_id,
        "Fecha_Inicio": from_date,
        "Fecha_Fin": to_date,
        "Comentario": comment,
        "Tipo_Ausencia": reason_code,
        "Cantidad": cantidad,
        "Persona_Asignada": supervisor,
    }]
    
    response = r.request("POST", url=f"{RRHH_BASE_URL}/empleados/TransaccionAccionPersonalEmpleado", headers=header, json=body)

    if response.status_code == 200:
        data = response.json()['result']
    
    return data


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"


@mcp.tool()
def echo_tool(message: str) -> str:
    """Echo a message as a tool"""
    return f"Tool echo: {message}"


@mcp.prompt()
def echo_prompt(message: str) -> str:
    """Create an echo prompt"""
    return f"Please process this message: {message}"


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"



if __name__ == "__main__":
    mcp.run()