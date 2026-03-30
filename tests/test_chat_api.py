import requests
import json

# Test the chat API with proper session handling
BASE_URL = 'http://localhost:5000'

# Start a session to maintain cookies
session = requests.Session()

print("Testing Chat API...")

# First, try to access chat without login (should fail)
print("\n1. Testing chat without login:")
try:
    response = session.post(f'{BASE_URL}/chat/api/enviar', json={'pergunta': 'Quanto vendi hoje?'})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Try to login
print("\n2. Testing login:")
try:
    # Get the login page first to get any CSRF token if needed
    login_page = session.get(f'{BASE_URL}/login')
    print(f"Login page status: {login_page.status_code}")

    # Try to login with test user
    login_data = {
        'email': 'teste@exemplo.com',
        'senha': '123456'  # Assuming default password
    }

    login_response = session.post(f'{BASE_URL}/login', data=login_data, allow_redirects=True)
    print(f"Login response status: {login_response.status_code}")
    print(f"Login response URL: {login_response.url}")

    # Check if we're redirected to dashboard (success) or back to login (failure)
    if 'dashboard' in login_response.url:
        print("Login successful!")
    else:
        print("Login failed - trying admin user")
        # Try admin user
        login_data = {
            'email': 'admin@teste.com',
            'senha': 'admin123'
        }
        login_response = session.post(f'{BASE_URL}/login', data=login_data, allow_redirects=True)
        print(f"Admin login response status: {login_response.status_code}")
        print(f"Admin login response URL: {login_response.url}")

except Exception as e:
    print(f"Login error: {e}")

# Now try the chat API with session
print("\n3. Testing chat API with session:")
try:
    response = session.post(f'{BASE_URL}/chat/api/enviar',
                          json={'pergunta': 'Quanto vendi hoje?'},
                          headers={'Content-Type': 'application/json'})
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Response: {data}")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Test suggestions
print("\n4. Testing suggestions API:")
try:
    response = session.get(f'{BASE_URL}/chat/api/sugestoes')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Suggestions: {len(data.get('sugestoes', []))} items")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")