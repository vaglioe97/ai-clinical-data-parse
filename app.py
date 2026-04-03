import streamlit as st
import os
import json
import time
from google import genai
from dotenv import load_dotenv

# Configuración de la página (Título en la pestaña del navegador)
st.set_page_config(page_title="Health-Tech AI Analyzer", page_icon="🧬")

# 1. Setup
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
CACHE_FILE = "lab_data_cache.json"

# --- TÍTULO Y DISEÑO ---
st.title("🧬 AI Metabolic & Aesthetic Analyzer")
st.markdown("---")

# 2. BARRA LATERAL (ENTRADA DE DATOS)
with st.sidebar:
    st.header("👤 Patient Profile")
    name = st.text_input("Name", value="Emanuel")
    age = st.number_input("Age", min_value=1, max_value=100, value=28)
    weight = st.number_input("Weight (kg)", value=77.0)
    height = st.number_input("Height (m)", value=1.70)
    fat_pct = st.slider("Body Fat %", 5, 40, 18)
    gym = st.selectbox("Gym Frequency", ["1-2x", "3-4x", "5x+ per week"], index=2)
    goal = st.text_area("Goal", value="Aesthetic improvement & Metabolic Health")
    
    st.markdown("---")
    # Botón para limpiar cache si quieres procesar otro PDF
    if st.button("Reset Lab Data (Clear Cache)"):
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
            st.success("Cache cleared!")

# 3. LÓGICA DE DATOS (REUTILIZAMOS TU FUNCIÓN)
def get_lab_data():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return f.read()
    return None # Si no hay cache, hay que subir el PDF

# 4. PANTALLA PRINCIPAL
lab_text = get_lab_data()

if lab_text is None:
    st.warning("⚠️ No lab data found. Please upload your blood test PDF.")
    uploaded_pdf = st.file_uploader("Upload Blood Test (PDF)", type="pdf")
    
    if uploaded_pdf:
        with st.spinner("Analyzing PDF (This takes ~4 minutes)..."):
            # Guardamos el archivo temporalmente para que la API lo lea
            with open("temp_blood_test.pdf", "wb") as f:
                f.write(uploaded_pdf.getbuffer())
            
            # Proceso de subida a Google
            file_upload = client.files.upload(file="temp_blood_test.pdf")
            time.sleep(10)
            
            extraction_prompt = "Extract all biochemical markers from this PDF clearly."
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=[file_upload, extraction_prompt]
            )
            
            # Guardamos en Cache
            with open(CACHE_FILE, "w") as f:
                f.write(response.text)
            
            st.success("Data extracted successfully! Refreshing...")
            st.rerun()

else:
    st.success("✅ Lab data loaded from memory.")
    
    # BOTÓN PARA GENERAR REPORTE
    if st.button("🚀 Generate Final Report"):
        with st.spinner("AI is thinking..."):
            master_prompt = f"""
            Role: Specialist in Clinical Nutrition & Endocrinology.
            Patient: {name}, {age} years, {weight}kg, {fat_pct}% fat, Gym: {gym}.
            Goal: {goal}
            
            LAB DATA:
            {lab_text}
            
            Provide a professional analysis on TSH, Lipid Profile, and Creatinine.
            Include 3 aesthetic strategies and a Risk Table.
            """
            
            final_response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=[master_prompt]
            )
            
            st.markdown("---")
            st.subheader("📋 Professional Analysis")
            st.write(final_response.text)