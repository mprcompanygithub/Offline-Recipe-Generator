import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_recipe(request: Request):
    try:
        data = await request.json()
        ingredients = data.get("ingredients", "")
        print(f"Received ingredients: {ingredients}")

        prompt = f"Generate a cooking recipe using these ingredients: {ingredients}. Return the title, ingredients list, and step-by-step instructions."

        # Request streamed response from DeepSeek/Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "deepseek-r1:1.5b", "prompt": prompt},
            stream=True
        )

        # Read and concatenate chunks safely
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line)
                    full_response += chunk.get("response", "")
                except Exception as e:
                    print("Chunk parse error:", e)

        return {"recipe": full_response.strip() or "No recipe returned."}

    except Exception as e:
        print("Backend Exception:", e)
        return {"recipe": f"Error: {str(e)}"}
