> This lab contains a DOM-based cross-site scripting vulnerability in the stock checker functionality. It uses the JavaScript `document.write` function, which writes data out to the page. The `document.write` function is called with data from `location.search` which you can control using the website URL. The data is enclosed within a select element.
> 
> To solve this lab, perform a cross-site scripting attack that breaks out of the select element and calls the `alert` function.

Ở bài này thì cách tiếp cận của ta tương tự lab trước nhưng có một điểm khác là nó sẽ không còn hiện respone trả về như hàm search lần trước. Trong lab này vị trí có lỗ hỏng nằm ở các tham số của dữ liệu ở hàm select và vị trí được chọn để check. Đầu tiên ta cần đọc source code của chương trình để xác định rõ hành vi cần phải làm là gì. 

![](images/Pasted%20image%2020261124233750.png)

Thì ở đây chúng ta có thể xác định được 1 cái luồng hoạt động của đoạn code có vài thao tác xử lý thừa dẫn đến lỗ hỏng như sau. Đầu tiên script sẽ lấy storeID về từ url thông qua hàm `location.search`. Từ đây ta đã có thể xác định hướng tiếp cận đầu tiên mình cần phải làm là chèn thêm 1 giá trị storeId vào url. Tiếp theo ta cần xem giá trị đó sẽ được xử lý như thế nào. Ở đây sau khi lấy xuống từ url thì script lại tạo thêm 1 vị trí lưu trữ khác vào thông qua `document.write` ghi toàn bộ xuống vào một hàm `<option selected>` nữa. Lúc này ta đã có thể xác định chính xác vị trí tấn công với việc thêm vào là vô cùng dư thừa và không hề có bất kỳ cơ chế lọc nào mà nhét thẳng vào `<option selected>`. Bây giờ ta thử chèn một giá trị vào tham số storeId thử xem nó sẽ được xử lý và lưu trữ như thế nào trên hệ thống.

![](images/Pasted%20image%2020261124234337.png)

Rõ ràng khi thêm vào thì ta đã thấy nó hiện như một phương án lựa chọn nữa trên chính trang web. Ở đây ta có thể viết lệnh JavaScript để nó có thể tấn công rồi:

`<img src=1 onerror=alert(1)>`

Vì lệnh được chèn vào một thẻ khác mà không hề lọc nó hoàn toàn chạy tốt.

![](images/Pasted%20image%2020261124234621.png)

Và như vậy là ta đã có thể in ra thông báo thông qua việc tấn công DOM XSS bởi một hàm xử lý thừa trong hệ thống và có thể dễ dàng được khai thác thông qua chèn 1 lệnh vào 1 thẻ khác để thao túng DOM dẫn đến DOM XSS.
