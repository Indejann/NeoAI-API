from flask import Flask, request, jsonify
import json, time, base64, binascii
from curl_cffi import requests as curl_requests

BASE_URL = "https://ai-server.neobrowser.ai/api"

def sign_payload(payload):
    crc = binascii.crc32(payload.encode("utf-8")) & 0xFFFFFFFF
    return base64.b64encode(f"{crc}YESANDNO{int(time.time())}".encode("utf-8")).decode("utf-8")

def parse_response(text):
    content = []
    for line in text.strip().split("\n"):
        try:
            data = json.loads(line.strip())
        except (json.JSONDecodeError, ValueError):
            continue
        if "text" in data and data.get("type") != 6:
            t = data["text"]
            if t and t.strip():
                content.append(t)
    return "".join(content).strip()

def send_message(message, model=None):
    payload = {"messages": [{"role": "user", "content": message}], "attachments": [], "contents": []}
    if model:
        payload["model"] = model
    body = json.dumps(payload, ensure_ascii=False)
    r = curl_requests.post(
        f"{BASE_URL}/chat",
        impersonate="chrome136",
        headers={"content-type": "application/json", "x-neo-signature": sign_payload(body)},
        data=body,
    )
    return parse_response(r.text)

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get('message', '').strip()
    if not msg:
        return jsonify({"error": "message is empty"}), 400
    return jsonify({"response": send_message(msg, data.get('model'))})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
