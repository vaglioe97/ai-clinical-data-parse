import os
import json
import time
from google import genai
from dotenv import load_dotenv


load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

CACHE_FILE = "lab_data_cache.json"
PDF_FILE = "blood_test.pdf"

patient_data = {
    "name": "Emanuel",
    "age": 28,
    "gender": "male",
    "is_athlete": True,
    "weight_kg": 77,
    "height_m": 1.70,
    "fat_percent": 18,
    "gym_frequency": "5x per week",
    "goal": "Aesthetic improvement (Body Recomposition) & Metabolic Health",
    "key_concerns": ["High LDL", "Elevated TSH", "Lipid Management"]
}

def get_lab_data_structured():
    """
    Reads the PDF only once and saves it as a JSON 'Cache'.
    """
    if os.path.exists(CACHE_FILE):
        print("--- Loading lab data from CACHE (Instant) ---")
        with open(CACHE_FILE, "r") as f:
            return f.read() # Retorna el texto del examen guardado
    print("--- CACHE NOT FOUND. Analyzing PDF... ---")
    uploaded_file = client.files.upload(file=PDF_FILE) # <--- AQUÍ SUBE EL PDF
    time.sleep(10)

    extraction_prompt = "Extract all biochemical markers from this PDF and list them clearly with values and units."
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[uploaded_file, extraction_prompt]
    )
    
    # Guardamos el resultado de la lectura en el archivo JSON/Texto
    with open(CACHE_FILE, "w") as f:
        f.write(response.text)
    
    return response.text

lab_text = get_lab_data_structured()

# 3. Final Master Prompt
master_prompt = f"""
Role: Specialist in Clinical Nutrition, Endocrinology, and Sports Medicine.
Goal: Body Recomposition and Metabolic Optimization.

Patient Data:
- Age: {patient_data['age']}
- Weight/Height: {patient_data['weight_kg']}kg / {patient_data['height_m']}m
- Body Fat: {patient_data['fat_percent']}% (Active Gym User 5x/week)
- Main Focus: Aesthetics (fat loss/muscle retention) and Lipid Control.

Task:
1. Analyze the attached PDF blood test results.
2. Focus on:
   - TSH (8.18): Explain how this level affects fat loss, water retention, and basal metabolism.
   - Lipid Profile: Address the LDL of 170+ vs the goal of body recomposition.
   - Kidney Health: Evaluate Creatinine (1.45) considering the 5x/week gym intensity.
3. Provide 3 Evidence-Based Strategies:
   - 1 for optimizing metabolism (considering the TSH).
   - 1 for lowering LDL through nutrition without sacrificing muscle protein synthesis.
   - 1 for aesthetic-focused supplementation/habits (e.g., fiber, omega-3, protein timing).
4. Create a "Risk vs Action" table.

Disclaimer: AI-generated. This is not medical advice. Consult an endocrinologist for TSH management.
"""

# 4. Execution
print("--- Generating Specialized Aesthetic Report... ---")
full_context = f"LAB RESULTS:\n{lab_text}\n\nINSTRUCTIONS:\n{master_prompt}"

final_response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[full_context] 
)

print("\n" + "="*40)
print("FINAL CLINICAL REPORT")
print("="*40)
print(final_response.text)