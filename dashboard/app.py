import os
import streamlit as st
import folium
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_folium import st_folium
from fpdf import FPDF

st.set_page_config(page_title="Maternidad Informada Puno", page_icon="🤰", layout="wide")

st.title("🤰 Maternidad Informada Puno")
st.markdown("### Modelo Analítico y Geoespacial para el Combate a la Desinformación en Salud Materno-Infantil")
st.markdown("---")

# ============================================================
# FUNCIONES
# ============================================================
def calcular_IVI(provincia_data):
    pesos = {'internet': 0.40, 'partos_sin': 0.30, 'desnutricion': 0.20, 'mortalidad': 0.10}
    x_internet = provincia_data['internet']
    x_partos = provincia_data['partos_sin']
    x_desnutricion = provincia_data['desnutricion']
    x_mortalidad = min((provincia_data['mortalidad'] / 150) * 100, 100)
    
    IVI = (pesos['internet'] * x_internet) + (pesos['partos_sin'] * x_partos) + \
          (pesos['desnutricion'] * x_desnutricion) + (pesos['mortalidad'] * x_mortalidad)
    
    if IVI <= 33: nivel, color, emoji = "Bajo", "green", "🟢"
    elif IVI <= 66: nivel, color, emoji = "Medio", "orange", "🟠"
    else: nivel, color, emoji = "Alto", "red", "🔴"
    
    return {'IVI': round(IVI, 2), 'nivel': nivel, 'color': color, 'emoji': emoji}

# ============================================================
# CARGAR DATOS REALES DESDE CSV
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Intentar cargar datos_puno.csv desde varias rutas posibles
ruta_datos = os.path.join(BASE_DIR, "data", "datos_puno.csv")
if not os.path.exists(ruta_datos):
    ruta_datos = os.path.join(BASE_DIR, "datos_puno.csv")

if os.path.exists(ruta_datos):
    df_datos = pd.read_csv(ruta_datos)
    st.success(f"✅ Datos cargados desde: {ruta_datos}")
    
    # Convertir CSV a diccionario de provincias
    provincias_data = {}
    for _, row in df_datos.iterrows():
        provincias_data[row['Provincia']] = {
            "lat": float(row['Lat']),
            "lon": float(row['Lon']),
            "internet": float(row['Internet']),
            "partos_sin": float(row['Partos_Sin']),
            "desnutricion": float(row['Desnutricion']),
            "mortalidad": float(row['Mortalidad'])
        }
    
    # Calcular IVI para cada provincia
    for nombre, data in provincias_data.items():
        provincias_data[nombre].update(calcular_IVI(data))
    
    # Crear DataFrame para visualizaciones
    df = pd.DataFrame([
        {"Provincia": nombre, "Hogares sin internet (%)": data["internet"], "Partos sin asistencia (%)": data["partos_sin"],
         "Desnutrición infantil (%)": data["desnutricion"], "Mortalidad materna (por 100mil)": data["mortalidad"],
         "IVI": data["IVI"], "Nivel de Vulnerabilidad": data["nivel"]}
        for nombre, data in provincias_data.items()
    ])
else:
    st.error(f"⚠️ No se encontró datos_puno.csv en {ruta_datos}")
    st.stop()

# ============================================================
# CORRELACIONES
# ============================================================
corr_internet_partos = round(np.corrcoef(df['Hogares sin internet (%)'], df['Partos sin asistencia (%)'])[0,1], 3)
corr_internet_mortalidad = round(np.corrcoef(df['Hogares sin internet (%)'], df['Mortalidad materna (por 100mil)'])[0,1], 3)

# ============================================================
# FILTROS
# ============================================================
st.sidebar.header("🔍 Filtros")
provincia_seleccionada = st.sidebar.selectbox("Seleccione una provincia:", ["Todas"] + list(provincias_data.keys()))
filtro_nivel = st.sidebar.multiselect("Filtrar por nivel:", ["Alto", "Medio", "Bajo"], default=["Alto", "Medio", "Bajo"])

if provincia_seleccionada != "Todas":
    df_filtrado = df[df["Provincia"] == provincia_seleccionada]
else:
    df_filtrado = df[df["Nivel de Vulnerabilidad"].isin(filtro_nivel)]

# ============================================================
# MAPA
# ============================================================
st.subheader("🗺️ Mapa de Vulnerabilidad Informativa (IVI)")
col_peru, col_puno = st.columns([1, 3])

with col_peru:
    st.markdown("##### 🇵🇪 Ubicación en Perú")
    m_peru = folium.Map(location=[-9.19, -75.0159], zoom_start=6, tiles="OpenStreetMap")
    folium.Marker(location=[-15.8402, -70.0219], popup="<b>Región Puno</b><br>Zona de intervención", icon=folium.Icon(color="red")).add_to(m_peru)
    st_folium(m_peru, width=400, height=450)

with col_puno:
    st.markdown("##### 📍 Detalle Regional - Puno")
    m_puno = folium.Map(location=[-15.5, -69.8], zoom_start=8, tiles="OpenStreetMap")
    for nombre, data in provincias_data.items():
        if filtro_nivel and data["nivel"] not in filtro_nivel: continue
        if provincia_seleccionada != "Todas" and nombre != provincia_seleccionada: continue
        radio = 25 if data["nivel"] == "Alto" else (20 if data["nivel"] == "Medio" else 15)
        folium.CircleMarker(location=[data["lat"], data["lon"]], radius=radio,
            popup=f"<b>{nombre}</b><br>IVI: {data['IVI']}<br>Nivel: {data['emoji']} {data['nivel']}",
            color=data["color"], fill=True, fill_color=data["color"], fill_opacity=0.6, weight=2).add_to(m_puno)
    st_folium(m_puno, width=900, height=450)

st.markdown("**Leyenda:** 🔴 Alto (IVI > 66) | 🟠 Medio (34-66) | 🟢 Bajo (IVI < 33)")
st.markdown("---")

# ============================================================
# INDICADORES CLAVE
# ============================================================
st.subheader("📊 Indicadores Clave (Promedio Filtrado)")
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Prom. Hogares sin Internet", f"{df_filtrado['Hogares sin internet (%)'].mean():.1f}%")
with col2: st.metric("Prom. Partos sin Asistencia", f"{df_filtrado['Partos sin asistencia (%)'].mean():.1f}%")
with col3: st.metric("Prom. Desnutrición Infantil", f"{df_filtrado['Desnutrición infantil (%)'].mean():.1f}%")
with col4: st.metric("Prom. Mortalidad Materna", f"{df_filtrado['Mortalidad materna (por 100mil)'].mean():.0f}")
st.markdown("---")

# ============================================================
# PESTAÑAS (AHORA CON 4 CORRECTAMENTE)
# ============================================================
st.subheader("📈 Análisis Comparativo por Provincia")
tab1, tab2, tab3, tab4 = st.tabs(["🌐 Conectividad", "🤰 Partos", "👶 Desnutrición", "🔬 Cohorte Gestantes"])

with tab1:
    fig1 = px.bar(df_filtrado, x="Provincia", y="Hogares sin internet (%)", color="Nivel de Vulnerabilidad",
                  color_discrete_map={"Alto": "red", "Medio": "orange", "Bajo": "green"}, title="% Hogares sin Internet")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    partos_con = 100 - df_filtrado["Partos sin asistencia (%)"].mean()
    partos_sin = df_filtrado["Partos sin asistencia (%)"].mean()
    df_partos = pd.DataFrame({"Tipo": ["Con asistencia", "Sin asistencia"], "Porcentaje": [partos_con, partos_sin]})
    fig2 = px.pie(df_partos, values="Porcentaje", names="Tipo", title="Distribución de Partos",
                  color_discrete_map={"Con asistencia": "green", "Sin asistencia": "red"})
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    fig3 = px.bar(df_filtrado.sort_values("Desnutrición infantil (%)", ascending=True), 
                  x="Desnutrición infantil (%)", y="Provincia", orientation="h", color="Nivel de Vulnerabilidad",
                  color_discrete_map={"Alto": "red", "Medio": "orange", "Bajo": "green"}, title="% Desnutrición Infantil")
    st.plotly_chart(fig3, use_container_width=True)

# ============================================================
# COHORTE DE GESTANTES (RUTA CORREGIDA)
# ============================================================
with tab4:
    st.markdown("### 🔬 Resultados de la Cohorte de Gestantes (n=75)")
    
    # Buscar cohorte_gestantes.csv en varias rutas posibles
    ruta_cohorte = os.path.join(BASE_DIR, "data", "data", "cohorte_gestantes.csv")
    if not os.path.exists(ruta_cohorte):
        ruta_cohorte = os.path.join(BASE_DIR, "data", "cohorte_gestantes.csv")
    
    if os.path.exists(ruta_cohorte):
        df_cohorte = pd.read_csv(ruta_cohorte)
        
        if provincia_seleccionada != "Todas":
            df_cohorte_filt = df_cohorte[df_cohorte['Provincia'] == provincia_seleccionada]
            st.info(f"📍 Mostrando {len(df_cohorte_filt)} gestantes de **{provincia_seleccionada}**")
        else:
            df_cohorte_filt = df_cohorte
            st.info(f"📍 Mostrando las {len(df_cohorte_filt)} gestantes de toda la región")
        
        if len(df_cohorte_filt) > 0:
            c1, c2, c3 = st.columns(3)
            c1.metric("Edad promedio", f"{df_cohorte_filt['Edad'].mean():.1f} años")
            c2.metric("Exposición a desinformación", f"{df_cohorte_filt['Exposicion_Desinformacion'].mean():.1f}%")
            c3.metric("Controles prenatales promedio", f"{df_cohorte_filt['Controles_Prenatales'].mean():.1f}")
            
            c4, c5 = st.columns(2)
            with c4:
                st.plotly_chart(
                    px.scatter(df_cohorte_filt, 
                              x="Edad", 
                              y="Exposicion_Desinformacion",
                              color="Nivel_Educativo",
                              hover_name="Provincia",
                              trendline="ols",
                              title="Edad vs Exposición a Desinformación"),
                    use_container_width=True
                )
            with c5:
                st.plotly_chart(
                    px.scatter(df_cohorte_filt,
                              x="Controles_Prenatales",
                              y="Exposicion_Desinformacion",
                              color="Nivel_Educativo",
                              hover_name="Provincia",
                              trendline="ols",
                              title="Controles Prenatales vs Exposición"),
                    use_container_width=True
                )
            
            with st.expander("📋 Ver datos anonimizados de la cohorte"):
                st.dataframe(df_cohorte_filt[['ID', 'Provincia', 'Edad', 'Nivel_Educativo', 'Exposicion_Desinformacion', 'Controles_Prenatales']])
        else:
            st.warning("No hay gestantes registradas en esta provincia en la cohorte.")
    else:
        st.error("⚠️ No se encontró `cohorte_gestantes.csv`")

st.markdown("---")

# ============================================================
# ANÁLISIS ESTADÍSTICO
# ============================================================
st.subheader("🧮 Análisis Estadístico: Correlación de Pearson")
col1, col2 = st.columns(2)
with col1:
    st.info(f"**🔗 Internet vs Partos sin asistencia**\n\nCoeficiente de Pearson: **r = {corr_internet_partos}**\n\n{'✅ Correlación FUERTE positiva' if abs(corr_internet_partos) > 0.7 else '⚠️ Correlación moderada'}")
with col2:
    st.info(f"**🔗 Internet vs Mortalidad materna**\n\nCoeficiente de Pearson: **r = {corr_internet_mortalidad}**\n\n{'✅ Correlación significativa' if abs(corr_internet_mortalidad) > 0.5 else '⚠️ Correlación débil'}")

fig_scatter = px.scatter(df, x="Hogares sin internet (%)", y="Partos sin asistencia (%)", size="IVI", color="Nivel de Vulnerabilidad",
                         hover_name="Provincia", color_discrete_map={"Alto": "red", "Medio": "orange", "Bajo": "green"},
                         title=f"Relación Conectividad vs Salud Materna (r = {corr_internet_partos})", trendline="ols", trendline_color_override="blue")
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# ============================================================
# FICHA DETALLADA
# ============================================================
st.subheader("📋 Ficha Detallada de la Provincia")
if provincia_seleccionada != "Todas":
    data = provincias_data[provincia_seleccionada]
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### 📍 {provincia_seleccionada}")
        st.markdown(f"**Nivel de Vulnerabilidad:** {data['emoji']} {data['nivel']}")
        st.markdown(f"**Puntaje IVI:** {data['IVI']} / 100")
        st.markdown(f"**Hogares sin internet:** {data['internet']}%")
    with col2:
        st.markdown(f"**Partos sin asistencia:** {data['partos_sin']}%")
        st.markdown(f"**Desnutrición infantil:** {data['desnutricion']}%")
        st.markdown(f"**Mortalidad materna:** {data['mortalidad']} por 100mil")
else:
    st.info("Seleccione una provincia en la barra lateral para ver su ficha detallada.")

st.markdown("---")
st.caption("Desarrollado por el Equipo Resiliencia Informativa Andina - Desafío OEA 2026 🇵🇪")
