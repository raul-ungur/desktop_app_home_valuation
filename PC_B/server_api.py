from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="server 01")

OLLAMA_URL = "http://localhost:11434/api/generate"

class LLMRequest(BaseModel):
    prompt: str

@app.get("/health")
def health():
    return {"status" : "ok"}

class HouseRequest(BaseModel):
    square: str
    rooms: str 
    bathrooms: str 
    garage: bool

@app.post("/api/estimate")
def estimate(house: HouseRequest):
    prompt = f""" i have a house with the following charaterristic:
    Square meters :{house.square}
    Rooms :{ house.rooms}
    Bathrooms : {house.bathrooms}
    Garage : {house.garage}
    give me a short desription of this house and an aproximate price ,without saying "consult real sources...."
    """
    response = requests.post(
                OLLAMA_URL,
                json={
                    "model":"qwen3:1.7b",
                    "prompt" : prompt,

                    "stream":False
                }
            )
    response.raise_for_status()
    
    ollama_data = response.json()
    return {
                "message" : ollama_data["response"]
            }



@app.post("/api/llm")
def generate(request: LLMRequest):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model":"qwen3:1.7b",
                "prompt" : request.prompt,
                "stream":False
            }
        )
        response.raise_for_status()

        data = response.json()
        return {
            "response" : data["response"]
        }
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Ollama non è attivo. Avvialo sul tuo computer.")
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=response.status_code, detail=f"Errore di Ollama: {response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore generico: {str(e)}")
    