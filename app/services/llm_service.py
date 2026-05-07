import os
from app.core.logger import logger
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in environment variables")

if LLM_PROVIDER == "groq":
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
else:
    raise ValueError("Unsupported LLM provider")


class LLMService:

    @staticmethod
    async def generate_response(prompt: str) -> str:
        try:
            # NOTE: Groq SDK is sync, so we keep it simple for now
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print("FULL ERROR:", e)
            logger.error(f"LLM Error: {str(e)}")
            return "LLM generation failed"