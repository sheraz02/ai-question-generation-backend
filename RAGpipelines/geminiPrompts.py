

def question_generation_prompt(prompt_text: str, num_questions: int = 5, difficulty: str = "medium") -> str:
    prompt = f"""
        You are an expert exam-question generator.

        Create exactly {num_questions} high-quality multiple-choice questions on the topic below:
        Topic: {prompt_text}
        Difficulty level: {difficulty}

        Your output MUST follow these rules EXACTLY:

        1. Output ONLY valid JSON (no explanation, no markdown, no text before or after).
        2. JSON structure must match the schema.

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
        - Generate ids (example: "1, 2, 3").

        Return ONLY the JSON. Ensure it is syntactically valid.
        """
    return prompt