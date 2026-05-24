from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from catalog_brain import CatalogBrain
from semantic_matcher import SemanticMatcher
from dialogue_engine import DialogueEngine
from llm_orchestrator import LLMOrchestrator

# ---------------------------------
# FastAPI App
# ---------------------------------

app = FastAPI()

# ---------------------------------
# Load systems
# ---------------------------------

brain = CatalogBrain()

all_assessments = brain.get_all_assessments()

matcher = SemanticMatcher(all_assessments)

dialogue = DialogueEngine()

llm = LLMOrchestrator()


# ---------------------------------
# Request Schema
# ---------------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# ---------------------------------
# Root Endpoint
# ---------------------------------

@app.get("/")
def home():

    return {
        "message": "SHL Nexus API Running"
    }


# ---------------------------------
# Health Endpoint
# ---------------------------------

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# ---------------------------------
# Chat Endpoint
# ---------------------------------

@app.post("/chat")
def chat(req: ChatRequest):

    # ---------------------------------
    # Empty protection
    # ---------------------------------

    if not req.messages:

        return {
            "reply":
            "Please provide a hiring or assessment request.",
            "recommendations": [],
            "end_of_conversation": False
        }

    latest_message = req.messages[-1].content

    # ---------------------------------
    # Prompt injection protection
    # ---------------------------------

    if dialogue.is_prompt_injection(latest_message):

        return {
            "reply":
            "I can only assist with SHL assessment recommendations and comparisons.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # ---------------------------------
    # Out-of-scope handling
    # ---------------------------------

    if dialogue.is_out_of_scope(latest_message):

        return {
            "reply":
            "I can only assist with SHL assessments and related comparisons.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # ---------------------------------
    # Comparison handling
    # ---------------------------------

    if dialogue.is_comparison_request(latest_message):

        left_name, right_name = dialogue.extract_comparison_items(
            latest_message
        )

        left_item = brain.find_assessment_by_name(left_name or "")

        right_item = brain.find_assessment_by_name(right_name or "")

        if left_item and right_item:

            comparison_reply = llm.generate_comparison_reply(
                left_item,
                right_item
            )

            return {
                "reply": comparison_reply,
                "recommendations": [],
                "end_of_conversation": False
            }

        return {
            "reply":
            "I could not identify both SHL assessments for comparison.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # ---------------------------------
    # Clarification handling
    # ---------------------------------

    if dialogue.needs_clarification(latest_message):

        return {
            "reply":
            "Could you share more about the role, seniority, and important skills or traits you want to assess?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # ---------------------------------
    # Build semantic context
    # ---------------------------------

    full_context = " ".join(
        [msg.content for msg in req.messages]
    )

    # ---------------------------------
    # Retrieve recommendations
    # ---------------------------------

    results = matcher.search(
        full_context,
        top_k=5
    )

    # ---------------------------------
    # Generate response
    # ---------------------------------

    ai_reply = llm.generate_recommendation_reply(
        full_context,
        results
    )

    # ---------------------------------
    # Format recommendations
    # ---------------------------------

    recommendations = []

    for item in results:

        recommendations.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": item["test_type"]
        })

    # ---------------------------------
    # Final response
    # ---------------------------------

    return {
        "reply": ai_reply,
        "recommendations": recommendations,
        "end_of_conversation": False
    }