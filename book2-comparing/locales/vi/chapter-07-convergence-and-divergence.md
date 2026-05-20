# Chapter 7 Hội tụ và Phân kỳ

## 7.1 Bắt đầu với phần mà chúng hội tụ

Nếu tôi phải đưa ra kết luận ngắn gọn nhất trước tiên, tôi sẽ nói: đúng vậy, chúng thực sự hội tụ.

Lý do rất đơn giản. Cả Claude Code và Codex đều không coi mô hình là một bên thực thi xứng đáng nhận được sự tin cậy trực tiếp. Cả hai hệ thống đều chấp nhận rằng:

- prompt không kiểm soát mọi thứ
- các công cụ phải được ràng buộc
- các phiên dài yêu cầu quản trị trạng thái (state governance)
- các quy tắc địa phương phải đi vào hệ thống
- việc thực thi đa Agent (multi-agent) yêu cầu phân chia vai trò và xác minh

Nói cách khác, cả hai đều đã vượt qua giai đoạn ngây thơ khi mọi người tưởng tượng rằng các mô hình mạnh hơn sẽ tự động giải quyết các vấn đề hệ thống bằng cách nào đó. Một khi hệ thống đạt đến điểm này, nó không còn coi Agent chỉ đơn thuần là một chatbot có đính kèm thêm vài công cụ nữa.

Vì vậy, ở cấp độ định hướng, chúng thực sự gặp nhau tại cùng một điểm đến: khung kiểm soát (harness) là lớp điều khiển thực sự, và mô hình là thành phần năng suất nhất nhưng cũng kém ổn định nhất nằm bên dưới nó.

## 7.2 Bây giờ là phần mà chúng phân nhánh

Nhưng sẽ là quá thô sơ nếu gọi chúng là giống hệt nhau về mặt cơ bản.

Trục chính của Claude Code trông giống như thế này:

- bắt đầu từ vòng lặp truy vấn (query loop)
- xử lý tính liên tục trong runtime
- bảo toàn trật tự bằng cách nén (compaction), điều phối công cụ (tool orchestration), ngắt (interrupts) và phục hồi (recovery)
- kết nối các quy tắc thực địa và thể chế của đội ngũ thông qua kỹ năng (skills), hook và xác minh (verification)

Trục chính của Codex trông giống như thế này hơn:

- bắt đầu từ các ranh giới mô-đun rõ ràng và các lớp điều khiển rõ ràng
- biến các chỉ dẫn thành các đoạn cắt (fragments)
- biến các công cụ thành các schema
- biến các ranh giới thực thi thành chính sách (policy)
- biến các phiên thành luồng (thread) / rollout / trạng thái (state)
- biến các quy tắc địa phương và hook thành các tài sản có cấu trúc (structured assets) và hệ thống sự kiện (event systems)

Hệ thống thứ nhất mang lại cảm giác giống như một hệ thống phát triển từ kinh nghiệm cơ học.

Hệ thống thứ hai mang lại cảm giác giống như một hệ thống phát triển từ thiết kế thể chế.

Đó là nơi sự phân nhánh thực sự tồn tại. Sự khác biệt không nằm ở điểm đến. Nó nằm ở khung xương (skeleton).

## 7.3 Nếu tôi phải dán cho chúng một cái nhãn khắt khe nhưng chính xác hơn

Tôi thậm chí sẵn sàng gọi chúng là hai hình thái chính trị khác nhau của khung kiểm soát (harness).

Claude Code gần gũi hơn với một nền cộng hòa runtime (runtime republic). Một phần lớn quyền lực tập trung vào vòng lặp chính (main loop) và điều phối thực địa, và trật tự được duy trì thông qua sự thương lượng liên tục với thực tế. Nó không chống lại thể chế; chỉ là các thể chế có xu hướng tồn tại để phục vụ cho phiên làm việc trực tiếp (live session).

Codex gần gũi hơn với một mặt phẳng điều khiển hiến pháp (constitutional control plane). Quyền lực trước tiên được viết vào các kiểu (types), đoạn cắt (fragments), chính sách (policy), luồng (threads) và hệ thống sự kiện. Tất nhiên runtime vẫn phán quyết, nhưng nó phán quyết bên trong một khuôn khổ rõ ràng hơn.

Đó là một mô tả cường điệu, nhưng nó làm sáng tỏ một điểm quan trọng: khung kiểm soát (harness) chưa bao giờ chỉ là một đống các bộ phận kỹ thuật. Nó còn là một cách phân chia quyền lực. Ai xác định ranh giới, ai giải thích trạng thái và ai nắm giữ thẩm quyền thực thi cuối cùng, tất cả cuối cùng đều xuất hiện trong kiến trúc.

## 7.4 Những gì các nhà xây dựng sau này nên học hỏi

Nếu một đội ngũ có ý định tự xây dựng Agent lập trình riêng, giá trị thực sự của sự so sánh này không phải là chọn phe. Đó là việc tránh được hai loại sai lầm.

Sai lầm đầu tiên là nghĩ rằng một bảng tính năng là đủ. Không phải vậy. Một đội ngũ phải quyết định mâu thuẫn chính của mình là gì. Vấn đề thực sự nằm ở chỗ các phiên dài vượt ra ngoài tầm kiểm soát, hay các nguồn quy tắc quá phân tán và ranh giới quyền hạn vẫn chưa rõ ràng? Các mâu thuẫn khác nhau sẽ thúc đẩy bạn hướng tới các hình thái khung kiểm soát (harness) khác nhau.

Sai lầm thứ hai là cố gắng ghép nối các tính năng hấp dẫn nhất của cả hai hệ thống mà không thực hiện các sự đánh đổi thực sự. Trong kỹ thuật, điều nguy hiểm nhất thường không phải là bản thân sự đánh đổi mà là việc từ chối thực hiện sự đánh đổi. Nếu bạn vừa muốn có sự linh hoạt hoàn toàn của runtime động, vừa muốn có một mặt phẳng điều khiển có cấu trúc hoàn toàn rõ ràng cùng một lúc, bạn thường sẽ kết thúc bằng việc không có cả hai.

Cách tiếp cận lành mạnh hơn là:

- nếu bạn lo sợ mất kiểm soát tại thực địa, hãy tăng cường nhịp đập runtime (runtime heartbeat) trước
- nếu bạn lo sợ sự trôi dạt thể chế (institutional drift), hãy làm rõ chỉ dẫn, công cụ, chính sách và trạng thái trước
- một khi mâu thuẫn chính ổn định, hãy dần dần xây dựng phía đối diện

Một cảnh báo nữa cần được nêu ra ở đây. Trong thực tế, nhiều hệ thống non trẻ không thực hiện đầy đủ nhiệm vụ nào cả. Chúng không làm cứng cáp kỷ luật runtime, cũng không làm cho lớp điều khiển thực sự rõ ràng. Thay vào đó, chúng chọn con đường thứ ba trông có vẻ dễ dàng hơn: tiếp tục nhồi nhét thêm nhiều tệp khởi động (bootstrap files), mô tả vai trò, giải thích kỹ năng và văn bản không gian làm việc vào prompt, với hy vọng rằng sự đầy đủ về thông tin sẽ bù đắp cho một khung xương yếu ớt. Các hệ thống như vậy thường tỏ ra khả thi trong ngắn hạn, nhưng qua các phiên dài hơn, chúng bộc lộ cùng một thất bại kép: token thì đắt đỏ, còn ngữ nghĩa hoạt động vẫn không ổn định.

## 7.5 Phán quyết cuối cùng

Câu hỏi ở tiêu đề giờ đây có thể được trả lời trực tiếp.

Chúng là sự hội tụ qua những con đường khác nhau.

Chúng cũng là các nhánh riêng biệt của cùng một vấn đề lớn hơn.

"Sự hội tụ" gọi tên thực tế mà cả hai đều chấp nhận: mô hình là không đáng tin cậy, và khung kiểm soát (harness) là nơi tạo ra trật tự.

"Các nhánh riêng biệt" gọi tên nền kinh tế chính trị (political economy) khác nhau mà qua đó thực tế được triển khai: Claude Code tin tưởng vào kỷ luật runtime hơn, trong khi Codex tin tưởng vào các lớp điều khiển rõ ràng hơn.

Các hệ thống chủ yếu dựa vào việc xếp chồng prompt (prompt stacking) để giữ ngữ cảnh cùng nhau nằm ở một vùng trung gian kém ổn định hơn. Chúng đã nhận ra rằng các mô hình sẽ quên và trôi dạt, vì vậy chúng thêm bộ nhớ, kỹ năng và nén bộ nhớ (compaction). Nhưng nếu quản trị ngữ cảnh vẫn tuân theo logic "tiêm trước, giải cứu sau" (inject first, rescue later), thì hệ thống vẫn chưa quyết định rõ ràng lớp nào sẽ nắm giữ trật tự.

Không có con đường nào vốn dĩ cao quý hơn. Câu hỏi thực sự là thế này: hệ thống của bạn đã sẵn sàng giam cầm sự không chắc chắn (uncertainty) ở lớp nào?

Vị trí của chiếc lồng đó quyết định hệ thống sẽ trở thành gì sau này.
