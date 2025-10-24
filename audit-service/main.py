from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Audit Service")
events = []

class Event(BaseModel):
    action: str
    length: int | None = None

@app.post("/event")
def add_event(ev: Event):
    doc = {"ts": datetime.utcnow().isoformat() + "Z", **ev.model_dump()}
    events.append(doc)
    if len(events) > 1000:
        events.pop(0)
    return {"status": "ok"}

@app.get("/history")
def history():
    return {"count": len(events), "events": events[-100:]}