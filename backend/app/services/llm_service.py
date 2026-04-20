from groq import Groq
import json 
import os
from dotenv import load_dotenv
from datetime import date
load_dotenv()

GROK_KEY = os.getenv("GROQ_API_KEY")

class LLMService:
    def __init__(self, api_key = GROK_KEY, model_id = "llama-3.3-70b-versatile", system_message = None):
        self.client = Groq(api_key = api_key)
        self.model_id = model_id
        self.system_message = system_message
        

    def _build_messages(self, prompt):
        messages = []

        if self.system_message:
            messages.append({
                "role": "system",
                "content": self.system_message
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        return messages
    

    def format_prompt(self, prompt, role="user"):
        return{
            "role" : role,
            "content" : prompt
        }
    
    def generate_text(self, prompt:str, temperature:float = 0.5, max_tokens:int = 1024): 
        
        try:
            response = self.client.chat.completions.create(
                model = self.model_id,
                messages = self._build_messages(prompt),
                max_tokens = max_tokens,
                temperature = temperature
            )
            return response.choices[0].message.content
        
        except Exception as e:
            raise RuntimeError(f"Error generating text: {e}")

    def generate_summary(self, transcript:str, max_tokens, temperature: float = 0.5):
        #zero-shot prompt
        prompt = f"""
        Summarize the given meeting transcript into clear, concise bullet points

        Rules:
        - Focus on discussion, key decisions and outcomes.
        - Ignore filler conversation
        - Do not repeat information
        - Output only bullet points, no nested bullets
        - Do not include any introduction, heading or explanation.
        - Do not write phrases like "Here are .." or "Following are.."
        Transcript: {transcript}"""

        try:
            response = self.client.chat.completions.create(
                temperature=temperature, 
                messages = self._build_messages(prompt),
                max_tokens=max_tokens,
                model=self.model_id
                )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return (f"Error: {e}")
        
        
    
    def extract_tasks(self, transcript:str, max_tokens, temperature:float = 0.3):
        #one-shot prompt
        prompt = f"""
        Extract action items in strict JSON format from meeting transcript. 
        Output must be a JSON array. 

        Each object must have only these fields:

        - task (string)
        - owner (string or null)
        - due_date (YYYY-MM-DD or null)
        - status (Pending or Completed)

        Rules:
        - If only day is given, write the due date with respect to current date: {date.today()}
        - Return raw JSON only, no explanation.
        - If a field is missing use null

        Transcript: {transcript}
        """
        try:
            responses = self.client.chat.completions.create(
                model=self.model_id,
                max_tokens=max_tokens,
                temperature=temperature,
                messages = self._build_messages(prompt)
            )

            content = responses.choices[0].message.content
            tasks = json.loads(content)
            return tasks
        
        except Exception as e:
            raise RuntimeError(f"Error: {e}")
    