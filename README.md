# maternidad-informada-Puno
Dashboard geoespacial para el combate a la desinformación en salud materno-infantil en Puno, Perú. Desafío de Datos para la Democracia - OEA 2026.
# 🤰 Maternidad Informada Puno
### Modelo Analítico y Geoespacial para el Combate a la Desinformación en Salud Materno-Infantil

**Equipo:** Resiliencia Informativa Andina  
**Desafío:** Desafío de Datos para la Democracia (OEA)  
**País:** Perú 🇵🇪  

## 📌 Descripción del Proyecto
Desarrollo de un tablero de control (dashboard) geoespacial interactivo que identifica las provincias y distritos de la región Puno con mayor vulnerabilidad a la desinformación en salud materno-infantil, mediante el cálculo del **Índice de Vulnerabilidad Informativa (IVI)**.

## 🧮 El Modelo: Índice de Vulnerabilidad Informativa (IVI)
El IVI se calcula ponderando cuatro variables clave de datos abiertos:
*   **Brecha Digital (30%)**: Hogares sin acceso a internet (INEI).
*   **Vulnerabilidad en Salud Materna (40%)**: Partos sin asistencia calificada y <4 controles prenatales (ENDES/MINSA).
*   **Nivel Educativo (20%)**: Población femenina >15 años sin secundaria completa (INEI).
*   **Exposición a Desinformación (10%)**: Frecuencia de bulos de salud desmentidos (Ojo Público, Convoca).
## 👥 Equipo: Resiliencia Informativa Andina (5 integrantes)

Nuestro equipo multidisciplinario combina rigor científico, conocimiento territorial y capacidad técnica en datos y análisis geoespacial:

| Rol | Nombre | Institución |
|-----|--------|-------------|
| **Líder de Proyecto / Experta Metodológica y Estadística** | Dra. Sandra Alejandra Fernández Macedo | Universidad Andina Néstor Cáceres Velásquez (UANCV) |
| **Especialista en Alto Riesgo y Emergencias Obstétricas** | Esperanza Cueva Rossel | Hospital Manuel Núñez Butrón - UANCV |
| **Especialista en Planificación de Servicios de Salud** | Sonia Benita Fernández Tapia | Universidad Andina Néstor Cáceres Velásquez (UANCV) |
| **Validador Clínico / Analista de Datos en Salud** | Dr. Julio Jimenez Agüero | Consulta Privada / UANCV |
| **Ingeniero Civil / Especialista en Análisis Geoespacial (SIG) y Desarrollo** | Wilfredo David Supo Pacori | Universidad Andina Néstor Cáceres Velásquez (UANCV) |


## 📂 Estructura del Repositorio
*   `/data`: Datasets procesados y limpios (CSV).
*   `/notebooks`: Notebooks de Jupyter con el proceso analítico reproducible.
*   `/src`: Scripts de Python para el cálculo del IVI y procesamiento.
*   `/docs`: Nota metodológica y manual de usuario del dashboard.

## 🔗 Fuentes de Datos Abiertos
*   [Plataforma Nacional de Datos Abiertos del Perú](https://www.datosabiertos.gob.pe/)
*   [INEI - ENDES y Censos Nacionales](https://www.gob.pe/inei)
*   [Ojo Público](https://ojo-publico.com/) y [Convoca](https://convoca.pe/)

## 📜 Licencia
Este proyecto es de código abierto bajo la licencia [MIT / GNU GPL]. Ver archivo `LICENSE`.
