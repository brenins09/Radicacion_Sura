import os
import re
import zipfile

class ProcesamientoArchivo:

    def __init__(self, ruta_carpeta_soportes):
        self.ruta_carpeta_soportes = ruta_carpeta_soportes


    def obtener_nombres_facturas(self):
        """Devuelve una lista con los nombres base (sin extensión) de las facturas encontradas."""
        
        carpeta_soportes = os.path.join(self.ruta_carpeta_soportes, "Soportes")
        return [
            os.path.splitext(f)[0]
            for f in os.listdir(carpeta_soportes)
            if os.path.isfile(os.path.join(carpeta_soportes, f))
            and not f.lower().endswith(".zip")
        ]


    def descomprimir_zip(self, ruta_zip, ruta_destino):
        """Descomprime un archivo ZIP si existe."""
        
        if not os.path.isfile(ruta_zip):
            print(f"Archivo ZIP no encontrado: {ruta_zip}")
            return

        os.makedirs(ruta_destino, exist_ok=True)
        with zipfile.ZipFile(ruta_zip, 'r') as archivo_zip:
            archivo_zip.extractall(ruta_destino)
            print(f"Descomprimido: {ruta_zip} {ruta_destino}")


    def descomprimir_soportes(self):
        """Orquesta la descompresión de las facturas según los nombres encontrados."""

        nombres_facturas = self.obtener_nombres_facturas()
        carpeta_soportes = os.path.join(self.ruta_carpeta_soportes, "Soportes")
        for nombre in nombres_facturas:
            ruta_zip = os.path.join(carpeta_soportes, f"{nombre}.zip")
            ruta_destino = os.path.join(carpeta_soportes, nombre)
            self.descomprimir_zip(ruta_zip, ruta_destino)

        
    def esrtucturar_nombres(self, respuesta_carga_soportes):
        nombres_archivos = [
            re.search(r'archivo (\S+\.pdf)', item['mensaje']).group(1)
            for item in respuesta_carga_soportes
            if re.search(r'archivo (\S+\.pdf)', item['mensaje'])
        ]
        return nombres_archivos

# carpeta_soportes = r"C:\Users\Usuario\Downloads\sura"
# carpeta_rips = r"C:\ruta\a\rips"
# data = [{'mensaje': 'Se carg� correctamente el archivo EPI_800185449_ACM1390708.pdf en el portal', 'numeroSolicitud': 'E462a5c44-070e-4812-9654-973ccf188c29'}, {'mensaje': 'Se carg� correctamente el archivo FEV_800185449_ACM1390708.pdf en el portal', 'numeroSolicitud': 'E462a5c44-070e-4812-9654-973ccf188c29'}, {'mensaje': 'Se carg� correctamente el archivo HAM_800185449_ACM1390708.pdf en el portal', 'numeroSolicitud': 'E462a5c44-070e-4812-9654-973ccf188c29'}, {'mensaje': 'Se carg� correctamente el archivo HAU_800185449_ACM1390708.pdf en el portal', 'numeroSolicitud': 'E462a5c44-070e-4812-9654-973ccf188c29'}, {'mensaje': 'Se carg� correctamente el archivo OPF_800185449_ACM1390708.pdf en el portal', 'numeroSolicitud': 'E462a5c44-070e-4812-9654-973ccf188c29'}, {'mensaje': 'Se carg� correctamente el archivo PDE_800185449_ACM1390708.pdf en el portal', 'numeroSolicitud': 'E462a5c44-070e-4812-9654-973ccf188c29'}, {'mensaje': 'Se carg� correctamente el archivo PDX_800185449_ACM1390708.pdf en el portal', 'numeroSolicitud': 'E462a5c44-070e-4812-9654-973ccf188c29'}, {'mensaje': 'Se carg� correctamente el archivo CRC_800185449_ACM1390708.pdf en el portal', 'numeroSolicitud': 'E462a5c44-070e-4812-9654-973ccf188c29'}]

#procesador = ProcesamientoArchivo(carpeta_soportes, carpeta_rips)
#nombres = procesador.obtener_nombres_facturas()
#print(nombres)
#procesador.descomprimir_soportes()
#salida = procesador.esrtucturar_nombres(data)
#print(salida)