
>This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you first need to determine the number of columns returned by the query. You can do this using a technique you learned in a [previous lab](https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns). The next step is to identify a column that is compatible with string data.
>
>The lab will provide a random value that you need to make appear within the query results. To solve the lab, perform a SQL injection UNION attack that returns an additional row containing the value provided. This technique helps you determine which columns are compatible with string data.

Ở bài này nhiệm vụ của ta là xác định số cột của truy vấn trả về và chèn dữ liệu string để xem cột nào được định dạng string và có thể chèn vào được. Đầu tiên ta nhìn cấu trúc request và đoán được dạng câu truy vấn SQL là:

`SELECT * FROM products WHERE category = 'Pets'`

![](images/Pasted%20image%2020261018143016.png)

Ở đây để xác định số cột thì đầu tiên ta cần chèn `UNION SELECT NULL` vào và tăng dần số cột nếu server còn báo lỗi cho đến khi không còn bị báo lỗi thì ta sẽ xác định được đúng sô slượng cột. Như ở đây mình đã xác định được số lượng cột truy vấn trả về là 3 do `UNION SELECT NULL,NULL,NULL` của mình đã hợp lệ. Khi ta chèn như vậy truy vấn SQL ban đầu sẽ trở thành:

`SELECT * FROM products WHERE category = 'Pets' UNION SELECT NULL,NULL,NULL --`

![](images/Pasted%20image%2020261018143142.png)

Nhưng đề bài còn yêu cầu ta cần phải xác định được cột có định dạng dữ liệu là string và chèn đoạn ký tự ngẫu nhiên được trang web cung cấp ta cần chèn được đoạn đó vào bảng và xuất ra. Vì vậy đầu tiên ta cần dò các cột xem cột nào có định dạng dữ liệu là string. Với 3 cột ta thực hiện 3 lần như sau:

`UNION SELECT '(random data)', NULL, NULL`

`UNION SELECT NULL, '(random data)', NULL`

`UNION SELECT NULL, NULL, '(random data)'`

Tương ứng với kiểm tra cột 1, 2, 3 có tương ứng với dữ liệu string không. Và ta xác định được ở cột 2 kiểu dữ liệu là string.

![](images/Pasted%20image%2020261018143643.png)

Vì vậy sau khi ta chèn được đoạn dữ liệu vào thì ta sẽ thu được bảng truy vấn cuối cùng có dạng như sau:

![](images/Pasted%20image%2020261018144748.png)









