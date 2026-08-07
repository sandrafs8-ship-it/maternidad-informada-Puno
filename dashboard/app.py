import os
import json
import streamlit as st
import folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
def calcular_IVI(data):
    pesos = {'internet': 0.30, 'partos_sin': 0.25, 'desnutricion': 0.20, 'mortalidad': 0.15, 'pobreza': 0.10}
    x_internet = data['internet']
    x_partos = data['partos_sin']
    x_desnutricion = data['desnutricion']
    x_mortalidad = min((data['mortalidad'] / 150) * 100, 100)
    x_pobreza = data.get('pobreza', 30)
    
    IVI = (pesos['internet'] * x_internet) + (pesos['partos_sin'] * x_partos) + \
          (pesos['desnutricion'] * x_desnutricion) + (pesos['mortalidad'] * x_mortalidad) + \
          (pesos['pobreza'] * x_pobreza)
    
    if IVI <= 33: nivel, color, emoji = "Bajo", "green", "🟢"
    elif IVI <= 66: nivel, color, emoji = "Medio", "orange", "🟠"
    else: nivel, color, emoji = "Alto", "red", "🔴"
    
    return {'IVI': round(IVI, 2), 'nivel': nivel, 'color': color, 'emoji': emoji}

# ============================================================
# CARGAR DATOS
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cargar datos de provincias
ruta_datos = os.path.join(BASE_DIR, "data", "datos_puno.csv")
if not os.path.exists(ruta_datos):
    ruta_datos = os.path.join(BASE_DIR, "datos_puno.csv")

if os.path.exists(ruta_datos):
    df_datos = pd.read_csv(ruta_datos)
    st.success(f"✅ Datos cargados: {len(df_datos)} provincias con {len(df_datos.columns)-3} indicadores")
    
    provincias_data = {}
    for _, row in df_datos.iterrows():
        prov_dict = {
            "lat": float(row['Lat']),
            "lon": float(row['Lon']),
            "internet": float(row['Internet']),
            "partos_sin": float(row['Partos_Sin']),
            "desnutricion": float(row['Desnutricion']),
            "mortalidad": float(row['Mortalidad']),
            "poblacion": float(row.get('Poblacion', 50000)),
            "hospitales": int(row.get('Hospitales', 1)),
            "centros_salud": int(row.get('Centros_Salud', 10)),
            "medicos_1000": float(row.get('Medicos_por_1000', 1.0)),
            "alfabetizacion": float(row.get('Alfabetizacion', 85)),
            "pobreza": float(row.get('Pobreza', 30)),
            "agua_potable": float(row.get('Agua_Potable', 70)),
            "desague": float(row.get('Desague', 65))
        }
        provincias_data[row['Provincia']] = prov_dict
        provincias_data[row['Provincia']].update(calcular_IVI(prov_dict))
    
    df = pd.DataFrame([
        {"Provincia": nombre, **{k: v for k, v in data.items() if k not in ['lat', 'lon']}}
        for nombre, data in provincias_data.items()
    ])
else:
    st.error("⚠️ No se encontró datos_puno.csv")
    st.stop()

# Cargar cohorte de gestantes
ruta_cohorte = os.path.join(BASE_DIR, "data", "data", "cohorte_gestantes.csv")
if not os.path.exists(ruta_cohorte):
    ruta_cohorte = os.path.join(BASE_DIR, "data", "cohorte_gestantes.csv")

if os.path.exists(ruta_cohorte):
    df_cohorte = pd.read_csv(ruta_cohorte)
    st.success(f"✅ Cohorte cargada: {len(df_cohorte)} gestantes con {len(df_cohorte.columns)} variables")
else:
    df_cohorte = None
    st.warning("⚠️ No se encontró cohorte_gestantes.csv")

# Cargar GeoJSON
ruta_geojson = os.path.join(BASE_DIR, "dashboard", "puno_provincias.geojson")
geojson_data = None
if os.path.exists(ruta_geojson):
    with open(ruta_geojson, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

# ============================================================
# CORRELACIONES
# ============================================================
corr_internet_partos = round(np.corrcoef(df['internet'], df['partos_sin'])[0,1], 3)
corr_internet_mortalidad = round(np.corrcoef(df['internet'], df['mortalidad'])[0,1], 3)

# ============================================================
# FILTROS
# ============================================================
st.sidebar.header("🔍 Filtros")
provincia_seleccionada = st.sidebar.selectbox("Seleccione una provincia:", ["Todas"] + list(provincias_data.keys()))
filtro_nivel = st.sidebar.multiselect("Filtrar por nivel:", ["Alto", "Medio", "Bajo"], default=["Alto", "Medio", "Bajo"])

if provincia_seleccionada != "Todas":
    df_filtrado = df[df["Provincia"] == provincia_seleccionada]
else:
    df_filtrado = df[df["nivel"].isin(filtro_nivel)]

# ============================================================
# MAPA CON GEOJSON
# ============================================================
st.subheader("🗺️ Mapa de Vulnerabilidad Informativa (IVI)")

col_peru, col_puno = st.columns([1, 3])

with col_peru:
    st.markdown("##### 🇵🇪 Ubicación en Perú")
    m_peru = folium.Map(location=[-9.19, -75.0159], zoom_start=6, tiles="OpenStreetMap")
    folium.Marker(location=[-15.8402, -70.0219], popup="<b>Región Puno</b><br>Zona de intervención", 
                  icon=folium.Icon(color="red")).add_to(m_peru)
    st_folium(m_peru, width=400, height=450)

with col_puno:
    st.markdown("##### 📍 Detalle Regional - Puno")
    m_puno = folium.Map(location=[-15.5, -69.8], zoom_start=8, tiles="OpenStreetMap")
    
    # Capa GeoJSON (si existe)
    if geojson_data:
        def estilo(feature):
            prov_name = feature['properties'].get('NOM_PROV', '')
            if prov_name in provincias_data:
                data = provincias_data[prov_name]
                if data['nivel'] in filtro_nivel:
                    return {"fillColor": data['color'], "color": data['color'], 
                            "weight": 2, "fillOpacity": 0.55}
            return {"fillColor": "gray", "color": "gray", "weight": 1, "fillOpacity": 0.2}
        
        folium.GeoJson(
            geojson_data,
            style_function=estilo,
            tooltip=folium.GeoJsonTooltip(fields=['NOM_PROV'], labels=False)
        ).add_to(m_puno)
    
    # Marcadores
    for nombre, data in provincias_data.items():
        if data['nivel'] not in filtro_nivel:
            continue
        if provincia_seleccionada != "Todas" and nombre != provincia_seleccionada:
            continue
        radio = 15 if data['nivel'] == "Alto" else (12 if data['nivel'] == "Medio" else 10)
        folium.CircleMarker(
            location=[data['lat'], data['lon']], radius=radio,
            popup=f"<b>{nombre}</b><br>IVI: {data['IVI']}<br>Población: {int(data['poblacion']):,}",
            color=data['color'], fill=True, fill_color=data['color'], fill_opacity=0.7, weight=2
        ).add_to(m_puno)
    
    st_folium(m_puno, width=900, height=450)

st.markdown("**Leyenda:** 🔴 Alto (IVI > 66) | 🟠 Medio (34-66) | 🟢 Bajo (IVI < 33)")
st.markdown("---")

# ============================================================
# INDICADORES CLAVE
# ============================================================
st.subheader("📊 Indicadores Clave")
col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.metric("Hogares sin Internet", f"{df_filtrado['internet'].mean():.1f}%")
with col2: st.metric("Partos sin Asistencia", f"{df_filtrado['partos_sin'].mean():.1f}%")
with col3: st.metric("Desnutrición Infantil", f"{df_filtrado['desnutricion'].mean():.1f}%")
with col4: st.metric("Mortalidad Materna", f"{df_filtrado['mortalidad'].mean():.0f}")
with col5: st.metric("Pobreza", f"{df_filtrado['pobreza'].mean():.1f}%")
st.markdown("---")

# ============================================================
# PESTAÑAS DE ANÁLISIS
# ============================================================
st.subheader("📈 Análisis Comparativo por Provincia")
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌐 Conectividad", "🤰 Partos", "👶 Desnutrición", "🏥 Infraestructura", "🔬 Cohorte"
])

with tab1:
    fig1 = px.bar(df_filtrado.sort_values('internet', ascending=False), 
                  x="Provincia", y="internet", color="nivel",
                  color_discrete_map={"Alto": "red", "Medio": "orange", "Bajo": "green"},
                  title="% Hogares sin Internet")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    partos_con = 100 - df_filtrado["partos_sin"].mean()
    partos_sin = df_filtrado["partos_sin"].mean()
    df_partos = pd.DataFrame({"Tipo": ["Con asistencia", "Sin asistencia"], 
                              "Porcentaje": [partos_con, partos_sin]})
    fig2 = px.pie(df_partos, values="Porcentaje", names="Tipo", title="Distribución de Partos",
                  color_discrete_map={"Con asistencia": "green", "Sin asistencia": "red"})
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    fig3 = px.bar(df_filtrado.sort_values("desnutricion", ascending=True),
                  x="desnutricion", y="Provincia", orientation="h", color="nivel",
                  color_discrete_map={"Alto": "red", "Medio": "orange", "Bajo": "green"},
                  title="% Desnutrición Infantil")
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.markdown("### 🏥 Infraestructura de Salud")
    col1, col2 = st.columns(2)
    with col1:
        fig_hosp = px.bar(df_filtrado, x="Provincia", y="hospitales", 
                          title="Hospitales por Provincia", color_discrete_sequence=["#2E86AB"])
        st.plotly_chart(fig_hosp, use_container_width=True)
    with col2:
        fig_med = px.bar(df_filtrado, x="Provincia", y="medicos_1000",
                        title="Médicos por 1000 habitantes", color_discrete_sequence=["#A23B72"])
        st.plotly_chart(fig_med, use_container_width=True)
    
    st.markdown("### 💧 Servicios Básicos")
    fig_servicios = go.Figure()
    fig_servicios.add_trace(go.Bar(name='Agua Potable', x=df_filtrado['Provincia'], 
                                   y=df_filtrado['agua_potable'], marker_color='#00B4D8'))
    fig_servicios.add_trace(go.Bar(name='Desagüe', x=df_filtrado['Provincia'],
                                   y=df_filtrado['desague'], marker_color='#FFA62B'))
    fig_servicios.update_layout(barmode='group', title="Cobertura de Servicios Básicos (%)")
    st.plotly_chart(fig_servicios, use_container_width=True)

with tab5:
    if df_cohorte is not None:
        st.markdown(f"### 🔬 Cohorte de Gestantes (n={len(df_cohorte)})")
        
        if provincia_seleccionada != "Todas":
            df_cohorte_filt = df_cohorte[df_cohorte['Provincia'] == provincia_seleccionada]
            st.info(f"📍 Mostrando {len(df_cohorte_filt)} gestantes de **{provincia_seleccionada}**")
        else:
            df_cohorte_filt = df_cohorte
            st.info(f"📍 Mostrando las {len(df_cohorte_filt)} gestantes de toda la región")
        
        if len(df_cohorte_filt) > 0:
            # Métricas principales
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Edad promedio", f"{df_cohorte_filt['Edad'].mean():.1f} años")
            c2.metric("Exposición desinformación", f"{df_cohorte_filt['Exposicion_Desinformacion'].mean():.1f}%")
            c3.metric("Controles prenatales", f"{df_cohorte_filt['Controles_Prenatales'].mean():.1f}")
            c4.metric("Confianza vacunas", f"{df_cohorte_filt['Confianza_Vacunas'].mean():.1f}/10")
            
            # Gráficos
            c5, c6 = st.columns(2)
            with c5:
                st.plotly_chart(
                    px.scatter(df_cohorte_filt, x="Edad", y="Exposicion_Desinformacion",
                              color="Nivel_Educativo", hover_name="Provincia", trendline="ols",
                              title="Edad vs Exposición a Desinformación"),
                    use_container_width=True)
            with c6:
                st.plotly_chart(
                    px.scatter(df_cohorte_filt, x="Controles_Prenatales", y="Exposicion_Desinformacion",
                              color="Nivel_Educativo", hover_name="Provincia", trendline="ols",
                              title="Controles Prenatales vs Exposición"),
                    use_container_width=True)
            
            # Análisis por nivel educativo
            st.markdown("### 📊 Análisis por Nivel Educativo")
            nivel_sel = st.multiselect("Filtrar por nivel educativo:", 
                                       sorted(df_cohorte_filt['Nivel_Educativo'].unique()),
                                       default=sorted(df_cohorte_filt['Nivel_Educativo'].unique()))
            df_viz = df_cohorte_filt[df_cohorte_filt['Nivel_Educativo'].isin(nivel_sel)]
            
            if len(df_viz) > 0:
                df_bar = df_viz.groupby('Provincia', as_index=False)['Controles_Prenatales'].mean()
                df_bar = df_bar.sort_values('Controles_Prenatales', ascending=False)
                st.plotly_chart(
                    px.bar(df_bar, x='Provincia', y='Controles_Prenatales',
                           title="🤱 Promedio de Controles Prenatales por Provincia",
                           color_discrete_sequence=["#2E86AB"]),
                    use_container_width=True)
                
                # Distribución de fuentes de información
                st.markdown("### 📱 Fuentes de Información de Salud")
                df_fuente = df_viz['Fuente_Info_Salud'].value_counts().reset_index()
                df_fuente.columns = ['Fuente', 'Cantidad']
                st.plotly_chart(
                    px.pie(df_fuente, values='Cantidad', names='Fuente',
                           title="¿De dónde obtienen información de salud?"),
                    use_container_width=True)
            
            with st.expander("📋 Ver datos anonimizados de la cohorte"):
                st.dataframe(df_cohorte_filt)
    else:
        st.warning("No se cargó la cohorte de gestantes")

st.markdown("---")

# ============================================================
# ANÁLISIS ESTADÍSTICO
# ============================================================
st.subheader("🧮 Análisis Estadístico: Correlación de Pearson")
col1, col2 = st.columns(2)
with col1:
    st.info(f"**🔗 Internet vs Partos sin asistencia**\n\nCoeficiente: **r = {corr_internet_partos}**\n\n{'✅ Correlación FUERTE positiva' if abs(corr_internet_partos) > 0.7 else '⚠️ Correlación moderada'}")
with col2:
    st.info(f"**🔗 Internet vs Mortalidad materna**\n\nCoeficiente: **r = {corr_internet_mortalidad}**\n\n{'✅ Correlación significativa' if abs(corr_internet_mortalidad) > 0.5 else '⚠️ Correlación débil'}")

fig_scatter = px.scatter(df, x="internet", y="partos_sin", size="IVI", color="nivel",
                         hover_name="Provincia", color_discrete_map={"Alto": "red", "Medio": "orange", "Bajo": "green"},
                         title=f"Relación Conectividad vs Salud Materna (r = {corr_internet_partos})",
                         trendline="ols", trendline_color_override="blue")
st.plotly_chart(fig_scatter, use_container_width=True)
st.markdown("---")

# ============================================================
# FICHA DETALLADA
# ============================================================
st.subheader("📋 Ficha Detallada de la Provincia")
if provincia_seleccionada != "Todas":
    data = provincias_data[provincia_seleccionada]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"### 📍 {provincia_seleccionada}")
        st.markdown(f"**Nivel:** {data['emoji']} {data['nivel']}")
        st.markdown(f"**IVI:** {data['IVI']} / 100")
        st.markdown(f"**Población:** {int(data['poblacion']):,}")
    with col2:
        st.markdown(f"**Internet:** {data['internet']}%")
        st.markdown(f"**Partos sin asistencia:** {data['partos_sin']}%")
        st.markdown(f"**Desnutrición:** {data['desnutricion']}%")
        st.markdown(f"**Mortalidad:** {data['mortalidad']} por 100mil")
    with col3:
        st.markdown(f"**Hospitales:** {data['hospitales']}")
        st.markdown(f"**Centros de salud:** {data['centros_salud']}")
        st.markdown(f"**Médicos/1000:** {data['medicos_1000']}")
        st.markdown(f"**Pobreza:** {data['pobreza']}%")
else:
    st.info("Seleccione una provincia en la barra lateral para ver su ficha detallada.")

st.markdown("---")
st.caption("Desarrollado por el Equipo Resiliencia Informativa Andina - Desafío OEA 2026 🇵🇪")
# Forzar actualización 2026
