import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- System Configuration ---
st.set_page_config(page_title="LB Code Enforcer", layout="centered", page_icon="⚖️")

# Retrieve API key securely from Streamlit secrets
API_KEY = st.secrets.get("GEMINI_API_KEY") 

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("System Alert: GEMINI_API_KEY not found in environment variables/secrets.")
    st.stop()

def analyze_violation(image):
    # Utilizing the vision-capable model
    model = genai.GenerativeModel('gemini-1.5-pro') 
    
    system_prompt = """
    You are an objective municipal code compliance analyzer for Long Beach, CA.
    Analyze the provided image for street vending/mobile food facility (MFF) violations against LBMC 5.73.
    
    Scan specifically for:
    1. ADA right-of-way obstruction (less than 4ft continuous sidewalk clearance).
    2. Stationary cart setups operating in residential zones.
    3. Buffer zone encroachment (within 15ft of hydrants, 20ft of crosswalks).
    4. Sanitation deficits (lack of mandated handwashing sink, improper wastewater disposal).
    
    Output exactly ONE highly specific, objective submission blurb ready for the Go Long Beach 311 app.
    Constraint: Strictly under 250 characters. No conversational filler. No introductory text. Focus purely on actionable, visual code enforcement facts.
    """
    
    try:
        response = model.generate_content([system_prompt, image])
        return response.text.strip()
    except Exception as e:
        return f"API Pipeline Error: {str(e)}"

# --- Interface Layout ---
st.title("LBMC 5.73 Violation Analyzer")
st.markdown("Automated computer vision intake for Go Long Beach app submissions.")

# Drag and drop component
uploaded_file = st.file_uploader("Upload or Drag & Drop physical evidence (JPG/PNG)", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # Display the evidence
    image = Image.open(uploaded_file)
    st.image(image, caption="Visual Evidence Secured", use_column_width=True)
    
    # Execution trigger
    if st.button("Synthesize Enforcement Blurb"):
        with st.spinner("Cross-referencing LBMC 5.73 database..."):
            blurb = analyze_violation(image)
            
            st.divider()
            st.subheader("Optimized Go Long Beach Payload:")
            st.info(blurb)
            
            # Validation check
            char_count = len(blurb)
            if char_count <= 250:
                st.success(f"Constraint met: {char_count}/250 characters. Ready for copy-paste.")
            else:
                st.warning(f"Constraint failed: {char_count}/250 characters. Manual truncation required.")
