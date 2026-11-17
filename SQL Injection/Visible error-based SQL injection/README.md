>This lab contains a SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie. The results of the SQL query are not returned.
>
>The database contains a different table called `users`, with columns called `username` and `password`. To solve the lab, find a way to leak the password for the `administrator` user, then log in to their account.

Ở bài này ta sẽ tấn công mù bằng cách nhìn cách server báo lỗi khái niệm ở các định dạng đầu vào của ta. Đầu tiên ta thử xem request server sẽ trông như thế nào và xác định vị trí có thể tấn công.

![](images/Pasted%20image%2020261117103655.png)

Ở đây ta có thể thấy vị trí tấn công sẽ là TrackingID nơi server sẽ truy vấn vào database để check và từ đó ta có thể khai thác và tấn công vào vị trí này. Trước tiên ta cần kiểm tra thử nó sẽ trả về như thế nào nếu đầu vào của chúng ta lỗi định dạng. Ta thử với câu lệnh như sau:

`CAST('x' AS INT)`

Server trả về là 'ERROR: invalid input syntax for type integer: "x"'. Ở đây ta thấy nội dung mà ta bỏ vào bị lỗi đó là x hiển thị trong truy vấn hoàn toàn.

![](images/Pasted%20image%2020261117105127.png)

Vì thế nên ta sẽ thử với câu lệnh SELECT trong CAST để có thể xuất bị trí admin xem sao. Thì khi ta để nguyên TrackingID và lệnh SELECT trong CAST sau AND thì server báo là lệnh AND cần phải là câu lệnh boolean và rõ ràng server cũng giới hạn ký tự khiến câu lệnh bị thực hiện thiếu. Thế nên ta sẽ bỏ luôn phần TrackingID gốc và chỉ viết phần payload để kiểm tra vị trí đầu tiên trong cột username của bảng users là gì như sau:

`1=CAST(SELECT username FROM users LIMIT 1 AS INT)`

![](images/Pasted%20image%2020261117111116.png)

Lúc này ta thấy được vị trí đầu tiên trong cột username đó chính xác là administrator và bị server làm lộ hoàn toàn qua việc truy vấn của người dùng. Thế nên tiếp theo ta sẽ tiến hành tìm mật khẩu bằng cách viết payload tương tự như dò vị trí của username chỉ khác là đổi username thành cột password như sau:

`1=CAST(SELECT password FROM users LIMIT 1 AS INT)`

![](images/Pasted%20image%2020261117111019.png)

Và như vậy là ta đã có thể lấy được mật khẩu của administrator từ đây ta sẽ tiến hành đăng nhập vào.

![](images/Pasted%20image%2020261117111243.png)

Cuối cùng ta đã có thể đăng nhập bằng cách dò mật khẩu và tài khoản một cách đơn giản thông qua sơ suất cơ bản trong việc tạo dựng backend khi không hề có cơ chế lọc và khiến server khi lỗi định dạng sẽ liền trả toàn bộ nội dung của truy vấn người dùng lên màn hình dẫn đến việc có thể khai thác dễ dàng tài khoản và mở ra cánh cửa vào trong cơ sở dữ liệu dành cho attacker.
