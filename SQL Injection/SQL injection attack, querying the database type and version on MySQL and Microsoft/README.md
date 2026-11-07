> This lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.
> 
> To solve the lab, display the database version string.

Ở bài này ta cũng được yêu cầu làm sao để xuất ra được phiên bản của DBMS đang sử dụng. Trước tiên ta sẽ tiến hành quét để xác định các lỗi có thể xảy ra cũng như là vị trí lỗ hỏng có thể bị chèn và DBMS đang được sử dụng là gì.

![](images/Pasted%20image%2020261107150833.png)

![](images/Pasted%20image%2020261107150902.png)

Ở đây chúng ta nhận được kết quả là DBMS đang sử dụng là MySQL và lỗi mà mình có thể tận dụng để có thể chèn được SQL vào để xuất phiên bản sẽ nằm ở lỗi **UNION query**. Theo ta thấy thì ở đây ta cần chèn NULL ở cột đầu tiên và định dạng string nằm ở cột thứ 2 để mình có thể xuất phiên bản ở cột này. Bây giờ ta sẽ tiến hành viết payload đặc trưng dành cho DBMS là MySQL.

```
UNION SELECT NULL, @@version-- -
```

Giải thích cho việc ta cần thêm - ở cuối. Do đặc trưng của MySQL khi comment cần phải đúng cấu trúc -- *comment* thì cần đảm bảo có khoảng trắng nhưng khi mình đặt lên url có thể sẽ bị lọc bỏ khoảng trắng cuối chuỗi. Thế nên ta cần thêm - để giữ lại được khoảng trắng đảm bảo cấu trúc comment trong MySQL. 

![](images/Pasted%20image%2020261107151634.png)

![](images/Pasted%20image%2020261107151647.png)

Và như thế là mình đã có thể xuất ra được phiên bản của DBMS là **MySQL 8.0.42** và được đóng gói bằng **ubuntu 20.04.1**.
