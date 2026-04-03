# AI-Assisted Clinical Data Parser

A specialized tool built with Python and Streamlit to automate the extraction of biochemical data from medical lab reports using Google's Gemini 3 Flash API.

## Features
- **Multimodal Analysis:** Processes PDF and Image lab reports.
- **Smart Parsing:** Uses Prompt Engineering to structure data into JSON.
- **Data Visualization:** Displays clinical results in an organized dashboard.

## Tech Stack
- **Language:** Python 3.10+
- **Framework:** Streamlit
- **AI Model:** Google Gemini (Generative AI)
- **Data Handling:** Pandas, JSON

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Add your `GOOGLE_API_KEY` to a `.env` file.
4. Run the app: `streamlit run app.py`.
