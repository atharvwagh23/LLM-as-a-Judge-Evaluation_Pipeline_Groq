<div align="center">

# ⚖️ LLM-as-a-Judge Evaluation Pipeline

### Automatically benchmark one LLM's answers using another LLM as the judge

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-API-F55036?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-Data-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

</div>

---

## 📖 Overview

**LLM Evaluation** is a lightweight pipeline that measures how good an LLM's answers are, without manual grading.

It works in three steps:

1. A **Generator LLM** answers questions from a curated golden dataset.
2. A **Judge LLM** compares each generated answer to the golden (reference) answer.
3. The judge scores it across **10 quality dimensions** and results are saved to CSV.

Both models run through the [Groq API](https://groq.com/), and the models are fully configurable via environment variables, so you can swap in any pair to compare.

---

## ✨ Features

- 🤖 **Two-model architecture**: separate generator and judge models
- 🏆 **Golden dataset**: 10 database-concept Q&A pairs used as ground truth
- 📊 **10-metric scoring rubric**: from correctness to safety
- 🧾 **Structured JSON output**: judge responses are enforced as JSON and safely parsed, with a regex fallback
- 💾 **CSV export**: every question, answer, and score saved for analysis
- ⚙️ **Configurable**: change models with a single line in `.env`

---

## 🧠 How It Works

```
┌──────────────────┐     question      ┌──────────────────┐
│  Golden Dataset  │ ────────────────▶ │  Generator LLM   │
│ (question+answer)│                   │    (MODEL1)      │
└──────────────────┘                   └────────┬─────────┘
         │                                      │ generated answer
         │ golden answer                        ▼
         │                             ┌──────────────────┐
         └───────────────────────────▶ │    Judge LLM     │
                                       │    (MODEL2)      │
                                       └────────┬─────────┘
                                                │ 10 scores (JSON)
                                                ▼
                                    📄 data/evaluation_results.csv
```

---

## 📏 Evaluation Metrics

The judge scores each answer from **0 to 10** on:

| # | Metric | What it measures |
|---|--------|------------------|
| 1 | **Correctness** | Is the answer factually right? |
| 2 | **Relevance** | Does it address the question asked? |
| 3 | **Completeness** | Does it cover the key points of the golden answer? |
| 4 | **Faithfulness** | Does it stay true to the reference answer? |
| 5 | **Hallucination** | Is it free of made-up information? *(10 = no hallucination)* |
| 6 | **Reasoning Quality** | Is the explanation logically sound? |
| 7 | **Fluency & Readability** | Is it well written and easy to read? |
| 8 | **Coherence** | Is it consistent and well structured? |
| 9 | **Safety & Toxicity** | Is it free of harmful content? |
| 10 | **Semantic Similarity** | How close is the meaning to the golden answer? |

---

## 🗂️ Project Structure

```
LLM-evaluation/
├── 📁 data/
│   ├── goldendataset.json        # Ground-truth Q&A pairs
│   └── evaluation_results.csv    # Output: answers + judge scores
├── 🐍 main.py                    # Entry point
├── 🐍 evaluator.py               # Orchestrates the evaluation loop
├── 🐍 generator_llm.py           # Generates answers (MODEL1)
├── 🐍 judge_llm.py               # Scores answers (MODEL2)
├── 🐍 generate_goldendataset.py  # Builds the golden dataset
├── 📄 requirements.txt
├── 📄 pyproject.toml
└── 📄 .env_example
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.12+**
- A free [Groq API key](https://console.groq.com/keys)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/LLM-evaluation.git
cd LLM-evaluation
```

### 2️⃣ Install dependencies

Using **pip**:

```bash
pip install -r requirements.txt
```

Or using **uv**:

```bash
uv sync
```

### 3️⃣ Configure environment variables

Copy the example file and fill in your values:

```bash
cp .env_example .env
```

```env
GROQ_API_KEY=your_api_key_here
MODEL1=your-generator-model-name
MODEL2=your-judge-model-name
```

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key |
| `MODEL1` | Model that **generates** the answers |
| `MODEL2` | Model that **judges** the answers |

> 💡 Browse available model names in the [Groq models list](https://console.groq.com/docs/models). For fairer judging, use a stronger model for `MODEL2`.

### 4️⃣ (Optional) Regenerate the golden dataset

```bash
python generate_goldendataset.py
```

### 5️⃣ Run the evaluation

```bash
python main.py
```

You'll see each question, the generated answer, and the judge's scores print live in the terminal. When finished, results are saved to `data/evaluation_results.csv`.

---

## 📊 Sample Results

Average judge scores across the 10-question golden dataset:

| Metric | Avg Score |
|--------|:---------:|
| Correctness | 9.60 |
| Relevance | 9.90 |
| Completeness | 9.40 |
| Faithfulness | 9.20 |
| Hallucination | 9.80 |
| Reasoning Quality | 9.30 |
| Fluency & Readability | 9.90 |
| Coherence | 9.90 |
| Safety & Toxicity | 10.00 |
| Semantic Similarity | 9.25 |
| **Overall** | **⭐ 9.62 / 10** |

---

## 📄 Example Output

**Question:** What is a primary key?

**Golden answer:**
> A primary key is a unique identifier for a record in a database table.

**Generated answer:**
> A primary key is a unique identifier for each record in a database table, ensuring no duplicate rows and enabling efficient data retrieval and relationships. It cannot contain NULL values and is often a single column, though it can be a composite of multiple columns.

**Judge scores:**

```json
{
  "correctness": 10,
  "relevance": 10,
  "completeness": 10,
  "faithfulness": 9,
  "hallucination": 10,
  "reasoning_quality": 9,
  "fluency_and_readability": 10,
  "coherence": 10,
  "safety_and_toxicity": 10,
  "semantic_similarity": 9
}
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Core language |
| **Groq** | Fast LLM inference API |
| **Pandas** | Results handling and CSV export |
| **python-dotenv** | Environment variable management |
| **NumPy / Rich** | Data utilities and terminal output |

---

