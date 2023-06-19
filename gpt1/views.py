

# Create your views here.
from django.shortcuts import render, redirect
# from .icici_chat2 import inputdata
from .bot_with_conv import inputdata
from .chart import chart1
from openai.error import APIError, APIConnectionError, RateLimitError
# from .icici_chat3 import RetrievalAssistant , Message
# from django.contrib.sessions.backends.db import SessionStore
import json
# conversastion = RetrievalAssistant()
# def index(request):
#     chat = '' # Define response with a default value
#     if request.method == 'POST':
#             message = request.POST['chat']
#             responce = inputdata(message)
#             chat = [{'text': message, 'responce': responce}]
#             print(chat)
#             # do something with the message, e.g. save it to a database
#             # return redirect('home')
#         # else:
#         #     messages = []
#             # get any existing messages from the database or other source
#     return render(request, 'home.html', {'chat': chat})
# def new_chat(request):
    
#     # response = render(request, 'home1.html')
#     response = render(request, 'home3.html')
#     response.delete_cookie('chat')
#     return response

    # return render(request, 'home1.html', {'chat': chat})

    # response = render(request, 'home1.html', {'chat': chat})
    # return response

import re
# def index(request):
#     # Retrieve the chat messages from the cookie or create an empty list
#     chat = request.COOKIES.get('chat', [])
#     if isinstance(chat, str):
#         chat = json.loads(chat)
#     elif not isinstance(chat, list):
#         chat = []
    
#     if request.method == 'POST':
#         if 'chat' in request.POST:
#             message = request.POST['chat']
#             regex = r"(graph)|(chart)|(bar)"
#             match = re.search(regex, message.lower())
#             print(match)
#             if match:
#                 # print("bkbvbvb")
#                 try:
#                     chart = chart1(message)
#                     graph = chart[1].replace("\\","/")
                    
#                     chat.append({'text': message, 'response': chart[0] , "image":graph})
#                     response = render(request, 'home3.html', {'chat': chat})
#                     response.set_cookie('chat', json.dumps(chat))
#                 # response.localStorage.setItem('chat',json.dumps(chat))
#                     return response
#                 except Exception as e:
#                 # Handle other exceptions
#                     error_message = f"An error occurred: {e}"
#                     return render(request, 'error.html', {'error_message': error_message})

                    
#             # messages = []
#             # user_message = Message('user',message)
#             # messages.append(user_message.message())
#             # response2 = conversastion.ask_assistant(message)
#             else:
#                 try:
#                     response_chat = inputdata(message)
                    
                    
#                     print("Response:  ",response_chat)
#                     pattern = r"https?://[^\s]+\.png|https?://[^\s]+\.jpg|https?://[^\s]+\.jpeg" # Regex pattern to match the image URL
#                     # match = re.search(pattern, response) # Search for the URL in the response string
#                     # pattern = r"https?://[^\s]+\.(?:png|jpg)(?![^\s,])"
#                     # pattern1 = r"https?://[^\s]+(?:\.png|\.jpg|\.jpeg)(?![\w?&.])"
#                     pattern2 = r"(https?://[^\s]+\.(?:png)(\?[\w=&.%-]*)?)"
#                     matches = re.findall(pattern, response_chat) # Find all the URLs in the response string
#                     image_urls = [match for match in matches]
#                     print(image_urls)
                    
#                     response1 = re.sub(pattern2, "", response_chat)
#                     # print(response1)
#                     chat.append({'text': message, 'response': response1,"image_url":image_urls})
#                     # Store the updated chat messages in the cookie
#                     # response1.set_cookie('chat', json.dumps(chat))
#                     # response = render(request, 'home1.html', {'chat': chat})
#                     response = render(request, 'home3.html', {'chat': chat})
#                     response.set_cookie('chat', json.dumps(chat))
#                     # response.localStorage.setItem('chat',json.dumps(chat))
#                     return response
                
#                 except APIError as e:
#                 # Pass the API error message to the template
#                     error_message = f"OpenAI API returned an API Error: {e}"
#                     return render(request, 'error.html', {'error_message': error_message})

#                 except APIConnectionError as e:
#                 # Pass the connection error message to the template
#                     error_message = f"Failed to connect to OpenAI API: {e}"
#                     return render(request, 'error.html', {'error_message': error_message})

#                 except RateLimitError as e:
#                 # Pass the rate limit error message to the template
#                     error_message = f"OpenAI API request exceeded rate limit: {e}"
#                     return render(request, 'error.html', {'error_message': error_message})
#                 except Exception as e:
#                     # Handle other exceptions
#                     error_message = f"An error occurred: {e}"
#                     return render(request, 'error.html', {'error_message': error_message})

#         # elif 'clear' in request.POST:
#         #     # Clear the chat cookie
#         #     chat = []
#         #     response = render(request, 'home1.html')
#         #     response.delete_cookie('chat')
#         #     return response

#     # return render(request, 'home1.html', {'chat': chat})
#     return render(request, 'home3.html', {'chat': chat})
conversation = []
def new_chat(request):
    conversation.clear() 
    # response = render(request, 'home1.html')
    response = render(request, 'home3.html')
    response.delete_cookie('chat')
    return response

def index(request):
    # Retrieve the chat messages from the cookie or create an empty list
    chat = request.COOKIES.get('chat', [])
    if isinstance(chat, str):
        chat = json.loads(chat)
    elif not isinstance(chat, list):
        chat = []
    
    # print("CONVERSATION" , conversation)
    if request.method == 'POST':
        if 'chat' in request.POST:
            message = request.POST['chat']
            print("MEssage" , message)
            regex = r"(graph)|(chart)|(bar)"
            match = re.search(regex, message.lower())
            print(match)
            if match:
                # print("bkbvbvb")
                try:
                    chart = chart1(message)
                    graph = chart[1].replace("\\","/")
                    
                    chat.append({'text': message, 'response': chart[0] , "image":graph})
                    response = render(request, 'home3.html', {'chat': chat})
                    response.set_cookie('chat', json.dumps(chat))
                # response.localStorage.setItem('chat',json.dumps(chat))
                    return response
                except Exception as e:
                # Handle other exceptions
                    error_message = f"An error occurred: {e}"
                    return render(request, 'error.html', {'error_message': error_message})

                    
            # messages = []
            # user_message = Message('user',message)
            # messages.append(user_message.message())
            # response2 = conversastion.ask_assistant(message)
            else:
                try:
                    # response_chat = inputdata(message)
                    
                    response_chat = inputdata(message,conversation)
                    print("Response:  ",response_chat)
                    pattern = r"https?://[^\s]+\.png|https?://[^\s]+\.jpg|https?://[^\s]+\.jpeg" # Regex pattern to match the image URL
                    # match = re.search(pattern, response) # Search for the URL in the response string
                    # pattern = r"https?://[^\s]+\.(?:png|jpg)(?![^\s,])"
                    # pattern1 = r"https?://[^\s]+(?:\.png|\.jpg|\.jpeg)(?![\w?&.])"
                    pattern2 = r"(https?://[^\s]+\.(?:png)(\?[\w=&.%-]*)?)"
                    matches = re.findall(pattern, response_chat) # Find all the URLs in the response string
                    image_urls = [match for match in matches]
                    print(image_urls)
                    
                    response1 = re.sub(pattern2, "", response_chat)
                    # print(response1)
                    chat.append({'text': message, 'response': response1,"image_url":image_urls})
                    # Store the updated chat messages in the cookie
                    response = render(request, 'home3.html', {'chat': chat})
                    response.set_cookie('chat', json.dumps(chat))
                    return response
                
                except APIError as e:
                # Pass the API error message to the template
                    error_message = f"OpenAI API returned an API Error: {e}"
                    return render(request, 'error.html', {'error_message': error_message})

                except APIConnectionError as e:
                # Pass the connection error message to the template
                    error_message = f"Failed to connect to OpenAI API: {e}"
                    return render(request, 'error.html', {'error_message': error_message})

                except RateLimitError as e:
                # Pass the rate limit error message to the template
                    error_message = f"OpenAI API request exceeded rate limit: {e}"
                    return render(request, 'error.html', {'error_message': error_message})
                except Exception as e:
                    # Handle other exceptions
                    error_message = f"An error occurred: {e}"
                    return render(request, 'error.html', {'error_message': error_message})
                
    return render(request, 'home3.html', {'chat': chat})







