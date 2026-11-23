> This lab contains a stored cross-site scripting vulnerability in the comment functionality.
> 
> To solve this lab, submit a comment that calls the `alert` function when the blog post is viewed.

Ở bài này yêu cầu được đặt ra cho chúng ta đó là làm sao để có thể in ra một thông báo trên hệ thống mà nó đảm bảo được tính tồn tại mỗi khi có người dùng vào đúng vị trí đã bị tấn công sẽ phải chịu ảnh hưởng của payload. Đó chính là bản chất của stored XSS thế nên ở đây trước tiên ta cần xác định được vị trí tấn công là cái đầu tiên. Ta thử đăng tải 1 comment để xem nó sẽ được post và lưu trên server như thế nào.

![](images/Pasted%20image%2020261124000707.png)
![](images/Pasted%20image%2020261124000716.png)
![](images/Pasted%20image%2020261124000735.png)

Ở đây ta có thể thấy comment của ta đã được lưu trên bài post của hệ thống thế nên ta sẽ tiến hành xem nó lưu theo hình thức nào.

![](images/Pasted%20image%2020261124000815.png)

Ta bật chế độ devtool lên để xem source code HTML của server thì thấy rõ phần nội dung của comment ta sẽ nằm trong một thẻ HTML. Nếu server không có bất kỳ cơ chế lọc nào mình hoàn toàn có thể chèn tấn công javascript vào đây và thực hiện một cuộc tấn công stored XSS vào chính vị trí này nơi mà hệ thống sẽ lưu trữ lại hoàn toàn nội dung mà ta post lên.

![](images/Pasted%20image%2020261124000915.png)

Lúc này ta thử post thêm 1 comment mới với phần nội dung lần này là 1 payload in ra thông báo bằng câu lệnh javascipt để hệ thống lưu trữ lại và tấn công khiến payload tồn tại lâu dài trong url này.

![](images/Pasted%20image%2020261124000935.png)
![](images/Pasted%20image%2020261124000943.png)

Và như vậy sau khi gửi thì ta đã chính thức thành công với việc lưu 1 payload trên server đảm bảo được tính chất persistant của nó. Đây cũng là bản chất của stored XSS và sự khác biệt của nó với reflected XSS. Vì với reflected XSS nội dung sẽ được gửi lại qua 1 phản hồi mang tính tạm thời và không lưu trữ lâu dài trên hệ thống. Trái ngược với việc đó stored XSS có độ nguy hiểm hơn rất nhiều khi nó tồn tại được trên hệ thống. Như ví dụ trên chỉ cần một client nào sau này vào trang đều sẽ phải nhận thông báo trên vì comment của attacker vẫn còn tồn tại ở đó. Thậm chí nguy hiểm hơn là attacker có thể gửi ra bên ngoài cookie của victim mỗi khi họ vào url đó.
