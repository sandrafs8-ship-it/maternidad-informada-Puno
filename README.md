# 🤰 Maternidad Informada Puno
### Modelo Analítico y Geoespacial para el Combate a la Desinformación en Salud Materno-Infantil

> **Desafío de Datos para la Democracia - OEA 2026**  
> 🌐 **Aplicación en Vivo:** [https://maternidad-informada-puno-sor4mo8eyt8n39ngzpmzpk.streamlit.app/](https://maternidad-informada-puno-sor4mo8eyt8n39ngzpmzpk.streamlit.app/)

---

## 📌 Descripción del Proyecto
Desarrollo de un tablero de control (dashboard) geoespacial interactivo que identifica las provincias de la región Puno con mayor vulnerabilidad a la desinformación en salud materno-infantil. La herramienta utiliza el **Índice de Vulnerabilidad Informativa (IVI)** para priorizar intervenciones y facilitar la toma de decisiones basada en datos abiertos.

## 🧮 Metodología: Índice de Vulnerabilidad Informativa (IVI)
El IVI es un índice compuesto (0-100) calculado mediante la ponderación de cuatro variables clave. Los pesos fueron definidos en base a la evidencia de impacto directo en la salud materna:

| Indicador | Peso | Justificación | Fuente de Datos (Objetivo) |
| :--- | :---: | :--- | :--- |
| **Hogares sin internet** | 40% | Acceso a información digital y telemedicina | INEI (Censos / ENAHO) |
| **Partos sin asistencia calificada** | 30% | Resultado directo de desinformación en salud | MINSA (HIS / ENDES) |
| **Desnutrición infantil** | 20% | Indicador de salud preventiva fallida | MINSA / INEI |
| **Mortalidad materna** | 10% | Consecuencia extrema (evento centinela) | MINSA (Sala Situacional) |

*Fórmula:* $IVI = \sum_{i=1}^{n} (w_i \times x_i)$, donde $x_i$ es el valor normalizado del indicador.

## 💻 Stack Tecnológico
- **Lenguaje:** Python 3.14
- **Framework Web:** Streamlit
- **Visualización Geoespacial:** Folium, Streamlit-Folium
- **Análisis de Datos:** Pandas, NumPy
- **Estadística:** SciPy, Statsmodels (Correlación de Pearson)
- **Reportes:** FPDF2 (Generación de kits en PDF)

## 🚀 Cómo Ejecutar el Proyecto Localmente
1. Clonar el repositorio:  
   `git clone https://github.com/sandrafs8-ship-it/maternidad-informada-Puno.git`
2. Instalar dependencias:  
   `pip install -r dashboard/requirements.txt`
3. Ejecutar la aplicación:  
   `streamlit run dashboard/dashboard/app.py`

## 📂 Estructura del Repositorio
```text
maternidad-informada-Puno/
├── dashboard/
│   ├── dashboard/
│   │   ├── app.py                 # Código principal del dashboard Streamlit
│   │   ├── requirements.txt       # Dependencias del proyecto
│   │   └── puno_provincias.geojson # Límites geoespaciales de Puno (Fase 2)
├── README.md                      # Este archivo
└── LICENSE                        # Licencia de código abierto
