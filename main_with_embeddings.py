# Importing the modules
from amazon import amazon, find_laptop, set_background  
from amazon_embed import find_laptop, set_background   #Custom modules
from streamlit_chat import message
import streamlit as st
from PIL import Image
import requests
import base64
import pickle
import base64
import os
import re

API_KEY = ''  # Enter your API key

#################------SOME PAGE DESIGNING !--------###################

st.set_page_config(
     page_title="The Advisor", # name of page
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded" )


set_background('lap_4.png') # Setting the background of page

st.markdown(f'''                
        <style>
            .sidebar .sidebar-content {{
                width: 375px;
            }}
        </style>
    ''',unsafe_allow_html=True) # Setting the sidebar width

# Setting page title
st.markdown("<h1 style='font-family:Courier; color:Brown; font-size: 70px;text-align: center;'>THE ADVISOR</h1>",unsafe_allow_html=True)
if st.button('V_main'):
    #################------Initializing the session states--------###################
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []    # To record the response of the BOT
    if 'past' not in st.session_state:
        st.session_state['past'] = []          # To record the response of the USER

    ## To make our bot remember everyting a USER & BOT says by appending the responses at the end of "pre_prompt"
    if 'pre_prompt' not in st.session_state:   
        st.session_state['pre_prompt']=[''''A conversation where Digit_Tech who is a laptop reviewer, laptop advisor, tech enthusiast, honest, truthful person is helping and advising Linus in purchasing a laptop using the complete review of laptop knowledge. -- Digit_Tech: Hey Linus, how's it going? -- Linus: Not bad, Digit_Tech. How about you? -- Digit_Tech: Can't complain. Just reviewing some new laptops. -- Linus: Oh, you are doing a great job. By the way, I needed to purchase a new laptop. -- Digit_Tech: You have come to the right place. Just tell me about your usage. -- Linus: Ok, I just need it for casual browsing, streaming. Kindly suggest a good one in low budget. -- Digit_Tech: Well, Linus, this might sound surprising, but for casual browsing and streaming, almost anything will do. The main requirement should be a good processor and at least 4 GB of RAM. Also, the battery should last at least 6 hours. Also, make sure the laptop has a DVD drive. -- Linus: I don't know much about a laptop. Can you suggest the best one for me? -- Digit_Tech: Ok, let me see. First, which operating system are you using? -- Linus: I prefer Windows, I hate Mac interface -- Digit_Tech: Ok, that shouldn't be a problem. What about you budget? -- Linus: Well, not more than 35,000 rupees. -- Digit_Tech: That is great, I think I have a laptop in mind for you. -- Linus: Ok, tell me. -- Digit_Tech: Well, this laptop is from Lenovo, the Ideapad Slim 3. It has Windows 10, a full HD 14 inch display for viewing streaming content in good quality and 10th Gen Intel Core I5 processor combined with 8 GB of RAM for fast browsing. -- Linus: What about battery life? --  Digit_Tech: Well, it has 55W battery, which lasts 7 to 9 hours because of its low power consuming 15W TDP intel processor -- Linus: Ok, sounds good. What about price? -- Digit_Tech: It should be around 38990 rupees, but do check it online. -- Linus: Any drawbacks -- Digital_Tech: Yes, there are some small build quality and charging issues, also it is not a laptop I would recommend for video or photo editing -- Linus: Can you suggest another laptop for my friend. -- Digit_Tech: Yes, Tell me more about the requirements. -- ''']

    #################------Now we send the USER responses to the model--------###################

    # To ensure our "appending" of prompts is within approved length we use the if condition. Inside "Else" condition we summarize the "pre_prompt" to make it shorter.
    if (len(st.session_state['pre_prompt'][-1])//6)<2030:  
        def query(txt):                     # The query function takes a text input i.e the response of the user
            # Add the "pre_prompt" and the name of the bot "Digit_Tech" to the USER input in next 2 lines
            txt=f'Linus: {txt}. Digit_Tech:'   
            prompt=st.session_state['pre_prompt'][-1]+txt 
            # Get the response..........
            response=requests.post(
                    "https://api.ai21.com/studio/v1/j1-grande/The_First_Advisor/complete",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    json={
                        "prompt": prompt, 
                        "numResults": 1, 
                        "maxTokens": 100, 
                        "stopSequences": ["--"],
                        "topP": 0.98,
                        "temperature": 0.7 } )
            return response.json()['completions'][0]['data']['text']  # Format the response
            
    #################------Ask the USER for its response to the model--------###################
        def get_text():
            input_text = st.text_input(label='Tell me more about the requirements like the OS, Memory, Display etc:',key="input")
            return input_text
        user_input = get_text()
        check_box=st.checkbox('Check for Viewing Amazon.com results')
    #################------ Send the reponse to the model only if the USER responds ! --------###################
        if user_input:
            output = query(user_input)
            st.session_state.past.append(user_input)   # continue to add the USER response to the session state of USER
            st.session_state.generated.append(output)   # continue to add the BOT response to the session state of BOT
            st.session_state['pre_prompt'].append(st.session_state['pre_prompt'][-1]+f'Linus: {st.session_state.past[-1]}. Digit_Tech: {st.session_state.generated[-1]} -- ')  # continue to add the USER and BOT response to the "pre_prompt" session state to create a memory!

    #################------ Code to diplay the laptops the BOT recommends in the sidebar --------###################
    #################------ RAPIDAPI => FROM AMAZON => NEEDS API => IS EXTRA ! --------###################
            if check_box:
                response=find_laptop(st.session_state.generated[-1])  # find laptop name from the last message of the bot
                if response:
                    # Display the Laptop Image, Name, Price, URL from AMAZON US
                    for i in range(len(response)):
                        st.sidebar.image(response[i]['imageUrl'],use_column_width=True)      
                        st.sidebar.markdown(response[i]['title'], unsafe_allow_html=True) 
                        st.sidebar.markdown(response[i]['price'], unsafe_allow_html=True) 
                        st.sidebar.markdown(response[i]['detailPageURL'], unsafe_allow_html=True)
                
    #################------ Code that prints the messages --------###################
        if st.session_state['generated']:   # i.e if the BOT responds
            for i in range(len(st.session_state['generated'])-1, -1, -1):  # Print messages in reverse order of a list i.e newest to oldest
                message(st.session_state["generated"][i], key=str(i))      # Print BOT messages
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user') # Print USER messages

    #################------ The "if pre_prompt length exceeds token limit, then summarize" Else  --------###################
    else:
        summary=requests.post("https://api.ai21.com/studio/v1/experimental/summarize",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "text": f"st.session_state['pre_prompt']",   # Summarize the whole conversation between the BOT and USER till now 
            }
        )
        st.session_state['pre_prompt']=[summary.json()['summaries'][0]['text']+' -- ']  # And replace the pre_prompt session state with just the summary


    #------|||||||||||||||||||||| END ||||||||||||||||||||||--------#


 #################### EXPERIMENTAL CODE FOR INFORMATION RETRIEVAL USING EMBEDDING SEARCH + CHAT + CONTEXT + SUMMARIZATION ##########################
if st.button('V_experimental_embeddings'):
    #################------Initializing the session states--------###################
    pre_prompt=[''''A conversation where Digit_Tech who is a laptop reviewer, laptop advisor, tech enthusiast, honest, truthful person is helping and advising Linus in purchasing a laptop using the complete review of laptop knowledge. -- Digit_Tech: Hey Linus, how's it going? -- Linus: Not bad, Digit_Tech. How about you? -- Digit_Tech: Can't complain. Just reviewing some new laptops. -- Linus: Oh, you are doing a great job. By the way, I needed to purchase a new laptop. -- Digit_Tech: You have come to the right place. Just tell me about your usage. -- Linus: Ok, I just need it for casual browsing, streaming. Kindly suggest a good one in low budget. -- Digit_Tech: Well, Linus, this might sound surprising, but for casual browsing and streaming, almost anything will do. The main requirement should be a good processor and at least 4 GB of RAM. Also, the battery should last at least 6 hours. Also, make sure the laptop has a DVD drive. -- Linus: I don't know much about a laptop. Can you suggest the best one for me? -- Digit_Tech: Ok, let me see. First, which operating system are you using? -- Linus: I prefer Windows, I hate Mac interface -- Digit_Tech: Ok, that shouldn't be a problem. What about you budget? -- Linus: Well, not more than 35,000 rupees. -- Digit_Tech: That is great, I think I have a laptop in mind for you. -- Linus: Ok, tell me. -- Digit_Tech: Well, this laptop is from Lenovo, the Ideapad Slim 3. It has Windows 10, a full HD 14 inch display for viewing streaming content in good quality and 10th Gen Intel Core I5 processor combined with 8 GB of RAM for fast browsing. -- Linus: What about battery life? --  Digit_Tech: Well, it has 55W battery, which lasts 7 to 9 hours because of its low power consuming 15W TDP intel processor -- Linus: Ok, sounds good. What about price? -- Digit_Tech: It should be around 38990 rupees, but do check it online. -- Linus: Any drawbacks -- Digital_Tech: Yes, there are some small build quality and charging issues, also it is not a laptop I would recommend for video or photo editing -- Linus: Can you suggest another laptop for my friend. -- Digit_Tech: Yes, Tell me more about the requirements. -- ''']

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []    # To record the response of the BOT
    if 'past' not in st.session_state:
        st.session_state['past'] = []          # To record the response of the USER
    ## To make our bot remember everyting a USER & BOT says by appending the responses at the end of "pre_prompt"
    if 'pre_prompt' not in st.session_state:   
        st.session_state['pre_prompt']=pre_prompt


    ########### To create separate conversational prompts - to be appended in front of the "context" from the reviews" ###
    ########### as the model hallucinates if we just use the previous long prompt ################
    # if 'pre_prompt_context' not in st.session_state:   
    #     st.session_state['pre_prompt_context']=['''A conversation where Digit_Tech who is a laptop reviewer, laptop advisor, tech enthusiast, honest, truthful person is helping and advising Linus in purchasing a laptop using the complete review of laptop knowledge. -- ''']
    # st.write(st.session_state.pre_prompt)     # for debugging \_-()-_/




    #################------Now we send the USER responses to the model--------###################
    # To ensure our "appending" of prompts is within approved length we use the if condition. Inside "Else" condition we summarize the "pre_prompt" to make it shorter.
    if (len(st.session_state['pre_prompt'][-1])//6)<2030:  
        def query(txt):                     # The query function takes a text input i.e the response of the user
            # Add the "pre_prompt" and the name of the bot "Digit_Tech" to the USER input in next 2 lines
            txt=f'Linus: {txt}. Digit_Tech:'   
            prompt=st.session_state['pre_prompt'][-1]+txt 
            # Get the response..........
            response=requests.post(
                    "https://api.ai21.com/studio/v1/j1-jumbo/complete",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    json={
                        "prompt": prompt, 
                        "numResults": 1, 
                        "maxTokens": 100, 
                        "stopSequences": ["--"],
                        "topP": 0.98,
                        "temperature": 0.7 } )
            return response.json()['completions'][0]['data']['text']  # Format the response
            
    #################------Ask the USER for its response to the model--------###################
        def get_text():
            input_text = st.text_input(label='Tell me more about the requirements like the OS, Memory, Display etc:',key="input")
            return input_text
        user_input = get_text()
        # check_box=st.checkbox('Check for Viewing Amazon.com results')
    #################------ Send the reponse to the model only if the USER responds ! --------###################
        if user_input:
            st.session_state.past.append(user_input)   # continue to add the USER response to the session state of USER

    #----------------------------------------------------------------------------------------------------------#
    ############ Search within the user and bot messages to find a laptop name --> If name found in the messages --> Try getting the similarity between the embeddings of the reviews and the message --> best match is displayed in the sidebar --> and is also used as a context for next questions by the user -----> here unfortunately the model gets distracted, might be code error :/ ##########
            context_user=find_laptop(st.session_state.past[-1])
            if len(st.session_state.generated)>0:
                context_bot=find_laptop(st.session_state.generated[-1]) 
            else:
                context_bot='no_laptop_in_the_chat'

            if (context_user!='no_laptop_in_the_chat'):
                st.sidebar.write(context_user)
                output=query(f"{user_input} Answer the query from the following laptop review step by step:{context_user}")
                st.session_state['pre_prompt'].append(st.session_state['pre_prompt'][-1]+f'Linus: {user_input} Digit_Tech: {output} -- ')
                st.session_state.generated.append(output)   # continue to add the BOT response to the session state of BOT
                # st.session_state['pre_prompt']=pre_prompt

            elif (context_bot!='no_laptop_in_the_chat'):
                st.sidebar.write(context_bot)
                output=query(f"{user_input} Answer the query from following laptop review step by step:{context_bot}")
                st.session_state['pre_prompt'].append(st.session_state['pre_prompt'][-1]+f'Linus: {user_input} Digit_Tech: {output} -- ')
                st.session_state.generated.append(output)
                # st.session_state['pre_prompt']=pre_prompt

            else:
                output=query(user_input)
                st.session_state.generated.append(output)
                st.session_state['pre_prompt'].append(st.session_state['pre_prompt'][-1]+f'Linus: {st.session_state.past[-1]}. Digit_Tech: {st.session_state.generated[-1]} -- ')  # continue to add the USER and BOT response to the "pre_prompt" session state to create a memory!

    #################------ Code to find the laptops --------###################
            # if check_box:
            #      # find laptop name from previous message
            #     response_user=find_laptop(st.session_state.past[-1])
            #     response_bot=find_laptop(st.session_state.generated[-1]) 
            #     if (response_user!='no_laptop_in_the_chat'):
            #         context=response_user
            #     if (response_bot!='no_laptop_in_the_chat'):
            #         context=response_bot
                


                
    #################------ Code that prints the messages --------###################
        if st.session_state['generated']:   # i.e if the BOT responds
            for i in range(len(st.session_state['generated'])-1, -1, -1):  # Print messages in reverse order of a list i.e newest to oldest
                message(st.session_state["generated"][i], key=str(i))      # Print BOT messages
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user') # Print USER messages

    #################------ The "if pre_prompt length exceeds token limit, then summarize" Else  --------###################
    else:
        summary=requests.post("https://api.ai21.com/studio/v1/experimental/summarize",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "text": f"st.session_state['pre_prompt']",   # Summarize the whole conversation between the BOT and USER till now 
            }
        )
        st.session_state['pre_prompt']=[summary.json()['summaries'][0]['text']+' -- ']  # And replace the pre_prompt session state with just the summary


    #------|||||||||||||||||||||| END ||||||||||||||||||||||--------#


