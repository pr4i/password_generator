from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, random, string, httpx, math
from fastapi.middleware.cors import CORSMiddleware

POLICY_URL = os.getenv("POLICY_URL", "http://policy-service:5001")
AUDIT_URL = os.getenv("AUDIT_URL", "http://audit-service:5002")

app = FastAPI(title="Password Generator API")

# --- Добавляем CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно заменить "*" на ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenParams(BaseModel):
    length: int = 12
    use_lower: bool = True
    use_upper: bool = True
    use_digits: bool = True
    use_symbols: bool = True

def _alphabet(params: GenParams):
    alphabet = ""
    if params.use_lower:
        alphabet += string.ascii_lowercase
    if params.use_upper:
        alphabet += string.ascii_uppercase
    if params.use_digits:
        alphabet += string.digits
    if params.use_symbols:
        alphabet += "!@#$%^&*()-_=+[]{};:,.?/"
    if not alphabet:
        alphabet = string.ascii_letters + string.digits
    return alphabet

@app.post("/generate")
async def generate(params: GenParams):
    alphabet = _alphabet(params)
    pwd = "".join(random.choice(alphabet) for _ in range(params.length))

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            # ask policy-service for score/entropy
            pol = await client.post(f"{POLICY_URL}/check", json={"password": pwd})
            pol.raise_for_status()
            policy = pol.json()
        except Exception as e:
            policy = {"score": None, "entropy_bits": None, "message": f"policy error: {e}"}

        try:
            # send audit event
            await client.post(f"{AUDIT_URL}/event", json={"action": "generated", "length": params.length})
        except Exception as e:
            pass

    return {"password": pwd, "policy": policy}

@app.get("/history")
async def history():
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            r = await client.get(f"{AUDIT_URL}/history")
            r.raise_for_status()
            return r.json()
        except Exception as e:
            raise HTTPException(502, f"audit error: {e}")