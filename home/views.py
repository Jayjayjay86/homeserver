from django.shortcuts import render
from django.http import JsonResponse
from .models import TranslatedContent
import openai
from google.cloud import translate

api_key = "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"


def generate_chatbot_response(student_name, prompts):
    openai.api_key = api_key

    # Construct the prompt string with student's name and prompts
    prompt = f"Please write a lesson brief for Student Name: {student_name}\nPrompts:\n"
    for i, p in enumerate(prompts, start=1):
        prompt += f"{i}. {p}\n"

    response = openai.Completion.create(
        engine="davinci",  # Use the appropriate engine
        prompt=prompt,
        max_tokens=200,  # Limit the response to 200 tokens (words)
    )
    print(response)
    chatbot_response = response.choices[0].text.strip()
    print(chatbot_response)
    return chatbot_response


def home(request):
    context = {}
    return render(request, "home.html", context)
