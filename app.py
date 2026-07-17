import streamlit as st
from google import genai
from PIL import Image

# --- System Configuration ---
st.set_page_config(page_title="LB Code Enforcer", layout="centered", page_icon="⚖️")

# Retrieve API key securely from Streamlit secrets
API_KEY = st.secrets.get("GEMINI_API_KEY") 

if API_KEY:
    # Initialize the modern, unified Gen AI Client
    client = genai.Client(api_key=API_KEY)
else:
    st.error("System Alert: GEMINI_API_KEY not found in environment variables/secrets.")
    st.stop()

def analyze_violation(image):
    system_prompt = """
    You are an expert, hyper-objective municipal code enforcement auditor for the City of Long Beach, CA.
    Analyze the provided image for any and all structural, spatial, or logistical violations of Long Beach Municipal Code (LBMC) Chapter 5.73 and Mobile Food Facility (MFF) regulations.
    
    Execute a comprehensive scan against the following strict legal matrix:
    
    1. SPATIAL & GEOMETRIC SETBACKS:
       - Sidewalk Path: Less than 4 feet of clear continuous path (5 feet in high-volume areas).
       - Curb Edge: Setups within 18 inches of the curb.
       - 5-Foot Rule: Within 5 feet of bus/Metro stops or above-ground utility structures.
       - 10-Foot Rule: Within 10 feet of driveways, alley approaches, crosswalks, ATMs, or building exits.
       - 15-Foot Rule: Within 15 feet of intersections, outdoor dining parklets, monuments, or public restrooms.
       - Proximity: Within 20 feet of another stationary vendor or a single-family home.
       - Macro Zones: Within 100 feet of a Fire/Police station or Hospital; or within 500 feet of a freeway ramp.
    
    2. ZONING & TEMPORAL RESTRICTIONS:
       - Stationary setups operating in an exclusively residential zone (only moving/roaming vendors allowed).
       - Operations within 1 block of a school on school days between 7:00 a.m. and 5:00 p.m.
    
    3. LOGISTICAL & HARDWARE COMPLIANCE:
       - Customer seating provided (tables/chairs placed on the sidewalk for customer use).
       - Footprint exceeding 100 sq ft or canopies exceeding 10x10 feet.
       - Use of unpermitted amplified sound, speakers, or flashing signs facing a highway.
       - Trash accumulation or failure to clear a 10-foot radius of debris.
    
    4. HEALTH & SANITATION (VISUAL INFRACTIONS):
       - Lack of a built-in handwashing sink (or a standard picnic cooler used instead of mechanical refrigeration for perishables).
       - Leaving equipment, food, or carts completely unattended on public property.
    
    OUTPUT REQUIREMENT:
    Identify the single most legally airtight, visually provable infraction. 
    Generate exactly ONE highly specific submission blurb optimized for the Go Long Beach 311 app.
    
    CONSTRAINT: Strictly 250 characters or less. Zero fluff. Start directly with the violation facts.
    """
    
    try:
        # Utilizing the modern, fast vision-capable model
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=[system_prompt, image]
        )
        return response.text.strip()
    except Exception as e:
        return f"API Pipeline Error: {str(e)}"

# --- Interface Layout ---
st.title("Street Vendor - LBMC 5.73 Violation Analyzer")
st.markdown("Automated computer vision intake for Go Long Beach app submissions.")

# Drag and drop component
uploaded_file = st.file_uploader("Upload or Drag & Drop physical evidence (JPG/PNG)", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # Display the evidence
    image = Image.open(uploaded_file)
    st.image(image, caption="Visual Evidence Secured", use_column_width=True)
    
    # Execution trigger
    if st.button("Generate Enforcement Statement"):
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
