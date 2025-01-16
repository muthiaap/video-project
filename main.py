import streamlit as st
from get_data import GetData
from text_generated import TextGenerated
from video_generated import VideoEditor

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
text_fontsize = st.sidebar.slider("Font Size", min_value=20, max_value=100, value=50)
text_color = st.sidebar.color_picker("Text Color", value="#FFFFFF")
text_duration = st.sidebar.slider("Text Duration (seconds)", min_value=1, max_value=30, value=10)

if st.sidebar.button("Generate Video"):
    if not (uploaded_file and api_key and cif_input and video_path):
        st.error("Please provide all required inputs!")
    else:
        try:
            # Step 1: Process Excel Data
            st.write("Processing Excel data...")
            data_processor = GetData(uploaded_file)
            subheader_values = data_processor.get_data(cif=cif_input)  # Convert CIF to string if needed
            if not subheader_values:
                st.error("No matching data found for the given CIF.")
                st.stop()

            st.write(f"Found {len(subheader_values)} transaction patterns.")

            # Step 2: Generate Text with Groq
            st.write("Generating text with Groq...")
            text_generator = TextGenerated(api_key)
            generated_text = text_generator.get_response(user_input=data_processor)
            st.write("Generated Text:", generated_text)

            # Step 3: Create Video with Text
            st.write("Creating video with overlay text...")
            video_editor = VideoEditor(imagemagick_path="/opt/homebrew/bin/convert")
            output_path = f"output_video_{cif_input}.mp4"  # Use CIF to name the output file
            video_editor.add_text_to_video(
                video_path=video_path,
                output_path=output_path,
                text=generated_text,
                fontsize=text_fontsize,
                text_color=text_color,
                position="center",
                duration=text_duration,
            )

            st.success(f"Video generated successfully! Saved as {output_path}")
            st.video(output_path)  # Optionally display the video in the Streamlit app
        except Exception as e:
            st.error(f"An error occurred: {e}")
