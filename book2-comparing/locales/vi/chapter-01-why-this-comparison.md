# Chương 1: Tại sao chúng ta so sánh Claude Code và Codex

## 1.1 Bởi vì cả hai đều không tin tưởng mô hình

Gọi Claude Code và Codex là "các mô hình viết mã" là không đúng trọng tâm. Sự so sánh thú vị không phải là "ai có nhiều nút bấm hơn", mà là cách mỗi khung điều khiển (harness) chấp nhận một thực tế mà hoạt động tiếp thị thường che giấu: mô hình không thể được tin cậy để vận hành shell, tệp tin, mạng hoặc trạng thái một cách vô hạn chế. Nó ảo tưởng (hallucinates), quên ngữ cảnh và tự đắc một cách vô căn cứ. Một khi mô hình đó chạm vào terminal, hệ thống tệp hoặc một phiên làm việc nhiều vòng (multi-round session), vấn đề không còn là "câu trả lời có đúng không?" mà là "ai dọn dẹp đống hỗn độn này?"

Claude Code trông giống như một hệ thống được sinh ra từ các cuộc đánh giá sự cố (incident reviews). Đọc `query.ts`, `toolOrchestration.ts`, `compact.ts` và các prompt xung quanh — bạn sẽ thấy một hệ thống luôn dự liệu về thất bại, sự mệt mỏi và quay lui (rollback). Codex cũng trung thực như thế, nhưng nó thể hiện sự không tin tưởng thông qua các mô-đun tường minh: luồng (thread), triển khai (rollout), chỉ thị phân mảnh (fragment instructions), chính sách thực thi (exec policies), hộp cát (sandboxing) và sơ đồ công cụ (tool schemas). Mỗi mô-đun đều tuyên bố rõ trách nhiệm của mình thay vì phó mặc cho trực giác của mô hình.

Vì vậy, sự so sánh này là về cách mỗi khung điều khiển thuần hóa tính không đáng tin cậy — chứ không phải về việc ai có thể thực thi được nhiều lệnh hơn.

## 1.2 Claude Code: Khung điều khiển ưu tiên thời gian chạy

Thế mạnh của Claude Code tập trung xung quanh vòng lặp chính (main loop) bởi vì nó bắt đầu từ một câu hỏi: "Mô hình đã đang chạy theo chu kỳ. Làm thế nào để đảm bảo vòng này không phá hỏng vòng tiếp theo?" Hệ thống ít quan tâm đến "các prompt đẹp đẽ" mà quan tâm nhiều hơn đến việc phân lớp prompt (prompt layering), cô đọng (compacting), cổng phân quyền (permission gating), ngắt (interrupts), điều phối công cụ (tool orchestration) và vòng đời của Agent con được rẽ nhánh (forked agent life cycles). Công việc diễn ra ở thời gian chạy (runtime): quản lý sự phình to của tin nhắn (message inflation), định tuyến lại đầu ra của công cụ (tool output rerouting), cắt tỉa ngữ cảnh (context trimming), cô lập Agent con (child-agent isolation) và các giai đoạn xác minh độc lập (independent verification phases). Khung điều khiển này phát triển từ những ca làm việc thực tế — vì vậy nó giải quyết "công việc bẩn thỉu" thông qua luồng điều khiển (control flow), chứ không chỉ thông qua các giao diện trang nhã.

## 1.3 Codex: Kiểm soát có cấu trúc ngay từ đầu

Codex đi theo một con đường khác. Thiết kế của nó coi các chỉ thị là các phân mảnh có định kiểu và có ranh giới (typed, bounded fragments). `AGENTS.md`, `skills` và các phân mảnh của người dùng xuất hiện trong các prompt dưới dạng các phần được đánh dấu với token bắt đầu và kết thúc. Công cụ là các đối tượng ưu tiên sơ đồ (schema-first objects). Chính sách thực thi (exec policy) là một crate riêng biệt chứa các chính sách, quy tắc, đánh giá và trình phân tích cú pháp. Điểm nhấn là làm cho trật tự trở nên tường minh, có thể lắp ghép (composable) và có thể giải thích được.

Điều này mang lại hai kết quả ngay lập tức: mặt phẳng điều khiển (control plane) dễ giải thích hơn (bạn có thể theo vết lý do tại sao một phân mảnh lại tồn tại), và dễ phát triển theo lập trình hơn (thêm các quy tắc hiển thị, hợp nhất hoặc ưu tiên mới mà không cần viết lại thời gian chạy).

## 1.4 Cùng một câu hỏi, những điểm xuất phát khác nhau

Cả hai hệ thống đều cố gắng giữ cho một mô hình không đáng tin cậy không thực hiện những việc không thể chấp nhận được. Claude Code bắt đầu bằng cách hỏi làm thế nào một vòng lặp đang chạy có thể duy trì sự mạch lạc; Codex bắt đầu bằng cách hỏi làm thế nào thông tin điều khiển có thể được chuyển thành các cấu trúc tường minh, có thể lắp ghép. Claude Code thiên về kỷ luật thời gian chạy (runtime discipline); Codex thiên về cơ sở hạ tầng có định kiểu (typed infrastructure).

## 1.5 Tại sao sự khác biệt này lại quan trọng

Hướng đi mà một nhóm lựa chọn thường quyết định cách văn hóa của nhóm đó phát triển. Nhấn mạnh tính liên tục thời gian chạy (runtime continuity), và bạn sẽ bị ám ảnh bởi việc phục hồi (recovery), ngắt (interruption), ô nhiễm trạng thái (state pollution), vũ đạo công cụ (tool choreography) và độ tin cậy của phiên làm việc dài. Nhấn mạnh việc kiểm soát tường minh (explicit control), và bạn sẽ bị ám ảnh bởi ranh giới chỉ thị, phân cấp cấu hình (config hierarchies), sơ đồ công cụ, ngôn ngữ chính sách và trạng thái luồng bền vững (persistent thread state).

Cả hai con đường đều hợp lệ. Sai lầm là trộn lẫn chúng mà không có sự rõ ràng, dẫn đến việc mất cả kỷ luật thời gian chạy lẫn trật tự thể chế.

## 1.6 Bài học rút ra

Claude Code và Codex là các triết lý thiết kế khung điều khiển, chứ không phải là danh sách kiểm tra tính năng. Chúng hội tụ ở việc chấp nhận rằng các mô hình là không đáng tin cậy; chúng phân kỳ ở những gì chúng xây dựng xung quanh sự thừa nhận đó. Cuốn sách này sẽ bóc tách sự phân kỳ đó.
