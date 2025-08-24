import random
from llama_cpp import Llama

llm = Llama(
    model_path=".phi2-gguf/phi-2.Q3_K_M.gguf",
    n_ctx=2048,
    n_threads=4
)

style = random.choice([
    "Use a confident and enthusiastic tone.",
    "Keep a formal and concise style.",
    "Make it warm and approachable.",
    "Highlight innovation and adaptability."
])

prompt = """
You are a professional career coach. Write a polished, tailored cover letter.

Resume:
John Doe – Data Engineer with 5 years of experience in SQL, Python, and cloud data pipelines. Built scalable ETL systems at ACME Corp, improving reporting speed by 40%.

Job Description:
We are seeking a Data Engineer with strong SQL, Python, and cloud experience. The candidate should have experience in building data pipelines and optimizing performance.

Instructions:
- Write a 2-paragraph professional cover letter.
- Use a polite, confident tone.
- Mention one quantified achievement from the resume.
- Reuse 2–3 keywords from the job description.
- End with enthusiasm and availability.
"""

out = llm(prompt, max_tokens=300, temperature=1.0, top_p=0.9)
print(out["choices"][0]["text"])
