from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
from fastapi.middleware.cors import CORSMiddleware

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptInput(BaseModel):
    use_case: str
    details: dict

@app.post("/generate")
async def generate_response(prompt_input: PromptInput):
    prompt = build_prompt(prompt_input.use_case, prompt_input.details)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that drafts legal documents."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"response": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"error": str(e)}

def build_prompt(use_case: str, details: dict) -> str:
    if use_case == "rental_agreement":
        return (
            f"Draft a leave and license agreement with the following details:\\n"
            f"Licensor: {details.get('licensor_name')}\\n"
            f"Licensee: {details.get('licensee_name')}\\n"
            f"Premises: {details.get('address')}\\n"
            f"Monthly Rent: ₹{details.get('rent')}\\n"
            f"Deposit: ₹{details.get('deposit')}\\n"
            f"Start Date: {details.get('start_date')}\\n"
            f"End Date: {details.get('end_date')}\\n"
            f"Add standard Indian rental clauses."
        )
    return ""
