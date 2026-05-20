# Giới thiệu

![Cover: Harness Engineering: A Design Guide to Claude Code](assets/cover-wxb-en.svg)

> Cuốn sách này không đặt câu hỏi liệu một mô hình có thể viết mã nguồn hay không. Nó đặt câu hỏi làm thế nào để giữ cho một mô hình viết mã nguồn không làm chệch hướng một hệ thống kỹ thuật một khi nó được tích hợp vào các terminal, kho lưu trữ (repository) và quy trình làm việc của nhóm (team workflow).

Đây không phải là một tập hợp các chú thích mã nguồn được chắp vá, cũng không phải là một chuyến tham quan tính năng. Nó tập trung vào cách Claude Code kiểm soát một mô hình không ổn định vào một trật tự kỹ thuật bền vững, nơi mặt phẳng điều khiển (control plane), vòng lặp chính (main loop), quyền của công cụ (tool permissions), quản trị ngữ cảnh (context governance), lộ trình khôi phục (recovery paths), xác minh đa agent (multi-agent verification) và các thực tiễn của nhóm (team practices) tạo thành một bộ khung nhất quán.

Cuốn sách này bắt đầu từ ba giả định khi đọc:

- Trọng tâm không nằm ở khả năng của mô hình, mà ở cách khung kiểm soát (harness) tổ chức các ràng buộc và việc thực thi
- Mục tiêu không phải là tường thuật chi tiết từng dòng hàm, mà là tại sao runtime phải phát triển theo hướng này
- Giá trị không nằm ở việc thu thập các mẹo cá nhân, mà ở việc biến cấu trúc thành thực tiễn nhóm có thể tái sử dụng

Thứ tự đọc khuyến nghị:

1. [Lời nói đầu: Khung kiểm soát (Harness), Terminal và các Ràng buộc Kỹ thuật](preface.md)
2. [Chương 1 Tại sao Kỹ thuật Khung kiểm soát (Harness Engineering) lại quan trọng](chapter-01-why-harness-engineering.md)
3. [Chương 2 Prompt không phải là Tính cách, Prompt là Mặt phẳng Điều khiển (Control Plane)](chapter-02-prompt-is-control-plane.md)
4. [Chương 3 Vòng lặp Truy vấn (Query Loop): Nhịp đập của một Hệ thống Agent](chapter-03-query-loop-heartbeat.md)
5. [Chương 4 Công cụ, Quyền hạn và Ngắt (Tools, Permissions, and Interrupts): Tại sao Agent không thể chạm trực tiếp vào thế giới](chapter-04-tools-permissions-interrupts.md)
6. [Chương 5 Quản trị Ngữ cảnh (Context Governance): Bộ nhớ, CLAUDE.md và Rút gọn (Compact) như một Cơ chế Ngân sách](chapter-05-context-memory-compact.md)
7. [Chương 6 Lỗi và Khôi phục (Errors and Recovery): Một Hệ thống Agent tiếp tục hoạt động sau khi Thất bại](chapter-06-errors-and-recovery.md)
8. [Chương 7 Công việc Đa Agent và Xác minh (Multi-Agent Work and Verification): Quản lý sự Không ổn định thông qua Phân công Lao động](chapter-07-multi-agent-and-verification.md)
9. [Chương 8 Áp dụng trong Nhóm (Team Adoption): Biến một Công cụ Thông minh thành một Thể chế có thể Tái sử dụng](chapter-08-team-landing-practices.md)
10. [Chương 9 Mười Nguyên lý của Kỹ thuật Khung kiểm soát (Harness Engineering)](chapter-09-ten-principles.md)
11. [Phụ lục A Bảng kiểm (Checklists): Biến các Nguyên lý thành các Ràng buộc khả thi](appendix-a-checklists.md)
12. [Phụ lục B Sơ đồ: Vẽ Bộ khung Runtime](appendix-b-diagram-notes.md)
13. [Phụ lục C Bản đồ Nguồn (Source Map): Những File nào làm Cơ sở cho mỗi Chương](appendix-c-source-map.md)

Nếu bạn chỉ muốn xem nhận định tổng hợp trước, hãy chuyển đến [Chương 9](chapter-09-ten-principles.md).
