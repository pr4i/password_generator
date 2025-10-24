from fastapi import FastAPI
from pydantic import BaseModel
import math

app = FastAPI(title="Policy Service")

class Payload(BaseModel):
    password: str

def estimate_entropy_bits(pwd: str) -> float:
    # rough estimator by character class size
    charset = 0
    lowers = any(c.islower() for c in pwd)
    uppers = any(c.isupper() for c in pwd)
    digits = any(c.isdigit() for c in pwd)
    symbols = any(not c.isalnum() for c in pwd)
    if lowers: charset += 26
    if uppers: charset += 26
    if digits: charset += 10
    if symbols: charset += 33  # approx common symbols
    charset = max(charset, 26)
    return len(pwd) * math.log2(charset)

@app.post("/check")
def check(p: Payload):
    ent = estimate_entropy_bits(p.password)
    # score 0..4 похожий на zxcvbn-подобную шкалу
    if ent < 28:
        score = 0
    elif ent < 36:
        score = 1
    elif ent < 60:
        score = 2
    elif ent < 128:
        score = 3
    else:
        score = 4
    return {"entropy_bits": round(ent, 2), "score": score, "message": "ok"}