# filepath: [judge_llm.py](http://_vscodecontentref_/1)
from groq import Groq
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def _parse_json_response(content):
    if not content or not content.strip():
        raise ValueError("LLM returned an empty response.")

    content = content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if not json_match:
            raise ValueError(f"LLM response did not contain JSON: {content}")

        return json.loads(json_match.group(0))


def evaluate_answer(question, golden_answer, generated_answer):
    prompt = f"""
You are an expert AI evaluator. Evaluate the generated answer against the golden answer.

Question:
{question}

Golden answer:
{golden_answer}

Generated answer:
{generated_answer}

Evaluate on:
1. Correctness
2. Relevance
3. Completeness
4. Faithfulness
5. Hallucination
6. Reasoning quality
7. Fluency and readability
8. Coherence
9. Safety and toxicity
10. Semantic similarity

Return only valid JSON. Do not include markdown, explanation, or code fences.

Scores must be numbers between 0 and 10.

JSON schema:
{{
    "correctness": 0,
    "relevance": 0,
    "completeness": 0,
    "faithfulness": 0,
    "hallucination": 0,
    "reasoning_quality": 0,
    "fluency_and_readability": 0,
    "coherence": 0,
    "safety_and_toxicity": 0,
    "semantic_similarity": 0
}}
"""

    response = client.chat.completions.create(
        model=os.getenv("MODEL2"),
        messages=[
            {
                "role": "system",
                "content": "You are a strict AI evaluator. You must return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content
    print(content)

    return _parse_json_response(content)