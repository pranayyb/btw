import streamlit as st
from groq import Groq
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize session state for user_prompt
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""

def generate_prompts(user_prompt):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a highly creative AI specialized in generating concise but elaborative text-to-image prompts. Just provide direct answers."},
            {"role": "user", "content": user_prompt},
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_completion_tokens=512,
        top_p=1,
        stop=None,
        stream=False,
    )
    
    text_to_image_prompt = chat_completion.choices[0].message.content.strip()
    
    # Create JSON output with different seeds
    json_output = {}
    for i in range(4):
        json_output[str(i)] = {
            "seed": i,
            "text_to_image_prompt": text_to_image_prompt,
            "image_to_video_prompt": f"A cinematic sequence showing {text_to_image_prompt.lower()} with smooth, dynamic camera movements."
        }
    
    return text_to_image_prompt, json_output

# Streamlit UI
st.title("Dream to AI Prompt Generator")

st.session_state.user_prompt = st.text_area("Enter a dream description:", value=st.session_state.user_prompt)

if st.button("Generate Prompt"):
    if st.session_state.user_prompt:
        text_prompt, json_result = generate_prompts(st.session_state.user_prompt)
        
        st.subheader("Generated Text-to-Image Prompt:")
        st.write(text_prompt)
        
        st.subheader("Generated JSON Output:")
        st.json(json_result)
    else:
        st.warning("Please enter a dream description.")
