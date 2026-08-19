# ITS YOLO - Detección de Señales y Objetos

Este repositorio contiene los scripts utilizados para la detección de señales de tránsito, vehículos y otros objetos mediante modelos de visión computacional basados en **YOLO**.

El proyecto permite realizar detecciones utilizando diferentes fuentes de video:

* Cámara IP mediante transmisión **RTSP**.
* Videos de **YouTube**.
* Cámara conectada al equipo.
* Modelos YOLO genéricos.
* Modelos YOLO entrenados específicamente para tráfico y señalizaciones.

---

# 📂 Estructura del proyecto

La estructura principal es:

```text
its-yolo/
│
├── best_masentrenado.pt
├── best_reentrenado.pt
├── camara_yolo.py
├── deteccion_senales_roboflow.py
├── deteccion_senales_yt.py
├── README.md
└── .gitignore
```

Los modelos `.pt` deben permanecer dentro de la carpeta principal junto con los scripts de Python.

## Modelo recomendado

Actualmente se recomienda utilizar:

```text
best_reentrenado.pt
```

No es necesario crear una carpeta adicional en el disco `C:` para almacenar los modelos.

---

# 🐍 1. Instalar Python

Para utilizar el proyecto es necesario tener instalado Python.

Se recomienda utilizar:

```text
Python 3.11
```

o:

```text
Python 3.12
```

Durante la instalación de Python se recomienda activar:

```text
Add Python to PATH
```

Para comprobar la instalación:

```powershell
py --version
```

o:

```powershell
python --version
```

Ejemplo:

```text
Python 3.12.x
```

---

# ⚙️ 2. Instalar dependencias

Las dependencias solamente necesitan instalarse una vez en la computadora.

Actualizar `pip`:

```powershell
py -m pip install --upgrade pip
```

Instalar las librerías utilizadas por el proyecto:

```powershell
py -m pip install -U ultralytics opencv-python mysql-connector-python yt-dlp
```

Principales dependencias:

```text
ultralytics
    Ejecución, entrenamiento y tracking de modelos YOLO.

opencv-python
    Lectura y procesamiento de cámaras, videos e imágenes.

mysql-connector-python
    Conexión de Python con MySQL.

yt-dlp
    Descarga de videos de YouTube.
```

---

# ✅ 3. Verificar dependencias

Ejecutar:

```powershell
py -c "from ultralytics import YOLO; import cv2; import mysql.connector; import yt_dlp; print('TODO INSTALADO CORRECTAMENTE')"
```

Resultado esperado:

```text
TODO INSTALADO CORRECTAMENTE
```

---

# 🧠 4. Verificar el modelo

El archivo:

```text
best_reentrenado.pt
```

debe encontrarse en la misma carpeta que los scripts.

Para comprobar que puede cargarse:

```powershell
py -c "from ultralytics import YOLO; modelo=YOLO('best_reentrenado.pt'); print(modelo.names)"
```

Esto mostrará las clases que reconoce el modelo.

Ejemplo:

```text
{0: 'clase_1', 1: 'clase_2', 2: 'clase_3'}
```

---

# 🗄️ 5. XAMPP y MySQL

Los scripts que registran detecciones requieren MySQL.

Antes de ejecutarlos:

1. Abrir **XAMPP Control Panel**.
2. Localizar **MySQL**.
3. Presionar **Start**.

Debe aparecer:

```text
MySQL → Running
```

No es necesario iniciar Apache para ejecutar YOLO.

Solamente:

```text
MySQL
```

---

# 🔐 6. Configuración de MySQL

Actualmente los scripts utilizan:

```text
Host: localhost
Usuario: root
Contraseña: vacía
```

Equivalente a:

```python
host="localhost"
user="root"
password=""
```

Si el usuario `root` tiene contraseña, será necesario modificar:

```python
password=""
```

por:

```python
password="CONTRASEÑA"
```

---

# 🗃️ 7. Base de datos

El sistema puede crear automáticamente:

```text
registro_senales_db
```

y la tabla:

```text
registros_roboflow
```

donde pueden almacenarse:

```text
ID
Fecha y hora
Tipo de objeto
Track ID
Confianza
```

Por lo tanto, normalmente solamente es necesario iniciar MySQL desde XAMPP.

---

# ▶️ 8. Ejecutar detección de YouTube

Archivo:

```text
deteccion_senales_yt.py
```

Antes de ejecutarlo:

1. Abrir XAMPP.
2. Iniciar MySQL.
3. Abrir la carpeta `its-yolo`.
4. Verificar que exista `best_reentrenado.pt`.

Ejecutar:

```powershell
py deteccion_senales_yt.py
```

El flujo es:

```text
Video de YouTube
       ↓
Descarga del video
       ↓
Modelo YOLO
       ↓
Detección
       ↓
Tracking
       ↓
Registro en MySQL
       ↓
Video procesado
```

---

# 🎥 9. Ejecutar cámara IP / RTSP

Archivo:

```text
deteccion_senales_roboflow.py
```

Ejecutar:

```powershell
py deteccion_senales_roboflow.py
```

Antes de utilizarlo deben comprobarse los datos de la cámara configurados dentro del código:

```text
Dirección IP
Usuario
Contraseña
Puerto
Ruta RTSP
```

La computadora debe tener acceso de red a la cámara.

Se recomienda utilizar:

```text
best_reentrenado.pt
```

---

# 📷 10. Ejecutar camara_yolo.py

Archivo:

```text
camara_yolo.py
```

Ejecutar:

```powershell
py camara_yolo.py
```

Este script puede utilizarse principalmente para pruebas de:

* Cámara.
* OpenCV.
* YOLO.
* Detección de objetos generales.

---

# 🎮 11. Comprobar GPU

Si la computadora cuenta con tarjeta gráfica NVIDIA:

```powershell
nvidia-smi
```

También se puede comprobar desde Python:

```powershell
py -c "import torch; print('CUDA disponible:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

Resultado deseado:

```text
CUDA disponible: True
GPU: NVIDIA GeForce ...
```

Si aparece:

```text
CUDA disponible: False
```

YOLO podrá funcionar mediante CPU, pero el entrenamiento y procesamiento serán considerablemente más lentos.

---

# 🔁 12. Uso normal del proyecto

Después de realizar la instalación inicial no es necesario volver a instalar las dependencias.

Cada vez que se quiera utilizar:

```text
1. Abrir XAMPP
2. Iniciar MySQL
3. Abrir la carpeta its-yolo
4. Ejecutar el script requerido
```

Por ejemplo:

```powershell
py deteccion_senales_yt.py
```

---

# 🧠 ENTRENAMIENTO DE MODELOS YOLO

Además de utilizar los modelos existentes, este proyecto permite entrenar nuevos modelos o continuar entrenando:

```text
best_reentrenado.pt
```

El entrenamiento puede realizarse de dos formas:

```text
1. Entrenamiento local
2. Entrenamiento mediante Google Colab
```

Para ambos métodos se necesita primero un dataset correctamente etiquetado.

---

# 📚 13. Preparar el dataset

Para entrenar YOLO se necesitan:

```text
Imágenes
+
Etiquetas
```

Cada imagen utilizada para entrenamiento debe tener su correspondiente archivo `.txt`.

Ejemplo:

```text
imagen001.jpg
imagen001.txt

imagen002.jpg
imagen002.txt
```

La estructura recomendada es:

```text
dataset/
│
├── data.yaml
│
├── images/
│   │
│   ├── train/
│   │   ├── imagen001.jpg
│   │   ├── imagen002.jpg
│   │   └── ...
│   │
│   ├── val/
│   │   ├── imagen101.jpg
│   │   ├── imagen102.jpg
│   │   └── ...
│   │
│   └── test/
│       └── ...
│
└── labels/
    │
    ├── train/
    │   ├── imagen001.txt
    │   ├── imagen002.txt
    │   └── ...
    │
    ├── val/
    │   ├── imagen101.txt
    │   ├── imagen102.txt
    │   └── ...
    │
    └── test/
        └── ...
```

La carpeta `test` es opcional.

Las carpetas necesarias como mínimo son:

```text
images/train
images/val
labels/train
labels/val
```

---

# 🏷️ 14. Etiquetas YOLO

Cada archivo `.txt` contiene las coordenadas de los objetos encontrados en la imagen.

Formato:

```text
clase centro_x centro_y ancho alto
```

Ejemplo:

```text
0 0.515625 0.423611 0.150000 0.220000
```

Si hay varios objetos en una imagen:

```text
0 0.515625 0.423611 0.150000 0.220000
1 0.720000 0.330000 0.110000 0.180000
2 0.220000 0.600000 0.200000 0.250000
```

Cada línea representa un objeto.

Las coordenadas utilizadas por YOLO están normalizadas.

---

# 📄 15. Crear data.yaml

El archivo:

```text
data.yaml
```

le indica a YOLO dónde se encuentra el dataset y qué clases debe detectar.

Ejemplo para entrenamiento local:

```yaml
path: C:/Users/USUARIO/Documents/its-yolo/dataset

train: images/train
val: images/val
test: images/test

names:
  0: clase_1
  1: clase_2
  2: clase_3
```

Las clases deben sustituirse por las clases reales del proyecto.

Para consultar las clases del modelo actual:

```powershell
py -c "from ultralytics import YOLO; modelo=YOLO('best_reentrenado.pt'); print(modelo.names)"
```

Si se va a continuar entrenando el mismo modelo con las mismas clases, se recomienda conservar los mismos nombres y el mismo orden de clases.

---

# 📁 16. Estructura para entrenamiento local

Cuando se vaya a entrenar localmente se pueden agregar:

```text
its-yolo/
│
├── best_masentrenado.pt
├── best_reentrenado.pt
│
├── camara_yolo.py
├── deteccion_senales_roboflow.py
├── deteccion_senales_yt.py
│
├── entrenar_modelo.py
│
├── dataset/
│   ├── data.yaml
│   ├── images/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   │
│   └── labels/
│       ├── train/
│       ├── val/
│       └── test/
│
├── README.md
└── .gitignore
```

La carpeta `dataset` y `entrenar_modelo.py` solamente son necesarios si se desea realizar entrenamiento local.

---

# 💻 17. Entrenar localmente

Para entrenar utilizando el modelo actual como punto de partida se recomienda continuar desde:

```text
best_reentrenado.pt
```

Esto permite aprovechar todo lo que el modelo ya aprendió anteriormente.

Crear un archivo llamado:

```text
entrenar_modelo.py
```

con el siguiente contenido:

```python
from ultralytics import YOLO
import torch


def main():

    print("")
    print("==========================================")
    print("       ENTRENAMIENTO YOLO")
    print("==========================================")
    print("")

    # Comprobar dispositivo
    if torch.cuda.is_available():

        dispositivo = 0

        print("[SISTEMA] GPU detectada:")
        print(torch.cuda.get_device_name(0))

    else:

        dispositivo = "cpu"

        print("[SISTEMA] No se encontró GPU CUDA.")
        print("[SISTEMA] Se utilizará CPU.")


    print("")
    print("[SISTEMA] Cargando modelo...")
    print("")


    # Continuar entrenamiento desde el modelo actual
    modelo = YOLO(
        "best_reentrenado.pt"
    )


    # Entrenamiento
    modelo.train(

        # Dataset
        data="dataset/data.yaml",

        # Número de épocas
        epochs=100,

        # Resolución de entrenamiento
        imgsz=640,

        # GPU o CPU
        device=dispositivo,

        # Carpeta donde se guardarán resultados
        project="entrenamientos",

        # Nombre del entrenamiento
        name="reentrenamiento"
    )


    print("")
    print("==========================================")
    print("       ENTRENAMIENTO TERMINADO")
    print("==========================================")
    print("")


if __name__ == "__main__":
    main()
```

---

# ▶️ 18. Ejecutar entrenamiento local

Abrir una terminal dentro de:

```text
its-yolo
```

y ejecutar:

```powershell
py entrenar_modelo.py
```

Si existe una GPU compatible con CUDA, el programa intentará utilizarla.

Si no existe, utilizará CPU.

Durante el entrenamiento aparecerán datos similares a:

```text
Epoch
GPU_mem
box_loss
cls_loss
dfl_loss
Instances
Size
```

Ejemplo:

```text
1/100
2/100
3/100
...
100/100
```

Cada época representa una vuelta completa al dataset de entrenamiento.

---

# 📦 19. Resultado del entrenamiento local

Al utilizar:

```python
project="entrenamientos"
name="reentrenamiento"
```

se generará una estructura similar a:

```text
its-yolo/
│
└── entrenamientos/
    └── reentrenamiento/
        │
        ├── weights/
        │   ├── best.pt
        │   └── last.pt
        │
        ├── results.csv
        ├── results.png
        └── ...
```

Los dos archivos principales son:

```text
best.pt
last.pt
```

## best.pt

Es el modelo que obtuvo el mejor resultado durante el entrenamiento.

Este es normalmente el archivo que se utiliza posteriormente para detección.

## last.pt

Es el modelo correspondiente al último estado guardado del entrenamiento.

Puede utilizarse para continuar un entrenamiento interrumpido.

---

# 🔄 20. Reemplazar el modelo anterior

Después de validar que el nuevo:

```text
best.pt
```

funciona correctamente, se puede copiar a la carpeta principal.

Ejemplo:

```text
entrenamientos/
└── reentrenamiento/
    └── weights/
        └── best.pt
```

Copiarlo a:

```text
its-yolo/
```

y renombrarlo, por ejemplo:

```text
best_reentrenado_nuevo.pt
```

Antes de reemplazar definitivamente:

```text
best_reentrenado.pt
```

se recomienda conservar una copia del modelo anterior.

---

# 🧪 21. Probar el modelo nuevo

Para revisar sus clases:

```powershell
py -c "from ultralytics import YOLO; modelo=YOLO('best_reentrenado_nuevo.pt'); print(modelo.names)"
```

También se puede probar sobre una imagen:

```powershell
yolo predict model=best_reentrenado_nuevo.pt source="imagen_prueba.jpg" show=True
```

O mediante Python:

```python
from ultralytics import YOLO

modelo = YOLO(
    "best_reentrenado_nuevo.pt"
)

modelo.predict(
    source="imagen_prueba.jpg",
    show=True,
    conf=0.35
)
```

Después de comprobar que funciona correctamente se puede utilizar en los scripts principales.

---

# 🆕 22. Entrenar un modelo desde un modelo genérico

Si se desea realizar un entrenamiento nuevo en lugar de continuar desde:

```text
best_reentrenado.pt
```

se puede utilizar un modelo YOLOv8 preentrenado.

Ejemplo:

```python
from ultralytics import YOLO


def main():

    modelo = YOLO(
        "yolov8n.pt"
    )

    modelo.train(
        data="dataset/data.yaml",
        epochs=100,
        imgsz=640,
        project="entrenamientos",
        name="modelo_nuevo"
    )


if __name__ == "__main__":
    main()
```

La primera vez que se utilice:

```text
yolov8n.pt
```

Ultralytics puede descargar automáticamente el modelo si no existe en la computadora.

---

# ⚡ 23. Entrenamiento mediante comando

También es posible entrenar sin crear `entrenar_modelo.py`.

Para continuar entrenando el modelo personalizado:

```powershell
yolo detect train model=best_reentrenado.pt data=dataset/data.yaml epochs=100 imgsz=640
```

Para entrenar desde un YOLOv8 genérico:

```powershell
yolo detect train model=yolov8n.pt data=dataset/data.yaml epochs=100 imgsz=640
```

Sin embargo, para este proyecto se recomienda utilizar:

```text
entrenar_modelo.py
```

porque permite controlar y documentar más fácilmente la configuración utilizada.

---

# ⏯️ 24. Continuar un entrenamiento interrumpido

Si un entrenamiento se interrumpe, se puede continuar utilizando:

```text
last.pt
```

Ejemplo:

```python
from ultralytics import YOLO


def main():

    modelo = YOLO(
        "entrenamientos/reentrenamiento/weights/last.pt"
    )

    modelo.train(
        resume=True
    )


if __name__ == "__main__":
    main()
```

Ejecutar:

```powershell
py continuar_entrenamiento.py
```

Esto permite continuar desde el punto donde quedó el entrenamiento anterior.

---

# ☁️ ENTRENAMIENTO EN GOOGLE COLAB

Google Colab permite utilizar una computadora remota desde el navegador.

Esto resulta útil cuando:

* La computadora local no tiene GPU.
* La GPU local no es suficientemente potente.
* Se desea realizar el entrenamiento sin ocupar la computadora principal.

---

# ☁️ 25. Preparar archivos para Google Colab

Para entrenar mediante Colab se recomienda preparar:

```text
dataset.zip
best_reentrenado.pt
```

El archivo:

```text
dataset.zip
```

debe contener:

```text
dataset/
│
├── data.yaml
│
├── images/
│   ├── train/
│   ├── val/
│   └── test/
│
└── labels/
    ├── train/
    ├── val/
    └── test/
```

También subir:

```text
best_reentrenado.pt
```

si se desea continuar entrenando el modelo actual.

---

# 📁 26. Crear carpeta en Google Drive

Se recomienda crear en Google Drive:

```text
ITS-YOLO
```

y colocar:

```text
Google Drive/
└── ITS-YOLO/
    ├── dataset.zip
    └── best_reentrenado.pt
```

Los resultados del entrenamiento también pueden guardarse dentro de esta carpeta.

---

# 🌐 27. Abrir Google Colab

Crear un nuevo Notebook de Google Colab.

Antes de iniciar el entrenamiento cambiar el entorno de ejecución para utilizar GPU.

Buscar la configuración:

```text
Entorno de ejecución
        ↓
Cambiar tipo de entorno de ejecución
        ↓
Acelerador de hardware
        ↓
GPU
```

La disponibilidad y modelo exacto de GPU pueden variar dependiendo de Google Colab.

---

# 🎮 28. Comprobar GPU en Colab

Primera celda:

```python
!nvidia-smi
```

Después:

```python
import torch

print(
    "CUDA disponible:",
    torch.cuda.is_available()
)

if torch.cuda.is_available():

    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )
```

Resultado esperado:

```text
CUDA disponible: True
```

---

# ⚙️ 29. Instalar Ultralytics en Colab

Ejecutar:

```python
!pip install -U ultralytics
```

Después comprobar:

```python
from ultralytics import YOLO

print(
    "Ultralytics instalado correctamente"
)
```

---

# ☁️ 30. Conectar Google Drive

Ejecutar:

```python
from google.colab import drive

drive.mount(
    "/content/drive"
)
```

Google solicitará autorización para acceder a Drive.

Después podrá utilizarse:

```text
/content/drive/MyDrive/
```

---

# 📦 31. Extraer el dataset

Si se guardó:

```text
Google Drive/ITS-YOLO/dataset.zip
```

ejecutar:

```python
!mkdir -p /content/its-yolo
```

Después:

```python
!unzip -q "/content/drive/MyDrive/ITS-YOLO/dataset.zip" -d "/content/its-yolo"
```

La estructura resultante debe quedar:

```text
/content/its-yolo/
└── dataset/
    ├── data.yaml
    ├── images/
    └── labels/
```

---

# 📄 32. Modificar data.yaml para Colab

En la computadora local el archivo podría utilizar:

```yaml
path: C:/Users/USUARIO/Documents/its-yolo/dataset
```

Esa ruta no existe en Google Colab.

Para Colab debe utilizarse:

```yaml
path: /content/its-yolo/dataset

train: images/train
val: images/val
test: images/test

names:
  0: clase_1
  1: clase_2
  2: clase_3
```

IMPORTANTE:

Los nombres de las clases deben ser los mismos utilizados por el dataset.

Si se continúa entrenando:

```text
best_reentrenado.pt
```

se recomienda mantener las mismas clases y el mismo orden.

---

# 🧠 33. Entrenar best_reentrenado.pt en Google Colab

El modelo se encuentra en:

```text
/content/drive/MyDrive/ITS-YOLO/best_reentrenado.pt
```

Ejecutar:

```python
from ultralytics import YOLO


modelo = YOLO(
    "/content/drive/MyDrive/ITS-YOLO/best_reentrenado.pt"
)


resultados = modelo.train(

    data="/content/its-yolo/dataset/data.yaml",

    epochs=100,

    imgsz=640,

    device=0,

    project="/content/drive/MyDrive/ITS-YOLO/entrenamientos",

    name="reentrenamiento_colab"
)
```

En este caso:

```text
device=0
```

indica que se utilizará la GPU principal asignada por Google Colab.

---

# 📦 34. Resultado del entrenamiento en Colab

Los resultados quedarán guardados directamente en Google Drive:

```text
Google Drive/
└── ITS-YOLO/
    └── entrenamientos/
        └── reentrenamiento_colab/
            └── weights/
                ├── best.pt
                └── last.pt
```

El modelo recomendado para utilizar posteriormente es:

```text
best.pt
```

---

# ⏯️ 35. Continuar entrenamiento en Colab

Si el entrenamiento se interrumpe y existe:

```text
last.pt
```

se puede continuar:

```python
from ultralytics import YOLO


modelo = YOLO(
    "/content/drive/MyDrive/ITS-YOLO/entrenamientos/reentrenamiento_colab/weights/last.pt"
)


modelo.train(
    resume=True
)
```

---

# 🆕 36. Entrenar desde YOLOv8n en Google Colab

Si se desea generar un nuevo modelo en lugar de continuar el actual:

```python
from ultralytics import YOLO


modelo = YOLO(
    "yolov8n.pt"
)


modelo.train(

    data="/content/its-yolo/dataset/data.yaml",

    epochs=100,

    imgsz=640,

    device=0,

    project="/content/drive/MyDrive/ITS-YOLO/entrenamientos",

    name="modelo_nuevo_colab"
)
```

---

# 📥 37. Utilizar el modelo generado en el proyecto

Después del entrenamiento descargar o copiar:

```text
best.pt
```

a la carpeta:

```text
its-yolo/
```

Se recomienda primero renombrarlo:

```text
best_reentrenado_nuevo.pt
```

La estructura sería:

```text
its-yolo/
│
├── best_reentrenado.pt
├── best_reentrenado_nuevo.pt
├── deteccion_senales_yt.py
├── deteccion_senales_roboflow.py
└── ...
```

Primero probar el modelo nuevo.

Cuando se confirme que funciona correctamente, puede sustituirse el modelo anterior.

---

# 📊 38. Qué significa epochs

Durante el entrenamiento se utiliza:

```python
epochs=100
```

Una época representa una pasada completa por todas las imágenes del conjunto de entrenamiento.

Ejemplo:

```text
Epoch 1
    YOLO analiza todo el dataset

Epoch 2
    YOLO vuelve a analizar todo el dataset

...

Epoch 100
```

Más épocas no garantizan automáticamente un mejor modelo.

Es importante revisar los resultados de validación obtenidos durante el entrenamiento.

---

# 🖼️ 39. Qué significa imgsz

En los ejemplos se utiliza:

```python
imgsz=640
```

Esto indica el tamaño utilizado por YOLO durante el entrenamiento.

Para el entrenamiento inicial del proyecto se recomienda comenzar con:

```text
640
```

Posteriormente puede ajustarse dependiendo del rendimiento de la GPU y del tamaño de los objetos que se desean detectar.

---

# 🎯 40. Reentrenar o comenzar desde cero

## Si ya existe un modelo bueno

Utilizar:

```python
modelo = YOLO(
    "best_reentrenado.pt"
)
```

Este es el método recomendado para seguir mejorando el modelo actual con nuevas imágenes correctamente etiquetadas.

## Si se desea crear un modelo nuevo

Utilizar:

```python
modelo = YOLO(
    "yolov8n.pt"
)
```

Esto permite comenzar desde un modelo YOLOv8 genérico preentrenado.

---

# ⚠️ 41. Recomendaciones antes de entrenar

Antes de comenzar:

* Revisar que todas las imágenes estén correctamente etiquetadas.
* Revisar que las clases estén en el orden correcto.
* Evitar imágenes sin sus respectivos archivos de etiquetas cuando deberían contener objetos.
* Separar correctamente las imágenes de entrenamiento y validación.
* Verificar `data.yaml`.
* Comprobar que el modelo `.pt` pueda cargarse.
* Verificar la GPU si se va a utilizar CUDA.
* Conservar una copia del modelo anterior.
* No reemplazar `best_reentrenado.pt` hasta validar el nuevo modelo.

---

# 🛑 42. XAMPP no es necesario para entrenar

La base de datos MySQL se utiliza durante los scripts de detección.

Para ejecutar:

```text
entrenar_modelo.py
```

no es necesario iniciar:

```text
XAMPP
MySQL
```

El entrenamiento solamente necesita:

```text
Python
Ultralytics
Dataset
Modelo YOLO
GPU o CPU
```

XAMPP vuelve a ser necesario cuando se ejecuten los scripts que registran las detecciones en MySQL.

---

# 🛠️ 43. Problemas comunes

## Python no se reconoce

Probar:

```powershell
py --version
```

Si tampoco funciona, instalar Python y agregarlo al PATH.

---

## No se encuentra Ultralytics

Error:

```text
ModuleNotFoundError: No module named 'ultralytics'
```

Solución:

```powershell
py -m pip install -U ultralytics
```

---

## No se encuentra OpenCV

Error:

```text
ModuleNotFoundError: No module named 'cv2'
```

Solución:

```powershell
py -m pip install opencv-python
```

---

## No se encuentra MySQL Connector

Error:

```text
ModuleNotFoundError: No module named 'mysql'
```

Solución:

```powershell
py -m pip install mysql-connector-python
```

---

## No se encuentra yt-dlp

Error:

```text
ModuleNotFoundError: No module named 'yt_dlp'
```

Solución:

```powershell
py -m pip install -U yt-dlp
```

---

## Error al conectar con MySQL

Comprobar:

```text
XAMPP
↓
MySQL
↓
Running
```

También revisar:

```text
host
usuario
contraseña
```

---

## No se encuentra el modelo

Comprobar que:

```text
best_reentrenado.pt
```

esté dentro de:

```text
its-yolo/
```

---

## Error de dataset durante entrenamiento

Comprobar:

```text
dataset/data.yaml
dataset/images/train
dataset/images/val
dataset/labels/train
dataset/labels/val
```

También comprobar que los nombres de las imágenes coincidan con sus archivos `.txt`.

Ejemplo correcto:

```text
images/train/carro001.jpg
labels/train/carro001.txt
```

---

## CUDA disponible aparece False

Ejecutar:

```powershell
nvidia-smi
```

y:

```powershell
py -c "import torch; print(torch.cuda.is_available())"
```

Si existe una GPU NVIDIA pero PyTorch no reconoce CUDA, revisar la instalación de PyTorch y los controladores NVIDIA.

El entrenamiento también puede realizarse utilizando Google Colab.

---

# 📌 44. Comandos principales

## Instalar dependencias

```powershell
py -m pip install --upgrade pip
```

```powershell
py -m pip install -U ultralytics opencv-python mysql-connector-python yt-dlp
```

## Comprobar dependencias

```powershell
py -c "from ultralytics import YOLO; import cv2; import mysql.connector; import yt_dlp; print('TODO INSTALADO CORRECTAMENTE')"
```

## Ver clases

```powershell
py -c "from ultralytics import YOLO; modelo=YOLO('best_reentrenado.pt'); print(modelo.names)"
```

## Ejecutar YouTube

```powershell
py deteccion_senales_yt.py
```

## Ejecutar RTSP

```powershell
py deteccion_senales_roboflow.py
```

## Ejecutar cámara

```powershell
py camara_yolo.py
```

## Entrenar localmente

```powershell
py entrenar_modelo.py
```

## Comprobar GPU

```powershell
nvidia-smi
```

```powershell
py -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

---

# ✅ Flujo completo del proyecto

## Utilizar un modelo

```text
Abrir XAMPP
      ↓
Iniciar MySQL
      ↓
Abrir its-yolo
      ↓
Ejecutar script
      ↓
YOLO detecta objetos
      ↓
Tracking
      ↓
Registro en MySQL
```

## Entrenar localmente

```text
Recolectar imágenes
      ↓
Etiquetar imágenes
      ↓
Crear dataset YOLO
      ↓
Configurar data.yaml
      ↓
py entrenar_modelo.py
      ↓
Entrenamiento
      ↓
best.pt
      ↓
Probar modelo
      ↓
Utilizarlo en el proyecto
```

## Entrenar en Google Colab

```text
Preparar dataset.zip
      ↓
Subir a Google Drive
      ↓
Abrir Google Colab
      ↓
Activar GPU
      ↓
Instalar Ultralytics
      ↓
Montar Google Drive
      ↓
Extraer dataset
      ↓
Entrenar
      ↓
best.pt guardado en Drive
      ↓
Copiar a its-yolo
      ↓
Probar modelo
```

---

# 📌 Nota final

Para utilizar normalmente el sistema no es necesario entrenar nuevamente el modelo.

El entrenamiento solamente debe realizarse cuando se quiera:

* Agregar nuevas imágenes.
* Mejorar detecciones existentes.
* Mejorar detecciones bajo diferentes condiciones.
* Agregar más variedad al dataset.
* Corregir clases que el modelo no detecta correctamente.
* Generar una nueva versión del modelo.

El modelo recomendado actualmente para ejecutar el proyecto es:

```text
best_reentrenado.pt
```

Antes de sustituirlo por un nuevo entrenamiento, siempre se recomienda conservar una copia del modelo anterior.
