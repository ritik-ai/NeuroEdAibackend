from django.shortcuts import render

# Create your views here.
from langchain_anthropic import ChatAnthropic
from django.views.decorators.csrf import csrf_exempt
from typing import Annotated, Literal, TypedDict
from langchain_core.messages import HumanMessage
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import SystemMessage
import os
from openai import OpenAI

@tool
def morning_wishes_agent():
    """Generate morning wishes using the Gemini 1.5 Flash model."""
    try:
        llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv('GEMINI_API_KEY')
        )

        system_message = SystemMessage(
            content="You are a morning wishes assistant. Generate a cheerful morning greeting."
        )

        messages = [system_message]

        morning_wish = llm.invoke(messages)
        print(morning_wish)
        return morning_wish
    except Exception as e:
        return f"An error occurred: {str(e)}"



@tool
def Coversion_agents():
    """Converstion Ai agents """
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is a LLM?"}
            ]
        )

    except:
        Exception as e:
        return f"An error occurred: {str(e)}"
    


@tool
def Subject_info():
    """this is Subject info"""
    



@tool
def Sentment_Analysis():
 """Sentiment Analysis"""

@tool
def Notification_Alert():
    """Notification Alert"""

