# CAMARA_YOLO - Detección de Señales y Objetos

Proyecto de visión computacional basado en **YOLOv8** para detectar señales de tránsito, vehículos y otros objetos mediante cámara IP/RTSP y videos de YouTube.

---

## 📂 Estructura principal

```text
CAMARA_YOLO/
│
├── imagenes/
├── runs/
│
├── best_entrenado.pt
├── best_masentrenado.pt
├── best_reentrenado.pt
├── best_roboflow.pt
├── best.pt
│
├── camara_yolo.py
├── deteccion_senales_roboflow.py
├── deteccion_senales_yt.py
├── entrenar.py
├── README.md
└── ...
```

El modelo recomendado actualmente para los scripts principales es:

```text
best_reentrenado.pt
```

Los modelos `.pt` deben permanecer dentro de la carpeta principal `CAMARA_YOLO`.

---

# ⚙️ Instalación

## 1. Instalar Python

Se recomienda utilizar:

```text
Python 3.11 o Python 3.12
```

Durante la instalación activar:

```text
Add Python to PATH
```

Comprobar la instalación:

```powershell
py --version
```

---

## 2. Instalar XAMPP

Instalar **XAMPP** para utilizar MySQL.

Para ejecutar los scripts de detección solamente es necesario iniciar:

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

Antes de utilizar los scripts que registran detecciones:

```text
1. Abrir XAMPP
2. Iniciar MySQL
3. Abrir CAMARA_YOLO
4. Ejecutar el script
```

La base de datos y tabla necesarias son creadas automáticamente por el código si todavía no existen.

Si el usuario `root` tiene contraseña, debe actualizarse también dentro de los scripts.

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

Antes de ejecutarlo revisar dentro del código:

```text
IP
Usuario
Contraseña
Puerto
Ruta RTSP
```

La computadora debe tener acceso de red a la cámara.

---

## Cámara / YOLO genérico

```powershell
py camara_yolo.py
```

---

# 🎮 Comprobar GPU NVIDIA

Si la computadora cuenta con una GPU NVIDIA:

```powershell
nvidia-smi
```

Comprobar si PyTorch puede utilizarla:

```powershell
py -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

Si aparece:

```text
CUDA: True
```

la GPU está disponible para YOLO.

---

# 🧠 ENTRENAMIENTO DE MODELOS

El entrenamiento se realiza utilizando datasets creados y etiquetados en **Roboflow**.

Existen dos formas:

```text
1. Entrenamiento local
   Roboflow → ZIP → CAMARA_YOLO → entrenar.py

2. Google Colab
   Roboflow → código de descarga → Colab → entrenamiento
```

XAMPP y MySQL **no son necesarios para entrenar**.

---

# 💻 ENTRENAMIENTO LOCAL

## 1. Preparar el dataset en Roboflow

En Roboflow:

```text
1. Abrir el proyecto
2. Subir las imágenes
3. Etiquetar los objetos
4. Revisar las clases
5. Generar una versión del dataset
6. Exportar la versión
```

Al exportar seleccionar un formato compatible con **Ultralytics YOLO / YOLOv8**.

Después seleccionar la opción para descargar el dataset como:

```text
ZIP
```

---

# 2. Extraer el ZIP

Crear dentro de `CAMARA_YOLO` una carpeta llamada:

```text
dataset
```

Extraer dentro de ella el contenido descargado desde Roboflow.

Debe quedar aproximadamente:

```text
CAMARA_YOLO/
│
├── best_reentrenado.pt
├── entrenar.py
│
├── dataset/
│   ├── data.yaml
│   ├── train/
│   │   ├── images/
│   │   └── labels/
│   ├── valid/
│   │   ├── images/
│   │   └── labels/
│   └── test/
│       ├── images/
│       └── labels/
│
└── ...
```

Roboflow genera las imágenes, etiquetas y el archivo:

```text
data.yaml
```

No es necesario crear esos archivos manualmente.

El código `entrenar.py` busca automáticamente el `data.yaml` dentro de la carpeta `dataset`.

---

# 3. Código entrenar.py

Crear el archivo:

```text
CAMARA_YOLO/entrenar.py
```

con el siguiente código:

```python
from ultralytics import YOLO
import torch
import os


# ============================================================
# CONFIGURACIÓN DEL ENTRENAMIENTO
# ============================================================

# Modelo que se utilizará como punto de partida.
MODELO = "best_reentrenado.pt"

# Carpeta donde se extrajo el ZIP de Roboflow.
CARPETA_DATASET = "dataset"

# Cantidad máxima de épocas.
EPOCHS = 100

# Tamaño de imagen utilizado durante el entrenamiento.
IMGSZ = 640

# Nombre con el que se guardará este entrenamiento.
NOMBRE_ENTRENAMIENTO = "reentrenamiento_local"


# ============================================================
# BUSCAR data.yaml DE ROBOFLOW
# ============================================================

def buscar_data_yaml(carpeta):

    for raiz, carpetas, archivos in os.walk(carpeta):

        if "data.yaml" in archivos:

            return os.path.join(
                raiz,
                "data.yaml"
            )

    return None


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("")
    print("==============================================")
    print("         ENTRENAMIENTO LOCAL YOLO")
    print("==============================================")
    print("")


    # --------------------------------------------------------
    # RUTA DEL PROYECTO
    # --------------------------------------------------------

    ruta_proyecto = os.path.dirname(
        os.path.abspath(__file__)
    )


    # --------------------------------------------------------
    # COMPROBAR MODELO
    # --------------------------------------------------------

    ruta_modelo = os.path.join(
        ruta_proyecto,
        MODELO
    )

    if not os.path.exists(ruta_modelo):

        print("[ERROR] No se encontró el modelo:")
        print(ruta_modelo)

        return


    print("[MODELO]")
    print(ruta_modelo)
    print("")


    # --------------------------------------------------------
    # COMPROBAR DATASET
    # --------------------------------------------------------

    ruta_dataset = os.path.join(
        ruta_proyecto,
        CARPETA_DATASET
    )

    if not os.path.exists(ruta_dataset):

        print("[ERROR] No se encontró la carpeta del dataset:")
        print(ruta_dataset)

        print("")
        print(
            "Extrae el ZIP descargado desde Roboflow "
            "dentro de una carpeta llamada 'dataset'."
        )

        return


    # --------------------------------------------------------
    # BUSCAR data.yaml
    # --------------------------------------------------------

    data_yaml = buscar_data_yaml(
        ruta_dataset
    )

    if data_yaml is None:

        print("[ERROR] No se encontró data.yaml.")
        print("")
        print(
            "Verifica que el ZIP de Roboflow "
            "se haya extraído correctamente."
        )

        return


    print("[DATASET]")
    print(data_yaml)
    print("")


    # --------------------------------------------------------
    # COMPROBAR GPU
    # --------------------------------------------------------

    if torch.cuda.is_available():

        dispositivo = 0

        print("[GPU] CUDA disponible")

        print(
            "[GPU]",
            torch.cuda.get_device_name(0)
        )

    else:

        dispositivo = "cpu"

        print("[GPU] CUDA no disponible.")
        print("[GPU] Se utilizará CPU.")


    print("")


    # --------------------------------------------------------
    # CARGAR MODELO
    # --------------------------------------------------------

    print("[SISTEMA] Cargando modelo...")

    model = YOLO(
        ruta_modelo
    )

    print("[SISTEMA] Modelo cargado correctamente.")
    print("")


    # --------------------------------------------------------
    # ENTRENAMIENTO
    # --------------------------------------------------------

    print("==============================================")
    print("          INICIANDO ENTRENAMIENTO")
    print("==============================================")
    print("")

    resultados = model.train(

        # Dataset generado por Roboflow.
        data=data_yaml,

        # Número máximo de épocas.
        epochs=EPOCHS,

        # Resolución de entrenamiento.
        imgsz=IMGSZ,

        # GPU 0 si existe. CPU si no hay CUDA.
        device=dispositivo,

        # Batch automático cuando existe GPU.
        batch=-1 if torch.cuda.is_available() else 8,

        # Detener si el modelo deja de mejorar.
        patience=30,

        # Guardar los pesos.
        save=True,

        # Generar gráficas de resultados.
        plots=True,

        # Carpeta principal de resultados.
        project=os.path.join(
            ruta_proyecto,
            "runs",
            "entrenamientos"
        ),

        # Nombre de esta ejecución.
        name=NOMBRE_ENTRENAMIENTO
    )


    # --------------------------------------------------------
    # RUTA DEL MODELO RESULTANTE
    # --------------------------------------------------------

    ruta_resultado = os.path.join(
        ruta_proyecto,
        "runs",
        "entrenamientos",
        NOMBRE_ENTRENAMIENTO,
        "weights"
    )


    print("")
    print("==============================================")
    print("         ENTRENAMIENTO TERMINADO")
    print("==============================================")
    print("")

    print("[RESULTADOS]")
    print(ruta_resultado)

    print("")
    print("[MODELO GENERADO]")

    print(
        os.path.join(
            ruta_resultado,
            "best.pt"
        )
    )

    print("")


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":
    main()
```

---

# 4. ¿Para qué sirve entrenar.py?

`entrenar.py` automatiza el entrenamiento local.

El proceso que realiza es:

```text
Ejecutar entrenar.py
        ↓
Buscar best_reentrenado.pt
        ↓
Buscar carpeta dataset
        ↓
Encontrar data.yaml de Roboflow
        ↓
Comprobar GPU
        ↓
Cargar el modelo
        ↓
Entrenar
        ↓
Guardar best.pt
```

Esto evita tener que escribir el comando completo de entrenamiento cada vez.

---

# 5. ¿Qué hay que cambiar antes de entrenar?

La configuración se encuentra al principio de `entrenar.py`.

## MODELO

```python
MODELO = "best_reentrenado.pt"
```

Indica qué modelo se utilizará como punto de partida.

Para seguir mejorando el modelo actual:

```python
MODELO = "best_reentrenado.pt"
```

Si posteriormente existe otro modelo:

```text
best_nuevo.pt
```

se puede cambiar a:

```python
MODELO = "best_nuevo.pt"
```

El archivo debe existir dentro de:

```text
CAMARA_YOLO/
```

---

## CARPETA_DATASET

```python
CARPETA_DATASET = "dataset"
```

Indica dónde está el dataset exportado desde Roboflow.

Si se mantiene:

```text
CAMARA_YOLO/dataset/
```

no es necesario modificar este valor.

---

## EPOCHS

```python
EPOCHS = 100
```

Indica la cantidad máxima de épocas de entrenamiento.

Ejemplos:

Entrenamiento corto de prueba:

```python
EPOCHS = 20
```

Entrenamiento normal:

```python
EPOCHS = 100
```

Entrenamiento más largo:

```python
EPOCHS = 150
```

Para comenzar se recomienda utilizar:

```python
EPOCHS = 100
```

---

## IMGSZ

```python
IMGSZ = 640
```

Indica la resolución utilizada durante el entrenamiento.

Se recomienda mantener:

```python
IMGSZ = 640
```

como configuración inicial.

---

## NOMBRE_ENTRENAMIENTO

```python
NOMBRE_ENTRENAMIENTO = "reentrenamiento_local"
```

Sirve para diferenciar los entrenamientos.

Por ejemplo:

```python
NOMBRE_ENTRENAMIENTO = "senales_version_2"
```

generará:

```text
runs/
└── entrenamientos/
    └── senales_version_2/
```

Para cada entrenamiento nuevo se recomienda utilizar un nombre diferente.

Ejemplos:

```python
NOMBRE_ENTRENAMIENTO = "senales_v2"
```

```python
NOMBRE_ENTRENAMIENTO = "senales_v3"
```

```python
NOMBRE_ENTRENAMIENTO = "prueba_150_epochs"
```

---

# 6. Ejecutar entrenamiento local

Abrir `CAMARA_YOLO` desde Visual Studio Code.

En la terminal comprobar que se encuentre dentro de la carpeta del proyecto.

Ejemplo:

```text
PS C:\Users\USUARIO\Documents\CAMARA_YOLO>
```

Ejecutar:

```powershell
py entrenar.py
```

No es necesario iniciar XAMPP para entrenar.

---

# 7. Resultado del entrenamiento

Al finalizar se generará:

```text
CAMARA_YOLO/
└── runs/
    └── entrenamientos/
        └── reentrenamiento_local/
            └── weights/
                ├── best.pt
                └── last.pt
```

## best.pt

```text
best.pt
```

Es el modelo que se debe probar y utilizar después del entrenamiento.

## last.pt

```text
last.pt
```

Corresponde al último estado guardado del entrenamiento.

Puede utilizarse para continuar un entrenamiento interrumpido.

---

# 8. Probar el nuevo modelo

Copiar:

```text
best.pt
```

a la carpeta principal y renombrarlo para no sobrescribir inmediatamente el modelo anterior.

Ejemplo:

```text
best_nuevo.pt
```

Quedaría:

```text
CAMARA_YOLO/
│
├── best_reentrenado.pt
├── best_nuevo.pt
└── ...
```

Comprobar que el modelo cargue:

```powershell
py -c "from ultralytics import YOLO; model=YOLO('best_nuevo.pt'); print(model.names)"
```

Después de comprobar que funciona correctamente se puede utilizar en los scripts de detección.

---

# ☁️ ENTRENAMIENTO EN GOOGLE COLAB

Google Colab permite realizar el mismo entrenamiento utilizando una GPU en la nube.

En este caso Roboflow puede generar directamente el código necesario para descargar el dataset.

---

# 1. Activar GPU

En Google Colab:

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

# 2. Instalar librerías

Ejecutar:

```python
!pip install -U ultralytics roboflow
```

---

# 3. Obtener el código de Roboflow

Desde Roboflow:

```text
Proyecto
→ Versions
→ Seleccionar versión
→ Export / Download Dataset
→ Formato YOLO
→ Show Download Code
```

Roboflow generará un código específico para el proyecto.

Ejemplo de referencia:

```python
from roboflow import Roboflow

rf = Roboflow(
    api_key="TU_API_KEY"
)

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

Se debe utilizar **el código generado por Roboflow**, no copiar los valores del ejemplo.

La API Key no debe subirse a GitHub ni guardarse en este README.

---

# 4. Comprobar el dataset

Después de descargarlo:

```python
print(dataset.location)
```

Roboflow indicará la carpeta donde se descargó el dataset.

---

# 5. Subir el modelo a Colab

Si se desea seguir entrenando:

```text
best_reentrenado.pt
```

subir ese archivo a Google Colab.

Desde el explorador de archivos de Colab:

```text
Archivos
→ Subir
→ best_reentrenado.pt
```

Normalmente quedará como:

```text
/content/best_reentrenado.pt
```

---

# 6. Entrenar en Google Colab

Ejecutar:

```python
from ultralytics import YOLO


# Modelo que se continuará entrenando.
model = YOLO(
    "/content/best_reentrenado.pt"
)


# Entrenamiento.
model.train(

    # data.yaml generado por Roboflow.
    data=f"{dataset.location}/data.yaml",

    # Cantidad de épocas.
    epochs=100,

    # Resolución.
    imgsz=640,

    # GPU de Google Colab.
    device=0,

    # Nombre del entrenamiento.
    name="reentrenamiento_colab"
)
```

---

# 7. ¿Qué cambiar en Colab?

Para cambiar las épocas:

```python
epochs=100
```

Por ejemplo:

```python
epochs=150
```

Para cambiar el tamaño de imagen:

```python
imgsz=640
```

Para cambiar el modelo:

```python
model = YOLO(
    "/content/best_reentrenado.pt"
)
```

Si se subió otro modelo:

```python
model = YOLO(
    "/content/best_nuevo.pt"
)
```

---

# 8. Descargar el resultado de Colab

Al finalizar el entrenamiento se generará una carpeta:

```text
runs/
└── detect/
    └── reentrenamiento_colab/
        └── weights/
            ├── best.pt
            └── last.pt
```

Descargar:

```text
best.pt
```

y copiarlo posteriormente dentro de:

```text
CAMARA_YOLO/
```

Se recomienda renombrarlo antes de reemplazar el modelo anterior.

Por ejemplo:

```text
best_colab_nuevo.pt
```

---

# 🔄 Resumen: entrenamiento local

```text
Roboflow
   ↓
Subir y etiquetar imágenes
   ↓
Generar versión
   ↓
Exportar formato YOLO
   ↓
Descargar ZIP
   ↓
Extraer en CAMARA_YOLO/dataset
   ↓
Configurar entrenar.py
   ↓
py entrenar.py
   ↓
runs/entrenamientos/.../weights/best.pt
   ↓
Probar modelo
```

---

# ☁️ Resumen: Google Colab

```text
Roboflow
   ↓
Generar versión
   ↓
Obtener código de descarga
   ↓
Abrir Google Colab
   ↓
Activar GPU
   ↓
Instalar Ultralytics y Roboflow
   ↓
Ejecutar código generado por Roboflow
   ↓
Subir best_reentrenado.pt
   ↓
Ejecutar entrenamiento
   ↓
Descargar best.pt
   ↓
Copiarlo a CAMARA_YOLO
```

---

# 📌 Comandos principales

## Instalar dependencias

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

## Entrenar localmente

```powershell
py entrenar.py
```

## Comprobar GPU

```powershell
nvidia-smi
```

---

# ✅ Uso normal

Después de realizar la instalación inicial:

```text
1. Abrir XAMPP
2. Iniciar MySQL
3. Abrir CAMARA_YOLO
4. Ejecutar el script requerido
```

Por ejemplo:

```powershell
py deteccion_senales_yt.py
```

Para entrenar un modelo:

```text
1. Exportar el dataset desde Roboflow
2. Colocarlo en CAMARA_YOLO/dataset
3. Revisar la configuración de entrenar.py
4. Ejecutar py entrenar.py
5. Obtener best.pt
6. Probar el nuevo modelo
```

No es necesario crear ni activar un entorno virtual.
