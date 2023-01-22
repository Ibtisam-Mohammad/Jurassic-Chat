# Importing the modules
import streamlit as st
import re, pickle
import numpy as np
import requests
import base64

API_KEY = '' # Enter your API key


with open('embedding_review.pkl','rb') as f:
    embedding_of_reviews=pickle.load(f)
with open('review_in_chunks.pkl','rb') as f:
    review_chunks=pickle.load(f)
##############################

 #Taken from "https://github.com/AI21Labs/ai21studio-devhub/blob/main/examples/embeddings/embeddings_examples.ipynb"
def create_embeddings(texts): 
    resp = requests.post(
        "https://api.ai21.com/studio/v1/experimental/embed",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"texts": texts})
    if resp.status_code != 200:
        raise Exception(f"Completion request failed with status {resp.status_code}")
    embeddings = [x['embedding'] for x in resp.json()['results']]
    return embeddings

#################------- Finding the Laptop using Jurassic-1 Grande Instruct -------###################

def find_laptop(text_prompt):
    response = requests.post("https://api.ai21.com/studio/v1/j1-grande/The_First_Advisor/complete",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "prompt": f'''If the laptop is not in the following context, reply "No Laptop in the question".\nContext: This laptop is from Asus, the ROG Strix GL502VM. It has Windows 10, a full HD 15.6 inch display for viewing streaming content in good quality and 8th Gen Intel Core I7 processor combined with 16 GB of RAM for fast browsing.\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: Asus ROG Strix GL502VM\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: What about Lenovo, the Ideapad 330. It has Windows 10, a full HD 15.6 inch display for viewing streaming content in good quality and 8th Gen Intel Core I7 processor combined with 8 GB of RAM for fast browsing.\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: Lenovo Ideapad 330\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: This laptop is just for office work, not for gaming or editing.\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: No Laptop in the question\n--\nIf the laptop is not in the context, reply "No Laptop in the question".\nContext:The MacBook Pro 16-inch has some pretty big shoes to fill, those of the 17-inch MacBook Pro which Apple discontinued back in 2012.\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: The MacBook Pro 16-inch\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: The laptop had been rumoured for a very long time, with many people looking forward to it being real.\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: No Laptop in the question\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: The Microsoft Surface Laptop is one clean rounded rectangle when the lid is shut. The aluminium cover looks like a clean slate with a tiny, tiled mirror (the Microsoft logo) in the middle.\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: Microsoft Surface\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: Help in purchasing a good laptop for gaming.\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: No Laptop in the question\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: Which laptop do you recommend for office work?\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: Asus No Laptop in the question\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: I'm looking for a lightweight laptop for travel. What do you recommend?\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: No Laptop in the question\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: The Dell XPS 13 is a great option for business professionals.\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: Dell XPS 13\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: I need a laptop for gaming and video editing. What should I get?\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: No Laptop in the question\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: The Lenovo ThinkPad T490 is a durable option for professionals.\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: Lenovo ThinkPad T490\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: I'm looking for a laptop with a long battery life. What should I get?\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: No Laptop in the question\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: The HP Spectre x360 is a great 2-in-1 option for versatile use.\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: HP Spectre x360\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: I need a laptop for graphic design work. What do you recommend?\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: No Laptop in the question\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: The Razer Blade Pro is a high-performance gaming laptop.\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: Razer Blade Pro\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: I need a laptop for running virtual machines. What should I get?\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: No Laptop in the question\n--\nIf the laptop is not in the following context, reply "No Laptop in the question".\nContext: The Asus ROG Zephyrus G15 is a powerful laptop for gaming and content creation.\nQuestion: Get the name of laptop from above context.\nGive only and only the laptop brand plus model and nothing else in the Answer: Asus ROG Zephyrus G15\n--\nIf the laptop is not in the context, reply "No Laptop in the question".\nContext: {text_prompt}\Give only and only the laptop brand plus model and nothing else in the Answer:''',
        "numResults": 1,
        "maxTokens": 10,
        "temperature": 0.12,
        "topKReturn": 0,
        "topP":1.0,
        "countPenalty": {
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        "frequencyPenalty": {
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        "presencePenalty": {
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
      },
      "stopSequences":["--"]
    }
)
    laptop_name=response.json()['completions'][0]['data']['text']
    if (len(laptop_name)>6) and ('Laptop'.lower() not in laptop_name.lower()):   # The model sometimes outputs the laptops it knows or are in the previous answers so setting some limit
        print('-------'+laptop_name)
        return question_context(text_prompt) 
    else:
        print('no_laptop_in_the_chat',laptop_name)
        return 'no_laptop_in_the_chat'

#################-------  -------###################

def question_context(USER_QUESTION):
    question = np.squeeze(create_embeddings([f"{USER_QUESTION}"]))
    dot_list=[]
    for m,i in enumerate(embedding_of_reviews):
        for n,j in enumerate(i):
            dot=np.dot(j, question)
            dot_list.append([m,n,dot])
    review_arg=dot_list[np.argmax(np.array(dot_list)[:,2])]
    review_context=review_arg[0]
    review_para=review_arg[1]
    review_arg=dot_list[np.argmax(np.array(dot_list)[:,2])]
    main_context=review_chunks[review_context][review_para]
    return main_context
#################------- Setting Background Image (Help from Streamlit forum + Stackoverflow) -------###################

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    opacity:1.0;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)



#################------- Demo code -------###################
# For getting the review embeddings
# full_review_emb=[]
# full_review_txt=[]
# for i in np.arange(0,206):
#     len_txt=0
#     txt_list=[] 
#     done=False
#     while done==False:
#         if len(txt_list)==0:
#             txt=('.').join(df.iloc[i]['completion'][len_txt:len_txt+2000].split('.')[:-1])
#         else:
#             txt=('.').join(df.iloc[i]['completion'][len_txt:len_txt+2000].split('.')[1:-1])
#         len_txt+=len(txt)
#         if len(txt)<=0:
#             break
#         txt_list.append(txt)
#     print(len_txt,len(txt),len(txt_list))
#     full_review_emb.append(create_embeddings(txt_list))
#     full_review_txt.append(txt_list)
    # time.sleep(1)



#------|||||||||||||||||||||| END ||||||||||||||||||||||--------#
