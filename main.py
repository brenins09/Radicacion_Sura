import os
from dotenv import load_dotenv
from pages.login_sura import login_sura
from api.radicacion_sura_api import RadicacionSuraApi
from core.perocesamiento_archivos import ProcesamientoArchivo


nombre_carpeta_rips         = "JSON"
nombre_carpeta_soportes     = "Soportes"
email_notificaciones        = "lfvaldes@cyt.com.co"
base_url                    = "https://apiprocesadorrips.segurossura.com.co"
path_carpeta_soportes       = r"C:\Users\Usuario\Downloads\sura"


#cargar el archivo env y llamar las variables
load_dotenv()
url_sura = os.getenv("URL")
usuario_sura = os.getenv("USUARIO")
contrasenia_sura = os.getenv("CONTRASENIA")


#Llamar el loguin para obtener la cookies de inicio de sesion
#token = login_sura(usuario_sura, contrasenia_sura, url_sura)
token = "2411e1e08e48b6e1e8f160e8e708d5ff61885496a3a4aa926f951a162294f041"
print(f"Token de acceso: {token}")


# Instancias clases "ProcesamientoArchivos" y "RadicacionSuraApi"
procesamiento_archivos = ProcesamientoArchivo(path_carpeta_soportes)
api = RadicacionSuraApi(base_url, token, email_notificaciones)

# Descomprimir los soportes
nombres_facturas = procesamiento_archivos.obtener_nombres_facturas()
procesamiento_archivos.descomprimir_soportes()
print(f"Obtuvo los nombres de las facturas {nombres_facturas}")


#-------CARGAR LAS FACTURAS-------
print("<<<<<<<<<<<<<<<<<<<<<<<<<FACTURAS>>>>>>>>>>>>>>>>>>>>>>>")
listado_facturas_procesadas = []
for nombre_factura in nombres_facturas:
    ruta_pdf_factura = os.path.join(path_carpeta_soportes, nombre_carpeta_soportes, nombre_factura + ".pdf")
    print(f"Ruta completa de la factura a cargar: {ruta_pdf_factura}")
    respuesta_carga_factura = api.cargar_facturas(ruta_pdf_factura)
    print(f"Respues de la carga de facturas{respuesta_carga_factura}")
    if respuesta_carga_factura == 200:
        print(f"Factura: {nombre_factura} cargada exitosamente!")
        listado_facturas_procesadas.append(nombre_factura + ".pdf")


#-------CARGAR LOS SOPORTES------
print("<<<<<<<<<<<<<<<<<<<<<<<<<SPORTES>>>>>>>>>>>>>>>>>>>>>>>")
print(f"Asi quedaron las facturas procesadas: {listado_facturas_procesadas}")
listado_soportes_procesados = []
for nombre_factura in nombres_facturas:
    print("Antes de validar si la factura si fue cargada exitosamente en los soportes!")
    if f"{nombre_factura}.pdf" in listado_facturas_procesadas:
        print(f"Si la factura fue cargada exitosamente y se encuetra en la lista de procesadas")
        carpeta_soportes = os.path.join(path_carpeta_soportes, nombre_carpeta_soportes, nombre_factura, nombre_factura)
        respuesta_carga_soportes = api.cargar_soportes(carpeta_soportes, nombre_factura)
        print(f"Esta es la respues de los soportes cargados: {respuesta_carga_soportes}")
        nombres_soportes_estructurados = procesamiento_archivos.esrtucturar_nombres(respuesta_carga_soportes)
        print(f"Despues de estructurar los nombres: {nombres_soportes_estructurados}")
        listado_soportes_procesados.extend(nombres_soportes_estructurados)


#-------CARGAR LOS RIPS---------
print("<<<<<<<<<<<<<<<<<<<<<<<<<RIPS>>>>>>>>>>>>>>>>>>>>>>>")
listado_rips_procesados = []
carpeta_rips = os.path.join(path_carpeta_soportes, nombre_carpeta_rips)
for nombre_subcarpeta in os.listdir(carpeta_rips):
    print("Antes de validar si la factura si fue cargada exitosamente en los rips!")
    if f"{nombre_factura}.pdf" in listado_facturas_procesadas:
        print(f"Si la factura fue cargada exitosamente y se encuetra en la lista de procesadas en los rips")
        ruta_subcarpeta = os.path.join(carpeta_rips, nombre_subcarpeta)
        if os.path.isdir(ruta_subcarpeta):
            # Obtener los archivos dentro de la subcarpeta
            archivos = os.listdir(ruta_subcarpeta)
            ruta_archivo_1 = os.path.join(ruta_subcarpeta, archivos[0])
            ruta_archivo_2 = os.path.join(ruta_subcarpeta, archivos[1])
            print(f"Archivo1: {ruta_archivo_1}; archivo2: {ruta_archivo_2} nombre de la factura: {nombre_subcarpeta}")
            respuesta_carga_rips = api.cargar_rips(ruta_archivo_1, ruta_archivo_2, nombre_subcarpeta)
            if archivos[1].lower().endswith('.json'):
                listado_rips_procesados.append(archivos[1])
            elif archivos[0].lower().endswith('.json'):
                listado_rips_procesados.append(archivos[0])




#------ENVIAR LOS ARCHIVOS-------


#listas de lo que se proceso
print("--------------------------------------------")
print(f"Listado facturas: {listado_facturas_procesadas}")
print("--------------------------------------------")
print(f"Listado soportes: {listado_soportes_procesados}")
print("--------------------------------------------")
print(f"Listado rips: {listado_rips_procesados}")