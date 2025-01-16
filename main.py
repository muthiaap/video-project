import streamlit as st
from get_data import GetData
from text_generated import TextGenerated
from video_generated import VideoTextOverlay

def hex_to_bgr(hex_color):
    """
    Convert a hex color code (e.g., #FFFFFF) to a BGR tuple for OpenCV.
    :param hex_color: Hex color code as a string.
    :return: Tuple (B, G, R)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (4, 2, 0))  # Convert RGB to BGR

# Set up Streamlit UI
st.title("Personalized Video Creator")
st.sidebar.title("Configuration")

# Upload Excel File
st.sidebar.subheader("Step 1: Upload Excel File")
uploaded_file = st.sidebar.file_uploader("Upload your Excel file", type=["xlsx"])
api_key = st.sidebar.text_input("Groq API Key", type="password")

# Step 2: CIF Input as a Number
st.sidebar.subheader("Step 2: Enter CIF")
cif_input = st.sidebar.number_input(
    "Enter CIF", min_value=1, step=1, format="%d", help="CIF must be a positive integer"
)

# Step 3: Video Settings
st.sidebar.subheader("Step 3: Video Settings")
video_path = st.sidebar.text_input("Path to Video Template")
font_scale = st.sidebar.slider("Font Scale", min_value=0.5, max_value=3.0, value=1.0, step=0.1)
text_color_hex = st.sidebar.color_picker("Text Color", value="#FFFFFF")
font_thickness = st.sidebar.slider("Font Thickness", min_value=1, max_value=5, value=2)
shadow_color_hex = st.sidebar.color_picker("Shadow Color", value="#000000")
shadow_offset_x = st.sidebar.slider("Shadow Offset X", min_value=-10, max_value=10, value=2)
shadow_offset_y = st.sidebar.slider("Shadow Offset Y", min_value=-10, max_value=10, value=2)
text_duration = st.sidebar.slider("Text Duration (seconds)", min_value=1, max_value=30, value=10)

if st.sidebar.button("Generate Video"):
    if not (uploaded_file and api_key and cif_input and video_path):
        st.error("Please provide all required inputs!")
    else:
        try:
            # Convert hex colors to BGR
            text_color = hex_to_bgr(text_color_hex)
            shadow_color = hex_to_bgr(shadow_color_hex)

            # Step 1: Process Excel Data
            st.write("Processing Excel data...")
            data_processor = GetData(uploaded_file)
            subheader_values = data_processor.get_data(cif=cif_input)  # Convert CIF to string if needed
            if not subheader_values:
                st.error("No matching data found for the given CIF.")
                st.stop()

            st.write(f"Found {len(subheader_values)} transaction patterns.")
            # st.write(f"{subheader_values}")

            # Step 2: Generate Text with Groq
            st.write("Generating text with Groq...")
            text_generator = TextGenerated(api_key)
            generated_text = text_generator.get_response(user_input=data_processor)
            st.write("Generated Text:", generated_text)

            # Step 3: Create Video with Text
            st.write("Creating video with overlay text...")
            output_path = f"/Users/muthia_ap/Documents/RAG/video-project/output/output_video_{cif_input}.mp4"  # Use CIF to name the output file
            video_editor = VideoTextOverlay(
                video_path=video_path,
                output_path=output_path,
                font_scale=font_scale,
                text_color=text_color,
                font_thickness=font_thickness,
                shadow_color=shadow_color,
                shadow_offset=(shadow_offset_x, shadow_offset_y)
            )
            video_editor.add_text(
                text=generated_text,
                duration=text_duration,
            )

            st.success(f"Video generated successfully! Saved as {output_path}")
            st.video(output_path)
        except Exception as e:
            st.error(f"An error occurred: {e}")
