import logging
from groq import Groq


class GroqClient:
    def __init__(self, api_key, model_name="llama-3.3-70b-versatile"):
        self.client = Groq(api_key=api_key)
        self.model_name = model_name

    def generate_answer(self, query, context):
        try:
            prompt = f"Based on the following documents, answer the question:\n\n{context}\n\nQuestion: {query}"

            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}], model=self.model_name
            )
            return completion.choices[0].message.content
        except Exception as e:
            logging.error(f"Error generating answer from Groq API: {str(e)}")
            raise
