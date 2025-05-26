import torch
from transformers import pipeline

def process_query(text):
    try:
        generator = pipeline('text-generation', 
                            model='gpt2',  # Using lighter model
                            device=0 if torch.cuda.is_available() else -1)
        return generator(text, max_length=50)[0]['generated_text']
    except Exception as e:
        print(f"LLM Error: {str(e)}")
        return "I encountered an error"