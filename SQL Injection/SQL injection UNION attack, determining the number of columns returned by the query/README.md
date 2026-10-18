
>This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. The first step of such an attack is to determine the number of columns that are being returned by the query. You will then use this technique in subsequent labs to construct the full attack.
>
>To solve the lab, determine the number of columns returned by the query by performing a SQL injection UNION attack that returns an additional row containing null values.

Ở bài này nhiệm vụ của ta sẽ là xác định số cột của truy vấn trả về. Ở bước đầu tiên ta cần xác định vị trí truy cập database có thể bị SQL Injection. Thì ở trang này ta thấy phần truy vấn url sẽ tìm kiếm trong database để trả về kết quả của category. Ta có thể dự đoán được đoạn mã SQL được viết dạng như sau:

`SELECT * FROM products WHERE category = 'Gifts'`

![](images/Pasted%20image%2020261018135738.png)

Lúc này để kiểm tra số lượng cột trả về trong truy vấn ta sẽ sử dụng lệnh kiểm tra NULL như sau:

`UNION SELECT NULL`

Để xem có đúng số cột đó hay không và nếu server báo lỗi thì ta sẽ tăng số lượng cột để xem chính xác số lượng cột mà server trả về:

![](images/Pasted%20image%2020261018140007.png)

Ở lượt thử 1 cột thì rõ ràng servêr đã báo lỗi vì vậy ta sẽ tiếp tục tăng lên từ từ thành:

`UNION SELECT NULL, NULL`
`UNION SELECT NULL, NULL, NULL`

![](images/Pasted%20image%2020261018140106.png)

Đến đây ta đã hoàn thành và xác định được server này trả truy vấn về với 3 cột.











