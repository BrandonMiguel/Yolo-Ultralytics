from ultralytics import YOLO
import os


# ============================================================
# CONFIGURACIÓN
# ============================================================

# Modelo YOLOv8 que se utilizará como base.
# Si no existe en la PC, Ultralytics lo descarga automáticamente.
MODELO_BASE = "yolov8n.pt"

# Ruta donde se extrajo el ZIP descargado desde Roboflow.
CARPETA_DATASET = r"C:\dataset-roboflow"

# Cantidad de épocas de entrenamiento.
EPOCHS = 100

# Resolución utilizada durante el entrenamiento.
IMGSZ = 640

# Nombre con el que se guardará este entrenamiento.
NOMBRE_ENTRENAMIENTO = "senalizacion_v10"


# ============================================================
# BUSCAR data.yaml
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
    print("          ENTRENAMIENTO LOCAL YOLO")
    print("==============================================")
    print("")


    # ========================================================
    # RUTA DEL PROYECTO CAMARA_YOLO
    # ========================================================

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

    if not os.path.exists(CARPETA_DATASET):

        print("")
        print("[ERROR] No se encontró:")
        print(CARPETA_DATASET)
        print("")
        print(
            "Comprueba que el dataset de Roboflow "
            "esté extraído en esa carpeta."
        )

        return


    # ========================================================
    # BUSCAR data.yaml
    # ========================================================

    data_yaml = buscar_data_yaml(
        CARPETA_DATASET
    )


    if data_yaml is None:

        print("")
        print("[ERROR] No se encontró data.yaml.")
        print("")
        print(
            "Comprueba que el ZIP de Roboflow "
            "se haya extraído correctamente."
        )

        return


    print("")
    print("[DATASET ENCONTRADO]")
    print(data_yaml)
    print("")


    # ========================================================
    # CARGAR MODELO BASE
    # ========================================================

    print("[SISTEMA] Cargando modelo:")
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

        # data.yaml generado por Roboflow
        data=data_yaml,

        # Cantidad de épocas
        epochs=EPOCHS,

        # Resolución de entrenamiento
        imgsz=IMGSZ,

        # Carpeta donde se guardarán los resultados
        project=os.path.join(
            ruta_proyecto,
            "runs",
            "entrenamientos"
        ),

        # Nombre de este entrenamiento
        name=NOMBRE_ENTRENAMIENTO,

        # Guardar pesos del modelo
        save=True,

        # Generar gráficas del entrenamiento
        plots=True
    )


    # ========================================================
    # RUTA DEL MODELO RESULTANTE
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
# EJECUTAR PROGRAMA
# ============================================================

if __name__ == "__main__":
    main()