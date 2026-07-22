import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static

# Configuración de la página
st.set_page_config(page_title="Maternidad Informada Puno", page_icon="🤰", layout="wide")

# Encabezado
st.title("🤰 Maternidad Informada Puno")
st.markdown("### Modelo Analítico y Geoespacial para el Combate a la Desinformación en Salud Materno-Infantil")
st.markdown("---")

# Barra lateral para filtros
st.sidebar.header("Filtros")
provincia_seleccionada = st.sidebar.selectbox(
    "Seleccione una provincia de Puno:",
    ["Todas", "Puno", "San Román", "Huanc
     )

# Sección principal: Mapa y Datos
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Mapa de Vulnerabilidad Informativa (IVI)")
    st.info("Aquí se renderizará el mapa geoespacial interactivo con codificación por colores (🔴 Alto, 🟡 Medio, 🟢 Bajo) usando Folium/Geopandas.")
    # TODO: Ingeniero integrará aquí el mapa real con shapefiles del INEI

with col2:
    st.subheader("📊 Ficha de la Provincia")
    if provincia_seleccionada != "Todas":
        st.markdown(f"**Provincia:** {provincia_seleccionada}")
        st.markdown("**Estado:** 🔴 Vulnerabilidad Alta (Ejemplo)")
        st.markdown("**Factores de riesgo:**")
        st.write("- 65% de hogares sin internet")
        st.write("- 30% de partos sin asistencia calificada")

    st.markdown("---")
        st.markdown("⚠️ **Bulos detectados:**")
        st.write("- 'El hierro del MINSA esteriliza a las mujeres andinas'")
        
        st.markdown("---")
        st.markdown("💡 **Recomendación:**")
        st.write("Activar red de obstetras comunitarias y distribuir material impreso bilingüe.")
    else:
        st.write("Seleccione una provincia para ver el detalle.")

# Botón de Innovación: Kit de Verificación
st.markdown("---")
st.subheader("📥 Exportar Kit de Verificación")
st.write("Genere una infografía en PDF opt
         if st.button("Descargar Kit para WhatsApp (PDF)"):
    st.success("✅ Generando PDF con mitos y realidades... (Funcionalidad en desarrollo por el equipo técnico)")

# Pie de página
st.markdown("---")
st.caption("Desarrollado por el Equipo Res
