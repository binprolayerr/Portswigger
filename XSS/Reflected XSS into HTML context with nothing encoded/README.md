> This lab contains a simple reflected cross-site scripting vulnerability in the search functionality.
> 
> To solve the lab, perform a cross-site scripting attack that calls the `alert` function.

Ở bài này yêu cầu của ta là chèn một thông báo ra màn hình bằng việc thực hiện tấn công XSS qua hàm search. Đầu tiên ta thử search xem phản hồi của trang web sẽ dạng như thế nào.

![](images/Pasted%20image%2020261123232625.png)

Ở đây ta có thể thấy khi ta search trên thanh tìm kiếm thì nó sẽ thực hiện lệnh phía sau biến search trên url. Nếu đúng theo dự đoán thì code sẽ thực hiện in ra bằng html thế nên nếu ta chèn 1 đoạn mã javascript và ép chương trình thực hiện vẫn hoàn toàn có thể tạo nên một cuộc tấn công XSS. Viết đoạn script để in thông báo như sau:

`<script>alert(1)</script>`

Sau đó ta bỏ nó vào tham số search trên url để truy vấn và khiến chương trình thực hiện và trả phản hồi ngay trên trang của client.

![](images/Pasted%20image%2020261123232657.png)

Vậy là ta đã có thể nhận thành công thông báo.

![](images/Pasted%20image%2020261123232809.png)

Bởi vì không có bất cứ cơ chế lọc đầu vào nào của hàm search nên dễ dàng dẫn đến một cuộc tấn công XSS hay thậm chí đây chỉ là cách attacker xác định lỗi và họ sẽ có thể khai thác sâu hơn vào thông tin người dùng và phân quyền mà một người dùng bị lợi dụng có thể bị khai thác.
