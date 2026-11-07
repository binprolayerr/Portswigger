> This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.
> 
> The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.
> 
> To solve the lab, log in as the `administrator` user.

Ở bài này nhiệm vụ của ta cũng cần phải làm sao để đăng nhập được vào tài khoản administrator. Đầu tiên ta cần tiếp cận với các lỗ hổng SQL ta cần quét xem có thể có lỗ hổng ở vị trí nào, lỗi gì và đánh giá tiếp cận như nào.

![](images/Pasted%20image%2020261107180537.png)

![](images/Pasted%20image%2020261107180607.png)

Sau khi quét ta được báo cáo như sau. Ở đây ta thấy lỗ hổng vẫn nằm ở phần truy vấn vào cơ sở dữ liệu để lấy thông tin sản phẩm. Ta hoàn toàn có thể ép xuất nội dung tài khoản nằm trong cơ sở dữ liệu thông qua việc tận dụng truy vấn UNION với lỗi là hệ thống chấp nhận **UNION query**. Đầu tiên ta cần xuất tất cả các bảng có trong cơ sở dữ liệu để xem đâu là mục tiêu của mình sẽ tấn công. Vì ở đây sử dụng DBMS là Oracle và bảng xuất ra 2 cột nên ta sẽ viết truy vấn chèn như sau:

```sql
' UNION SELECT table_name, NULL FROM all_tables--
```

![](images/Pasted%20image%2020261107180736.png)

Ở đây ta có một tên bảng nghi ngờ sẽ là bảng chứa dữ liệu người dùng là **USERS_KGFFCZ** thế nên ta sẽ xem trong bảng này có những cột nào với câu lệnh truy vấn như sau:

```sql
' UNION SELECT column_name, NULL FROM all_tab_columns WHERE table_name = 'USERS_KGFFCZ'--
```

![](images/Pasted%20image%2020261107181107.png)

Lúc này mình đã xác định được 2 cột chứa thông tin tài khoản và mật khẩu là **USERNAME_TRCRFW** và **PASSWORD_ICIJQR**. Vì vậy ta sẽ tiến hành xuất nội dung trong cột ra để lấy được tài khoản:

```sql
' UNION SELECT USERNAME_TRCRFW, PASSWORD_ICIJQR FROM USERS_KGFFCZ--
```

![](images/Pasted%20image%2020261107181209.png)

Ở đây ta đã có được thông tin tài khoản và mật khẩu của toàn bộ users ta sẽ lấy và tiến hành đăng nhập vào administrator.

![](images/Pasted%20image%2020261107181233.png)

Vậy là ta đã thành công tiếp cận và đăng nhập được vào tài khoản admin với DBMS là Oracle.
