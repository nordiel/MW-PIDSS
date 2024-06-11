import gradio as gr
import os

from openai import OpenAI
from dotenv import load_dotenv, dotenv_values

# load enviornment variable from .env file
load_dotenv()

# define the API key imported from the .env file
client = OpenAI(api_key=os.getenv("API_KEY"))

# Initialize messages list with a system message
messages = [{"role": "system", "content": "You are a Phishing Identification and Decision support system that will give a phishing percentage as well as reasons as to why a given email may be a Phishing email. You should first propmpt the Phishing percentage and then continue explaining why you believe this email is a Phishing email. Be polite and offer insights."}]

# Define the function that performs Phishing Identification and Decision Support
def PIDSS_GPT(email):
    
    # Append the user's email in text format as a message in the messages list
    messages.append({"role": "user", "content": email})
    
    # Make API call to the OpenAI Chat Completion API
    response = client.chat.completions.create(model="gpt-3.5-turbo",  # Use the GPT-3.5 turbo model
    messages=messages)  # Send the list of messages to the API)

    # Get the response from the API and extract GPT's reply
    PIDSS_reply = response.choices[0].message.content
    
    # Append the GPT's reply to the messages list
    messages.append({"role": "assistant", "content": PIDSS_reply})
 
    # Return GPT's reply
    return PIDSS_reply

# Create the Gradio interface with custom styling
demo = gr.Interface(
    
    fn=PIDSS_GPT,  # Use the PIDSS_GPT function as the processing function
    inputs=gr.Textbox(lines=5, label="Copy email here"),  # Input textbox to receive the email
    outputs=gr.Textbox(label="Phishing Identification Results"),  # Output textbox to display results
    title="Phishing Identification and Decision Support System", # Set the title of the interface
    theme=gr.themes.Base(
    primary_hue="yellow",
    secondary_hue= "green",
    neutral_hue="gray",
    )
)
try:
# Set share=False to run the interface locally
    demo.launch(share=False) 
     
except Exception as e:
    # Handle any other exception
    print(f"An unexpected error occurred: {e}")
    
else:
    # This block executes if no exception occurs
    print("PIDSS loaded successfully.")