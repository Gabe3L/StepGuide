from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.models.auto.modeling_auto import AutoModelForSeq2SeqLM
import torch

MODEL_NAME = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def paraphrase_instruction(instruction: str, num_return_sequences=1, max_length=80) -> list:
    prompt = f"Reword this instruction clearly and concisely: {instruction}"
    inputs = tokenizer(prompt, return_tensors="pt", max_length=128, truncation=True)

    outputs = model.generate(
        **inputs,
        max_length=max_length,
        num_beams=4,
        num_return_sequences=num_return_sequences,
        temperature=0.7,
        early_stopping=True,
        do_sample=True
    )

    return [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

if __name__ == "__main__":
    test_input = "There is a tree slightly to your left. Turn right."
    results = paraphrase_instruction(test_input, num_return_sequences=3)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r}")
