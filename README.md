# PortSwigger Web Security Academy - Writeups

Repo này là nơi mình ghi lại **writeup (WU)** cho các lab trên [PortSwigger Web Security Academy](https://portswigger.net/web-security) trong quá trình tự học Web Security.

Mỗi lab được trình bày theo hướng: **đề bài → phân tích → khai thác** kèm ảnh chụp từng bước để dễ theo dõi và để mình xem lại sau này.

## Mục đích

- Hệ thống lại kiến thức về các lỗ hổng web phổ biến (OWASP Top 10).
- Rèn thói quen ghi chép giải thích lại bằng lời của mình thay vì chỉ làm cho xong.
- Làm tài liệu tham khảo cho bản thân và những ai đang học cùng.

## Cấu trúc repo

Mỗi chủ đề là một thư mục riêng bên trong gồm các LAB trong cấu trúc từng lab sẽ là file `README.md` (nội dung writeup) và thư mục `images/` (ảnh minh họa):

```text
.
├── README.md                # Trang giới thiệu chung (file này)
├── SQL Injection/
│   ├── SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
│       ├── README.md
│       └── images/
│   ├── SQL injection vulnerability allowing login bypass
│       ├── README.md
│       └── images/
│   ├── SQL injection with filter bypass via XML encoding
│       ├── README.md
│       └── images/
```

## Mục lục

| Chủ đề | Writeup | Trạng thái |
| ------ | ------- | ---------- |
| SQL Injection | [Xem writeup](./SQL%20Injection) | Đang cập nhật |


## Cách đọc

1. Chọn chủ đề trong bảng mục lục ở trên.
2. Mở Lab bạn cần tìm và đọc `README.md` của chủ đề đó các lab được sắp xếp theo thứ tự mình làm.
3. Ảnh minh họa nằm trong thư mục `images/` cùng cấp và được hiển thị trực tiếp trong bài viết.

## Lưu ý

- Tất cả kỹ thuật trong repo chỉ được thực hiện trên **môi trường lab do PortSwigger cung cấp** nhằm mục đích học tập.
- Không áp dụng lên hệ thống thật khi chưa được sự cho phép của chủ sở hữu.
- Writeup phản ánh cách hiểu của mình tại thời điểm làm bài nếu có sai sót hoặc cách giải hay hơn mọi góp ý đều được hoan nghênh (qua Issues hoặc Pull Request).

## Tham khảo

- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
