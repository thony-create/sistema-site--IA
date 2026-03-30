import urllib.request
from urllib.error import HTTPError

try:
    print("Testing dashboard redirect...")
    # Attempting to access protected route
    req = urllib.request.Request('http://127.0.0.1:5000/dashboard', method='GET')
    # Prevent automatic redirect handling to see the 302
    class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    opener = urllib.request.build_opener(NoRedirectHandler)
    res = opener.open(req)
    
    print(f"Status: {res.status}")
except HTTPError as e:
    print(f"Status Code: {e.code}")
    print(f"Location: {e.headers.get('Location')}")
    if e.code == 302 and 'login' in e.headers.get('Location', ''):
        print("SUCCESS! Redirect works properly without NameError.")
    else:
        print("FAILED or unexpected result.")
except Exception as e:
    print(f"Connection Error: {e}")
