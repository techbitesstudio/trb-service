# uv venv .venv --python=3.12
# source .venv/bin/activate
# uv pip install transformers torch

import time
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM

def load_model_and_tokenizer(model_id, local_dir="./local_models"):
    """
    Load model and tokenizer, checking local storage first.
    If not available locally, download from Hugging Face and save locally.
    """
    local_model_path = Path(local_dir) / model_id.split("/")[-1]
    local_model_path.mkdir(parents=True, exist_ok=True)

    print(f"Checking for model in {local_model_path}")

    if (local_model_path / "config.json").exists():
        print("Loading model from local storage...")
        load_start = time.time()
        tokenizer = AutoTokenizer.from_pretrained(local_model_path)
        model = AutoModelForCausalLM.from_pretrained(local_model_path)
        print(f"Model loaded in {time.time() - load_start:.2f} seconds")
    else:
        print(f"Model not found locally. Downloading from Hugging Face ({model_id})...")
        download_start = time.time()
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)
        print(f"Model downloaded in {time.time() - download_start:.2f} seconds")

        print("Saving model locally...")
        save_start = time.time()
        tokenizer.save_pretrained(local_model_path)
        model.save_pretrained(local_model_path)
        print(f"Model saved in {time.time() - save_start:.2f} seconds")

    return tokenizer, model

# Load model and tokenizer
model_id = "HuggingFaceTB/SmolLM2-360M-Instruct"
tokenizer, model = load_model_and_tokenizer(model_id)

def enhance_with_ai(prompt_type, sentence):
    start_time = time.time()

    if prompt_type == "job_responsibility":
        prompt = f"Rewrite the following sentence in a professional tone:\n{sentence}\nProfessional version:"
    else:
        prompt = f"""Rewrite this sentence in a professional tone. Keep it clear and concise.
        
        Input: {sentence}
        
        Output:"""

    inputs = tokenizer(prompt, return_tensors="pt")
    generation_start = time.time()
    outputs = model.generate(**inputs, max_new_tokens=300, temperature=0.7, do_sample=True)

    generation_end = time.time()

    # Decode and clean up the output
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract just the response after "Output:"
    if "Output:" in decoded:
        rewritten_text = decoded.split("Output:", 1)[1].strip()
    else:
        # Fallback if the output format isn't as expected
        rewritten_text = decoded.replace(prompt, "").strip()
    
    # Remove any markdown formatting or special instructions
    cleaned_text = []
    for line in rewritten_text.split('\n'):
        line = line.strip()
        if line and not any(word in line.lower() for word in ['bullet', 'point', 'placeholder', 'must contain']):
            # Remove any remaining markdown characters
            line = line.replace('*', '').replace('-', '').strip()
            cleaned_text.append(line)
    
    # Join with spaces and ensure proper punctuation
    rewritten_text = ' '.join(cleaned_text).strip()
    if rewritten_text and not any(rewritten_text.endswith(p) for p in ['.', '!', '?']):
        rewritten_text += '.'

    total_time = time.time() - start_time
    generation_time = generation_end - generation_start

    return rewritten_text, total_time, generation_time

def generate_cover_letter():
    """Generate a professional cover letter for a resume without any input parameters."""
    start_time = time.time()
    
    prompt = "Write a professional cover letter for a job application. The job field is pharmacy. Make it generic but compelling, highlighting key skills and enthusiasm for the role:"
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Start measuring generation time specifically
    generation_start = time.time()
    outputs = model.generate(**inputs, max_new_tokens=300, temperature=0.7, do_sample=True)
    generation_end = time.time()
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True).split(":")[-1].strip().replace("\n", "")
    
    end_time = time.time()
    total_time = end_time - start_time
    generation_time = generation_end - generation_start
    
    return result, total_time, generation_time
