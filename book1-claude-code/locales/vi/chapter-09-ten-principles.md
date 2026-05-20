# Chương 9 Mười Nguyên lý của Kỹ thuật Khung kiểm soát (Harness Engineering)

Technical writing has a bad habit: after presenting enough detail, it avoids making judgments, as if showing complexity exempts conclusion responsibility. It does not. Complexity remains complexity, but judgment is still required. Teams carry principles forward, not function names from one source version.

Viết tài liệu kỹ thuật có một thói quen xấu: sau khi trình bày đủ chi tiết, người viết thường né tránh đưa ra nhận định, như thể việc chỉ ra sự phức tạp sẽ miễn trừ trách nhiệm đưa ra kết luận. Thực tế không phải vậy. Phức tạp vẫn là phức tạp, nhưng nhận định vẫn là điều cần thiết. Các đội ngũ mang theo các nguyên lý tiến lên phía trước, chứ không phải các tên hàm từ một phiên bản mã nguồn cụ thể.

Xuyên suốt tám chương trước, chúng ta liên tục xoay quanh một thực tế: các mô hình là không đáng tin cậy, nhưng các hệ thống vẫn có thể đáng tin cậy nếu độ tin cậy được xây dựng bên trong khung kiểm soát (harness) chứ không phải ủy quyền cho các mô hình.

Chương này không lập luận lại các chi tiết. Nó nén cuốn sách lại thành mười nguyên lý. Chúng không phải là những khẩu hiệu. Chúng đến từ những nhận định thực tế được phản ánh trong mã nguồn và cấu trúc kỹ thuật của Claude Code.

## 9.1 Coi mô hình là các thành phần không ổn định, không phải đồng nghiệp

Đồng nghiệp có thể được tin tưởng giao phó trách nhiệm ổn định. Các mô hình thì không. Các mô hình có thể nói chuyện như đồng nghiệp, nhưng chúng không tự động có được sự ổn định, trách nhiệm giải trình hoặc phán đoán bền vững ở cấp độ đồng nghiệp. Nhận thức điều này càng sớm, hệ thống càng sớm phát triển được ranh giới phân quyền, lộ trình khôi phục, chốt chặn xác minh và khả năng rollback.

## 9.2 Prompt là một phần của mặt phẳng điều khiển (control plane)

Các prompt hệ thống định nghĩa giao thức hành vi. Cùng với runtime, lược đồ công cụ (tool schema), bộ nhớ và các hook, chúng tạo thành mặt phẳng điều khiển (control plane). Nếu prompt chỉ được coi là vật trang trí cho tính cách nhân vật (persona), bạn sẽ nhận được các hệ thống biểu diễn tốt về mặt ngôn từ nhưng hành xử không có tính kỷ luật.

## 9.3 Vòng lặp truy vấn (Query loop) là nhịp đập của hệ thống agent

Các agent thực tế phụ thuộc vào các vòng lặp thực thi liên tục. Quản trị đầu vào, tiêu thụ luồng dữ liệu (stream), lập lịch công cụ, các nhánh khôi phục và điều kiện dừng đều thuộc về nhịp đập này. Nếu không có vòng lặp truy vấn, các hệ thống có thể trình diễn tốt nhưng không phải là các môi trường thực thi (runtimes).

## 9.4 Công cụ là các giao diện thực thi được quản lý

Một khi mô hình chạm vào shell, hệ thống tệp, Git và mạng, câu hỏi sẽ chuyển từ "liệu nó có thể nói ra điều đó không" sang "liệu nó có để lại hậu quả không". Do đó, các công cụ phải được lập lịch, ủy quyền, có thể bị ngắt và phải đóng sổ cái. Một công cụ càng nguy hiểm thì càng ít được đối xử như một năng lực thông thường.

## 9.5 Ngữ cảnh là bộ nhớ làm việc

Có khả năng nhồi nhét ngữ cảnh không có nghĩa là ngữ cảnh nên bị nhồi nhét. Các quy tắc lâu dài, bộ nhớ bền vững, tính liên tục của phiên và đối thoại tạm thời nên được quản trị theo từng lớp. Rút gọn (compact) tồn tại để bảo tồn nền tảng ngữ nghĩa (semantic substrate) cho công việc tiếp tục. Quản lý ngữ cảnh tốt tối ưu hóa không phải cho "nhiều hơn", mà là cho "có thể quản trị được".

## 9.6 Đường dẫn lỗi là đường dẫn chính

Lỗi prompt quá dài (prompt-too-long), giới hạn token đầu ra (max-output-tokens), các ngắt, vòng lặp hook và lỗi rút gọn là thời tiết bình thường đối với các agent phiên làm việc dài. Phục hồi, ngắt mạch (circuit breaking), giới hạn số lần thử lại và bảo vệ chống vòng lặp vô hạn phải tồn tại ngay từ thời điểm thiết kế, chứ không phải vá víu sau khi sự cố xảy ra.

## 9.7 Phục hồi nên tối ưu hóa cho việc tiếp tục công việc

Sau khi cắt ngắn (truncation), việc tiếp tục công việc thường tốt hơn là tóm tắt lại. Khi quá trình rút gọn thất bại, trước tiên hãy khôi phục lại nhịp thở. Sự lịch thiệp thực sự của kỹ thuật là không nhốt người dùng bên trong các trạng thái lỗi.

## 9.8 Đa agent quan trọng vì nó phân chia sự không chắc chắn

Đa agent đặt việc nghiên cứu, triển khai, xác minh và tổng hợp vào các thùng chứa trách nhiệm khác nhau. Trạng thái được cô lập, vai trò được tách biệt và điều phối viên hội tụ lại sự hiểu biết. Giá trị thực sự của tính song song không chỉ nằm ở tốc độ, mà là ranh giới trách nhiệm sắc nét hơn.

## 9.9 Xác minh phải độc lập

Người triển khai tự nhiên sẽ quá tin tưởng vào các thay đổi của chính họ. Các mô hình thậm chí còn làm thế nhiều hơn. Đối với công việc quan trọng, xác minh nên là một giai đoạn độc lập chuyên trách, lý tưởng nhất là với quyền sở hữu vai trò độc lập. Nếu không, khái niệm "hoàn thành" sẽ nhanh chóng xuống cấp thành "đã viết xong và cảm thấy ổn".

## 9.10 Các thể chế trong nhóm quan trọng hơn mẹo cá nhân

Một chuyên gia có thể thuần hóa agent bằng kinh nghiệm. Một nhóm không thể trông cậy vào điều đó. Các nhóm cần:

- tệp `CLAUDE.md` phân lớp
- các ranh giới phê duyệt rõ ràng
- các kỹ năng có thể thực thi
- các hook vòng đời (lifecycle hooks)
- các bản ghi hội thoại có thể truy vết (traceable transcripts)
- định nghĩa xác minh thống nhất

Chỉ khi kỹ thuật cá nhân được thể chế hóa, hệ thống agent mới có thể trở thành năng lực của tổ chức thay vì tay nghề thủ công của cá nhân.

## 9.11 Một câu kết luận cuối cùng

Nếu toàn bộ cuốn sách phải được nén lại một lần nữa:

> Kỹ thuật Khung kiểm soát (Harness Engineering) đặt câu hỏi làm thế nào các hệ thống vẫn có thể hoạt động như những hệ thống kỹ thuật khi bản thân các mô hình không đáng tin cậy.

Những gì mã nguồn Claude Code thực sự giảng giải là sự tiết chế: coi sự không ổn định là một đầu vào đã biết, sau đó thiết kế prompt, vòng lặp, công cụ, bộ nhớ, rút gọn, khôi phục, xác minh và quy trình làm việc của nhóm xung quanh đầu vào đó. Đó chính là lý do tại sao nó rất xứng đáng được nghiên cứu như một mẫu vật thiết kế.

Tại thời điểm này, kết luận đơn giản hơn nhiều so với hành trình đi đến đó. Phần khó khăn không phải là nói ra các nguyên lý, mà là chấp nhận chúng: đặt khung kiểm soát lên trên sự phấn khích, thể chế lên trên sự thông minh và xác minh lên trên sự tự tin. Các nhóm nội tâm hóa được ba điều này đã đứng trước ngưỡng cửa của Kỹ thuật Khung kiểm soát.
