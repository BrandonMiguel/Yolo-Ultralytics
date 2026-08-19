# ITS YOLO - Detección de Señales y Objetos

Este repositorio contiene los scripts utilizados para la detección de señales de tránsito, vehículos y otros objetos mediante modelos de visión computacional basados en **YOLO**.

El proyecto permite realizar detecciones utilizando diferentes fuentes de video, como:

* Cámara IP mediante transmisión **RTSP**.
* Videos de **YouTube**.
* Cámara utilizada directamente desde Python.
* Modelos YOLO genéricos y modelos entrenados específicamente para detección de tráfico y señalizaciones.

---

## 📂 Estructura del proyecto

Los archivos principales del proyecto se encuentran dentro de la misma carpeta:

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

Los modelos `.pt` deben permanecer dentro de la carpeta principal del proyecto junto con los scripts de Python.

### Modelo recomendado

Actualmente se recomienda utilizar:

```text
best_reentrenado.pt
```

Este modelo fue entrenado específicamente para detección de tráfico y señalizaciones.

No es necesario crear una carpeta adicional en el disco `C:` para almacenar los modelos.

---

# 🐍 1. Instalar Python

Para utilizar el proyecto es necesario tener instalado **Python**.

Se recomienda utilizar una versión moderna de Python, por ejemplo:

```text
Python 3.11
```

o:

```text
Python 3.12
```

Durante la instalación de Python se recomienda activar la opción:

```text
Add Python to PATH
```

Una vez instalado, abrir **CMD**, **PowerShell** o la terminal de **Visual Studio Code** y ejecutar:

```powershell
py --version
```

También puede utilizarse:

```powershell
python --version
```

Si Python está correctamente instalado se mostrará algo similar a:

```text
Python 3.12.x
```

---

# ⚙️ 2. Instalar las dependencias

Las dependencias solamente necesitan instalarse **una vez en la computadora**.

Primero actualizar `pip`:

```powershell
py -m pip install --upgrade pip
```

Después instalar las librerías utilizadas por el proyecto:

```powershell
py -m pip install -U ultralytics opencv-python mysql-connector-python yt-dlp
```

Las principales librerías utilizadas son:

### Ultralytics

Utilizada para cargar y ejecutar los modelos YOLO.

```text
ultralytics
```

### OpenCV

Utilizada para trabajar con cámaras, videos, imágenes y ventanas de visualización.

```text
opencv-python
```

### MySQL Connector

Permite conectar Python con la base de datos MySQL.

```text
mysql-connector-python
```

### yt-dlp

Utilizada para obtener y descargar videos de YouTube que posteriormente son procesados por YOLO.

```text
yt-dlp
```

---

# ✅ 3. Verificar las dependencias

Después de instalar las librerías se puede comprobar que todo esté correctamente instalado ejecutando:

```powershell
py -c "from ultralytics import YOLO; import cv2; import mysql.connector; import yt_dlp; print('TODO INSTALADO CORRECTAMENTE')"
```

Si todo está correcto aparecerá:

```text
TODO INSTALADO CORRECTAMENTE
```

---

# 🧠 4. Verificar el modelo entrenado

El archivo:

```text
best_reentrenado.pt
```

debe permanecer dentro de la carpeta principal `its-yolo`.

Ejemplo:

```text
its-yolo/
│
├── best_reentrenado.pt
└── deteccion_senales_yt.py
```

Para comprobar que el modelo puede cargarse correctamente se puede ejecutar:

```powershell
py -c "from ultralytics import YOLO; modelo=YOLO('best_reentrenado.pt'); print(modelo.names)"
```

Si el modelo funciona correctamente aparecerán en pantalla las clases que fue entrenado para detectar.

---

# 🗄️ 5. XAMPP y MySQL

Los scripts que registran detecciones requieren tener disponible un servidor **MySQL**.

El proyecto está preparado para trabajar con MySQL mediante **XAMPP**.

Antes de ejecutar estos scripts:

1. Abrir **XAMPP Control Panel**.
2. Localizar el servicio **MySQL**.
3. Presionar:

```text
Start
```

Debe aparecer MySQL ejecutándose correctamente.

```text
MySQL → Running
```

No es necesario iniciar Apache para ejecutar los scripts de YOLO.

Solamente es necesario:

```text
MySQL
```

---

# 🔐 6. Configuración actual de MySQL

Actualmente los scripts utilizan una conexión local similar a:

```text
Host: localhost
Usuario: root
Contraseña: vacía
```

Es decir:

```python
host="localhost"
user="root"
password=""
```

Por lo tanto, para utilizar el proyecto sin realizar modificaciones se recomienda que MySQL de XAMPP utilice la configuración local predeterminada.

Si el usuario `root` de MySQL tiene una contraseña configurada, será necesario modificar el valor:

```python
password=""
```

por la contraseña correspondiente.

Ejemplo:

```python
password="mi_contraseña"
```

---

# 🗃️ 7. Base de datos de detecciones

El sistema está preparado para crear automáticamente la base de datos utilizada para almacenar las detecciones.

La base utilizada es:

```text
registro_senales_db
```

Dentro de ella se utiliza la tabla:

```text
registros_roboflow
```

En esta tabla pueden almacenarse datos como:

```text
ID
Fecha y hora
Tipo de objeto
Track ID
Confianza
```

Por lo tanto, normalmente no es necesario crear manualmente la base de datos antes de ejecutar el programa.

Solamente es necesario asegurarse de que **MySQL esté iniciado en XAMPP**.

---

# 📁 8. Abrir el proyecto

El proyecto puede guardarse, por ejemplo, dentro de:

```text
C:\Users\USUARIO\Documents\its-yolo
```

Abrir esa carpeta utilizando **Visual Studio Code**.

También puede abrirse desde una terminal:

```powershell
cd "C:\Users\USUARIO\Documents\its-yolo"
```

Si Visual Studio Code se encuentra agregado al PATH también puede utilizarse:

```powershell
code .
```

---

# ▶️ 9. Ejecutar detección mediante video de YouTube

El archivo:

```text
deteccion_senales_yt.py
```

está diseñado para procesar un video de YouTube utilizando el modelo entrenado.

Antes de ejecutarlo:

1. Abrir XAMPP.
2. Iniciar MySQL.
3. Abrir el proyecto.
4. Verificar que `best_reentrenado.pt` esté dentro de la carpeta.
5. Ejecutar el script.

Comando:

```powershell
py deteccion_senales_yt.py
```

También puede utilizarse:

```powershell
python deteccion_senales_yt.py
```

El programa realiza el siguiente proceso:

```text
Video de YouTube
        ↓
Descarga temporal del video
        ↓
Modelo YOLO
        ↓
Detección y Tracking
        ↓
Visualización de detecciones
        ↓
Registro en MySQL
        ↓
Generación del video procesado
```

El video procesado se genera automáticamente dentro de la carpeta del proyecto.

---

# 🎥 10. Ejecutar detección mediante cámara IP / RTSP

El archivo:

```text
deteccion_senales_roboflow.py
```

está diseñado para analizar una transmisión de video proveniente de una cámara IP mediante **RTSP**.

Para ejecutarlo:

```powershell
py deteccion_senales_roboflow.py
```

Antes de ejecutarlo se debe comprobar la configuración de conexión de la cámara dentro del código.

Dependiendo de la cámara utilizada pueden requerirse datos como:

```text
Dirección IP
Usuario
Contraseña
Puerto
Dirección RTSP
```

También es necesario que la computadora tenga acceso a la misma red donde se encuentra la cámara.

Este script utiliza el modelo entrenado específicamente para detección de señales y tráfico.

Se recomienda utilizar:

```text
best_reentrenado.pt
```

---

# 📷 11. Ejecutar camara_yolo.py

El archivo:

```text
camara_yolo.py
```

permite realizar pruebas de detección mediante YOLO.

Este script utiliza un modelo YOLO para detectar objetos comunes y puede utilizarse principalmente para pruebas de funcionamiento de cámara y detección.

Para ejecutarlo:

```powershell
py camara_yolo.py
```

---

# 🧠 12. Modelos disponibles

Actualmente el proyecto contiene los siguientes modelos:

```text
best_masentrenado.pt
best_reentrenado.pt
```

Para las pruebas principales del sistema se recomienda:

```text
best_reentrenado.pt
```

Los modelos deben permanecer dentro de la misma carpeta del proyecto.

---

# 🎯 13. Cambiar el modelo utilizado

Los scripts que utilizan un modelo entrenado cargan un archivo `.pt`.

Por ejemplo:

```python
best_reentrenado.pt
```

Si posteriormente se genera un modelo mejor entrenado, solamente será necesario colocar el nuevo archivo `.pt` dentro de la carpeta del proyecto y modificar en el código el nombre del modelo que se desea utilizar.

Ejemplo:

```python
ruta_modelo = os.path.join(
    RUTA_PROYECTO,
    "best_reentrenado.pt"
)
```

---

# 🚗 14. deteccion_senales_yt.py

Este script permite procesar videos provenientes de YouTube.

Utiliza el modelo entrenado:

```text
best_reentrenado.pt
```

Entre sus funciones se encuentran:

* Descargar temporalmente un video de YouTube.
* Procesar el video mediante YOLO.
* Detectar objetos y señalizaciones.
* Realizar seguimiento de objetos mediante Tracking.
* Asignar un identificador a los objetos detectados.
* Mostrar las cajas de detección.
* Mostrar la confianza de las detecciones.
* Registrar detecciones en MySQL.
* Evitar registrar repetidamente el mismo Track ID.
* Generar un video procesado.
* Reproducir posteriormente el resultado de manera fluida.

---

# 🚦 15. deteccion_senales_roboflow.py

Este script está diseñado principalmente para trabajar con una cámara IP mediante una transmisión:

```text
RTSP
```

Utiliza el modelo personalizado entrenado para reconocer señalizaciones y elementos relacionados con tráfico.

Puede utilizarse para detectar elementos como:

```text
Señales de tránsito
Automóviles
Camiones
Motocicletas
Bicicletas
Camionetas
Otros objetos incluidos durante el entrenamiento
```

Las clases exactas disponibles dependen del modelo `.pt` utilizado.

---

# 📹 16. camara_yolo.py

Este script permite realizar detecciones mediante una cámara utilizando YOLO.

Puede utilizarse principalmente para comprobar:

* Comunicación con la cámara.
* Lectura del video.
* Funcionamiento de OpenCV.
* Funcionamiento de YOLO.
* Detección de objetos comunes.

---

# 💻 17. Instalación rápida en otra computadora

En una computadora nueva solamente es necesario realizar la instalación inicial una vez.

### Paso 1 - Instalar Python

Comprobar:

```powershell
py --version
```

### Paso 2 - Actualizar pip

```powershell
py -m pip install --upgrade pip
```

### Paso 3 - Instalar dependencias

```powershell
py -m pip install -U ultralytics opencv-python mysql-connector-python yt-dlp
```

### Paso 4 - Comprobar instalación

```powershell
py -c "from ultralytics import YOLO; import cv2; import mysql.connector; import yt_dlp; print('TODO INSTALADO CORRECTAMENTE')"
```

### Paso 5 - Copiar o clonar el proyecto

La estructura debe contener al menos:

```text
its-yolo/
│
├── best_reentrenado.pt
├── camara_yolo.py
├── deteccion_senales_roboflow.py
└── deteccion_senales_yt.py
```

### Paso 6 - Abrir XAMPP

Iniciar:

```text
MySQL
```

### Paso 7 - Abrir la carpeta del proyecto

Por ejemplo:

```powershell
cd "C:\Users\USUARIO\Documents\its-yolo"
```

### Paso 8 - Ejecutar el script

Por ejemplo:

```powershell
py deteccion_senales_yt.py
```

---

# 🔁 18. Uso normal después de la instalación

Después de realizar la instalación inicial **no es necesario volver a instalar las dependencias cada vez que se utilice el programa**.

Para ejecuciones posteriores solamente se debe:

### 1. Abrir XAMPP

```text
MySQL → Start
```

### 2. Abrir el proyecto

```text
its-yolo
```

### 3. Ejecutar el script deseado

YouTube:

```powershell
py deteccion_senales_yt.py
```

Cámara IP / RTSP:

```powershell
py deteccion_senales_roboflow.py
```

Cámara YOLO:

```powershell
py camara_yolo.py
```

El flujo normal de trabajo será:

```text
Encender computadora
        ↓
Abrir XAMPP
        ↓
Iniciar MySQL
        ↓
Abrir proyecto ITS YOLO
        ↓
Ejecutar script .py
        ↓
Detección funcionando
```

---

# 🎮 19. Verificar el uso de GPU NVIDIA

Si la computadora cuenta con una tarjeta gráfica NVIDIA, puede comprobarse desde PowerShell ejecutando:

```powershell
nvidia-smi
```

También puede verificarse desde Python:

```powershell
py -c "import torch; print('CUDA disponible:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No se está utilizando CUDA')"
```

Si aparece:

```text
CUDA disponible: True
```

significa que PyTorch puede utilizar la GPU NVIDIA.

Si aparece:

```text
CUDA disponible: False
```

el programa podrá continuar funcionando mediante CPU, aunque el procesamiento puede ser más lento.

---

# 🛠️ 20. Problemas comunes

## Python no se reconoce

Si aparece:

```text
'python' no se reconoce como un comando
```

probar:

```powershell
py --version
```

Si tampoco funciona, instalar Python y asegurarse de agregarlo al PATH.

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

Comprobar que:

```text
XAMPP → MySQL → Running
```

También verificar:

```text
host
usuario
contraseña
```

configurados dentro del script.

---

## No se encuentra el modelo

Comprobar que:

```text
best_reentrenado.pt
```

se encuentre dentro de la misma carpeta donde está el script.

Ejemplo correcto:

```text
its-yolo/
│
├── best_reentrenado.pt
└── deteccion_senales_yt.py
```

---

# 📌 Resumen de comandos

## Instalar dependencias

```powershell
py -m pip install --upgrade pip
```

```powershell
py -m pip install -U ultralytics opencv-python mysql-connector-python yt-dlp
```

## Comprobar instalación

```powershell
py -c "from ultralytics import YOLO; import cv2; import mysql.connector; import yt_dlp; print('TODO INSTALADO CORRECTAMENTE')"
```

## Comprobar modelo

```powershell
py -c "from ultralytics import YOLO; modelo=YOLO('best_reentrenado.pt'); print(modelo.names)"
```

## Ejecutar YouTube

```powershell
py deteccion_senales_yt.py
```

## Ejecutar cámara IP / RTSP

```powershell
py deteccion_senales_roboflow.py
```

## Ejecutar cámara YOLO

```powershell
py camara_yolo.py
```

## Comprobar GPU

```powershell
nvidia-smi
```

```powershell
py -c "import torch; print('CUDA disponible:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

---

# ✅ Flujo recomendado

Una vez que la computadora se encuentre correctamente configurada, el uso cotidiano del proyecto se reduce a:

```text
1. Abrir XAMPP
2. Iniciar MySQL
3. Abrir la carpeta its-yolo
4. Ejecutar el script requerido
```

Ejemplo:

```powershell
py deteccion_senales_yt.py
```

No es necesario crear ni activar entornos virtuales para utilizar este proyecto bajo la configuración indicada en este README.
