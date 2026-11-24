> This lab contains a DOM-based cross-site scripting vulnerability in the search query tracking functionality. It uses the JavaScript `document.write` function, which writes data out to the page. The `document.write` function is called with data from `location.search`, which you can control using the website URL.
> 
> To solve this lab, perform a cross-site scripting attack that calls the `alert` function.

Ở bài này ta cần khai thác lỗi DOM XSS xuất hiện trên trang web ở hàm truy vấn của thanh tìm kiếm. Đề bài gợi ý rằng việc hàm này sử dụng hàm JavaScript đó chính là `document.write` và để ghi dữ liệu lên trang và hàm `location.search` để lấy dữ liệu tìm kiếm. Mà 2 hàm này chính là những hàm cơ bản điển hình dẫn đến lỗi DOM XSS giúp attacker có thể khai thác dễ dàng mã JavaScript được chèn vào trong HTML. Ta cần phân tích cách hoạt động của 2 hàm này trước. Trước tiên là với `document.write` là một hàm sẽ ghi ra màn hình kết quả nằm trong nó thậm chí đó là một đoạn code JavaScript thì nó vẫn chạy và không hề có bất cứ cơ chế lọc nào khiến cho kết quả đoạn code hiển nhiên nằm trên respone cho người dùng. Còn với `location.search` hàm này sẽ tìm kiếm và lấy dữ liệu từ url về là toàn bộ nội dung nằm sau dấu "?" trên url sẽ được lấy xuống. Từ 2 khả năng trên chúng ta hoàn toàn có thể kết hợp được chức năng của 2 hàm này để thực hiện một cuộc tấn công thao túng DOM. Đó là DOM XSS. Đầu tiên ta cần thử xem khi ta tìm kiếm 1 nội dung nó sẽ trả về điều gì trong đoạn code respone. Ta chọn thử 1 chuỗi mà dài một tí và đoán là sẽ không có trong database để search.

![](images/Pasted%20image%2020261124223537.png)

Sau khi search ta tiến hành xem đoạn code respone xem những nội dung ta nhập vào nó sẽ nằm ở đâu.

![](images/Pasted%20image%2020261124223735.png)

Thì ở đây ta phát hiện có 2 vị trí mà nội dung của mình xuất hiện với cái đầu tiên nó nằm trong 1 thẻ HTML đó chính là thẻ `<h1>` với nội dung là số lượng kết quả tìm kiếm. Ở đây nếu ta khai thác nó có thể là 1 điểm Reflected XSS. Nhưng có hướng tiếp cận thứ 2 đó chính là DOM XSS ở vị trí xuất hiện thứ 2 của chuỗi khi nó nằm trong một thẻ `<img>`. Lúc này ta phân tích luồng hoạt động của đoạn code trang web để nội dung có thể được ghi vào vị trí đó. Theo luồng thì đầu tiên nội dung sẽ được lấy về thông qua hàm `location.search` và ghi vào biến `query`. Sau đó ghi query ra màn hình thông qua hàm `document.write` mà không hề có bấm kỳ cơ chế lọc input nào. Lúc này ta có thể thấy truy vấn sẽ có dạng là:

`<img src="/resources/images/tracker.gif?searchTerms=nguyenminhhihi">`

Ta giả định thử vì `document.write` không hề lọc nên ta hoàn toàn có thể thử bằng việc đóng đoạn code trên lại để thực hiện thêm 1 lệnh JavaScript nữa ngay bên trong thẻ `<img>` như sau:

`<img src="/resources/images/tracker.gif?searchTerms=nguyenminhhihi" onload=alert(1)">`

Nó sẽ giúp in được thông báo ra màn hình vì vậy ta sẽ thêm vào url một đoạn nữa là:

`nguyenminhhihi"onload=alert(1)`

![](images/Pasted%20image%2020261124223904.png)

Vậy là ta đã có thể thao túng DOM in được thông báo ra màn hình từ việc khai thác lỗ hỏng DOM XSS.
