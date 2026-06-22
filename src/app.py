import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Biblioteca Jorge Roa Martínez — Tablero de Perfiles",
    page_icon="📚",
    layout="wide"
)

# ── Paleta coherente con la tesis ─────────────────────────────────────────
COLORES = {
    0: "#F39C12",
    1: "#1A3A5C",
    2: "#2E86AB",
    3: "#C0392B",
}
NOMBRES = {
    0: "Físico Perdido",
    1: "Digital Consolidado",
    2: "Digital Perdido",
    3: "Físico Activo",
}
DESCRIPCIONES = {
    0: "Usuarios que usaron exclusivamente servicios físicos hace más de 2 años y no han retornado. Representan usuarios perdidos del canal presencial.",
    1: "Usuarios activos con alta frecuencia y uso predominantemente digital. Son el segmento más valioso y numeroso de la biblioteca.",
    2: "Usuarios con contacto mínimo y puntual en recursos digitales hace más de un año. Alto potencial de reactivación.",
    3: "Usuarios con uso físico activo y moderado. Veteranos de la biblioteca con mayor antigüedad promedio.",
}
COLOR_MAP = {NOMBRES[k]: v for k, v in COLORES.items()}

NOMBRES_FAC = {
    'salud': 'Salud', 'ingenierias': 'Ingenierías',
    'ciencias_educacion': 'Cs. Educación', 'tecnologia': 'Tecnología',
    'apoyo_administrativo': 'Apoyo Adm.', 'bellas_artes': 'Bellas Artes',
    'ciencias_empresariales': 'Cs. Empresariales', 'ciencias_agrarias': 'Cs. Agrarias',
    'mecanica': 'Mecánica', 'ciencias_ambientales': 'Cs. Ambientales',
    'externo': 'Externo', 'ciencias_basicas': 'Cs. Básicas',
    'fac_desconocida': 'Desconocida', 'biblioteca': 'Biblioteca',
    'rectoria': 'Rectoría', 'univirtual': 'Univirtual', 'ilex': 'ILEX',
}

# ── Carga de datos ─────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    rfm = pd.read_csv("df_rfm_limpio.csv", index_col=0)
    rfm["cluster"] = rfm["cluster"].astype(int)
    rfm["perfil"]  = rfm["cluster"].map(NOMBRES)

    cols_fac = ["codigo", "facultad", "nombre_recurso", "tipo_recurso", "anio", "mes",
                "semana_semestre", "periodo_academico", "nivel_academico_final",
                "cluster", "fechas"]
    fac = pd.read_csv("df_fac.csv", low_memory=False, usecols=cols_fac)
    fac["cluster"] = fac["cluster"].astype(int)
    fac["perfil"]  = fac["cluster"].map(NOMBRES)
    fac["fechas"]  = pd.to_datetime(fac["fechas"], errors="coerce")
    fac["facultad_label"] = fac["facultad"].map(NOMBRES_FAC).fillna(fac["facultad"])
    return rfm, fac

rfm, fac = cargar_datos()

# ── Sidebar ────────────────────────────────────────────────────────────────
st.sidebar.markdown("## Biblioteca UTP")
st.sidebar.markdown("### Filtros")

perfiles_disponibles = ["Todos"] + [NOMBRES[i] for i in sorted(NOMBRES)]
perfil_sel = st.sidebar.selectbox("Perfil de usuario", perfiles_disponibles)

facultades_disponibles = ["Todas"] + sorted(
    fac["facultad_label"].dropna().unique().tolist()
)
facultad_sel = st.sidebar.selectbox("Facultad", facultades_disponibles)

anios_disponibles = sorted(fac["anio"].dropna().unique().astype(int).tolist())
anio_sel = st.sidebar.multiselect("Año", anios_disponibles, default=anios_disponibles)

st.sidebar.markdown("---")
st.sidebar.markdown("**Modelo:** K-Means K=4")
st.sidebar.markdown("**Silhouette:** 0.4269")
st.sidebar.markdown("**Periodo:** 2022–2025")
st.sidebar.markdown("**Usuarios:** 19.081")
st.sidebar.markdown("**Registros:** 1.784.919")

st.sidebar.markdown("---")
st.sidebar.markdown("#### ¿Qué significa cada perfil?")
for k, v in NOMBRES.items():
    color = COLORES[k]
    st.sidebar.markdown(
        f"<span style='color:{color}; font-weight:bold'>● {v}</span><br>"
        f"<small>{DESCRIPCIONES[k]}</small>",
        unsafe_allow_html=True
    )
    st.sidebar.markdown("")

# ── Aplicar filtros ────────────────────────────────────────────────────────
rfm_f = rfm.copy()
fac_f = fac[fac["anio"].isin(anio_sel if anio_sel else anios_disponibles)].copy()

if perfil_sel != "Todos":
    rfm_f = rfm_f[rfm_f["perfil"] == perfil_sel]
    fac_f = fac_f[fac_f["perfil"] == perfil_sel]

if facultad_sel != "Todas":
    fac_f = fac_f[fac_f["facultad_label"] == facultad_sel]

# ── Encabezado ─────────────────────────────────────────────────────────────
st.markdown("## Biblioteca Jorge Roa Martínez — UTP")
st.markdown("### Tablero de Monitoreo de Perfiles de Usuario")
st.caption("Modelo K-Means K=4 · Silhouette 0.4269 · Periodo 2022–2025 · 19.081 usuarios · 1.784.919 registros")
st.markdown("---")

# ── KPIs ───────────────────────────────────────────────────────────────────
st.markdown("#### Resumen de perfiles")
col1, col2, col3, col4 = st.columns(4)

dist = rfm.groupby("cluster").size().reset_index(name="usuarios")
dist["perfil"] = dist["cluster"].map(NOMBRES)
dist["pct"]    = (dist["usuarios"] / dist["usuarios"].sum() * 100).round(1)

for i, col in enumerate([col1, col2, col3, col4]):
    row = dist[dist["cluster"] == i].iloc[0]
    color = COLORES[i]
    with col:
        st.metric(
            label=NOMBRES[i],
            value=f"{int(row['usuarios']):,}",
            delta=f"{row['pct']}% del total"
        )
        st.markdown(
            f"<p style='font-size:11px; color:{color}; margin-top:-10px;'>"
            f"{DESCRIPCIONES[i]}</p>",
            unsafe_allow_html=True
        )

if perfil_sel != "Todos":
    cluster_sel = [k for k, v in NOMBRES.items() if v == perfil_sel][0]
    st.info(f"**{perfil_sel}:** {DESCRIPCIONES[cluster_sel]}")
st.markdown("---") 

# ── Fila 1: Distribución + Top Recursos ───────────────────────────────────
col_a, col_b = st.columns([1, 1])

with col_a:
    st.markdown("##### Distribución de perfiles")
    st.caption("Proporción de usuarios por perfil sobre el total de 19.081 usuarios únicos.")
    fig_pie = px.pie(
        dist, values="usuarios", names="perfil",
        color="perfil", color_discrete_map=COLOR_MAP,
        hole=0.45,
        hover_data=["usuarios", "pct"],
    )
    fig_pie.update_traces(
        textposition="outside", textinfo="percent+label",
        pull=[0.03]*4,
        hovertemplate="<b>%{label}</b><br>Usuarios: %{value:,}<br>Proporción: %{percent}<extra></extra>"
    )
    fig_pie.update_layout(showlegend=False,
                          margin=dict(t=30, b=30, l=20, r=20), height=360)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_b:
    st.markdown("##### Top 10 Recursos Más Demandados")
    st.caption("Volumen absoluto de interacciones. Permite visualizar qué recursos sostienen la operatividad de la biblioteca.")

    top_10 = fac_f["nombre_recurso"].value_counts().nlargest(10).index
    df_top10 = fac_f[fac_f["nombre_recurso"].isin(top_10)].copy()
    df_bar = df_top10.groupby(["nombre_recurso", "perfil"]).size().reset_index(name="interacciones")

    fig_top = px.bar(
        df_bar,
        y="nombre_recurso",
        x="interacciones",
        color="perfil",
        orientation="h",
        color_discrete_map=COLOR_MAP,
        category_orders={"nombre_recurso": list(top_10[::-1])},
        labels={"nombre_recurso": "", "interacciones": "Total de registros"}
    )
    fig_top.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Perfil: %{fullData.name}<br>"
            "Interacciones: %{x:,}<extra></extra>"
        )
    )
    fig_top.update_layout(
        margin=dict(t=20, b=20, l=10, r=20), height=360,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, title=None),
        xaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.2)')
    )
    st.plotly_chart(fig_top, use_container_width=True)

st.markdown("---")

# ── Fila 2: Facultades en riesgo ──────────────────────────────────────────
st.markdown("##### Usuarios en riesgo por facultad")
st.caption("Proporción de usuarios por perfil dentro de cada facultad. Las facultades con mayor barra naranja+azul claro tienen más usuarios perdidos.")

facultades_validas = list(NOMBRES_FAC.keys())
fac_riesgo_filtrado = fac_f[fac_f["facultad"].isin(facultades_validas)].copy()

usuarios_fac = (fac_riesgo_filtrado.groupby(["facultad", "cluster"])["codigo"]
                .nunique().reset_index(name="usuarios"))
usuarios_fac["total"]  = usuarios_fac.groupby("facultad")["usuarios"].transform("sum")
usuarios_fac["pct"]    = (usuarios_fac["usuarios"] / usuarios_fac["total"] * 100).round(1)
usuarios_fac["perfil"] = usuarios_fac["cluster"].map(NOMBRES)
usuarios_fac["facultad_label"] = usuarios_fac["facultad"].map(NOMBRES_FAC)

riesgo_orden = (
    usuarios_fac[usuarios_fac["cluster"].isin([0, 2])]
    .groupby("facultad")["pct"].sum()
    .sort_values(ascending=True)
)
orden_labels = [NOMBRES_FAC.get(f, f) for f in riesgo_orden.index]
riesgo_total = riesgo_orden.reset_index()
riesgo_total.columns = ["facultad", "pct_riesgo_total"]
usuarios_fac = usuarios_fac.merge(riesgo_total, on="facultad", how="left")

fig_fac = px.bar(
    usuarios_fac, x="pct", y="facultad_label",
    color="perfil", orientation="h",
    color_discrete_map=COLOR_MAP, barmode="stack",
    labels={"pct": "% usuarios", "facultad_label": ""},
    category_orders={"facultad_label": orden_labels},
    custom_data=["usuarios", "total", "pct_riesgo_total"],
)
fig_fac.update_traces(
    hovertemplate=(
        "<b>%{fullData.name}</b><br>"
        "Facultad: %{y}<br>"
        "Usuarios: %{customdata[0]:,}<br>"
        "% de la facultad: %{x}%<br>"
        "Total facultad: %{customdata[1]:,}<br>"
        "% en riesgo total: %{customdata[2]:.1f}%<extra></extra>"
    )
)
fig_fac.update_layout(
    margin=dict(t=20, b=20, l=20, r=20), height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    xaxis=dict(range=[0, 105]),
)
st.plotly_chart(fig_fac, use_container_width=True)

st.markdown("---")

# ── Fila 3: Comportamiento semanal ────────────────────────────────────────
st.markdown("##### Comportamiento por semana del semestre")
st.caption("% normalizado por perfil. Permite identificar si cada perfil responde diferente a los momentos clave del semestre.")

if "semana_semestre" in fac_f.columns:
    sem = (fac_f.groupby(["semana_semestre", "perfil"])
           .size().reset_index(name="registros"))
    sem = sem[sem["semana_semestre"].between(1, 18)]
    sem["pct"] = sem.groupby("perfil")["registros"].transform(
        lambda x: x / x.sum() * 100).round(2)

    fig_sem = px.line(
        sem, x="semana_semestre", y="pct",
        color="perfil", color_discrete_map=COLOR_MAP,
        markers=True,
        labels={"semana_semestre": "Semana del semestre",
                "pct": "% de actividad del perfil"},
        custom_data=["registros"],
    )
    fig_sem.update_traces(
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"
            "Semana: %{x}<br>"
            "% actividad: %{y:.1f}%<br>"
            "Registros: %{customdata[0]:,}<extra></extra>"
        )
    )
    fig_sem.add_vrect(x0=6.5, x1=9.5,
                      fillcolor="rgba(200,200,200,0.15)",
                      annotation_text="Parciales midterm",
                      annotation_position="top left", line_width=0)
    fig_sem.add_vrect(x0=13.5, x1=16.5,
                      fillcolor="rgba(243,156,18,0.08)",
                      annotation_text="Parciales finales",
                      annotation_position="top left", line_width=0)
    fig_sem.update_layout(
        margin=dict(t=30, b=20, l=20, r=20), height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig_sem, use_container_width=True)

st.markdown("---")

# ── Tabla de Diagnóstico por Perfil ──────────────────────────────────────
st.markdown("##### Diagnóstico por Perfil")
st.caption("Métricas complementarias — antigüedad, canal predominante y recursos más consultados.")
tabla = rfm.groupby("perfil").agg(
    Usuarios           = ("cluster",     "count"),
    Antiguedad_mediana = ("tenure_dias", "median"),
    Pct_usa_fisico     = ("usa_fisico",  "mean"),
).reset_index().rename(columns={"perfil": "Perfil"})

rec_fisico = (
    fac[fac["tipo_recurso"] == "fisico"]
    .groupby("perfil")["nombre_recurso"]
    .agg(lambda x: x.value_counts().index[0] if len(x) > 0 else "N/A")
    .reset_index()
    .rename(columns={"perfil": "Perfil", "nombre_recurso": "Recurso físico top"})
)
rec_digital = (
    fac[fac["tipo_recurso"] == "digital"]
    .groupby("perfil")["nombre_recurso"]
    .agg(lambda x: x.value_counts().index[0] if len(x) > 0 else "N/A")
    .reset_index()
    .rename(columns={"perfil": "Perfil", "nombre_recurso": "Recurso digital top"})
)
tabla = tabla.merge(rec_fisico,  on="Perfil", how="left")
tabla = tabla.merge(rec_digital, on="Perfil", how="left")
tabla["Recurso físico top"]   = tabla["Recurso físico top"].fillna("N/A")
tabla["Recurso digital top"]  = tabla["Recurso digital top"].fillna("N/A")
tabla["Usuarios"]             = tabla["Usuarios"].apply(lambda x: f"{x:,}")
tabla["Antigüedad (días)"]    = tabla["Antiguedad_mediana"].round(0).astype(int)
tabla["Tiene uso físico (%)"] = (tabla["Pct_usa_fisico"] * 100).round(1).astype(str) + "%"

cols_mostrar = [
    "Perfil", "Usuarios",
    "Antigüedad (días)", "Tiene uso físico (%)",
    "Recurso físico top", "Recurso digital top"
]
tabla = tabla[cols_mostrar]
orden_perfiles = [NOMBRES[i] for i in sorted(NOMBRES)]
tabla["Perfil"] = pd.Categorical(tabla["Perfil"], categories=orden_perfiles, ordered=True)
tabla = tabla.sort_values("Perfil")
st.dataframe(tabla, use_container_width=True, hide_index=True)
st.markdown("---")
st.caption("Biblioteca Jorge Roa Martínez · UTP · Especialización en Analítica y Ciencia de Datos · 2026 · Modelo: K-Means K=4 · Silhouette: 0.4269")