from fastapi import FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime
import os

# ✅ Import our local AI engine
from local_ai import local_ai_generate

app = FastAPI()

API_KEY = os.getenv("AI_AGENT_KEY", "12345-abcde-67890")
sessions: Dict[str, Dict] = {}
transcripts: Dict[str, List[Dict]] = {}

api_key_header = APIKeyHeader(name="Authorization")

def auth_check(header: str):
    token = header
    if header.startswith("Bearer "):
        token = header.split(" ", 1)[1]
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

class InteractRequest(BaseModel):
    record_id: str
    inquiry_text: str
    metadata: Optional[Dict] = {}

class InteractResponse(BaseModel):
    record_id: str
    action: str
    response_text: str
    status_marker: str
    transaction_state: str
    escalation_flag: bool = False

class HandoverRequest(BaseModel):
    record_id: str
    reason: str
    last_message: str

class HandoverResponse(BaseModel):
    record_id: str
    action: str
    assigned_to: str
    status_marker: str

def init_session(record_id, metadata):
    if record_id not in sessions:
        sessions[record_id] = {
            "status_marker": "clarifying",
            "transaction_state": "pending",
            "metadata": metadata
        }
        transcripts[record_id] = []

@app.post("/interact", response_model=InteractResponse)
def interact(req: InteractRequest, header: str = Security(api_key_header)):
    auth_check(header)
    rid = req.record_id
    init_session(rid, req.metadata or {})
    transcripts[rid].append({"role": "user", "text": req.inquiry_text, "time": datetime.utcnow().isoformat()})

    session = sessions[rid]
    status, txn = session["status_marker"], session["transaction_state"]

    escalate = False
    text = req.inquiry_text.lower()

    # ✅ Use local AI engine for response generation
    if status == "clarifying":
        response, escalate = local_ai_generate(transcripts[rid], req.inquiry_text)
        status = "handover" if escalate else "awaiting_confirmation"

    elif status == "awaiting_confirmation" and "confirm" in text:
        txn, status, escalate = "confirmed", "confirmed", True
        response = "Acknowledged. Escalating to a human operator for action."

    else:
        response = "Please clarify what you mean."

    session["status_marker"], session["transaction_state"] = status, txn
    transcripts[rid].append({"role": "agent", "text": response, "time": datetime.utcnow().isoformat()})

    return InteractResponse(
        record_id=rid,
        action="escalate" if escalate else "respond",
        response_text=response,
        status_marker=status,
        transaction_state=txn,
        escalation_flag=escalate
    )

@app.post("/handover", response_model=HandoverResponse)
def handover(req: HandoverRequest, header: str = Security(api_key_header)):
    auth_check(header)
    rid = req.record_id
    if rid not in transcripts:
        raise HTTPException(status_code=404, detail="Record not found")

    sessions[rid]["status_marker"] = "handover"
    print(f"[HANDOVER] {rid} -> {req.reason}\nTranscript:", transcripts[rid])

    return HandoverResponse(
        record_id=rid,
        action="escalate",
        assigned_to="VA_operator",
        status_marker="handover"
    )

@app.get("/")
def root():
    return {"status": "ok", "message": "AI-Agent is running with local AI engine. Go to /docs to test."}