import os
import json
import requests
from io import BytesIO
from datetime import date

class RadicacionSuraApi:

    def __init__(self, base_url: str, token: str, email_notificacion: str):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.email_notificacion = email_notificacion
        self.headers = {
            "x-apptag-token": self.token,
            "Origin": "https://procesadorrips.segurossura.com.co",
            "Referer": "https://procesadorrips.segurossura.com.co/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*"
        }


    def _procesar_respuesta(self, response):
        """
        Procesa la respuesta de un request HTTP, validando el estado y el contenido.
        Retorna un diccionario con la respuesta JSON o un error estructurado.
        """
        try:
            json_response = response.json()
        except ValueError:
            print("Error: La respuesta no es un JSON válido.")
            return {
                "error": "Respuesta no es JSON",
                "status_code": response.status_code,
                "contenido": response.text
            }

        if response.status_code == 200:
            return json_response
        else:
            print(f"Error en la respuesta: {json_response}")
            return {
                "error": "Respuesta con error",
                "status_code": response.status_code,
                "contenido": json_response
            }


    def cargar_facturas(self, archivo_path) -> str:
        """
        Carga un archivo PDF al endpoint de SURA con datos del prestador.
        
        - token: str, token de autorización.
        - archivo_path: str, ruta local al archivo PDF.
        """

        # Fecha actual para el radicado
        hoy = date.today()
        fecha_formateada = f"{hoy.year}/{hoy.month}/{hoy.day}"

        url = f"{self.base_url}/api/v1/fe/loadFile"
        nombre_archivo = os.path.basename(archivo_path)

        fields = {
            "version": "V2",
            "folder": nombre_archivo,  # <- esto debe ser igual al nombre real
            "data": (
                '{"lineaNegocio":"EPS","fechaCarga":"2025/6/6","nombrePlan":"Plan de beneficio en salud",'
                f'"nombrePrestador":"AVIDANTI SAS","emailPrestador":"{self.email_notificacion}",'
                '"dniPrestador":"800185449","nitDv":"8001854499","tipoDocumento":"A"}'
            )
        }

        with open(archivo_path, "rb") as f:
            files = {
                "file": (nombre_archivo, f, "application/pdf")
            }
            response = requests.post(url, headers=self.headers, data=fields, files=files)

        print("Código de estado:", response.status_code)

        try:
            return response.status_code
        except ValueError:
            print("No se pudo decodificar la respuesta como JSON.")
            return {"error": "Respuesta no es JSON", "contenido": response.text}


    def cargar_soportes(self, carpeta_path: str, nombre_factura: int) -> dict:
        """Carga todos los archivos PDF dentro de una carpeta al endpoint /load/support."""

        url = f"{self.base_url}/api/v1/load/support"
        folder = nombre_factura
        data_json = json.dumps({
            "lineaNegocio": "EPS",
            "fechaCarga": "2025/6/6",
            "nombrePlan": "Plan de beneficio en salud",
            "nombrePrestador": "AVIDANTI SAS",
            "emailPrestador": self.email_notificacion,
            "dniPrestador": "800185449",
            "tipoDniPrestador": "A",
            "idProveedor": "800185449",
            "tipoIdProveedor": "A",
            "nitDv": "8001854499"
        })
        data = {
            "version": "V2",
            "folder": folder,
            "data": data_json
        }

        files = []
        archivos_abiertos = []

        for nombre_archivo in os.listdir(carpeta_path):
            if nombre_archivo.lower().endswith(".pdf"):
                ruta_archivo = os.path.join(carpeta_path, nombre_archivo)
                f = open(ruta_archivo, "rb")
                archivos_abiertos.append(f)
                files.append(("file", (nombre_archivo, f, "application/pdf")))

        if not files:
            print("[cargar_soportes_desde_carpeta] No se encontraron archivos PDF en la carpeta.")
            return {"error": "No hay archivos PDF en la carpeta para cargar."}

        try:
            response = requests.post(url, headers=self.headers, data=data, files=files)
            print(f"[cargar_soportes_desde_carpeta] Código de estado: {response.status_code}")
            return self._procesar_respuesta(response)
        finally:
            for f in archivos_abiertos:
                f.close()

        
    def cargar_rips(self, archivo_json_path, archivo_txt_path, nombre_factura):
        url = f"{self.base_url}/api/v1/rips/loadJson"
        nombre_json = os.path.basename(archivo_json_path)
        nombre_txt = os.path.basename(archivo_txt_path)
        folder = nombre_factura
        fields = {
            "version": "V2",
            "folder": folder,
            "lineaNegocio": "EPS",
            "email": self.email_notificacion
        }
        headers = {
            "x-apptag-token": self.token,
            "Origin": "https://procesadorrips.segurossura.com.co",
            "Referer": "https://procesadorrips.segurossura.com.co/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*"
        }
        with open(archivo_json_path, "rb") as f_json, open(archivo_txt_path, "rb") as f_txt:
            files = {
                "file": (nombre_json, f_json, "application/json"),
                "cuv": (nombre_txt, f_txt, "text/plain")
            }
            response = requests.post(url, headers=headers, data=fields, files=files)
        print("Código de estado:", response.status_code)
        try:
            return response.json()
        except ValueError:
            print("No se pudo decodificar la respuesta como JSON.")
            return {"error": "Respuesta no es JSON", "contenido": response.text}


    def enviar_archivos(self, lista_facturas_procesadas, lista_soportes_procesados, lista_rips_procesados) -> dict:
            """Carga múltiples archivos RIPS al endpoint /load/files."""

            url = f"{self.base_url}/api/v1/load/files"

            data_payload = {
                "lineaNegocio": "EPS",
                "fechaCarga": "2025/6/6",
                "nombrePlan": "Plan de beneficio en salud",
                "nombrePrestador": "AVIDANTI SAS",
                "emailPrestador": self.email_notificacion,
                "dniPrestador": "800185449",
                "idProveedor": "800185449",
                "tipoIdProveedor": "A",
                "tipoDniPrestador": "A"
            }

            body_payload = {
                "fileRips": lista_rips_procesados,
                "fileElectronic": lista_facturas_procesadas,
                "soportes": lista_soportes_procesados
            }

            def fake_file(name):
                return (name, BytesIO(b"contenido de prueba"))

            files = {
                'data': (None, json.dumps(data_payload), 'application/json'),
                'body': (None, json.dumps(body_payload), 'application/json'),
                'typeDocument': (None, 'Factura'),
                'version': (None, 'V2'),
            }

            for f in body_payload["fileRips"] + body_payload["fileElectronic"] + body_payload["soportes"]:
                files[f] = fake_file(f)

            response = requests.post(url, headers=self.headers, files=files)
            print(f"[cargar_archivos_rips] Código de estado: {response.status_code}")
            return self._procesar_respuesta(response)
