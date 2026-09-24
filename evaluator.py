import json
import pandas as pd

from generator_llm import generate_answer
from judge_llm import evaluate_answer

def run_evaluation():

    with open("data/goldendataset.json", "r") as f:
        dataset = json.load(f)

    result = []

    for item in dataset:

        question = item["question"]
        golden_answer = item["answer"]

        print("-"*50)
        print(f"\nQuestion: {question}")

        generated_answer = generate_answer(question)

        print(f"\nGenerated Answer: {generated_answer}")

        evaluation = evaluate_answer(question, golden_answer, generated_answer)
        
        print("\n Judge evaluation:")
        print(evaluation)

        row = {
            "question": question,
            "golden_answer": golden_answer,
            "generated_answer": generated_answer,
            "evaluation": evaluation
        }

        result.append(row)
    df = pd.DataFrame(result)
    df.to_csv("data/evaluation_results.csv", index=False)

    print("\n")
    print("Evaluation completed")