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