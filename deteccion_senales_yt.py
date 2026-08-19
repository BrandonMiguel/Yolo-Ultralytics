from ultralytics import YOLO
import cv2
import mysql.connector
from datetime import datetime
import os
import yt_dlp
import time


# ============================================================
# CONFIGURACION GENERAL
# ============================================================

# Misma resolución que utilizabas originalmente.
IMGSZ = 480

# Misma confianza que utilizabas originalmente.
CONFIANZA_YOLO = 0.35

# Confianza mínima para registrar en MySQL.
CONFIANZA_MINIMA_DB = 0.50

# FPS del video final para la demostración.
FPS_SALIDA = 20


# ============================================================
# RUTA DEL PROYECTO
# ============================================================

RUTA_PROYECTO = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# BASE DE DATOS
# ============================================================

def inicializar_db():

    conexion_raiz = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        use_pure=True
    )

    cursor_raiz = conexion_raiz.cursor()

    cursor_raiz.execute(
        "CREATE DATABASE IF NOT EXISTS registro_senales_db"
    )

    conexion_raiz.commit()

    cursor_raiz.close()
    conexion_raiz.close()


    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="registro_senales_db",
        use_pure=True
    )

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_roboflow (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fecha_hora DATETIME,
            tipo_objeto VARCHAR(50),
            track_id INT,
            confianza FLOAT
        )
    """)

    conn.commit()

    return conn


# Inicializamos la BD.
db_conn = inicializar_db()

db_cursor = db_conn.cursor()

# Evita registrar varias veces el mismo objeto.
ids_contados = set()


# ============================================================
# MODELO YOLO
# ============================================================

ruta_modelo = os.path.join(
    RUTA_PROYECTO,
    "best_reentrenado.pt"
)


if not os.path.exists(ruta_modelo):

    print("")
    print("[ERROR] No se encontró el modelo:")
    print(ruta_modelo)
    print("")

    db_cursor.close()
    db_conn.close()

    exit()


print("[SISTEMA] Cargando modelo YOLO...")


model = YOLO(
    ruta_modelo
)


# ============================================================
# VIDEO DE YOUTUBE
# ============================================================

# CAMBIA AQUÍ EL VIDEO SI LO NECESITAS.
url_youtube = (
    "https://www.youtube.com/watch?v=bKSU1Rp1Wgk"
)


# ============================================================
# DESCARGAR VIDEO LOCALMENTE
# ============================================================
#
# ESTE ES EL CAMBIO QUE SOLUCIONA TU ERROR.
#
# Ya NO hacemos:
#
# cv2.VideoCapture(url_directa_video)
#
# porque OpenCV está fallando al abrir directamente
# la URL temporal de googlevideo.
#
# Ahora yt_dlp descarga primero el video.
# Después OpenCV abre un archivo normal del disco.
# ============================================================


plantilla_video = os.path.join(
    RUTA_PROYECTO,
    "video_youtube_temporal.%(ext)s"
)


ydl_opts = {

    # Descargar únicamente VIDEO.
    #
    # Primero intenta conseguir video de hasta 480p
    # codificado en H.264 (avc1), que suele tener
    # muy buena compatibilidad con OpenCV.
    #
    # Si no existe H.264, utiliza cualquier otro
    # formato de video de hasta 480p.
    #
    # NO descargamos audio porque YOLO no lo utiliza.
    "format":
        "bv[height<=480][vcodec^=avc1]"
        "/bv[height<=480]",

    # Lugar donde se guardará el video temporal.
    "outtmpl": plantilla_video,

    # No descargar playlists completas.
    "noplaylist": True,

    # Reemplazar un video temporal anterior.
    "overwrites": True,

    # Mostrar el progreso de yt-dlp.
    "quiet": False,

    # Mostrar advertencias si existen.
    "no_warnings": False,

    # Reintentos en caso de una falla temporal.
    "retries": 10,

    # Reintentos para videos descargados por fragmentos.
    "fragment_retries": 10,
}


print("")
print("==============================================")
print("       DESCARGANDO VIDEO DE YOUTUBE")
print("==============================================")
print("")


try:

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:

        # download=True:
        #
        # A diferencia del código anterior,
        # AHORA SÍ descargamos el archivo.
        info = ydl.extract_info(
            url_youtube,
            download=True
        )

        # yt_dlp nos devuelve la ruta del archivo
        # que acaba de descargar.
        ruta_video_original = (
            ydl.prepare_filename(info)
        )


except Exception as e:

    print("")
    print("[ERROR] No fue posible descargar el video.")
    print(e)
    print("")

    db_cursor.close()
    db_conn.close()

    exit()


# ============================================================
# LOCALIZAR ARCHIVO DESCARGADO
# ============================================================
#
# Normalmente prepare_filename nos dará exactamente
# la ruta correcta.
#
# Pero añadimos esta comprobación por seguridad.
# ============================================================

if not os.path.exists(ruta_video_original):

    posibles_extensiones = [
        ".mp4",
        ".mkv",
        ".webm",
        ".mov"
    ]


    encontrado = False


    for extension in posibles_extensiones:

        posible = os.path.join(
            RUTA_PROYECTO,
            "video_youtube_temporal"
            + extension
        )


        if os.path.exists(posible):

            ruta_video_original = posible

            encontrado = True

            break


    if not encontrado:

        print("")
        print(
            "[ERROR] yt_dlp terminó, pero no se encontró "
            "el archivo descargado."
        )
        print("")

        db_cursor.close()
        db_conn.close()

        exit()


print("")
print("[SISTEMA] Video descargado correctamente:")
print(ruta_video_original)
print("")


# ============================================================
# ABRIR VIDEO LOCAL
# ============================================================
#
# Primero intentamos FFmpeg explícitamente.
#
# Si por alguna razón ese backend no está disponible,
# intentamos nuevamente dejando que OpenCV elija.
# ============================================================

camara = cv2.VideoCapture(
    ruta_video_original,
    cv2.CAP_FFMPEG
)


# Fallback.
if not camara.isOpened():

    camara.release()

    camara = cv2.VideoCapture(
        ruta_video_original
    )


if not camara.isOpened():

    print("")
    print(
        "[ERROR] OpenCV tampoco pudo abrir "
        "el archivo local."
    )

    print(
        "[ARCHIVO]",
        ruta_video_original
    )

    print("")

    db_cursor.close()
    db_conn.close()

    exit()


print(
    "[SISTEMA] OpenCV abrió correctamente "
    "el video local."
)


# ============================================================
# INFORMACION DEL VIDEO
# ============================================================

fps_original = camara.get(
    cv2.CAP_PROP_FPS
)


if (
    fps_original <= 1
    or fps_original > 120
):

    fps_original = 30.0


ancho = int(
    camara.get(
        cv2.CAP_PROP_FRAME_WIDTH
    )
)


alto = int(
    camara.get(
        cv2.CAP_PROP_FRAME_HEIGHT
    )
)


total_frames = int(
    camara.get(
        cv2.CAP_PROP_FRAME_COUNT
    )
)


if total_frames > 0:

    duracion_video = (
        total_frames
        /
        fps_original
    )

else:

    duracion_video = 0


print("")
print(
    f"[VIDEO] FPS originales: "
    f"{fps_original:.2f}"
)

print(
    f"[VIDEO] Resolución: "
    f"{ancho}x{alto}"
)

if duracion_video > 0:

    minutos = int(
        duracion_video // 60
    )

    segundos = int(
        duracion_video % 60
    )

    print(
        f"[VIDEO] Duración: "
        f"{minutos}:{segundos:02d}"
    )


print(
    f"[VIDEO] Demostración final: "
    f"{FPS_SALIDA} FPS"
)

print("")


# ============================================================
# RUTA DEL VIDEO PROCESADO
# ============================================================

ruta_video_procesado = os.path.join(
    RUTA_PROYECTO,
    "demo_yolo_procesada.mp4"
)


# Si existe uno anterior,
# lo eliminamos para evitar conflictos.
if os.path.exists(
    ruta_video_procesado
):

    try:

        os.remove(
            ruta_video_procesado
        )

    except Exception:

        pass


# ============================================================
# CREAR VIDEO FINAL
# ============================================================

fourcc = cv2.VideoWriter_fourcc(
    *"mp4v"
)


video_writer = cv2.VideoWriter(
    ruta_video_procesado,
    fourcc,
    FPS_SALIDA,
    (ancho, alto)
)


if not video_writer.isOpened():

    print("")
    print(
        "[ERROR] No se pudo crear "
        "demo_yolo_procesada.mp4"
    )
    print("")

    camara.release()

    db_cursor.close()
    db_conn.close()

    exit()


# ============================================================
# CREAR VENTANA DE PROCESAMIENTO
# ============================================================
#
# ESTA VENTANA SE MOSTRARÁ.
#
# Aquí podrás VER que:
#
# - YOLO está detectando.
# - las cajas están donde corresponde.
# - cada clase tiene color diferente.
#
# Esta etapa puede verse lenta.
#
# ESO ES NORMAL.
#
# Aquí YOLO todavía está trabajando.
# ============================================================

NOMBRE_VENTANA_PROCESO = (
    "YOLO - PROCESANDO VIDEO"
)


cv2.namedWindow(
    NOMBRE_VENTANA_PROCESO,
    cv2.WINDOW_NORMAL
)


# Ajustar tamaño inicial de la ventana.
cv2.resizeWindow(
    NOMBRE_VENTANA_PROCESO,
    960,
    540
)


# ============================================================
# VARIABLES PARA PASAR DE FPS ORIGINAL A 20 FPS
# ============================================================

intervalo_salida = (
    1.0
    /
    FPS_SALIDA
)


proximo_tiempo_salida = 0.0

indice_frame = 0

frames_procesados = 0


# ============================================================
# MYSQL
# ============================================================

registros_pendientes = 0

ultimo_commit = (
    time.perf_counter()
)


# ============================================================
# PROCESAR VIDEO
# ============================================================

print("")
print("==============================================")
print("       PROCESANDO VIDEO CON YOLO")
print("==============================================")
print("")
print(
    "Se abrirá una ventana para que puedas ver "
    "las detecciones."
)
print("")
print(
    "Esta primera etapa puede ir lenta porque "
    "YOLO está trabajando."
)
print("")
print(
    "Cuando termine se abrirá automáticamente "
    "la DEMOSTRACIÓN FLUIDA."
)
print("")
print("Q = cancelar")
print("")


cancelado = False


while True:

    # ========================================================
    # LEER FRAME ORIGINAL
    # ========================================================

    ret, frame = camara.read()


    if not ret:

        break


    # Tiempo de este frame dentro
    # del video original.
    tiempo_actual_video = (
        indice_frame
        /
        fps_original
    )


    indice_frame += 1


    # ========================================================
    # CONVERTIR VIDEO A 20 FPS
    # ========================================================
    #
    # Si el original tiene 30 FPS,
    # elegimos aproximadamente 20 de ellos.
    #
    # NO estamos acelerando el video.
    #
    # Conservamos la escala de tiempo original.
    # ========================================================

    if (
        tiempo_actual_video + 0.0001
        <
        proximo_tiempo_salida
    ):

        continue


    proximo_tiempo_salida += (
        intervalo_salida
    )


    # ========================================================
    # YOLO
    # ========================================================
    #
    # ESTA ES LA CONFIGURACION ORIGINAL.
    #
    # imgsz=480
    # conf=0.35
    # persist=True
    #
    # LO MÁS IMPORTANTE:
    #
    # YOLO analiza "frame".
    #
    # Después resultado.plot()
    # dibuja las cajas SOBRE ESE MISMO FRAME.
    #
    # Por lo tanto:
    #
    # NO usamos cajas antiguas.
    # NO usamos otro hilo.
    # NO usamos flujo óptico.
    # NO movemos coordenadas.
    #
    # La caja pertenece exactamente a
    # la detección de esa imagen.
    # ========================================================

    resultados = model.track(
        frame,
        imgsz=IMGSZ,
        conf=CONFIANZA_YOLO,
        persist=True,
        verbose=False
    )


    resultado = resultados[0]


    # ========================================================
    # DATOS DE LAS DETECCIONES
    # ========================================================

    nombres_clases = (
        resultado.names
    )


    if (
        resultado.boxes is not None
        and
        resultado.boxes.id is not None
    ):

        track_ids = (
            resultado.boxes.id
            .cpu()
            .numpy()
        )


        clases = (
            resultado.boxes.cls
            .cpu()
            .numpy()
        )


        confianzas = (
            resultado.boxes.conf
            .cpu()
            .numpy()
        )


        for (
            t_id,
            cls_id,
            conf_val
        ) in zip(
            track_ids,
            clases,
            confianzas
        ):

            track_id = int(
                t_id
            )

            cls = int(
                cls_id
            )

            conf = float(
                conf_val
            )


            # =================================================
            # GUARDAR EN BASE DE DATOS
            # =================================================

            if (
                conf
                >=
                CONFIANZA_MINIMA_DB
            ):

                if (
                    track_id
                    not in
                    ids_contados
                ):

                    ids_contados.add(
                        track_id
                    )


                    tipo = (
                        nombres_clases[
                            cls
                        ]
                    )


                    db_cursor.execute(
                        """
                        INSERT INTO registros_roboflow
                        (
                            fecha_hora,
                            tipo_objeto,
                            track_id,
                            confianza
                        )
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            datetime.now(),
                            tipo,
                            track_id,
                            round(
                                conf,
                                2
                            )
                        )
                    )


                    registros_pendientes += 1


                    print(
                        f"[BD] "
                        f"{tipo.upper()} registrada "
                        f"(ID: {track_id}) "
                        f"Confianza: {conf:.2f}"
                    )


    # ========================================================
    # COMMIT MYSQL
    # ========================================================

    ahora = time.perf_counter()


    if (
        registros_pendientes > 0
        and
        ahora - ultimo_commit >= 1
    ):

        db_conn.commit()

        registros_pendientes = 0

        ultimo_commit = ahora


    # ========================================================
    # CAJAS ORIGINALES DE ULTRALYTICS
    # ========================================================
    #
    # Cada clase utiliza su propio color.
    #
    # resultado.plot() utiliza las cajas
    # pertenecientes al resultado actual.
    # ========================================================

    annotated_frame = resultado.plot(
        conf=True,
        color_mode="class",
        line_width=2,
        labels=True,
        boxes=True
    )


    # ========================================================
    # GUARDAR FRAME CON DETECCIONES
    # ========================================================

    video_writer.write(
        annotated_frame
    )


    frames_procesados += 1


    # ========================================================
    # PREVISUALIZACION
    # ========================================================

    preview = (
        annotated_frame.copy()
    )


    # Texto superior.
    cv2.putText(
        preview,
        "",
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )


    # ========================================================
    # MOSTRAR VENTANA
    # ========================================================

    cv2.imshow(
        NOMBRE_VENTANA_PROCESO,
        preview
    )


    # ========================================================
    # TECLADO
    # ========================================================

    tecla = (
        cv2.waitKey(1)
        &
        0xFF
    )


    if tecla == ord("q"):

        cancelado = True

        break


    # ========================================================
    # PROGRESO EN CONSOLA
    # ========================================================

    if (
        frames_procesados
        %
        FPS_SALIDA
        ==
        0
    ):

        segundos_procesados = (
            frames_procesados
            /
            FPS_SALIDA
        )


        if duracion_video > 0:

            porcentaje = min(
                100.0,
                (
                    segundos_procesados
                    /
                    duracion_video
                )
                *
                100.0
            )


            print(
                f"[PROGRESO] "
                f"{porcentaje:.1f}%"
            )


# ============================================================
# TERMINAR PROCESAMIENTO
# ============================================================

if registros_pendientes > 0:

    db_conn.commit()


camara.release()

video_writer.release()

db_cursor.close()

db_conn.close()


cv2.destroyAllWindows()


if cancelado:

    print("")
    print(
        "[SISTEMA] Procesamiento cancelado."
    )

    exit()


# ============================================================
# VERIFICAR VIDEO FINAL
# ============================================================

if not os.path.exists(
    ruta_video_procesado
):

    print("")
    print(
        "[ERROR] No se generó "
        "demo_yolo_procesada.mp4"
    )
    print("")

    exit()


print("")
print("==============================================")
print("        VIDEO YOLO TERMINADO")
print("==============================================")
print("")
print(
    "[SISTEMA] Ahora abriré la demostración."
)
print("")


# ============================================================
# ABRIR VIDEO PROCESADO
# ============================================================

video_demo = cv2.VideoCapture(
    ruta_video_procesado,
    cv2.CAP_FFMPEG
)


if not video_demo.isOpened():

    video_demo.release()

    video_demo = cv2.VideoCapture(
        ruta_video_procesado
    )


if not video_demo.isOpened():

    print("")
    print(
        "[ERROR] No fue posible abrir "
        "la demostración procesada."
    )
    print("")

    exit()


# ============================================================
# LEER PRIMER FRAME
# ============================================================

ret, primer_frame = (
    video_demo.read()
)


if not ret:

    print(
        "[ERROR] El video procesado está vacío."
    )

    video_demo.release()

    exit()


# ============================================================
# VENTANA DE DEMOSTRACION
# ============================================================

NOMBRE_VENTANA_DEMO = (
    "YOLO - DEMOSTRACION"
)


cv2.namedWindow(
    NOMBRE_VENTANA_DEMO,
    cv2.WINDOW_NORMAL
)


cv2.resizeWindow(
    NOMBRE_VENTANA_DEMO,
    960,
    540
)


# ============================================================
# PANTALLA DE ESPERA
# ============================================================
#
# AHORA PUEDES:
#
# 1. Abrir OBS / Xbox Game Bar / grabador.
# 2. Acomodar esta ventana.
# 3. Empezar tu grabación.
# 4. Presionar ESPACIO.
#
# El video comenzará desde el principio.
# ============================================================

pantalla_inicio = (
    primer_frame.copy()
)


overlay = (
    pantalla_inicio.copy()
)


alto_inicio, ancho_inicio = (
    pantalla_inicio.shape[:2]
)


# Rectángulo oscuro arriba.
cv2.rectangle(
    overlay,
    (0, 0),
    (ancho_inicio, 110),
    (0, 0, 0),
    -1
)


cv2.addWeighted(
    overlay,
    0.65,
    pantalla_inicio,
    0.35,
    0,
    pantalla_inicio
)


cv2.putText(
    pantalla_inicio,
    "LISTO PARA GRABAR",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.9,
    (255, 255, 255),
    2,
    cv2.LINE_AA
)


cv2.putText(
    pantalla_inicio,
    "ESPACIO = iniciar",
    (20, 80),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (255, 255, 255),
    2,
    cv2.LINE_AA
)


print("")
print("==============================================")
print("         LISTO PARA QUE GRABES")
print("==============================================")
print("")
print("Inicia tu grabador de pantalla.")
print("")
print("Después presiona ESPACIO.")
print("")
print("ESPACIO = iniciar")
print("Q = salir")
print("")


# ============================================================
# ESPERAR ESPACIO
# ============================================================

while True:

    cv2.imshow(
        NOMBRE_VENTANA_DEMO,
        pantalla_inicio
    )


    tecla = (
        cv2.waitKey(30)
        &
        0xFF
    )


    # ESPACIO
    if tecla == 32:

        break


    # Q
    elif tecla == ord("q"):

        video_demo.release()

        cv2.destroyAllWindows()

        exit()


# ============================================================
# REGRESAR AL PRIMER FRAME
# ============================================================

video_demo.set(
    cv2.CAP_PROP_POS_FRAMES,
    0
)


# ============================================================
# REPRODUCCION A 20 FPS
# ============================================================

TIEMPO_FRAME = (
    1.0
    /
    FPS_SALIDA
)


proximo_frame = (
    time.perf_counter()
)


fps_real = 0.0

contador_fps = 0

inicio_fps = (
    time.perf_counter()
)


pausado = False


print("")
print("[DEMO] INICIADA")
print("")
print("ESPACIO = pausar/continuar")
print("Q = salir")
print("")


while True:

    # ========================================================
    # PAUSA
    # ========================================================

    if pausado:

        tecla = (
            cv2.waitKey(30)
            &
            0xFF
        )


        if tecla == ord("q"):

            break


        elif tecla == 32:

            pausado = False

            # Reiniciamos reloj para que
            # no intente recuperar tiempo perdido.
            proximo_frame = (
                time.perf_counter()
            )


        continue


    # ========================================================
    # LEER VIDEO YA PROCESADO
    # ========================================================

    ret, frame = (
        video_demo.read()
    )


    if not ret:

        print("")
        print("[DEMO] Fin del video.")
        print("")

        break


    # ========================================================
    # CALCULAR FPS REALES
    # ========================================================

    contador_fps += 1


    ahora = (
        time.perf_counter()
    )


    if (
        ahora - inicio_fps
        >=
        1.0
    ):

        fps_real = (
            contador_fps
            /
            (
                ahora - inicio_fps
            )
        )


        contador_fps = 0

        inicio_fps = (
            ahora
        )


    # ========================================================
    # MOSTRAR SOLO FPS
    # ========================================================

    cv2.putText(
        frame,
        f"FPS: {fps_real:.1f}",
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )


    # ========================================================
    # MOSTRAR VIDEO
    # ========================================================

    cv2.imshow(
        NOMBRE_VENTANA_DEMO,
        frame
    )


    # ========================================================
    # SINCRONIZAR 20 FPS
    # ========================================================

    proximo_frame += (
        TIEMPO_FRAME
    )


    tiempo_restante = (
        proximo_frame
        -
        time.perf_counter()
    )


    if tiempo_restante > 0:

        espera_ms = max(
            1,
            int(
                tiempo_restante
                *
                1000
            )
        )

    else:

        espera_ms = 1


    tecla = (
        cv2.waitKey(
            espera_ms
        )
        &
        0xFF
    )


    # Q = cerrar.
    if tecla == ord("q"):

        break


    # ESPACIO = pausa.
    elif tecla == 32:

        pausado = True


# ============================================================
# CERRAR PROGRAMA
# ============================================================

video_demo.release()

cv2.destroyAllWindows()


print("")
print(
    "[SISTEMA] Programa finalizado."
)