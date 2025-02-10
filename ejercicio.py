from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

# Endpoint GET
@app.get("/get")
def get_value():
    return "BircleAI"

# Endpoint POST
@app.post("/post")
async def post_external_api():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.publicapis.org/entries")
            response.raise_for_status()  # Raise an exception for HTTP errors
            response_data = response.json()
            print(response_data)  # Log the response to the console
            return response_data
    except httpx.HTTPStatusError as exc:
        print(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)

# Endpoint UPDATE
class Number(BaseModel):
    value: int

@app.put("/update")
def update_number(number: Number):
    squared_value = number.value ** 2
    return {"squared_value": squared_value}