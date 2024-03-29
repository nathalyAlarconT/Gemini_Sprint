import streamlit as st
import google.generativeai as genai

st.set_page_config(layout="wide")

# Set up the model general parameters
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

def inputs():
    st.sidebar.header("Corporate Asistant")

    google_key = st.sidebar.text_input("Google_api_key", value="", type="password")
    
    st.sidebar.subheader("Translator")

    text = st.sidebar.text_area("Input")
    
    button = st.sidebar.button("Translate to Corporate")
    
    st.sidebar.subheader("Meeting Notes")

    text_sum = st.sidebar.text_area("Notes Input")
    
    button2 = st.sidebar.button("Summarize")

    return google_key, text, button, text_sum, button2

def translator(text, key):
    
    genai.configure(api_key = key)
    
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    prompt_parts = [
        f"""You are a corporate assistant, and your objective is to review the input text and translate it into three different professional tones: a CORPORATE ELEGANT, a more CONCISE, and A FRIENDLY tone.\n
         text: you are kidding me! this is none sense your solution is not possible. 
         **Corporate Tone:**\n\n\"I am concerned that the proposed solution may not be feasible. I suggest we explore alternative options.\"\n\n
         **Concise Tone:**\n\n\"Solution infeasible. Explore alternatives.\"\n\n
         **Friendly Tone:**\n\n\"Thank you for your suggestion. I have reviewed the proposed solution and while it has merit, I am concerned about its feasibility. Let's collaborate to explore other options that may be more appropriate for our current situation.\"\n\ntext: {text}""",
    ]

    response = model.generate_content(prompt_parts)
    
    splitted_res = response.text.replace("**", "")
    corporate_content = splitted_res.split(":")[1].replace("\n\n", "").replace("Concise Tone", "").replace('"', "")
    consice_content = splitted_res.split(":")[2].replace("\n\n", "").replace("Friendly Tone", "").replace('"', "")
    friendly_content = splitted_res.split("Tone:")[3].replace("\n\n", "").replace('"', "")
    
    return corporate_content, consice_content, friendly_content

def meeting_notes(text, key):
    
    genai.configure(api_key = key)
    
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    prompt_parts = [
        f"you are a corporate assistant, your objective is to summarize input text and translate them to a corporate tone, . text: {text}",
        ]

    response = model.generate_content(prompt_parts)
    
    summary = response.text.replace("**", "")
    
    return summary

def main():
    # We call the sidebar
    google_key, text, button, text_sum, button2 = inputs()

    if button:

        st.title("Responses")

        corporate_content, consice_content, friendly_content = translator(text, google_key)
        
        st.subheader("Elegant Response :nerd_face:", divider='blue')
        with st.container(height=100):
            st.markdown(corporate_content, )

        st.subheader('Concise Response :face_with_monocle:', divider='green')
        with st.container(height=100):
            st.markdown(consice_content)

        st.subheader('Friendly Response :information_desk_person:', divider='violet')
        with st.container(height=100):
            st.markdown(friendly_content)

    elif button2:

        st.title("Meeting Notes")

        st.text(meeting_notes(text_sum, google_key))

if __name__ == "__main__":
    main()
