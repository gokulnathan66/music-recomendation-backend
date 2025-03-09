#gemini_communication
from .gemini_model import model


def gemani_response(predefined_prompt,user_prompt):

    chat_session = model.start_chat(
    history=[
            {'role': 'user', 'parts': [predefined_prompt]},
            {'role': 'model', 'parts': ['OK I understand. I will do my best!']}
    ]
    )
    response = chat_session.send_message(user_prompt)

    return response.text


#testing the function area
# userinput = input("Enter your prompt: ")
# predefined_prompt="""you are a model to tell me a joke about any topic you like, don't answer with a joke that is inappropriate or offensive, don't answer any other questions,
# if asked simply respond with "I am a model to tell jokes" """

# gemani_response(predefined_prompt,userinput)
# # print(gemani_response(predefined_prompt,userinput))
