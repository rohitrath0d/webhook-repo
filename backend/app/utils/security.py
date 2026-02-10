import hmac
import hashlib
import os
from flask import request

WEBHOOK_SECRET=os.getenv("WEBHOOK_SECRET")

def verify_github_signature(req: request) -> bool:
  header_signature = req.headers.get("X-Hub-Signature-256")
  
  if header_signature is None:
    return False
  
  payload =  req.data 
  computed_hmac = hmac.new(
    WEBHOOK_SECRET.encode(),
    msg=payload,
    digestmod=hashlib.sha256
  ).hexdigest()
  
  return hmac.compare_digest(f"sha256={computed_hmac}, header_signature")