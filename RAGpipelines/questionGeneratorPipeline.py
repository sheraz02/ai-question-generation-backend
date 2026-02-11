import os
import json
from typing import Any, Dict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI



load_dotenv()



def question_generation_prompt(topic: str, num_questions: int = 5, difficulty: str = "medium") -> str:
    """
    Generates a prompt for an LLM to create multiple-choice questions on a given topic.

    Args:
        topic (str): The topic for which questions should be generated.
        num_questions (int, optional): Number of questions to generate. Defaults to 5.
        difficulty (str, optional): Difficulty level ("easy", "medium", "hard"). Defaults to "medium".

    Returns:
        str: The fully formatted prompt.
    """
    prompt = f"""
        You are an expert exam-question generator.

        Create exactly {num_questions} high-quality multiple-choice questions on the following topic:
        Topic: {topic}
        Difficulty level: {difficulty}

        Your output MUST follow these rules EXACTLY:

        1. Output ONLY valid JSON (no explanation, no markdown, no text before or after).
        2. JSON structure must strictly follow the provided schema.

        3. Question requirements:
        - Must be clear, academically correct, and unambiguous.
        - Must NOT include definitions or explanations inside the question text.
        - Must NOT reveal clues that indicate the correct answer.

        4. Choices requirements:
        - Must be short, distinct, and mutually exclusive.
        - Must NOT include hints, clues, or overlapping meanings.
        - Must be similar in length to avoid revealing the correct choice.

        5. Explanation requirements:
        - Must be concise, factual, and directly reference why the correct answer is correct.
        - Must NOT repeat the question.
        - Must NOT mention distractors.

        6. IDs:
        - Generate sequential integer ids starting from 1.

        7. Related topic:
        - Write topic name to which, question is related

        8. Hint:
        - Must provide a useful, brief clue to aid in answering.

        Return ONLY the JSON. Ensure it is syntactically valid.
        """
    return prompt



def build_schema() -> Dict[str, Any]:
    """
    Returns a JSON schema for validating multiple-choice questions.

    Returns:
        Dict[str, Any]: The JSON schema.
    """
    return {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "question": {"type": "string"},
                        "choices": {
                            "type": "array",
                            "minItems": 2,
                            "items": {"type": "string"}
                        },
                        "correct_index": {"type": "integer", "minimum": 0},
                        "related_topic": {"type": "array"},
                        "hint": {"type": "string"},
                        "explanation": {"type": "string"}
                    },
                    "required": ["id", "question", "choices", "correct_index", "related_topic", "hint", "explanation"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["questions"],
        "additionalProperties": False
    }



class GeneratorClient:
    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.6):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = model_name
        self.temperature = temperature

        if not self.api_key:
            raise RuntimeError("Please set GOOGLE_API_KEY environment variable")

        # instantiate the LangChain wrapper LLM
        self.client = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            # you can pass other params here like max_tokens, timeout, etc.
        )

    def call_gemini(self, prompt: str, questions: int = 5, difficulty_level: str = "easy") -> Dict[str, Any]:
        """
        Use the LangChain ChatGoogleGenerativeAI wrapper and LangChain's structured-output helper
        to force JSON output matching build_schema().
        """
        final_prompt = question_generation_prompt(topic=prompt, num_questions=questions, difficulty=difficulty_level)

        try:
            # create a structured model that enforces the json_schema method
            structured_model = self.client.with_structured_output(
                schema=build_schema(),
                method="json_schema"
            )

            # call the model. It returns a dict when using with_structured_output(..., method="json_schema")
            response = structured_model.invoke(final_prompt)

            # response should already be a dict matching your schema
            # If it's wrapped in an AIMessage-like object, .content or .text might be needed,
            # but with_structured_output + method="json_schema" returns parsed dict per docs.
            if isinstance(response, dict):
                return response

            # fallback: try converting to dict if it's a string or has .text
            if hasattr(response, "text"):
                try:
                    return json.loads(response.text)
                except Exception:
                    return {"raw": response.text}
            if isinstance(response, str):
                try:
                    return json.loads(response)
                except Exception:
                    return {"raw": response}

            return {"full_response": str(response)}

        except Exception as e:
            # return the error so you can debug locally
            return {"error": str(e)}

# client = GeneratorClient()
# import json
# d = client.call_gemini(
#     prompt = 'international politics, current affairs',
#     difficulty_level='hard',
#     questions=100
# )
# print(json.dumps(d, indent=4))