from .models import user
from .serializers import RequestUserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from anthropic import Anthropic
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.checkpoint import MemorySaver
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_anthropic import AnthropicLLM
from django.views.decorators.cache import cache_page
import logging
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from langchain_google_genai import GoogleGenerativeAI
from pathlib import Path
from dotenv import load_dotenv
import json
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_vertexai.vision_models import VertexAIImageGeneratorChat
from PIL import Image
import io
import anthropic
# from some_anthropic_sdk import Client
import logging
import base64
import httpx
logger = logging.getLogger(__name__)
# from .form import RequestUserForm


# Load environment variables from .env file

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)


# Set up logging
logger = logging.getLogger(__name__)


client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)


@csrf_exempt
def google_gemani_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            promotedata = data.get('data')
            llm = GoogleGenerativeAI(
                model="gemini-1.5-flash", google_api_key=os.getenv('GEMINI_API_KEY'))
            # Handle the promotedata as needed
            system_message = SystemMessage(
                content=(
                    "You are a highly skilled assistant in HTML, CSS, and JavaScript coding. "
                    "You specialize in creating advanced animations using HTML, CSS, and JavaScript. "
                    "Your primary role is to explain chemistry. topics through engaging and informative animations. "
                    "Animations must be created first before any explanation of the topic. Without the animation, no topic should be explained. "
                    "Animations should be visually appealing, centered, and should help in understanding the concept effectively. "
                    "You should provide complete code for the animation in a single file. "
                    "Avoid using backticks inside code. "
                    "The background color of the animation should be white. "
                    "Text explanations should not be included inside the code. "
                    "Animations should be interactive, allowing users to control aspects like timing or visualization. "
                    "You should include real-life examples to make the chemistry concepts relatable. "
                    "Start by defining the topic, then provide an in-depth explanation of how it works, its functions, and applications only after the animation. "
                    "Discuss subtopics, their connections, and their functions in detail. "
                    "Critical thinking should be applied to provide a thorough and insightful explanation. "
                    "Make sure the animation clearly demonstrates the topic and facilitates a practical understanding. "
                    "No explanation should be given without the presence of an animation. "
                    "Engage with users in a friendly and human-like manner, ensuring that your responses are conversational and relatable. "
                    "If the user asks about previous learning, you should recall and summarize what has been learned before, providing a brief review or reference to earlier topics."
                )
            )
            messages = [
                system_message,
                HumanMessage(content=promotedata)
            ]
            response_data = llm.invoke(messages)
            print(response_data)

            return JsonResponse({'response_data': response_data})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)


# define the tools for the agenst to use


def google_image_gen():
    try:
        # Instantiate the image generator
        generator = VertexAIImageGeneratorChat()

        # Generate the image (adjust method name if needed)
        messages = [HumanMessage(content=["a cat at the beach"])]

        response = generator.invoke(messages)
        generated_image = response.content[0]

        # Convert binary data to an image
        image = Image.open(io.BytesIO(generated_image))

        # Display the image
        image.show()

    except Exception as e:
        # Handle the exception and provide a meaningful error message
        print(f"An error occurred: {e}")


# Example usage
if __name__ == "__main__":
    google_image_gen()


@csrf_exempt
@cache_page(60 * 15)
def anthropicdata(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Default message if 'data' is not provided
            promotedata = data.get('data', "How are you today?")

            logger.info("Received data: %s", promotedata)

            # Create a message using the Anthropic API
            message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.0,
                system="Respond only in Yoda-speak.",
                messages=[
                    {"role": "user", "content": promotedata}
                ]
            )
            response_content = message.content[0].text
            logger.info("Response content: %s", response_content)
            return JsonResponse({'response_data': response_content})
            # return JsonResponse({'response_data': 'Inspect the logs for the message object structure'})
        except json.JSONDecodeError:
            logger.error("Invalid JSON received", exc_info=True)
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error("Unexpected error", exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)
    logger.warning("Invalid method called")
    return JsonResponse({'error': 'Invalid method'}, status=405)


@csrf_exempt
def anthropicdata(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            promotedata = data.get('data')

            anthropic = ChatAnthropic
            model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

            System_message = SystemMessage(content=("You are an expert assistant specializing in physics."
                                                    "You teach students physics class {promotedata} "
                                                    "Provide clear and concise explanations of complex topics. "
                                                    "Use real-world examples to illustrate concepts. "
                                                    "Encourage critical thinking and problem-solving skills. "))

            user_question = data.get('question', '')

            messages = [

                {"role": "system", "content": System_message},
                {"role": "user", "content": user_question}
            ]

            # return JsonResponse({'response_data': 'Inspect the logs for the message object structure'})
        except json.JSONDecodeError:
            logger.error("Invalid JSON received", exc_info=True)
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    logger.warning("Invalid method called")
    return JsonResponse({'error': 'Invalid method'}, status=405)


# this is the code modifiers Ai


# def create_user(request):
#     if request.method == 'POST':
#         form = RequestUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'message': 'User created successfully!'})
#         else:
#             return JsonResponse({'errors': form.errors}, status=400)
#     else:
#         form = RequestUserForm()
#     return render(request, 'create_user.html', {'form': form})
@csrf_exempt
def save_data_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            user_email = data.get('user_email')
            user_password = data.get('user_password')
            user_Address = data.get('user_Address')
            user_country = data.get('user_country')
            user_plan = data.get('user_plan')
            user_desription = data.get('user_desription')

            # Create a new user object and save it
            user_save = user(
                user_email=user_email,
                user_password=user_password,
                user_Address=user_Address,
                user_country=user_country,
                user_plan=user_plan,
                user_description=user_desription,
            )
            user_save.save()

            return JsonResponse({'message': 'Data saved successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)