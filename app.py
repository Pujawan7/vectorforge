import streamlit as st
from PIL import Image
import google.generativeai as genai

# ------------------------ PAGE CONFIG ------------------------
st.set_page_config(
    page_title="VectorForge AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------ CUSTOM CSS (Modern, Clean, Card) ------------------------
st.markdown("""
<style>
    /* Global */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e9edf4 100%);
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    /* Header */
    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 0 1rem 0;
        border-bottom: 2px solid rgba(79,125,243,0.15);
        margin-bottom: 2rem;
    }
    .logo {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e2a4a 0%, #4f7df3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    .logo span {
        background: linear-gradient(135deg, #4f7df3 0%, #9b59b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .badge {
        background: #4f7df3;
        color: white;
        padding: 0.3rem 1.2rem;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(79,125,243,0.3);
        letter-spacing: 0.3px;
    }
    /* Cards */
    .card {
        background: white;
        border-radius: 20px;
        padding: 1.8rem 1.8rem 1.5rem 1.8rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(0,0,0,0.03);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 50px rgba(0,0,0,0.08);
    }
    .card-title {
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        color: #0b1e33;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .card-title .icon {
        font-size: 1.4rem;
    }
    /* Upload area */
    .upload-area {
        border: 2px dashed #d1d9e6;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        background: #fafcff;
        color: #8896ab;
        font-size: 0.95rem;
    }
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #4f7df3 0%, #3b64d4 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: 0.3s;
        width: 100%;
        box-shadow: 0 4px 12px rgba(79,125,243,0.25);
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(79,125,243,0.4);
    }
    .stButton button:active {
        transform: scale(0.98);
    }
    /* Prompt output */
    .prompt-box {
        background: #f1f4fa;
        border-radius: 12px;
        padding: 1.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        white-space: pre-wrap;
        border-left: 5px solid #4f7df3;
        margin: 0.5rem 0 1rem 0;
        max-height: 450px;
        overflow-y: auto;
        line-height: 1.6;
    }
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.2rem;
        border-top: 1px solid #e9edf4;
        color: #8896ab;
        font-size: 0.8rem;
    }
    /* Password gate */
    .login-box {
        max-width: 420px;
        margin: 8rem auto;
        text-align: center;
    }
    .login-box h1 {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e2a4a 0%, #4f7df3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .login-box p {
        color: #66758a;
        margin-bottom: 2rem;
    }
    /* Style select */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 1px solid #e9edf4;
    }
    /* Make file uploader nicer */
    .stFileUploader > div > button {
        background: #f8fafc !important;
        border: 1px solid #e9edf4 !important;
        border-radius: 12px !important;
        color: #1e2a4a !important;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------ SESSION STATE ------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "generated_prompt" not in st.session_state:
    st.session_state.generated_prompt = ""

# ------------------------ PASSWORD GATE ------------------------
PASSWORD = "VFACCESS2026"   # Ganti dengan kode akses Anda

def login():
    st.markdown("""
    <div class="login-box">
        <h1>🎨 VectorForge AI</h1>
        <p>Professional Vector Prompt Studio</p>
    </div>
    """, unsafe_allow_html=True)
    with st.form("login_form"):
        code = st.text_input("🔑 Enter Access Code", type="password", placeholder="Your Payhip code")
        submitted = st.form_submit_button("Unlock Dashboard")
        if submitted:
            if code == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid access code. Please try again.")

if not st.session_state.authenticated:
    login()
    st.stop()

# ------------------------ GEMINI SETUP ------------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.6-flash')   # Sesuai permintaan

# ------------------------ MASTER SYSTEM INSTRUCTION (REVISED) ------------------------
SYSTEM_INSTRUCTION = """
You are VectorForge AI, a professional vector prompt assistant.

CRITICAL RULE: For every prompt, you MUST include a "VISUAL DIFFERENTIATOR" section that compares the selected style with the 2 closest styles on at least 4 aspects: Silhouette, Shape Language, Depth Method, Line Behavior, Color Logic, Detail Density, Visual Energy.

Use the exact construction blueprint for each style (see below). The style MUST change how the asset is constructed, not just wording.

PRODUCTION PROMPT ORDER (must follow strictly):
1. VISUAL DIFFERENTIATOR
2. REFERENCE & VISUAL EXTRACTION
3. SUBJECT + SUPPORTING ELEMENTS
4. PRESERVATION
5. SELECTED STYLE CONSTRUCTION
6. SHAPE / SILHOUETTE
7. COLOR SYSTEM
8. MATERIAL / DETAIL
9. ISOLATED STOCK FORMAT
10. TRACE-FRIENDLY OUTPUT
11. NEGATIVE / EXCLUSION

STYLE BLUEPRINTS (fingerprints):
01 Clean Flat Vector: smooth natural silhouettes; solid fills; 2–4 controlled tones; crisp boundaries; medium-low detail.
02 Minimal Vector: aggressive reduction to recognition-critical shapes; very few internal forms; large color areas; restrained palette.
03 Geometric Vector: rebuild organic structures with circles, arcs, polygons; aligned edges; measured proportions.
04 Premium Stock Vector: sophisticated layered commercial modeling; refined highlight/shadow planes; polished material cues.
05 Paper Cut Vector: stacked paper-like cut pieces; visible layer overlaps; crisp cut boundaries; shallow dimensional separation.
06 Isometric Vector: consistent isometric spatial system; top/front/side planes; parallel edges; controlled 3D-like depth.
07 Low Poly Vector: deliberate polygon facets; angular silhouette; faceted tonal blocks; limited multi-tone palette.
08 Monoline Vector: line-first construction; consistent contour weight; internal information expressed mainly through lines.
09 Bold Poster Vector: oversized graphic silhouettes; large color fields; high contrast; simplified internal detail.
10 Sticker Vector: compact die-cut silhouette; strong continuous outer contour; vivid controlled palette.
11 Cute Friendly Vector: rounded softened forms; slightly playful proportions; cheerful controlled palette.
12 Mascot Vector: characterful product illustration; bold readable silhouette; simplified expressive feature grouping.
13 Hand-Drawn Vector: clean vector shapes with organic contour variation; subtle asymmetry; restrained flat fills.
14 Editorial Vector: art-directed abstraction; elegant silhouette simplification; unusual but intentional shape relationships.
15 Retro Commercial Vector: vintage advertising construction; bold contour shapes; limited warm palette; print-era separations.
16 Mid-Century Modern Vector: 1950s–60s organic geometry; simplified asymmetrical forms; muted coordinated palette.
17 Luxury Line Vector: elegant sparse contour drawing; thin-to-medium controlled line hierarchy; refined negative space.
18 Organic Flat Vector: flowing natural silhouettes; soft irregular curves; layered organic flat shapes; calm natural palette.
19 Infographic Vector: modular visual grammar; clearly separated information zones; consistent alignment; repeated modules.
20 Technical Vector: engineered construction; measured proportions; component separation; precise contours; disciplined alignment.
21 Duotone Vector: reduce to two dominant color families plus optional neutral; strong tonal grouping; graphic contrast.
22 Collage Vector: assembled cutout pieces; intentional overlaps; varied scale; visible layer boundaries; mixed shape fragments.
23 Gradient Vector: crisp silhouettes with purposeful smooth gradients inside controlled shapes; modern dimensional color transitions.
24 Pop Graphic Vector: energetic contemporary shapes; punchy color contrasts; playful scale shifts; bold rhythm.
25 Engraved Vector: etched contour construction; parallel hatch lines; crosshatching-like tonal areas; line-density modeling.
26 Pixel Grid Vector: hard-edged grid logic; stepped silhouettes; block-based internal shapes; limited palette; pixel-scale rhythm.

ADDITIONAL RULES:
- Isolated stock format: pure white #FFFFFF background, 1:1 square, generous whitespace, full visibility.
- Derive colors from the actual reference image.
- Preserve the subject, supporting elements, proportions, and key colors.
- Do not invent features not present in the reference.
- The prompt must be copy-ready, with concrete instructions for the AI generator.
"""

# ------------------------ STYLE CATALOG ------------------------
STYLES_CATALOG = [
    "01 — Clean Flat Vector", "02 — Minimal Vector", "03 — Geometric Vector",
    "04 — Premium Stock Vector", "05 — Paper Cut Vector", "06 — Isometric Vector",
    "07 — Low Poly Vector", "08 — Monoline Vector", "09 — Bold Poster Vector",
    "10 — Sticker Vector", "11 — Cute Friendly Vector", "12 — Mascot Vector",
    "13 — Hand-Drawn Vector", "14 — Editorial Vector", "15 — Retro Commercial Vector",
    "16 — Mid-Century Modern Vector", "17 — Luxury Line Vector", "18 — Organic Flat Vector",
    "19 — Infographic Vector", "20 — Technical Vector", "21 — Duotone Vector",
    "22 — Collage Vector", "23 — Gradient Vector", "24 — Pop Graphic Vector",
    "25 — Engraved Vector", "26 — Pixel Grid Vector"
]

# ------------------------ MAIN UI ------------------------
# HEADER
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="header"><div class="logo">Vector<span>Forge</span> AI</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="badge">⚡ Prompt Studio</div>', unsafe_allow_html=True)

# TWO-COLUMN LAYOUT
left_col, right_col = st.columns([1, 1.2], gap="large")

# ========== LEFT COLUMN ==========
with left_col:
    # Card: Upload
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="icon">📤</span> Upload Image</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(" ", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Preview", use_container_width=True)
            st.session_state.uploaded_image = image
        else:
            st.markdown('<div class="upload-area">Drop your image here or click to browse</div>', unsafe_allow_html=True)
            st.session_state.uploaded_image = None
        st.markdown('</div>', unsafe_allow_html=True)

    # Card: Style selection
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="icon">🎯</span> Select Style</div>', unsafe_allow_html=True)
        selected_style = st.selectbox(" ", STYLES_CATALOG, index=0, label_visibility="collapsed")
        # Show short description
        style_desc = selected_style.split('—')[1].strip() if '—' in selected_style else selected_style
        st.caption(f"📖 {style_desc}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Card: Generate
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="icon">⚡</span> Generate</div>', unsafe_allow_html=True)
        generate_btn = st.button("Generate Production Prompt", use_container_width=True)
        if generate_btn:
            if st.session_state.uploaded_image is None:
                st.error("Please upload an image first.")
            else:
                with st.spinner("🧠 Analyzing image and crafting prompt..."):
                    user_prompt = f"""
                    Style selected by user: {selected_style}.
                    Generate a complete Production Prompt following the VectorForge Master Instruction and the blueprint for this style.
                    Include the mandatory VISUAL DIFFERENTIATOR.
                    """
                    try:
                        response = model.generate_content([SYSTEM_INSTRUCTION, st.session_state.uploaded_image, user_prompt])
                        st.session_state.generated_prompt = response.text
                        st.success("✅ Prompt generated successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# ========== RIGHT COLUMN ==========
with right_col:
    st.markdown('<div class="card" style="min-height: 450px;">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><span class="icon">📋</span> Generated Prompt</div>', unsafe_allow_html=True)

    if st.session_state.generated_prompt:
        prompt_text = st.session_state.generated_prompt
        # Display in a styled div
        st.markdown(f'<div class="prompt-box">{prompt_text}</div>', unsafe_allow_html=True)

        # Copy button using custom HTML + JavaScript
        # We need to escape the prompt text for JS string
        escaped_prompt = prompt_text.replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n')
        copy_html = f"""
        <div style="display: flex; justify-content: flex-end; margin-top: 0.5rem;">
            <button onclick="navigator.clipboard.writeText(`{escaped_prompt}`).then(() => alert('✅ Copied to clipboard!')).catch(() => alert('Copy failed.'))" 
                    style="background: #e9edf4; border: none; border-radius: 8px; padding: 0.4rem 1.5rem; font-size: 0.85rem; color: #1e2a4a; cursor: pointer; font-weight: 500;">
                📋 Copy to clipboard
            </button>
        </div>
        """
        st.components.v1.html(copy_html, height=60)

        # Additional instructions (outside prompt)
        st.markdown("---")
        st.markdown("""
        ### 🛠️ Next Steps
        1. 📷 Upload the **same reference image** to your chosen AI image generator (Midjourney, DALL‑E, Stable Diffusion, etc.).
        2. 📋 Copy the prompt above.
        3. 🤖 Paste it and generate your vector artwork.
        4. 🔄 Return here to refine, choose another style, or upload a new image.

        ### ℹ️ Important
        - VectorForge creates **structured prompts** for clean, professional vector-style artwork.
        - Results depend on the AI image generator.
        - This tool does **not** directly convert raster images to editable SVG/EPS/AI.
        - Use a separate tracing tool for editable vector output.
        """)
    else:
        st.info("Your generated prompt will appear here. Upload an image, choose a style, and click 'Generate'.")

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------ FOOTER ------------------------
st.markdown('<div class="footer">VectorForge AI © 2025 · Built with Streamlit · All vector styles v5 revised</div>', unsafe_allow_html=True)
