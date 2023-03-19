from django.shortcuts import render, redirect
# import HttpResponse from django.urls
from django.http import HttpResponse

# ref - https://www.thepythoncode.com/article/web-assistant-django-with-gpt3-api-python

import openai
# import the generated API key from the secret_key file
from .key import CHATGPT_API_KEY

openai.api_key = CHATGPT_API_KEY

limit_phrase = " Make sure your answer is relevant to us federal employment"


def home(request):

    try:
        if request.method == "POST":
            message = request.POST["prompt"]
            response = generate_response(message + limit_phrase)

            context = {
                'formatted_response': response,
                'prompt': message
            }
        
            return render(request, 'webassistant/home.html', context)
    
        else:

            return render(request, 'webassistant/home.html')
    except:

        # this will redirect to the 404 page after any error is caught
        return redirect('error-handler')
    

def generate_response(prompt):
    # Set up the OpenAI GPT-3 engine
    engine = "text-davinci-002"

    # Generate a response using the OpenAI API
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Return the generated response
    return response.choices[0].text.strip()

# this is the view for handling errors
def error_handler(request):
    return render(request, 'webassistant/error.html')
