> This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.
> 
> The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.
> 
> To solve the lab, log in as the `administrator` user.

Ở bài này nhiệm vụ của chúng ta là cần phải tìm kiếm được password và mật khẩu của administrator để đăng nhập vào. Đầu tiên ta cần quét để tìm vị trí lỗ hỏng và lỗi có thể chèn vào.

![](images/Pasted%20image%2020261107161000.png)

![](images/Pasted%20image%2020261107161033.png)

Ở đây chúng ta đã xác định được vị trí lỗ hỏng nằm ở việc có thể bị chèn trong truy vấn sản phẩm. Ở đây ta có thể chèn truy vấn UNION để khai thác lỗi **UNION query**. Chúng ta cũng đã biết được là bảng trả về kết quả với 2 cột. Ở đây đầu tiên ta cần biết trong cơ sở dữ liệu có các bảng nào để xem bảng nào có khả năng lưu trữ thông tin người dùng và tấn công vào. Vì đây sử dụng DBMS là PostgreSQL chứ không phải Oracle nên ta có thể viết truy vấn tất cả các bảng của database như sau:

```sql
' UNION SELECT table_name, NULL FROM information_schema.tables--
```

![](images/Pasted%20image%2020261107170255.png)

Ở đây mình thấy một bảng có tên **users_dysowp** khả nghi sẽ chứa dữ liệu của người dùng nên ta sẽ tiến hành truy vấn thử xem bảng này có những cột nào: 

```sql
' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = 'users_dysowp'--
```

![](images/Pasted%20image%2020261107170422.png)

Lúc này chúng ta xác định được 2 cột ta có thể truy vấn để lấy tài khoản administrator nằm ở **username_dondgj** và **password_jlfzmp**. Lúc này ta tiến hành xuất kết quả từ các cột để lấy được tài khoản:

```sql
' UNION SELECT username_dondgj, password_jlfzmp FROM users_dysowp--
```

![](images/Pasted%20image%2020261107170518.png)

Ở đây ta đã có được tài khoản của administrator và ta sẽ đăng nhập vào để hoàn tất.

![](images/Pasted%20image%2020261107170545.png)

Như vậy là ta đã có thể đăng nhập được vào tài khoản administrator qua việc chèn SQL vào cơ sở dữ liệu để lấy được bảng tài khoản mật khẩu của tất cả users. Đây là một lỗ hỏng vô cùng nghiêm trọng vì chỉ cần có tài khoản của admin thì sẽ dẫn đến lộ toàn bộ thông tin của hệ thống đã phân quyền.
