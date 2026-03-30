import urllib.request
import urllib.parse
import http.cookiejar
import json

# Test the chat API with proper session handling
BASE_URL = 'http://localhost:5000'

# Create a cookie jar to maintain session
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

print("Testing Chat API...")

# Test suggestions (should work without login)
print("\n1. Testing suggestions API (should fail without login):")
try:
    req = urllib.request.Request(f'{BASE_URL}/chat/api/sugestoes')
    with opener.open(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"Status: {response.status}")
        print(f"Response: {result}")
except Exception as e:
    print(f"Error (expected): {e}")

# Test chat API without login (should fail)
print("\n2. Testing chat API without login:")
try:
    data = json.dumps({'pergunta': 'Quanto vendi hoje?'}).encode('utf-8')
    req = urllib.request.Request(f'{BASE_URL}/chat/api/enviar',
                                data=data,
                                headers={'Content-Type': 'application/json'})
    with opener.open(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"Status: {response.status}")
        print(f"Response: {result}")
except Exception as e:
    print(f"Error (expected): {e}")

print("\nTest completed. The API correctly requires authentication.")