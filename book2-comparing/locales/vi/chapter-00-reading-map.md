# Bản đồ Đọc: Cách đọc phối hợp Sách Một và Cuốn sách So sánh này

Nếu bạn coi cả hai thư mục đều là "sách về AI coding agent (Agent lập trình AI)", thì sự hiểu lầm dễ xảy ra nhất là cho rằng chúng là các tài liệu trùng lặp. Thực tế không phải vậy. Sự phân công nhiệm vụ của chúng rất rõ ràng.

Sách Một là sự mổ xẻ đơn hệ thống (single-system dissection). Sách sử dụng Claude Code như một mẫu vật để giải thích tại sao một Agent có thể kiểm soát được phải phát triển các bộ phận như mặt phẳng điều khiển (control plane), vòng lặp truy vấn (query loop), phân quyền công cụ (tool permissions), quản trị ngữ cảnh (context governance), đường dẫn phục hồi (recovery paths), xác minh đa Agent (multi-agent verification) và thể chế nhóm (team institutions). Câu hỏi trọng tâm của nó là: một khung điều khiển (harness) cần có bộ khung xương bên trong nào để hoạt động liên tục trong môi trường kỹ thuật thực tế?

Cuốn sách so sánh này là sự mổ xẻ so sánh (comparative dissection). Cuốn sách không còn chỉ hỏi tại sao Claude Code được thiết kế như vậy, mà đặt Claude Code và Codex cạnh nhau để so sánh cách mỗi hệ thống chấp nhận tính không đáng tin cậy của mô hình và thiết lập trật tự ở các lớp khác nhau. Câu hỏi trọng tâm của nó là: khi cả hai hệ thống cùng xây dựng một khung điều khiển, những lựa chọn nào là sự đồng thuận chung và những lựa chọn nào chỉ là các lộ trình kỹ thuật khác nhau?

Hiện tại, việc so sánh đó còn mang lại một lợi ích khác: một khi bạn mang những đánh giá này áp dụng vào các khung điều khiển bên thứ ba, bạn sẽ dễ dàng nhận ra một dạng lỗi phổ biến (failure mode). Nhiều hệ thống cũng quảng cáo về bộ nhớ (memory), kỹ năng (skills), cô đọng (compaction) và hỗ trợ đa Agent, nhưng trục quản trị ngữ cảnh của chúng thực chất vẫn chỉ dừng lại ở việc đẩy thêm nhiều văn bản vào prompt trước rồi cắt bớt hoặc cứu vãn sau. Lộ trình đó trông có vẻ như đem lại "nhiều thông tin hơn", nhưng trong thực tế nó thường tiêu tốn nhiều token hơn trong khi làm suy yếu ngữ nghĩa hoạt động (working semantics).

Nói cách khác, bạn có thể đọc chúng như hai bước tuần tự trong một chương trình nghiên cứu:

- Bước 1: trích xuất các nguyên lý chung của Kỹ nghệ Khung điều khiển (Harness Engineering) trong Sách Một.
- Bước 2: quan sát cách các nguyên lý đó được hiện thực hóa khác nhau trên hai hệ thống cụ thể trong cuốn sách so sánh này.

## Bắt đầu với Sách Một: Chín Đánh giá Cấu trúc từ Claude Code

Sách Một cô đọng lại thành chín đánh giá: đầu tiên, khung điều khiển ngăn chặn mô hình gây tổn hại cho môi trường kỹ thuật; prompt là một phần của mặt phẳng điều khiển; vòng lặp truy vấn là nhịp tim của Agent; công cụ là các giao diện thực thi (execution interfaces) được ràng buộc bởi ngữ nghĩa phê duyệt, điều phối và ngắt (interrupt semantics); nhiều ngữ cảnh hơn không phải lúc nào cũng tốt hơn, bộ nhớ / `CLAUDE.md` / cô đọng là các cơ chế quản trị ngân sách (budget-governance mechanisms); lỗi thuộc về luồng chính, phục hồi là ưu tiên hàng đầu; giá trị của đa Agent nằm ở việc phân chia vai trò và xác minh độc lập; việc triển khai trong nhóm phải kết tinh các quy tắc thành các thể chế có thể tái sử dụng; tất cả những điều này cùng nhau tạo thành một danh sách kiểm tra nguyên lý Kỹ nghệ Khung điều khiển ổn định.

Nếu chỉ đọc Sách Một, bạn sẽ có một ấn tượng mạnh mẽ: đặc trưng của Claude Code là quản trị thời gian chạy (runtime governance) — nó quan tâm trước hết đến cách phiên làm việc tiếp tục chạy, cách các công cụ tránh gây rắc rối, cách phục hồi tránh các vòng lặp vô hạn và cách xác minh tránh tính hình thức.

## Sau đó Đọc Cuốn sách So sánh này: Cùng một Vấn đề, Những Điểm xuất phát Khác nhau

Dựa trên nền tảng đó, cuốn sách này chia việc so sánh thành các lớp rõ ràng.

### Mặt phẳng Điều khiển

Claude Code hoạt động giống như việc lắp ráp prompt động (dynamic prompt assembly) hơn. Rất nhiều trật tự được gói gọn vào việc cấu thành prompt trong thời gian chạy (runtime prompt composition), trạng thái phiên (session state) và quản trị ngữ cảnh.

Codex hoạt động giống như kỹ nghệ lớp điều khiển tường minh hơn. Nó mô-đun hóa và định kiểu cho các phân mảnh chỉ thị (instruction fragments), chính sách phê duyệt (approval policies), sơ đồ công cụ (tool schema), luồng (thread), triển khai (rollout) và các điểm móc (hooks) nhiều nhất có thể.

### Tính Liên tục

Claude Code đặt tính liên tục trong vòng lặp chính và nhấn mạnh kỷ luật nhịp tim của vòng lặp truy vấn.

Codex phân bổ tính liên tục trên luồng, triển khai và cầu nối trạng thái (state bridge), nhấn mạnh vào quyền sở hữu trạng thái có cấu trúc và phục hồi.

### Công cụ và Phân quyền

Claude Code nghiêng về các ràng buộc trong thời gian chạy: phê duyệt tại thời điểm gọi, ngắt và ngăn chặn các hành động rủi ro tác động trực tiếp đến hệ thống.

Codex nghiêng về ngôn ngữ chính sách (policy language) và hợp đồng công cụ (tool contracts): sơ đồ (schema), chính sách phê duyệt, hộp cát (sandbox) và chính sách thực thi (exec policy) như những bộ phận tường minh.

### Quản trị Cục bộ

Claude Code có xu hướng hấp thụ trải nghiệm cục bộ vào bộ nhớ thực địa: `CLAUDE.md`, bộ nhớ, kỹ năng và các ràng buộc quy trình làm việc.

Codex có xu hướng gắn các thể chế cục bộ (local institutions) lên hệ thống tiêm ngữ cảnh (context injection) và hệ thống sự kiện (event systems) có cấu trúc: chỉ thị, kỹ năng, các điểm móc và ranh giới công cụ tường minh.

### Đa Agent và Xác minh

Claude Code nhấn mạnh việc phân chia vai trò đa Agent trong thời gian chạy, và kiên quyết rằng việc xác minh phải độc lập với việc triển khai.

Codex nhấn mạnh việc ủy quyền tường minh, trạng thái bền vững (persistent state) và sự cộng tác thông qua công cụ để việc xác minh trở thành một khả năng có thể theo dõi được, thay vì chỉ là một cử chỉ lịch sự sau cùng.

## Những Điều trở nên Rõ ràng Khi Đọc Chúng Cùng nhau

Đặt Sách Một và cuốn sách so sánh này cạnh nhau sẽ mang lại ba kết luận đầy đủ hơn.

### Thứ nhất, việc so sánh chủ yếu tập trung vào khung điều khiển

Cả hai cuốn sách đều chỉ ra cùng một thực tế: thách thức cốt lõi của các hệ thống lập trình AI là ngăn các mô hình mất kiểm soát trong terminal, hệ thống tệp, ranh giới phân quyền và các thể chế nhóm. Những cải tiến về khả năng diễn đạt của mô hình là quan trọng, nhưng chúng chỉ là thứ yếu so với vấn đề đó.

### Thứ hai, sự khác biệt chính giữa Claude Code và Codex là nơi thiết lập trật tự

Claude Code gần giống với một hệ thống được phát triển từ áp lực giải quyết sự cố thời gian chạy, ưu tiên tính liên tục, khả năng phục hồi và quản trị thực địa.

Codex gần giống với một hệ thống được phát triển từ thiết kế cấu trúc tường minh, ưu tiên việc đặt tên cho lớp điều khiển, biểu đạt chính sách, sự rõ ràng về ranh giới và khả năng lắp ghép (composability).

### Thứ ba, những người đi sau thường thu hoạch được nhiều hơn bằng cách xác định sự không chắc chắn chủ đạo của riêng họ

Nếu nỗi đau lớn nhất của bạn là sự mất ổn định trong các phiên làm việc dài, phục hồi mong manh và bỏ qua xác minh, hãy bắt đầu với kỷ luật thời gian chạy được nhấn mạnh trong Sách Một.

Nếu nỗi đau lớn nhất của bạn là các quy tắc rải rác, ranh giới phân quyền mơ hồ, hợp đồng công cụ không ổn định và hành vi không thể tái lập của nhóm, hãy bắt đầu với những bài học về lớp điều khiển tường minh mà cuốn so sánh này rút ra từ Codex.

Và nếu bạn gặp một hệ thống mà tính liên tục của nó phụ thuộc chủ yếu vào việc xếp chồng văn bản khởi động (bootstrap text), tệp định danh (identity files), danh mục kỹ năng (skill catalogs) và văn bản mô tả không gian làm việc vào prompt, đừng quá ấn tượng bởi sự đầy đủ bề ngoài của ngữ cảnh. Trong nhiều trường hợp, điều đó chỉ ra một trạng thái trung gian chưa thực sự quản trị được ngữ cảnh, chứ không phải là một con đường thứ ba trưởng thành.

## Lộ trình Đọc Khuyến nghị

Nếu bạn mới tiếp cận bộ tài liệu này, hãy sử dụng lộ trình sau:

1. Đọc [Lời tựa](preface.md) trước để xác nhận rằng tài liệu này đang so sánh nơi đặt trật tự, chứ không đơn thuần là liệt kê các tính năng.
2. Đọc [Chương 1 Tại sao Đặt Claude Code và Codex cạnh nhau](chapter-01-why-this-comparison.md) để thiết lập khung vấn đề.
3. Sau đó đọc các Chương từ 2 đến 6 theo trình tự trên năm trục: mặt phẳng điều khiển, tính liên tục, quản trị công cụ, thể chế cục bộ và xác minh đa Agent.
4. Nếu bạn chỉ muốn một sự tổng hợp nhanh chóng, hãy nhảy tới [Chương 7 Các Điểm đến Hội tụ, Các Nhánh Phân kỳ](chapter-07-convergence-and-divergence.md).
5. Nếu mục tiêu của bạn là tự xây dựng các hệ thống, hãy kết thúc với [Chương 8 Nếu bạn tự xây dựng một hệ thống: Học hỏi từ ai và Học gì trước tiên](chapter-08-how-to-choose-or-build.md). Chương đó hiện có thêm một sơ đồ ba lộ trình để giải thích tại sao một số khung điều khiển vẫn tạo cảm giác tốn kém và mất trật tự ngay cả khi ngữ cảnh của chúng trông có vẻ đầy đủ.

## Tóm tắt trong Một câu

Sách Một giải thích tại sao một Agent kiểm soát được phải phát triển theo cách này.

Cuốn sách so sánh này giải thích tại sao hai hệ thống khung điều khiển nghiêm túc vẫn phát triển theo cách khác nhau.
