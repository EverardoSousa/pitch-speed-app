
import streamlit as st
import requests
import numpy as np

# Simulador de API (puede reemplazarse por una API real como Statcast o MLB API)
def get_pitcher_data_from_api(pitcher_name):
    data = {
        "Jacob deGrom": {
            "avgSpeed": 97.2,
            "injuryFactor": 0.1,
            "restDays": 5,
            "stadiumFactor": 0.3,
            "temperature": 75,
            "pressureGame": 0.7
        },
        "Shohei Ohtani": {
            "avgSpeed": 96.5,
            "injuryFactor": 0.2,
            "restDays": 4,
            "stadiumFactor": 0.2,
            "temperature": 78,
            "pressureGame": 0.9
        },
        "Gerrit Cole": {
            "avgSpeed": 97.0,
            "injuryFactor": 0.05,
            "restDays": 6,
            "stadiumFactor": 0.4,
            "temperature": 65,
            "pressureGame": 0.6
        },
        "Max Scherzer": {
            "avgSpeed": 96.1,
            "injuryFactor": 0.3,
            "restDays": 3,
            "stadiumFactor": -0.2,
            "temperature": 82,
            "pressureGame": 1.0
        }
    }
    return data.get(pitcher_name, None)

def predict_speed(stats):
    return (stats["avgSpeed"] * (1 - 0.25 * stats["injuryFactor"]) +
            0.5 * stats["restDays"] +
            1.0 * stats["stadiumFactor"] +
            0.03 * stats["temperature"] -
            1.5 * stats["pressureGame"])

def expected_value(prob_over, momio):
    payout = momio / 100 if momio > 0 else 100 / abs(momio)
    return (prob_over * payout) - (1 - prob_over)

# Interfaz Streamlit
st.title("Predicción de Velocidad de Primer Lanzamiento y Evaluación de Apuesta")

pitchers = ["Jacob deGrom", "Shohei Ohtani", "Gerrit Cole", "Max Scherzer"]
pitcher = st.selectbox("Selecciona un pitcher", pitchers)

linea = st.number_input("Línea del casino (mph)", value=96.5)
momio = st.number_input("Momio (ej. -110)", value=-110)

if st.button("Calcular predicción y evaluar apuesta"):
    stats = get_pitcher_data_from_api(pitcher)
    if stats:
        velocidad = predict_speed(stats)
        prob_over = 1 / (1 + np.exp(-(velocidad - linea)))
        ev = expected_value(prob_over, momio)

        st.metric("Velocidad estimada del primer pitcheo", f"{velocidad:.2f} mph")
        st.metric("Probabilidad de Over", f"{prob_over*100:.2f}%")
        st.metric("Valor Esperado", f"{ev:.2f}")

        if ev > 0:
            st.success("✅ Recomendación: Apostar Over")
        else:
            st.error("❌ Recomendación: No apostar Over (posible Under)")
    else:
        st.warning("Pitcher no encontrado en base de datos")
