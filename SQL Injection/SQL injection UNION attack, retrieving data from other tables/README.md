
>This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you need to combine some of the techniques you learned in previous labs.
>
>The database contains a different table called `users`, with columns called `username` and `password`.
>
>To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the `administrator` user.

Ở bài này nhiệm vụ của ta là phải xuất dữ liệu được từ một bảng khác bảng đang được truy vấn đến. Với yêu cầu của đề bài là xuất ra được username và password từ bảng users. Trước tiên ta cũng cần phải kiểm tra xem truy vấn sẽ trả về số cột là bao nhiêu trước khi tiến hành viết lệnh để xuất được từ bảng users.

![](images/Pasted%20image%2020261018223543.png)

Thì ở đây ta đã xác định được số cột được truy vấn trả về là 2 cột và từ đây ta có thể viết mã để xuất dữ liệu từ 2 cột là username và password mà không cần điều chỉnh gì. Để xuất được dữ liệu cần thiết ta có thể viết mã như sau:

`UNION SELECT username,password FROM users`

![](images/Pasted%20image%2020261018223725.png)

Và như vậy ta đã có thể xuất được toàn bộ tài khoản và mật khẩu của danh sách users ra repsone và ta sẽ lấy mật khẩu của administrator để đăng nhập vào.

![](images/Pasted%20image%2020261018223800.png)

Vậy là chúng ta đã thành công sử dụng tiêm SQL để có thể truy xuất dữ liệu từ bảng khác bảng truy vấn và khai thác thành công lỗ hỏng để lộ thông tin và có thể sử dụng để đăng nhập vào tài khoản administrator.

![](images/Pasted%20image%2020261018223817.png)






