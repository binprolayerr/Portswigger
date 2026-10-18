
>This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.
>
>The database contains a different table called `users`, with columns called `username` and `password`.
>
>To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the `administrator` user.

Ở bài này đề bài yêu cầu ta phải xuất được danh sách username và password để lấy tìa khoản và đăng nhâp được vào adminstrator. Đầu tiên để có thể truy xuất được danh sách cần thiết ta cần phải biết số lượng cột mà truy vấn trả về.

![](images/Pasted%20image%2020261018230951.png)

Lúc này ta đã xác định được số lượng cột của truy vấn trả về là 2. Thế nên điều tiếp theo ta cần làm là kiểm tra xem các cột này có đúng định dạng của kiểu dữ liệu mà ta cần nó xuất ra và trả về là string chưa. Ta lần lượt kiểm thử ở 2 cột như sau:

`UNION SELECT 'a',NULL`

`UNION SELECT NULL,'a'`

![](images/Pasted%20image%2020261018231115.png)
![](images/Pasted%20image%2020261018231032.png)

Sau khi đã kiểm tra thử ở 2 cột thì ta xác định được chỉ có 1 cột có kiểu dữ liệu là string. Lúc này vấn đề của ta cần giải quyết là làm sao để xuất được dữ liệu của 2 cột là username và password vào cùng 1 cột. Ta sẽ sử dụng phép nối chuỗi và xem nội dung của từng dòng trong các cột là 1 chuỗi và ta sẽ nối nó lại 1 chuỗi ký tự để có thể xuất ra đúng định dạng dữ liệu là string. Ta thực hiện như sau:

`UNION SELECT NULL,username||'~'||password FROM users`

Với || là lệnh nối chuỗi trong Oracle và ta thêm 1 chuỗi nữa là '~' để đảm bảo có thể phân biệt được đâu là username và đâu là mật khẩu. Nhưng đừng quên vẫn phải có NULL ở cột đầu để đảm bảo số cột ta truy vấn bằng với số cột mà truy vấn sẽ trả lại cho chúng ta. Sau đó ta nối chúng lại và nhận được kết quả xuất ra respone.

![](images/Pasted%20image%2020261018231346.png)

Ở đây ta đã thu được tài khoản và mật khẩu của tất cả users. Tiếp đến ta sẽ tiến hành đăng nhập vào tài khoản administrator.

![](images/Pasted%20image%2020261018231429.png)

Vậy là chúng ta đã hoàn tất đăng nhập được vào tài khoản của administrator từ một lỗ hỏng có thể tiêm được SQL. Mặc dù chỉ có 1 cột có kiểu dữ liệu là string để ta xuất ra nhưng nếu ta muốn xuất nhiều cột vào thành đúng 1 cột ta hoàn toàn có thể sử dụng phép nối chuỗi trong từng loại hình database.

![](images/Pasted%20image%2020261018231451.png)
