from ultralytics import YOLO          # El cerebro de la Inteligencia Artificial que detecta objetos.
import cv2                            # OpenCV: La librería maestra para manipular video e imágenes.
import threading                      # Permite hacer varias tareas al mismo tiempo (Multihilos).
import time                           # Para manejar pausas y tiempos en el código.
import mysql.connector                # El puente de comunicación entre Python y tu servidor XAMPP.
from datetime import datetime         # Para obtener la fecha y hora exacta del sistema.
import os                             # Para verificar que el archivo del modelo exista

# --- CLASE PARA LEER LA CÁMARA SIN RETRASO (MULTITHREADING) ---
class LectorCamara:
    def __init__(self, url):
        self.cap = cv2.VideoCapture(url)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.ret, self.frame = self.cap.read()
        self.corriendo = True
        self.hilo = threading.Thread(target=self.actualizar, args=())
        self.hilo.daemon = True
        self.hilo.start()

    def actualizar(self):
        while self.corriendo:
            ret, frame = self.cap.read()
            if ret:
                self.ret = ret
                self.frame = frame

    def leer(self):
        return self.ret, self.frame

    def detener(self):
        self.corriendo = False
        self.hilo.join()
        self.cap.release()

# --- CONFIGURACIÓN DE BASE DE DATOS (MySQL en XAMPP) ---
def inicializar_db():
    conexion_raiz = mysql.connector.connect(
        host="localhost",
        user="root",
        password="" 
    )
    conexion_raiz.cursor().execute("CREATE DATABASE IF NOT EXISTS registro_senales_db")
    conexion_raiz.close()

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="registro_senales_db" 
    )
    cursor = conn.cursor()
    
    # [CAMBIO] Creamos la tabla 'registros_roboflow' para mantener tus experimentos separados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros_roboflow (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fecha_hora DATETIME,
            tipo_objeto VARCHAR(50),
            track_id INT,
            confianza FLOAT
        )
    ''')
    conn.commit() 
    return conn

db_conn = inicializar_db()
db_cursor = db_conn.cursor()
ids_contados = set()

# --- CONFIGURACIÓN DE YOLO ---
# Obtenemos automáticamente la carpeta donde está este archivo .py.
# De esta forma el proyecto puede copiarse a otra PC o a otra carpeta
# sin depender de una ruta fija como C:/GeneradorSenales.
RUTA_PROYECTO = os.path.dirname(
    os.path.abspath(__file__)
)

# Nombre del modelo que se utilizará.
# El archivo .pt debe estar en la misma carpeta que este script.
NOMBRE_MODELO = "best_reentrenado.pt"

ruta_tu_modelo = os.path.join(
    RUTA_PROYECTO,
    NOMBRE_MODELO
)

# Verificación de seguridad: si el modelo no existe, el programa
# muestra la ruta exacta donde lo está buscando y termina.
if not os.path.exists(ruta_tu_modelo):
    print(f"\n[ERROR] No se encontró el modelo '{NOMBRE_MODELO}'.")
    print("[RUTA ESPERADA]")
    print(ruta_tu_modelo)
    print("")
    print("Coloca el modelo entrenado en la misma carpeta que este script.")
    print("Si descargaste un archivo llamado 'best.pt', puedes renombrarlo")
    print(f"como '{NOMBRE_MODELO}' o cambiar NOMBRE_MODELO en este código.\n")
    exit()

print(f"[SISTEMA] Cargando modelo YOLO: {ruta_tu_modelo}")
model = YOLO(ruta_tu_modelo)

# --- INICIO DEL PROGRAMA ---
# Conexión a tu cámara Axis
url_camara = "rtsp://root:ITS-007900@192.168.1.192/axis-media/media.amp?resolution=1920x1080"
camara = LectorCamara(url_camara) 
time.sleep(1) 

cv2.namedWindow('YOLO ROBOFLOW - Deteccion Real', cv2.WINDOW_NORMAL)

mostrar_confianza = True
CONFIANZA_MINIMA_DB = 0.50 # Alerta al pasar el 50% de certeza en vivo

print("Sistema conectado a XAMPP listo. Presiona 'c' para ocultar/mostrar % o 'q' para salir.")

while True:
    ret, frame = camara.leer()
    if not ret or frame is None:
        print("No se pudo recibir el frame de la cámara Axis. Saliendo...")
        break

    # Rastreando todas las clases reales del dataset de Roboflow sin filtros
    resultados = model.track(frame, imgsz=640, conf=0.25, persist=True, verbose=False) 
    
    # Mapea dinámicamente los nombres de tus señales del mundo real
    nombres_clases = resultados[0].names

    if resultados[0].boxes is not None and resultados[0].boxes.id is not None:
        
        track_ids_raw = resultados[0].boxes.id.cpu().numpy()
        clases_raw = resultados[0].boxes.cls.cpu().numpy()
        confianzas_raw = resultados[0].boxes.conf.cpu().numpy()

        for t_id, cls_id, conf_val in zip(track_ids_raw, clases_raw, confianzas_raw):
            
            track_id = int(t_id)
            cls = int(cls_id)
            conf = float(conf_val)

            # Filtro de confianza mínima
            if conf >= CONFIANZA_MINIMA_DB:
                
                # Filtro de ID único (evita duplicar registros de la misma señal en MySQL)
                if track_id not in ids_contados:
                    ids_contados.add(track_id) 
                    
                    tipo = nombres_clases[cls]
                    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                    
                    # [CAMBIO] Inserción limpia a la nueva tabla de Roboflow
                    db_cursor.execute(
                        "INSERT INTO registros_roboflow (fecha_hora, tipo_objeto, track_id, confianza) VALUES (%s, %s, %s, %s)",
                        (ahora, tipo, track_id, round(conf, 2))
                    )
                    db_conn.commit() 
                    
                    print(f"[MySQL Roboflow] Guardado -> {ahora} | {tipo.upper()} (ID Track: {track_id}) con {round(conf*100, 1)}% certeza.")

    annotated_frame = resultados[0].plot(conf=mostrar_confianza)
    cv2.imshow('YOLO ROBOFLOW - Deteccion Real', annotated_frame)

    tecla = cv2.waitKey(1) & 0xFF 
    if tecla == ord('q'):
        break 
    elif tecla == ord('c'):
        mostrar_confianza = not mostrar_confianza
        estado = "ACTIVADA" if mostrar_confianza else "DESACTIVADA"
        print(f"[SISTEMA] Visualización de confianza: {estado}")

# Cierre ordenado de los servicios
camara.detener() 
cv2.destroyAllWindows() 
db_conn.close() 
print("Conexión a MySQL cerrada con éxito.")