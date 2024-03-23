# Content Summarization Bot
# We can automate the collection of user prompts and assistant responses to build a Bot. The ContentSummarizationBot will take your long 
# paragraphs as input and give you a concise summary in about 50 words

import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
import panel as pn  # GUI

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))
 
    return pn.Column(*panels)

pn.extension()

panels = [] # collect display 

context = [ {'role':'system', 'content':"""
# You are Content Summarization Bot,
a tool that takes in a piece of text as input and generates a concise summary
using prompt engineering techniques. This tool could be beneficial for quickly 
extracting key information from lengthy documents, articles, or research papers. |
Make sure that you condense the paragraph in not more than 50 words |
Finally you ask if the user is satisfied with the answer, If the user says no,
then you can generate some other response with key details for the user
"""}]


inp = pn.widgets.TextInput(value="Hi", placeholder='Enter your long text here…')
button_conversation = pn.widgets.Button(name="Chat with your Bot here")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

dashboard