# NeoAI-API
A reverse engineed wrapper for [neobrowser's](https://neobrowser.ai/) AI

# Info
Their signature is just a crc32 hashed version of the payload you're sending + an hardcoded delimiter + the current UNIX timestamp
lol

# Example usage

```python
import requests

response = requests.post('http://localhost:5001/api/chat', json={
    'message': 'Hello :)',
})
print(response.json())
```
https://ai.kzip.org/
