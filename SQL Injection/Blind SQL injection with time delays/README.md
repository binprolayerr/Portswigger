>This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.
>
>The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.
>
>To solve the lab, exploit the SQL injection vulnerability to cause a 10 second delay.

Ở lab này yêu cầu của ta đó là làm cho server trả về respone sau 10 giây bị delay để có thể thấy được lỗi khai thác mù SQL bằng thời gian delay.

Đầu tiên ta cần thử xem sử dụng lệnh của Microsoft xem nó có đúng DBMS mà server đang sử dụng hay không.

![](images/Pasted%20image%2020261120222711.png)

Sau khi thử thì không phải server sử dụng DBMS này nên ta thử chuyển sang PostgreSQL thì đúng là server sử dụng DBMS là PostgreSQL. 

![](images/Pasted%20image%2020261120222641.png)

Vậy là ta đã có thể khai thác thành công việc khiến server sẽ bị delay thời gian sau 10s nếu điều kiện đúng.

![](images/Pasted%20image%2020261120222653.png)

Chỉ cần sơ suất để có thể xảy ra lỗi delay time là một báo hiệu giúp mình có thể khai thác được nhiều thứ phía sau.
