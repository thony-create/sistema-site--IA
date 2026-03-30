from auth import validar_senha_forte

passwords = [
    "Cognix@123",
    "Cognix123", # missing special
    "cognix@123", # missing uppercase
    "COGNIX@123", # missing lowercase
    "Cognix@abc", # missing number
    "Cxg@1", # too short
]

for p in passwords:
    result = validar_senha_forte(p)
    print(f"Password '{p}': {'VALID' if result else 'INVALID'}")
