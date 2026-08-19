# ITS YOLO - Detección de Señales y Objetos

Proyecto de visión computacional basado en **YOLO** para detectar señales de tránsito, vehículos y otros objetos mediante cámara IP/RTSP o videos de YouTube.

---

## 📂 Estructura del proyecto

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

El modelo recomendado actualmente es:

```text
best_reentrenado.pt
```

Los modelos `.pt` deben permanecer dentro de la misma carpeta que los scripts.

---

# ⚙️ Instalación

## 1. Instalar Python

Se recomienda:

```text
Python 3.11 o Python 3.12
```

Durante la instalación marcar:

```text
Add Python to PATH
```

Comprobar:

```powershell
py --version
```

---

## 2. Instalar XAMPP

Instalar **XAMPP** para utilizar MySQL.

Para ejecutar los scripts solamente es necesario iniciar:

```text
MySQL
```

No es necesario iniciar Apache.

---

## 3. Instalar dependencias

Ejecutar una sola vez:

```powershell
py -m pip install --upgrade pip
```

Después:

```powershell
py -m pip install -U ultralytics opencv-python mysql-connector-python yt-dlp
```

Comprobar:

```powershell
py -c "from ultralytics import YOLO; import cv2; import mysql.connector; import yt_dlp; print('TODO INSTALADO CORRECTAMENTE')"
```

---

# 🗄️ MySQL

La configuración actual es:

```text
Host: localhost
Usuario: root
Contraseña: vacía
```

Antes de ejecutar los scripts:

```text
1. Abrir XAMPP
2. Iniciar MySQL
```

El sistema crea automáticamente la base de datos y tabla necesarias.

Si MySQL tiene contraseña para `root`, deberá modificarse también dentro de los scripts.

---

# ▶️ Ejecutar el proyecto

## Video de YouTube

```powershell
py deteccion_senales_yt.py
```

Utiliza el modelo:

```text
best_reentrenado.pt
```

---

## Cámara IP / RTSP

```powershell
py deteccion_senales_roboflow.py
```

Antes de ejecutarlo revisar en el código:

```text
IP
Usuario
Contraseña
Puerto
Ruta RTSP
```

---

## Cámara / YOLO genérico

```powershell
py camara_yolo.py
```

---

# 🎮 Comprobar GPU NVIDIA

Ejecutar:

```powershell
nvidia-smi
```

Después:

```powershell
py -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

Si aparece:

```text
CUDA: True
```

YOLO puede utilizar la GPU NVIDIA.

---

# 🧠 ENTRENAR O REENTRENAR UN MODELO

El dataset se prepara y etiqueta desde **Roboflow**.

El entrenamiento puede hacerse de dos formas:

```text
1. Localmente descargando el dataset .zip de Roboflow
2. Google Colab utilizando el código generado por Roboflow
```

---

# 📷 1. Preparar el dataset en Roboflow

Dentro de Roboflow:

```text
1. Crear o abrir el proyecto
2. Subir las imágenes
3. Etiquetar los objetos
4. Revisar las clases
5. Generar una nueva versión del dataset
6. Exportar en formato YOLOv8
```

Ejemplos de clases:

```text
alto
ceda_el_paso
carro
camion
moto
bicicleta
```

Las clases reales dependerán del proyecto.

---

# 💻 ENTRENAMIENTO LOCAL

## 2. Descargar dataset desde Roboflow

En la versión generada del dataset:

```text
Download Dataset
        ↓
Format: YOLOv8
        ↓
Download ZIP
```

Roboflow descargará un archivo `.zip` con las imágenes, etiquetas y el archivo `data.yaml`.

---

## 3. Extraer el dataset

Extraer el `.zip` dentro del proyecto y renombrar la carpeta, si es necesario, como:

```text
dataset
```

Debe quedar aproximadamente:

```text
its-yolo/
│
├── best_reentrenado.pt
│
├── dataset/
│   ├── data.yaml
│   │
│   ├── train/
│   │   ├── images/
│   │   └── labels/
│   │
│   ├── valid/
│   │   ├── images/
│   │   └── labels/
│   │
│   └── test/
│       ├── images/
│       └── labels/
│
├── deteccion_senales_yt.py
└── deteccion_senales_roboflow.py
```

La estructura exacta debe conservarse como la genere Roboflow.

No es necesario crear manualmente las etiquetas ni el `data.yaml`.

---

## 4. Revisar data.yaml

Roboflow genera automáticamente:

```text
data.yaml
```

Antes de entrenar solamente comprobar que exista.

Por ejemplo:

```text
dataset/data.yaml
```

---

## 5. Reentrenar el modelo actual

Abrir la terminal dentro de:

```text
its-yolo
```

Ejecutar:

```powershell
yolo detect train model=best_reentrenado.pt data=dataset/data.yaml epochs=100 imgsz=640
```

Esto utiliza como base:

```text
best_reentrenado.pt
```

y continúa aprendiendo utilizando el nuevo dataset exportado desde Roboflow.

---

## 6. Entrenar un modelo nuevo

Si se desea comenzar desde un YOLOv8 preentrenado:

```powershell
yolo detect train model=yolov8n.pt data=dataset/data.yaml epochs=100 imgsz=640
```

---

## 7. Resultado del entrenamiento

Al terminar se creará una carpeta similar a:

```text
runs/
└── detect/
    └── train/
        └── weights/
            ├── best.pt
            └── last.pt
```

El modelo principal generado es:

```text
best.pt
```

Se recomienda copiarlo a la carpeta principal y primero renombrarlo:

```text
best_nuevo.pt
```

Ejemplo:

```text
its-yolo/
│
├── best_reentrenado.pt
├── best_nuevo.pt
├── deteccion_senales_yt.py
└── deteccion_senales_roboflow.py
```

Primero probar `best_nuevo.pt` antes de reemplazar el modelo anterior.

---

# ☁️ ENTRENAMIENTO CON GOOGLE COLAB

En este método **no es necesario descargar manualmente el dataset `.zip`**.

Roboflow puede generar el código necesario para descargar directamente la versión del dataset dentro de Google Colab.

---

## 1. Abrir Google Colab

Crear un Notebook nuevo.

Activar GPU:

```text
Entorno de ejecución
→ Cambiar tipo de entorno de ejecución
→ GPU
```

Comprobar:

```python
!nvidia-smi
```

---

## 2. Instalar Ultralytics

Primera celda:

```python
!pip install -U ultralytics roboflow
```

---

## 3. Obtener el código desde Roboflow

Ir al proyecto de Roboflow:

```text
Proyecto
   ↓
Versions
   ↓
Seleccionar la versión
   ↓
Download Dataset
   ↓
YOLOv8
   ↓
Show Download Code
```

Roboflow mostrará un código Python específico para el proyecto.

Será similar a:

```python
from roboflow import Roboflow

rf = Roboflow(api_key="TU_API_KEY")

project = rf.workspace(
    "TU_WORKSPACE"
).project(
    "TU_PROYECTO"
)

version = project.version(
    NUMERO_VERSION
)

dataset = version.download(
    "yolov8"
)
```

**No copiar este ejemplo literalmente.**

Utilizar el código que Roboflow genere para el proyecto correspondiente.

---

## ⚠️ API Key

El código generado por Roboflow puede contener una:

```text
API Key
```

Esta clave es privada.

No debe subirse al repositorio de GitHub ni colocarse dentro del `README.md`.

Utilizarla solamente en el Notebook correspondiente.

---

## 4. Ejecutar código de Roboflow

Pegar el código proporcionado por Roboflow en una celda de Google Colab y ejecutarlo.

El dataset se descargará automáticamente dentro del entorno de Colab.

Después se puede comprobar la ruta con:

```python
print(dataset.location)
```

---

## 5. Subir el modelo actual

Si se desea continuar entrenando:

```text
best_reentrenado.pt
```

subirlo a Google Colab.

En el panel izquierdo:

```text
Archivos
→ Subir
→ best_reentrenado.pt
```

El archivo normalmente quedará en:

```text
/content/best_reentrenado.pt
```

---

## 6. Reentrenar en Google Colab

Después de ejecutar el código de Roboflow:

```python
from ultralytics import YOLO

model = YOLO(
    "/content/best_reentrenado.pt"
)

model.train(
    data=f"{dataset.location}/data.yaml",
    epochs=100,
    imgsz=640,
    device=0
)
```

El dataset descargado desde Roboflow se utilizará directamente.

---

## 7. Entrenar un modelo nuevo en Colab

Si no se desea utilizar `best_reentrenado.pt`:

```python
from ultralytics import YOLO

model = YOLO(
    "yolov8n.pt"
)

model.train(
    data=f"{dataset.location}/data.yaml",
    epochs=100,
    imgsz=640,
    device=0
)
```

---

## 8. Obtener best.pt desde Colab

Al terminar el entrenamiento se mostrará la carpeta donde fueron guardados los resultados.

Normalmente tendrá una estructura similar a:

```text
runs/
└── detect/
    └── train/
        └── weights/
            ├── best.pt
            └── last.pt
```

Descargar:

```text
best.pt
```

desde el explorador de archivos de Colab.

Después colocarlo dentro de:

```text
its-yolo/
```

y renombrarlo, por ejemplo:

```text
best_nuevo.pt
```

---

# 🧪 Probar el modelo nuevo

Desde la carpeta del proyecto:

```powershell
py -c "from ultralytics import YOLO; model=YOLO('best_nuevo.pt'); print(model.names)"
```

Para probarlo sobre una imagen:

```powershell
yolo predict model=best_nuevo.pt source="imagen_prueba.jpg" conf=0.35 show=True
```

Si el modelo funciona correctamente puede utilizarse posteriormente en:

```text
deteccion_senales_yt.py
deteccion_senales_roboflow.py
```

---

# 🔄 Resumen de entrenamiento local

```text
Roboflow
   ↓
Etiquetar imágenes
   ↓
Generar Version
   ↓
Export YOLOv8
   ↓
Download ZIP
   ↓
Extraer como dataset/
   ↓
Ejecutar:

yolo detect train model=best_reentrenado.pt data=dataset/data.yaml epochs=100 imgsz=640

   ↓
Obtener best.pt
```

---

# ☁️ Resumen de entrenamiento en Google Colab

```text
Roboflow
   ↓
Etiquetar imágenes
   ↓
Generar Version
   ↓
Download Dataset
   ↓
YOLOv8
   ↓
Show Download Code
   ↓
Copiar código a Colab
   ↓
Descargar dataset automáticamente
   ↓
Subir best_reentrenado.pt
   ↓
Entrenar
   ↓
Descargar best.pt
```

---

# 📌 Comandos principales

## Instalar proyecto

```powershell
py -m pip install --upgrade pip
```

```powershell
py -m pip install -U ultralytics opencv-python mysql-connector-python yt-dlp
```

## Ejecutar YouTube

```powershell
py deteccion_senales_yt.py
```

## Ejecutar RTSP

```powershell
py deteccion_senales_roboflow.py
```

## Entrenar localmente con dataset de Roboflow

```powershell
yolo detect train model=best_reentrenado.pt data=dataset/data.yaml epochs=100 imgsz=640
```

## Comprobar GPU

```powershell
nvidia-smi
```

---

# ✅ Uso normal

Una vez realizada la instalación:

```text
1. Abrir XAMPP
2. Iniciar MySQL
3. Abrir its-yolo
4. Ejecutar el script
```

Ejemplo:

```powershell
py deteccion_senales_yt.py
```

No es necesario crear ni activar un entorno virtual.
