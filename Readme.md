# 🦕 JURASSIC HACKATHON 🦕
## THE ADVISOR
This app tries to utilize the Jurassic model capabilites - The Advisor is a tool that is built to help users make informed decisions when purchasing a laptop at least for now). It should be able to aggregate and analyzes real-life reviews to provide a comprehensive understanding of the strengths and weaknesses of various laptop models. The user-friendly interface allows users to easily input their specific needs and preferences, such as battery life, storage capacity, and weight. 

## Features
* Aggregates and analyzes real-life reviews from multiple sources
* User doesn't need to check hundreds of reviews to arrive at a decision.
* User-friendly interface for inputting specific needs and preferences
* Helps users make more informed decisions by answering their questions about the laptops

## Usage
* Clone the repository to your local machine
``` git clone https://github.com/Ibtisam-Mohammad/Jurassic-Hackathon.git ```
* Install the dependencies: streamlit and streamlit-chat  :)
* Provide the API keys of the model (and RapidAPI for accessing Amazon for prices !)

## Working:
* There are 3 main features of the app:
  - First all the user input and the model output are fed back into the model next time a user asks a question to help the model answer questions based on previous interaction.
  - Secondly, the summarize API is called to summarize the prompts (as they get larger with each interaction) - not required generally, but in case !
  - Lastly about the interface, I have tried to embed the Amazon prices in it for ease of use, but it can be made better if done without streamlit (as the session loads casuse some problem) and using a better trained NER model.

## Further Work:
  - I think first the model needs to get the reults only from a particular database (reviews here) as it is hallucinating and mixing features of other laptops with the output ----- For that waiting for Jurassic-X or an embedding model able to handle longer texts (Jurassic-X would be better)
  - Better question/answer training data to teach the model to get the results only from the review database. I guess it could be done but with lot of examples, I may require Q/A for all the reviews !
  - Better way to "chat" with the model, maybe something reinforcement lear.............🙄
