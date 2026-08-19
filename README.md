# YOLO - Detección, Tracking y Entrenamiento

Este proyecto utiliza **Ultralytics YOLOv8** para realizar detección y seguimiento de objetos mediante visión computacional.

Los scripts incluidos permiten trabajar principalmente con:

* Videos de YouTube.
* Cámaras IP mediante RTSP.
* Modelos YOLO personalizados en formato `.pt`.
* Datasets creados y etiquetados en Roboflow.
* Registro de detecciones en una base de datos MySQL.
* Entrenamiento local desde Visual Studio Code.
* Entrenamiento desde Google Colab.

> **Importante:** los nombres de carpetas, modelos, datasets y proyectos utilizados en este documento son ejemplos.
> Pueden cambiarse dependiendo del equipo o proyecto donde se utilice YOLO.

---

# 📂 Estructura general del proyecto

Una estructura básica del proyecto puede ser:

```text
PROYECTO_YOLO/
│
├── best_reentrenado.pt
├── deteccion_senales_yt.py
├── deteccion_senales_roboflow.py
├── entrenar.py
└── README.md
```

El archivo:

```text
best_reentrenado.pt
```

representa el modelo YOLO entrenado utilizado por los scripts de detección.

Los scripts están preparados para buscar el modelo dentro de la misma carpeta donde se encuentra el código Python.

Por ejemplo:

```text
PROYECTO_YOLO/
│
├── best_reentrenado.pt
└── deteccion_senales_roboflow.py
```

Esto permite copiar todo el proyecto a otra computadora o carpeta sin depender de rutas específicas como:

```text
C:\GeneradorSenales
```

---

# ⚙️ INSTALACIÓN DEL PROYECTO

Esta configuración solamente necesita realizarse **una vez por computadora**.

Después de instalar todo correctamente, para utilizar normalmente el proyecto solamente será necesario:

```text
1. Abrir XAMPP.
2. Iniciar MySQL.
3. Abrir la carpeta del proyecto.
4. Ejecutar el script requerido.
```

---

# 🐍 1. Instalar Python

Es necesario tener Python instalado.

Se recomienda utilizar una versión moderna, por ejemplo:

```text
Python 3.11
```

o:

```text
Python 3.12
```

Durante la instalación de Python activar la opción:

```text
Add Python to PATH
```

Después abrir PowerShell, CMD o la terminal integrada de Visual Studio Code.

Comprobar:

```powershell
py --version
```

Debe aparecer algo parecido a:

```text
Python 3.12.x
```

---

# 🗄️ 2. Instalar XAMPP

Los scripts de detección utilizan una base de datos MySQL para registrar los objetos detectados.

Por este motivo es necesario instalar:

```text
XAMPP
```

Una vez instalado, abrir:

```text
XAMPP Control Panel
```

e iniciar:

```text
MySQL
```

No es necesario iniciar Apache para ejecutar estos scripts.

El flujo normal será:

```text
XAMPP
   ↓
MySQL
   ↓
Start
```

---

# 📦 3. Instalar las librerías necesarias

Abrir PowerShell, CMD o la terminal integrada de Visual Studio Code.

Primero actualizar `pip`:

```powershell
py -m pip install --upgrade pip
```

Después instalar todas las librerías utilizadas por los scripts:

```powershell
py -m pip install -U ultralytics opencv-python mysql-connector-python yt-dlp
```

---

## ¿Para qué sirve cada librería?

### ultralytics

```text
ultralytics
```

Es la librería principal de YOLO.

Permite:

* Cargar modelos `.pt`.
* Detectar objetos.
* Realizar tracking.
* Entrenar modelos.
* Validar modelos.
* Dibujar cajas de detección.

---

### opencv-python

```text
opencv-python
```

Instala la librería:

```python
cv2
```

Se utiliza para:

* Leer videos.
* Leer cámaras.
* Mostrar imágenes.
* Mostrar ventanas en tiempo real.
* Guardar videos procesados.
* Dibujar información sobre los frames.

---

### mysql-connector-python

```text
mysql-connector-python
```

Permite conectar Python con MySQL.

Se utiliza para guardar información como:

```text
Fecha y hora
Tipo de objeto
Track ID
Confianza
```

---

### yt-dlp

```text
yt-dlp
```

Se utiliza en el script de YouTube.

Permite descargar temporalmente un video de YouTube para posteriormente procesarlo con YOLO.

---

# ✅ 4. Comprobar que todo esté instalado

Ejecutar:

```powershell
py -c "from ultralytics import YOLO; import cv2; import mysql.connector; import yt_dlp; print('TODO INSTALADO CORRECTAMENTE')"
```

Si todo está correctamente instalado aparecerá:

```text
TODO INSTALADO CORRECTAMENTE
```

Si este comando funciona, la computadora ya cuenta con las principales dependencias necesarias para ejecutar el proyecto.

---

# 🗄️ 5. Configuración de MySQL

Los scripts utilizan una conexión MySQL similar a:

```python
host="localhost"
user="root"
password=""
```

Esto corresponde normalmente a una instalación local de XAMPP donde el usuario:

```text
root
```

no tiene contraseña.

Si en otra computadora MySQL utiliza contraseña, será necesario modificar:

```python
password=""
```

por:

```python
password="CONTRASEÑA"
```

---

# 🗃️ 6. Base de datos

Los scripts pueden crear automáticamente la base de datos utilizada para registrar las detecciones.

Por ejemplo:

```text
registro_senales_db
```

y una tabla similar a:

```text
registros_roboflow
```

donde se guarda información como:

```text
id
fecha_hora
tipo_objeto
track_id
confianza
```

Por lo tanto, normalmente no es necesario crear manualmente la base de datos.

Solamente se debe iniciar:

```text
XAMPP → MySQL
```

antes de ejecutar los scripts de detección.

---

# 🧠 7. Modelo YOLO

Los modelos entrenados tienen extensión:

```text
.pt
```

Ejemplos:

```text
best.pt
best_reentrenado.pt
modelo_v1.pt
modelo_senales.pt
```

Los scripts del proyecto utilizan por defecto:

```text
best_reentrenado.pt
```

El modelo debe colocarse dentro de la misma carpeta que los scripts.

Ejemplo:

```text
PROYECTO_YOLO/
│
├── best_reentrenado.pt
├── deteccion_senales_yt.py
└── deteccion_senales_roboflow.py
```

---

# 🔄 8. Utilizar otro modelo

Cuando se entrena YOLO normalmente se genera:

```text
best.pt
```

Si se desea utilizar ese nuevo modelo existen dos opciones.

## Opción 1 - Renombrar el modelo

Cambiar:

```text
best.pt
```

por:

```text
best_reentrenado.pt
```

y colocarlo dentro de la carpeta del proyecto.

---

## Opción 2 - Cambiar el nombre dentro del código

Si se desea conservar el nombre:

```text
best_nuevo.pt
```

se puede modificar:

```python
NOMBRE_MODELO = "best_reentrenado.pt"
```

por:

```python
NOMBRE_MODELO = "best_nuevo.pt"
```

---

# ▶️ 9. Ejecutar detección sobre un video de YouTube

El script:

```text
deteccion_senales_yt.py
```

realiza aproximadamente el siguiente proceso:

```text
Enlace de YouTube
       ↓
yt-dlp descarga el video
       ↓
OpenCV abre el video
       ↓
YOLO procesa los frames
       ↓
YOLO detecta los objetos
       ↓
Tracking asigna IDs
       ↓
Las detecciones se guardan en MySQL
       ↓
Se genera un video procesado
```

Antes de ejecutarlo:

```text
1. Abrir XAMPP.
2. Iniciar MySQL.
3. Verificar que exista el modelo .pt.
4. Revisar el enlace de YouTube configurado.
```

Ejecutar:

```powershell
py deteccion_senales_yt.py
```

El enlace del video puede cambiarse dentro del código:

```python
url_youtube = "URL_DEL_VIDEO"
```

---

# 📹 10. Ejecutar detección con cámara IP / RTSP

El script:

```text
deteccion_senales_roboflow.py
```

está diseñado para trabajar con una cámara IP mediante RTSP.

Antes de ejecutarlo se deben revisar los datos de la cámara:

```text
Dirección IP
Usuario
Contraseña
Puerto
Ruta RTSP
```

Ejemplo genérico:

```python
url_camara = "rtsp://USUARIO:CONTRASEÑA@IP/RUTA_RTSP"
```

La computadora debe tener comunicación de red con la cámara.

Después ejecutar:

```powershell
py deteccion_senales_roboflow.py
```

El programa:

```text
Lee la cámara
      ↓
YOLO analiza los frames
      ↓
Detecta objetos
      ↓
Asigna Track IDs
      ↓
Filtra por confianza
      ↓
Guarda detecciones en MySQL
      ↓
Muestra las cajas en pantalla
```

> No publicar usuarios, contraseñas, IPs privadas o direcciones RTSP reales en repositorios públicos.

---

# 🧠 ENTRENAMIENTO DE MODELOS YOLO

Los datasets utilizados para entrenar los modelos se preparan y etiquetan utilizando:

```text
Roboflow
```

Existen dos formas principales para entrenar:

```text
1. Entrenamiento local desde Visual Studio Code.
2. Entrenamiento desde Google Colab.
```

En ambos casos se puede utilizar como modelo base:

```text
yolov8n.pt
```

Al finalizar el entrenamiento YOLO generará principalmente:

```text
best.pt
last.pt
```

El modelo que normalmente se utiliza después es:

```text
best.pt
```

---

# 💻 ENTRENAMIENTO LOCAL

# 11. Exportar el dataset desde Roboflow

Cuando el dataset ya esté:

* Etiquetado.
* Revisado.
* Con las clases correctas.
* Con una versión generada.

Entrar a la versión correspondiente dentro de Roboflow.

Seleccionar:

```text
Download Dataset
```

Elegir formato:

```text
YOLOv8
```

y descargar:

```text
ZIP
```

---

# 12. Extraer el ZIP

Extraer el ZIP descargado.

En Windows se recomienda utilizar una ruta corta para evitar errores de:

```text
Ruta demasiado larga
```

Por ejemplo:

```text
C:\dataset-yolo
```

También podría ser:

```text
C:\dataset-roboflow
C:\dataset-v1
D:\dataset-senales
```

El nombre puede ser cualquiera.

Lo importante es conocer la ruta completa.

---

# 📂 13. Estructura del dataset

Roboflow normalmente genera una estructura similar a:

```text
DATASET/
│
├── data.yaml
│
├── train/
│   ├── images/
│   └── labels/
│
├── valid/
│   ├── images/
│   └── labels/
│
└── test/
    ├── images/
    └── labels/
```

Roboflow ya genera automáticamente:

```text
train
valid
test
images
labels
data.yaml
```

No es necesario crear esos archivos manualmente.

---

# 🔎 14. Comprobar data.yaml

Antes de entrenar es recomendable comprobar que el archivo:

```text
data.yaml
```

existe.

Desde PowerShell:

```powershell
Get-ChildItem "RUTA_DEL_DATASET" -Filter data.yaml -Recurse
```

Por ejemplo:

```powershell
Get-ChildItem "C:\dataset-yolo" -Filter data.yaml -Recurse
```

Debe mostrar una ruta similar a:

```text
C:\dataset-yolo\data.yaml
```

El archivo `data.yaml` le indica a YOLO:

* Dónde están las imágenes.
* Dónde están las etiquetas.
* Cuáles son las clases del dataset.
* Qué carpetas son entrenamiento y validación.

---

# 🐍 15. Crear entrenar.py

Dentro del proyecto crear:

```text
entrenar.py
```

Ejemplo:

```text
PROYECTO_YOLO/
│
├── entrenar.py
├── deteccion_senales_yt.py
├── deteccion_senales_roboflow.py
└── ...
```

Pegar el siguiente código:

```python
from ultralytics import YOLO
import os


# ============================================================
# CONFIGURACIÓN
# ============================================================

# Modelo YOLO que se utilizará como base.
# Si yolov8n.pt no existe en la PC, Ultralytics
# puede descargarlo automáticamente.
MODELO_BASE = "yolov8n.pt"


# Ruta donde se extrajo el ZIP de Roboflow.
#
# CAMBIAR ESTA RUTA por la ruta real donde se
# encuentra el dataset en la computadora.
CARPETA_DATASET = r"C:\RUTA\DEL\DATASET"


# Número de épocas.
#
# Una época significa que YOLO recorrió una vez
# todo el conjunto de imágenes de entrenamiento.
EPOCHS = 100


# Resolución utilizada durante el entrenamiento.
IMGSZ = 640


# Nombre con el que se guardará este entrenamiento.
#
# Es recomendable utilizar un nombre diferente
# para cada prueba o versión.
NOMBRE_ENTRENAMIENTO = "modelo_v1"


# ============================================================
# FUNCIÓN PARA BUSCAR data.yaml
# ============================================================

def buscar_data_yaml(carpeta):

    # Recorre todas las carpetas internas del dataset.
    for raiz, carpetas, archivos in os.walk(carpeta):

        # Si encuentra data.yaml devuelve su ruta.
        if "data.yaml" in archivos:

            return os.path.join(
                raiz,
                "data.yaml"
            )

    # Si no encuentra data.yaml devuelve None.
    return None


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("")
    print("==============================================")
    print("          ENTRENAMIENTO LOCAL YOLO")
    print("==============================================")
    print("")


    # ========================================================
    # RUTA DEL PROYECTO
    # ========================================================

    # Obtiene automáticamente la carpeta donde
    # está guardado entrenar.py.
    ruta_proyecto = os.path.dirname(
        os.path.abspath(__file__)
    )

    print("[PROYECTO]")
    print(ruta_proyecto)
    print("")


    # ========================================================
    # COMPROBAR DATASET
    # ========================================================

    print("[SISTEMA] Buscando dataset...")


    # Comprueba que la carpeta configurada exista.
    if not os.path.exists(CARPETA_DATASET):

        print("")
        print("[ERROR] No se encontró la carpeta:")
        print(CARPETA_DATASET)

        print("")
        print(
            "Revisa CARPETA_DATASET y confirma "
            "la ubicación donde extrajiste el ZIP."
        )

        return


    # ========================================================
    # BUSCAR data.yaml
    # ========================================================

    data_yaml = buscar_data_yaml(
        CARPETA_DATASET
    )


    # Si no encontró el archivo, detener.
    if data_yaml is None:

        print("")
        print("[ERROR] No se encontró data.yaml.")

        print("")
        print(
            "Comprueba que el ZIP de Roboflow "
            "se haya extraído completamente."
        )

        return


    print("")
    print("[DATASET ENCONTRADO]")
    print(data_yaml)
    print("")


    # ========================================================
    # CARGAR MODELO YOLO
    # ========================================================

    print("[SISTEMA] Cargando modelo base:")
    print(MODELO_BASE)
    print("")


    model = YOLO(
        MODELO_BASE
    )


    # ========================================================
    # INICIAR ENTRENAMIENTO
    # ========================================================

    print("==============================================")
    print("          INICIANDO ENTRENAMIENTO")
    print("==============================================")
    print("")


    model.train(

        # Archivo generado por Roboflow.
        data=data_yaml,

        # Cantidad de épocas.
        epochs=EPOCHS,

        # Resolución utilizada.
        imgsz=IMGSZ,

        # Carpeta donde se guardarán
        # todos los resultados.
        project=os.path.join(
            ruta_proyecto,
            "runs",
            "entrenamientos"
        ),

        # Nombre del entrenamiento.
        name=NOMBRE_ENTRENAMIENTO,

        # Guardar los pesos del modelo.
        save=True,

        # Crear gráficas del entrenamiento.
        plots=True
    )


    # ========================================================
    # UBICACIÓN DEL MODELO RESULTANTE
    # ========================================================

    ruta_best = os.path.join(
        ruta_proyecto,
        "runs",
        "entrenamientos",
        NOMBRE_ENTRENAMIENTO,
        "weights",
        "best.pt"
    )


    print("")
    print("==============================================")
    print("         ENTRENAMIENTO TERMINADO")
    print("==============================================")
    print("")

    print("[MEJOR MODELO GENERADO]")
    print("")
    print(ruta_best)
    print("")


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":
    main()
```

---

# ⚙️ 16. Qué cambiar antes de entrenar

Antes de ejecutar:

```powershell
py entrenar.py
```

revisar las variables del inicio.

---

## MODELO_BASE

```python
MODELO_BASE = "yolov8n.pt"
```

Indica qué modelo se utilizará como punto de partida.

Para crear un nuevo modelo utilizando YOLOv8:

```python
MODELO_BASE = "yolov8n.pt"
```

Si después se desea continuar entrenando un modelo propio:

```python
MODELO_BASE = r"C:\Modelos\best.pt"
```

---

## CARPETA_DATASET

```python
CARPETA_DATASET = r"C:\RUTA\DEL\DATASET"
```

Debe cambiarse por la ruta real.

Por ejemplo:

```python
CARPETA_DATASET = r"C:\dataset-yolo"
```

o:

```python
CARPETA_DATASET = r"D:\datasets\senalizacion"
```

La `r` antes de las comillas permite trabajar correctamente con rutas de Windows.

---

## EPOCHS

```python
EPOCHS = 100
```

Una época significa una pasada completa por el dataset.

Para una prueba corta:

```python
EPOCHS = 20
```

Para un entrenamiento normal:

```python
EPOCHS = 100
```

También puede utilizarse:

```python
EPOCHS = 150
```

dependiendo del proyecto.

---

## IMGSZ

```python
IMGSZ = 640
```

Representa la resolución utilizada durante el entrenamiento.

Como configuración inicial se recomienda mantener:

```text
640
```

---

## NOMBRE_ENTRENAMIENTO

```python
NOMBRE_ENTRENAMIENTO = "modelo_v1"
```

Sirve para identificar los resultados.

Por ejemplo:

```python
NOMBRE_ENTRENAMIENTO = "modelo_v1"
```

Otro entrenamiento:

```python
NOMBRE_ENTRENAMIENTO = "modelo_v2"
```

Otro:

```python
NOMBRE_ENTRENAMIENTO = "prueba_150_epochs"
```

Esto permite conservar varias pruebas separadas.

---

# ▶️ 17. Ejecutar entrenamiento local

Abrir la carpeta del proyecto en Visual Studio Code.

Abrir la terminal integrada y ejecutar:

```powershell
py entrenar.py
```

El código realizará:

```text
Busca la carpeta del dataset
        ↓
Busca data.yaml
        ↓
Carga yolov8n.pt
        ↓
Utiliza el dataset de Roboflow
        ↓
Entrena el modelo
        ↓
Guarda los resultados
        ↓
Genera best.pt
```

El entrenamiento puede tardar desde minutos hasta varias horas dependiendo de:

* Cantidad de imágenes.
* Número de épocas.
* Resolución.
* Procesador.
* Tarjeta gráfica.
* Capacidad general de la computadora.

---

# 📦 18. Resultado del entrenamiento local

Al terminar se generará una estructura similar a:

```text
PROYECTO_YOLO/
└── runs/
    └── entrenamientos/
        └── modelo_v1/
            └── weights/
                ├── best.pt
                └── last.pt
```

El archivo principal es:

```text
best.pt
```

Ese archivo contiene el modelo entrenado.

---

# ☁️ ENTRENAMIENTO DESDE GOOGLE COLAB

Google Colab permite realizar el entrenamiento desde el navegador.

En este método:

```text
Roboflow descarga automáticamente el dataset
                    ↓
Google Colab realiza el entrenamiento
                    ↓
Google Drive guarda los resultados
```

---

# 19. Crear un Notebook de Google Colab

Abrir Google Colab y crear un Notebook nuevo.

---

# 📦 20. Instalar Ultralytics y Roboflow

Primera celda:

```python
# Instala las librerías necesarias para:
# - Descargar el dataset desde Roboflow.
# - Entrenar YOLO.

!pip install -U ultralytics roboflow
```

---

# ☁️ 21. Conectar Google Drive

Nueva celda:

```python
# Conecta Google Drive con Google Colab.
#
# Esto permite guardar los resultados del entrenamiento
# en Drive y conservarlos después de cerrar Colab.

from google.colab import drive

drive.mount("/content/drive")
```

Google solicitará autorización.

---

# 📂 22. Crear una carpeta para guardar los entrenamientos

Nueva celda:

```python
import os


# Ruta de Google Drive donde se guardarán los resultados.
#
# El nombre PROYECTO_YOLO puede cambiarse.
RUTA_DRIVE = (
    "/content/drive/MyDrive/"
    "PROYECTO_YOLO"
)


# Crear automáticamente la carpeta de entrenamientos.
os.makedirs(
    f"{RUTA_DRIVE}/entrenamientos",
    exist_ok=True
)


print("Carpeta lista:")
print(RUTA_DRIVE)
```

Por ejemplo, podría cambiarse:

```python
RUTA_DRIVE = (
    "/content/drive/MyDrive/"
    "DeteccionSenales"
)
```

---

# 🤖 23. Obtener el código de Roboflow

Entrar al dataset terminado en Roboflow.

Buscar:

```text
Versions
→ Seleccionar versión
→ Download Dataset
→ YOLOv8
→ Show Download Code
```

Roboflow generará un código similar a:

```python
from roboflow import Roboflow


# Conexión a Roboflow.
rf = Roboflow(
    api_key="TU_API_KEY"
)


# Seleccionar workspace y proyecto.
project = rf.workspace(
    "TU_WORKSPACE"
).project(
    "TU_PROYECTO"
)


# Seleccionar la versión del dataset.
version = project.version(
    NUMERO_VERSION
)


# Descargar el dataset en formato YOLOv8.
dataset = version.download(
    "yolov8"
)
```

Los siguientes valores cambian dependiendo de cada proyecto:

```text
TU_API_KEY
TU_WORKSPACE
TU_PROYECTO
NUMERO_VERSION
```

Lo recomendable es copiar directamente el código generado por Roboflow.

> **IMPORTANTE:** la API Key es privada.
> No debe colocarse en GitHub, README, repositorios públicos ni capturas compartidas.

---

# ✅ 24. Comprobar que Roboflow descargó correctamente el dataset

Después de ejecutar el código de Roboflow:

```python
import os


# Construir la ruta al archivo data.yaml.
DATA_YAML = os.path.join(
    dataset.location,
    "data.yaml"
)


print("Dataset descargado en:")
print(dataset.location)


print("")


print("Archivo data.yaml:")
print(DATA_YAML)


print("")


print("¿Existe?")
print(
    os.path.exists(DATA_YAML)
)
```

El resultado importante es:

```text
True
```

Si aparece:

```text
True
```

significa que el dataset está listo para ser utilizado por YOLO.

---

# 🧠 25. Entrenar YOLO en Google Colab

Nueva celda:

```python
from ultralytics import YOLO


# ============================================================
# CONFIGURACIÓN
# ============================================================

# Modelo utilizado como punto de partida.
MODELO_BASE = "yolov8n.pt"


# Cantidad de épocas.
EPOCHS = 100


# Resolución de entrenamiento.
IMGSZ = 640


# Nombre de este entrenamiento.
NOMBRE_ENTRENAMIENTO = "modelo_v1"


# ============================================================
# CARGAR MODELO
# ============================================================

model = YOLO(
    MODELO_BASE
)


# ============================================================
# ENTRENAMIENTO
# ============================================================

results = model.train(

    # Dataset descargado desde Roboflow.
    data=DATA_YAML,

    # Cantidad de épocas.
    epochs=EPOCHS,

    # Resolución.
    imgsz=IMGSZ,

    # Guardar los resultados directamente
    # en Google Drive.
    project=f"{RUTA_DRIVE}/entrenamientos",

    # Nombre de esta ejecución.
    name=NOMBRE_ENTRENAMIENTO
)
```

---

# ⚙️ 26. Qué cambiar antes de entrenar en Colab

Revisar:

```python
MODELO_BASE = "yolov8n.pt"

EPOCHS = 100

IMGSZ = 640

NOMBRE_ENTRENAMIENTO = "modelo_v1"
```

El nombre puede cambiarse para cada entrenamiento.

Ejemplo:

```python
NOMBRE_ENTRENAMIENTO = "modelo_v2"
```

o:

```python
NOMBRE_ENTRENAMIENTO = "senalizacion_v3"
```

---

# 📍 27. Saber dónde quedó best.pt

Cuando termine el entrenamiento ejecutar:

```python
print("Mejor modelo generado:")

print(
    model.trainer.best
)
```

Mostrará una ruta similar a:

```text
/content/drive/MyDrive/PROYECTO_YOLO/entrenamientos/modelo_v1/weights/best.pt
```

El archivo:

```text
best.pt
```

se encuentra guardado en Google Drive.

Por lo tanto, aunque posteriormente se cierre Google Colab, el modelo permanecerá en Drive.

---

# 📥 28. Utilizar el modelo generado

Después de obtener:

```text
best.pt
```

descargarlo desde Google Drive.

Después colocarlo dentro de la carpeta del proyecto local.

Por ejemplo:

```text
PROYECTO_YOLO/
│
├── best_reentrenado.pt
├── deteccion_senales_yt.py
└── deteccion_senales_roboflow.py
```

Si los scripts esperan:

```text
best_reentrenado.pt
```

se puede renombrar:

```text
best.pt
```

como:

```text
best_reentrenado.pt
```

También puede mantenerse otro nombre cambiando:

```python
NOMBRE_MODELO = "best_reentrenado.pt"
```

---

# 🔄 29. Resumen del entrenamiento local

```text
ROBOFLOW
   ↓
Dataset terminado
   ↓
Generar versión
   ↓
Exportar como YOLOv8
   ↓
Descargar ZIP
   ↓
Extraer en una ruta corta
   ↓
Comprobar data.yaml
   ↓
Configurar entrenar.py
   ↓
py entrenar.py
   ↓
Esperar entrenamiento
   ↓
best.pt
```

---

# ☁️ 30. Resumen del entrenamiento en Google Colab

```text
ROBOFLOW
   ↓
Dataset terminado
   ↓
Generar versión
   ↓
Show Download Code
   ↓
GOOGLE COLAB
   ↓
Instalar ultralytics + roboflow
   ↓
Conectar Google Drive
   ↓
Ejecutar código generado por Roboflow
   ↓
Comprobar data.yaml
   ↓
Ejecutar entrenamiento
   ↓
Esperar
   ↓
best.pt guardado en Google Drive
```

---

# 🛠️ 31. Problemas comunes

## Error: No module named ultralytics

Ejecutar:

```powershell
py -m pip install -U ultralytics
```

---

## Error: No module named cv2

Ejecutar:

```powershell
py -m pip install -U opencv-python
```

---

## Error: No module named mysql

Ejecutar:

```powershell
py -m pip install -U mysql-connector-python
```

---

## Error: No module named yt_dlp

Ejecutar:

```powershell
py -m pip install -U yt-dlp
```

---

## Error al conectar con MySQL

Comprobar:

```text
XAMPP
→ MySQL
→ Running
```

También revisar dentro del código:

```python
host
user
password
```

---

## No se encuentra el modelo

Comprobar que el archivo:

```text
best_reentrenado.pt
```

esté en la misma carpeta que los scripts.

Ejemplo:

```text
PROYECTO_YOLO/
│
├── best_reentrenado.pt
├── deteccion_senales_yt.py
└── deteccion_senales_roboflow.py
```

---

## No se encuentra data.yaml

En entrenamiento local ejecutar:

```powershell
Get-ChildItem "RUTA_DEL_DATASET" -Filter data.yaml -Recurse
```

Después comprobar que esta variable tenga la ruta correcta:

```python
CARPETA_DATASET = r"C:\RUTA\DEL\DATASET"
```

---

## Windows muestra "ruta demasiado larga"

Extraer el dataset en una ubicación más corta.

Por ejemplo:

```text
C:\dataset-yolo
```

en lugar de una ruta larga como:

```text
C:\Users\Usuario\Documents\Proyectos\ProyectoYOLO\Datasets\Versiones\Version10\...
```

---

# 📌 32. Comandos rápidos

## Instalar todo en una PC nueva

```powershell
py -m pip install --upgrade pip
```

Después:

```powershell
py -m pip install -U ultralytics opencv-python mysql-connector-python yt-dlp
```

---

## Comprobar instalación

```powershell
py -c "from ultralytics import YOLO; import cv2; import mysql.connector; import yt_dlp; print('TODO INSTALADO CORRECTAMENTE')"
```

---

## Ejecutar detección sobre YouTube

```powershell
py deteccion_senales_yt.py
```

---

## Ejecutar cámara RTSP

```powershell
py deteccion_senales_roboflow.py
```

---

## Entrenar localmente

```powershell
py entrenar.py
```

---

# ✅ 33. Uso normal del proyecto

Una vez que la computadora ya tiene Python y todas las librerías instaladas:

```text
Abrir XAMPP
     ↓
Iniciar MySQL
     ↓
Abrir proyecto
     ↓
Verificar modelo .pt
     ↓
Ejecutar script
```

Por ejemplo:

```powershell
py deteccion_senales_yt.py
```

o:

```powershell
py deteccion_senales_roboflow.py
```

No es necesario crear ni activar un entorno virtual.

---

# ✅ 34. Flujo para entrenar

Para entrenamiento local:

```text
Roboflow
   ↓
Descargar ZIP
   ↓
Extraer dataset
   ↓
Configurar entrenar.py
   ↓
py entrenar.py
   ↓
best.pt
```

Para Google Colab:

```text
Roboflow
   ↓
Obtener código de descarga
   ↓
Colab
   ↓
Conectar Drive
   ↓
Descargar dataset
   ↓
Entrenar
   ↓
best.pt guardado en Drive
```

XAMPP y MySQL **no son necesarios durante el entrenamiento**.

Solamente se utilizan posteriormente cuando los scripts de detección necesitan registrar los objetos detectados.
