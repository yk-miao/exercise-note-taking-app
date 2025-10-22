# import libraries
from locale import currency
import os
from dotenv import load_dotenv 
from openai import OpenAI
from datetime import datetime


load_dotenv() # Loads environment variables from .env
token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"
# A function to call an LLM model and return the response

def call_llm_model(model, messages, temperature=1.0, top_p=1.0):
    client = OpenAI(base_url=endpoint, api_key=token)
    response = client.chat.completions.create(
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        model=model)
    return response.choices[0].message.content

# A function to translate text using the LLM model

def translate_text(text, target_language="Chinese"):
    prompt = f"Translate the following text to {target_language}: \n\n{text}"
    messages = [{"role": "user","content": prompt}]
    return call_llm_model(model, messages)


system_prompt_template = '''
Current datetime (ISO 8601): {current_datetime}

Extract the user's input into the following structured fields:
1. Title: A concise title of the note, fewer than 5 words.
2. Notes: A clear paragraph summarizing the user's intent.
3. Tags: An array of exactly 3 keywords categorizing the note.
4. EventDate: If a specific date is implied, output as ISO date YYYY-MM-DD; else null.
5. EventTime: If a specific time is implied, output as 24-hour time HH:MM; else null.

Rules:
- For relative times like "tmr"/"tomorrow", convert to absolute using Current datetime. If ambiguous, set null.
- If only time is present without a date, set EventTime and leave EventDate null.
- Output ONLY valid JSON on a single line with no extra text, newlines, or code fences.
- Output Title and Notes in the language: {lang}.

Example:
Input: "Badminton tmr 5pm @polyu".
Output: {{"Title": "Badminton at PolyU", "Notes": "Remember to play badminton at 5pm tomorrow at PolyU.", "Tags": ["badminton", "sports", "tomorrow"], "EventDate": "2025-10-23", "EventTime": "17:00"}}
'''

def process_user_notes(language, user_input):
    current_datetime = datetime.now().isoformat(timespec='minutes')
    system_prompt_filled = system_prompt_template.format(
        lang=language,
        current_datetime=current_datetime,
    )
    messages = [
        {
            "role": "system",
            "content": system_prompt_filled,
        },
        {
            "role": "user",
            "content": user_input,
        }]

    response_content = call_llm_model(model, messages)
    return response_content

# Run the main function if this script is executed
if __name__ == "__main__":
    print("Testing LLM with Chinese input:")
    result = process_user_notes("Chinese", "Get up tomorrow 7am")
    print(result)
    print("\n" + "="*50 + "\n")
    
    print("Testing LLM with English input:")
    result = process_user_notes("English", "Learn python programming and docker")
    print(result)
    print("\n" + "="*50 + "\n")
    
    print("Testing LLM with event input:")
    result = process_user_notes("English", "Meeting tomorrow at 3pm with the team about project updates")
    print(result)