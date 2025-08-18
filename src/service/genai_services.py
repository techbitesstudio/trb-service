# uv venv .venv --python=3.12
# source .venv/bin/activate
# uv pip install transformers torch

import time
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM

def load_model_and_tokenizer(model_id, local_dir="./local_models"):
    """
    Load model and tokenizer with 16-bit precision on CPU.
    Checks local storage first, then downloads from Hugging Face if needed.
    """
    import torch
    
    local_model_path = Path(local_dir) / model_id.split("/")[-1]
    local_model_path.mkdir(parents=True, exist_ok=True)

    print(f"Checking for model in {local_model_path}")
    
    # Force CPU usage
    device = torch.device("cpu")
    print("Using device:", device)
    
    # Configure model to use 16-bit precision
    torch_dtype = torch.float16
    print(f"Using {torch_dtype} precision")

    if (local_model_path / "config.json").exists():
        print("Loading model from local storage...")
        load_start = time.time()
        tokenizer = AutoTokenizer.from_pretrained(local_model_path)
        model = AutoModelForCausalLM.from_pretrained(
            local_model_path,
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=True
        )
        model.to(device)
        print(f"Model loaded in {time.time() - load_start:.2f} seconds")
    else:
        print(f"Model not found locally. Downloading from Hugging Face ({model_id})...")
        download_start = time.time()
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=True
        )
        model.to(device)
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
    import torch
    
    start_time = time.time()
    device = torch.device("cpu")
    
    try:
        # Prepare prompt
        if prompt_type == "job_responsibility":
            prompt = f"Rewrite the following sentence in a professional tone:\n{sentence}\nProfessional version:"
        else:
            prompt = f"""Rewrite this sentence in a professional tone. Keep it clear and concise.
            
            Input: {sentence}
            
            Output:"""

        # Tokenize and move to device
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        
        # Generate with optimized parameters for CPU
        generation_start = time.time()
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=200,  # Reduced from 300 for faster generation
                temperature=0.7,
                do_sample=True,
                num_beams=1,         # Use greedy search for speed
                pad_token_id=tokenizer.eos_token_id
            )
        generation_end = time.time()

        # Decode and clean up the output
        decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the response after "Output:" or fallback
        if "Output:" in decoded:
            rewritten_text = decoded.split("Output:", 1)[1].strip()
        else:
            rewritten_text = decoded.replace(prompt, "").strip()
        
        # Clean up the text
        cleaned_text = []
        for line in rewritten_text.split('\n'):
            line = line.strip()
            if line and not any(word in line.lower() for word in ['bullet', 'point', 'placeholder', 'must contain']):
                line = line.replace('*', '').replace('-', '').strip()
                cleaned_text.append(line)
        
        # Join with spaces and ensure proper punctuation
        rewritten_text = ' '.join(cleaned_text).strip()
        if rewritten_text and not any(rewritten_text.endswith(p) for p in ['.', '!', '?']):
            rewritten_text += '.'
            
        total_time = time.time() - start_time
        generation_time = generation_end - generation_start
        
        print(f"Total processing time: {total_time:.2f}s (Generation: {generation_time:.2f}s)")
        
        return rewritten_text, total_time, generation_time
        
    except Exception as e:
        print(f"Error in enhance_with_ai: {str(e)}")
        return "Error processing your request. Please try again.", 0, 0

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
