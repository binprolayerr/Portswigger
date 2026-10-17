
>This lab contains a SQL injection vulnerability in its stock check feature. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables.
>
>The database contains a `users` table, which contains the usernames and passwords of registered users. To solve the lab, perform a SQL injection attack to retrieve the admin user's credentials, then log in to their account.

Ở bài này ta thử tìm cách đăng nhập vào trang xem có thể có lỗ hỏng bảo mật nào ở phần đăng nhập không.

![](images/Pasted%20image%2020261017211038.png)

Tuy nhiên tác giả đã sử dụng WAF cho bài này để chặn việc bị tiêm SQL.

![](images/Pasted%20image%2020261017211222.png)

Thế nên ta thử tìm một vị trí khác trong trang web xem có phần nào có thể có lỗ hỏng bảo mật không. Thì ở phần check stock của trang web ta nhận thấy phần này xử lí dữ liệu để kiểm tra sản phẩm trong database và dữ liệu được xử lí bằng đoạn mã XML. Ta có thể dự đoán được việc truy vấn kiểm hàng có thể sẽ là:

`SELECT ... FROM products WHERE productID = 1 AND storeID = 1`

![](images/Pasted%20image%2020261017212517.png)

Nhận thấy ngay rằng việc truy vấn như vậy giúp ta hoàn toàn có thể thực hiện một cuộc tấn công SQL Injection. Thế nên ta tìm cách để UNION nó sang bảng users để thực hiện lấy được danh sách tên tài khoản và mật khẩu. Nhưng trước tiên ta cần biết truy vấn sẽ trả kết quả về dạng bao nhiêu cột để ta có thể xuất kết quả của mình theo đúng số cột trả về của truy vấn.

![](images/Pasted%20image%2020261017214241.png)

Nhưng trong lần thử đầu tiên ta phát hiện WAF cũng được áp dụng ở phần check stock trong trang web chứ không chỉ riêng ở phần login. Ta thử tìm cách bypass WAF này trước bằng cách encode nội dung lại để đánh lừa WAF và ta đã bypass thành công.

![](images/Pasted%20image%2020261017214323.png)

![](images/Pasted%20image%2020261017214404.png)

Ở đây sau 2 lần thử thì chúng ta đã xác định được số cột mà truy vấn trả về là 1. Từ đây ta sẽ tiến hành viết payload để lấy được danh sách tài khoản và mật khẩu. Ta có thể thực hiện như sau:

`UNION SELECT username || '~' || password FROM users`

Tiếp theo đó ta decode và để vào phía sau phần storeID. Payload của ta khi truyền vào được truy vấn sẽ có dạng như thế này:

`SELECT ... FROM products WHERE productID = 1 AND storeID = 1 UNION SELECT username || '~' || password FROM users`

Nó hoàn toàn xuất đúng 1 cột hợp lệ vì || trong SQL sẽ là dấu nối chuỗi giúp ta nối 2 cột độc lập thành 1 chuỗi duy nhất và xuất ra 1 cột duy nhất.

![](images/Pasted%20image%2020261017215150.png)

Lúc này ta đã thu được toàn bộ danh sách người dùng kèm với mật khẩu của họ. Ta tiến hành đăng nhập vào tài khoản của administrator.

![](images/Pasted%20image%2020261017215231.png)

Lúc này ta đã hoàn thành việc đăng nhập vào tài khoản của administrator do việc sử dụng WAF chưa đủ mạnh để loại bỏ việc có thể bị tấn công SQL Injection và lộ toàn bộ thông tin.

![](images/Pasted%20image%2020261017215312.png)









