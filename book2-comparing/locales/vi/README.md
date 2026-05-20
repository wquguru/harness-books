# Triết lý Thiết kế Khung kiểm soát của Claude Code và Codex

![Cover: The Harness Design Philosophies of Claude Code and Codex](assets/cover-wxb-en.svg)

Phụ đề: sự hội tụ, phân kỳ và các lựa chọn kỹ thuật đằng sau hai hệ thống coding-agent.

> “Cuộc sống là đau khổ, và kỹ thuật khung kiểm soát (harness engineering) là nghệ thuật biến sự đau khổ đó thành có chủ ý.”

Cuốn sách này là một phân tích so sánh cấu trúc của hai khung kiểm soát (harnesses): Claude Code, phát triển từ kinh nghiệm vận hành thực tế, và Codex, được sinh ra từ một lớp chính sách và kiểm soát vô cùng rõ ràng. Chúng ta không thống kê các công cụ; chúng ta xem xét nơi mỗi hệ thống giải phóng sự tin tưởng, cấu trúc quản trị và ràng buộc một mô hình cơ bản là không đáng tin cậy.

Ba giả định dẫn dắt câu chuyện này:

- So sánh tập trung vào thiết kế khung kiểm soát, không phải năng lực mô hình.
- Một khung kiểm soát là một hệ thống phân bổ quyền lực có chủ ý, không phải một bảng liệt kê tính năng.
- Sự khác biệt về mặt kỹ thuật thường xuất phát từ nơi trật tự được thiết lập, chứ không phải từ cách nó được gọi.

Thứ tự đọc khuyến nghị:

1. [Bản đồ Đọc sách: Cách đọc cuốn sách này cùng tập đầu tiên](chapter-00-reading-map.md)
2. [Lời tựa: Hai khung kiểm soát, không phải một bộ phụ kiện](preface.md)
3. [Chương 1: Tại sao chúng ta ghép cặp Claude Code và Codex](chapter-01-why-this-comparison.md)
4. [Chương 2: Hai mặt phẳng điều khiển—lắp ráp prompt động so với các phân đoạn hướng dẫn có cấu trúc](chapter-02-two-control-planes.md)
5. [Chương 3: Nhịp đập so với luồng, triển khai và cầu nối trạng thái](chapter-03-loop-thread-and-rollout.md)
6. [Chương 4: Công cụ, hộp cát và chính sách thực thi](chapter-04-tools-sandbox-and-exec-policy.md)
7. [Chương 5: Kỹ năng, hook và quản trị cục bộ](chapter-05-skills-hooks-and-local-governance.md)
8. [Chương 6: Ủy quyền, xác minh và trạng thái bền vững](chapter-06-delegation-verification-and-state.md)
9. [Chương 7: Sự hội tụ, phân kỳ và điểm giao thoa của các triết lý](chapter-07-convergence-and-divergence.md)
10. [Chương 8: Nếu bạn tự xây dựng khung kiểm soát, nên nghiên cứu điều gì trước tiên](chapter-08-how-to-choose-or-build.md)
11. [Phụ lục A: Bản đồ mã nguồn cho bài so sánh này](appendix-a-source-map.md)
12. [Phụ lục B: Bảng kiểm để phát hiện xem bạn đang ở gần khung kiểm soát nào hơn](appendix-b-checklists.md)

Để xem phiên bản tóm tắt của luận án, hãy nhảy tới [Chương 7](chapter-07-convergence-and-divergence.md).
