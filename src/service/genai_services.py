# uv venv .venv --python=3.12
# source .venv/bin/activate
# uv pip install transformers torch

import time
import os
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM

def load_model_and_tokenizer(model_id, local_dir="./local_models"):
    """
    Load model and tokenizer, checking local storage first.
    If not available locally, download from Hugging Face and save locally.
    """
    # Create local directory if it doesn't exist
    local_model_path = Path(local_dir) / model_id.split("/")[-1]
    local_model_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Checking for model in {local_model_path}")
    
    # Check if model exists locally
    if (local_model_path / "config.json").exists():
        print("Loading model from local storage...")
        load_start = time.time()
        tokenizer = AutoTokenizer.from_pretrained(local_model_path)
        model = AutoModelForCausalLM.from_pretrained(local_model_path)
        print(f"Model loaded from local storage in {time.time() - load_start:.2f} seconds")
    else:
        print(f"Model not found locally. Downloading from Hugging Face ({model_id})...")
        download_start = time.time()
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)
        print(f"Model downloaded in {time.time() - download_start:.2f} seconds")
        
        # Save model locally for future use
        print("Saving model to local storage...")
        save_start = time.time()
        tokenizer.save_pretrained(local_model_path)
        model.save_pretrained(local_model_path)
        print(f"Model saved in {time.time() - save_start:.2f} seconds")
    
    return tokenizer, model

# Load model and tokenizer
model_id = "HuggingFaceTB/SmolLM2-135M-Instruct"
tokenizer, model = load_model_and_tokenizer(model_id)

def enhance_with_ai(sentence):
    start_time = time.time()
    
    prompt = f"Rewrite the following sentence in a professional tone:\n{sentence}\nProfessional version:"
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Start measuring generation time specifically
    generation_start = time.time()
    outputs = model.generate(**inputs, max_new_tokens=50)
    generation_end = time.time()
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True).split("Professional version:")[-1].strip()
    
    end_time = time.time()
    total_time = end_time - start_time
    generation_time = generation_end - generation_start
    
    return result, total_time, generation_time

def generate_cover_letter():
    """Generate a professional cover letter for a resume without any input parameters."""
    start_time = time.time()
    
    prompt = "Write a professional cover letter for a job application. The job field is pharmacy. Make it generic but compelling, highlighting key skills and enthusiasm for the role:"
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Start measuring generation time specifically
    generation_start = time.time()
    outputs = model.generate(**inputs, max_new_tokens=300, temperature=0.7, do_sample=True)
    generation_end = time.time()
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True).split(":")[-1].strip()
    
    end_time = time.time()
    total_time = end_time - start_time
    generation_time = generation_end - generation_start
    
    return result, total_time, generation_time

# Example usage
sentence = "Dynamic and a skilled information technology specialist with proven success in developing and leading multiple projects involving a complete software development life cycle"
result, total_time, generation_time = enhance_with_ai(sentence)

print(f"Original: {sentence}")
print(f"Professional version: {result}")
print(f"Total processing time: {total_time:.2f} seconds")
print(f"Model generation time: {generation_time:.2f} seconds")

# Generate cover letter example
print("\n" + "="*50)
print("COVER LETTER GENERATION")
print("="*50)
cover_letter, cover_total_time, cover_generation_time = generate_cover_letter()
print(f"Generated Cover Letter:\n{cover_letter}")
print(f"Total processing time: {cover_total_time:.2f} seconds")
print(f"Model generation time: {cover_generation_time:.2f} seconds")