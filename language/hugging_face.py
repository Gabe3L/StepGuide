# from transformers.models.auto.tokenization_auto import AutoTokenizer
# from transformers.models.auto.modeling_auto import AutoModelForSeq2SeqLM

# class HuggingFace:
#     def __init__(self) -> None:
#         MODEL_NAME = "google/flan-t5-base"
#         self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
#         self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

#     def paraphrase_instruction(self, instruction: str, num_return_sequences=1, max_length=80) -> list:
#         prompt = f"Reword this instruction clearly and concisely: {instruction}"
#         inputs = self.tokenizer(prompt, return_tensors="pt", max_length=128, truncation=True)

#         outputs = self.model.generate(
#             **inputs,
#             max_length=max_length,
#             num_beams=4,
#             num_return_sequences=num_return_sequences,
#             temperature=0.7,
#             early_stopping=True,
#             do_sample=True
#         )

#         return [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

# if __name__ == "__main__":
#     hf = HuggingFace()
#     test_input = "There is a tree slightly to your left. Turn right."
#     results = hf.paraphrase_instruction(test_input, num_return_sequences=3)
#     for i, r in enumerate(results, 1):
#         print(f"{i}. {r}")
