# AI-Agent – Adaptive Interaction Service

Standalone containerized microservice exposing REST API for multi-step guided interactions.

## Local Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 4000
```

Then open http://127.0.0.1:4000/docs

## Docker Setup

```bash
docker-compose up --build
```

## Environment Variables

| Variable | Default | Purpose |
|---------|---------|---------|
| AI_AGENT_KEY | 12345-abcde-67890 | API key for auth |
| PORT | 4000 | Service port |
| LOG_LEVEL | debug | Log verbosity |

## Sample Request

```json
POST /interact
Authorization: Bearer 12345-abcde-67890
{
  "record_id": "12345",
  "inquiry_text": "Can you finish this by Friday?",
  "metadata": { "priority": "high" }
}
```

## Sample Response

```json
{
  "record_id": "12345",
  "action": "respond",
  "response_text": "Yes, we can schedule this for Friday. Would you like me to confirm?",
  "status_marker": "awaiting_confirmation",
  "transaction_state": "pending",
  "escalation_flag": false
}
```
