import pandas as pd

def calcular_iv(brecha_digital, salud_materna, educacion, exposicion_bulos):
    """
    Calcula el Índice de Vulnerabilidad Informativa (IVI)
    Fórmula: IVI = (0.30 * Brecha Digital) + (0.40 * Salud Materna) + (0.20 * Educación) + (0.10 * Exposición)
    """
    ivi = (0.30 * brecha_digital) + (0.40 * salud_materna) + (0.20 * educacion) + (0.10 * exposicion_bulos)
    return round(ivi, 2)

def clasificar_riesgo(ivi):
    """Clasifica el IVI en semáforos"""
    if ivi >= 70:
        return "Alto", "🔴"
    elif ivi >= 40:
        return "Medio", "🟡"
    else:
       return "Bajo", "🟢"

def cargar_datos():
    """
    Función placeholder para cargar los datasets limpios desde la carpeta /data
    """
    # TODO: df = pd.read_csv('../data/indicadores_puno_limpio.csv')
    # return df
    pass
