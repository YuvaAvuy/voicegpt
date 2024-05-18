import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3

# Set your API key directly (replace 'YOUR_API_KEY' with your actual API key)
api_key = "AIzaSyBuesdkuzLi9F-lhew1qIFnt7UX8z86M3A"

# Configure Generative AI with your API key
genai.configure(api_key=api_key)

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        st.write("Processing...")

        try:
            text = recognizer.recognize_google(audio)
            st.write(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    st.title("Yuva's LLM Application")
    st.write("Input: ")

    chat_history = []

    input_text = st.text_input("You:", key="text_input")
    st.write("Or use voice input:")

    if st.button("Voice Input", key="voice_input_button"):
        input_text = recognize_speech()

    if input_text:
        response = get_gemini_response(input_text)
        st.write("The Response is:")
        full_response = ""
        for chunk in response:
            try:
                if hasattr(chunk, 'text'):
                    st.write(chunk.text)
                    chat_history.append(("Bot", chunk.text))
                    full_response += chunk.text + " "
                else:
                    st.write("Response does not contain valid text.")
            except Exception as e:
                st.write(f"An error occurred: {e}")

        # Speak the response
        speak_text(full_response)

        chat_history.append(("You", input_text))

    st.write("The Chat History is:")
    for role, text in chat_history:
        st.write(f"{role}: {text}")

if __name__ == "__main__":
    main()
