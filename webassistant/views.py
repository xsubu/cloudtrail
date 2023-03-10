from django.shortcuts import render, redirect
# import HttpResponse from django.urls
from django.http import HttpResponse

# ref - https://www.thepythoncode.com/article/web-assistant-django-with-gpt3-api-python

import openai
# import the generated API key from the secret_key file
from .key import CHATGPT_API_KEY

openai.api_key = CHATGPT_API_KEY

# this is the home view for handling home page logic
def home(request):
    # the try statement is for sending request to the API and getting back the response
    # formatting it and rendering it in the template
    try:
        # checking if the request method is POST
        if request.method == 'POST':
            # getting prompt data from the form
            prompt = request.POST.get('prompt')
            # making a request to the API 
            response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=1, max_tokens=1000)
            # formatting the response input
            formatted_response = response['choices'][0]['text']
            # bundling everything in the context
            context = {
                'formatted_response': formatted_response,
                'prompt': prompt
            }
            # this will render the results in the home.html template
            return render(request, 'webassistant/home.html', context)
        # this runs if the request method is GET
        else:
            # this will render when there is no request POST or after every POST request
            return render(request, 'webassistant/home.html')
    # the except statement will capture any error
    except:
        # this will redirect to the 404 page after any error is caught
        return redirect('error-handler')


# this is the view for handling errors
def error_handler(request):
    return render(request, 'webassistant/error.html')
