import os

ruta_principal = r"C:\Users\Usuario\Downloads\sura\JSON"

# Iterar sobre cada elemento dentro de la carpeta principal
for carpeta in os.listdir(ruta_principal):
    ruta_carpeta = os.path.join(ruta_principal, carpeta)
    
    # Verificar que sea una carpeta
    if os.path.isdir(ruta_carpeta):
        print(f"Carpeta: {carpeta}")
        
        # Listar los archivos dentro de esta subcarpeta
        for archivo in os.listdir(ruta_carpeta):
            ruta_archivo = os.path.join(ruta_carpeta, archivo)
            
            # Verificar que sea un archivo
            if os.path.isfile(ruta_archivo):
                print(f"  Archivo: {archivo}")
        print()  # Línea en blanco para separar carpetas
