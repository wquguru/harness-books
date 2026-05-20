# Chương 6 Lỗi và Khôi phục: Một Hệ thống Agent tiếp tục Hoạt động sau Thất bại

## 6.1 Câu nói kém đáng tin cậy nhất trong ngành kỹ thuật là "trong điều kiện bình thường"

Nhiều tài liệu thiết kế chỉ mô tả "luồng thông thường (normal path)", như thể một luồng kịch bản thuận lợi (happy-path flow) đẹp đẽ có thể biến các lỗi thành thứ yếu. Một khi các hệ thống Agent (agent systems) đi vào thời gian chạy (runtime) thực tế, điều này sẽ đổ vỡ nhanh chóng: các mô hình bị cắt ngắn (truncated), các yêu cầu diễn ra quá lâu, các hook tạo ra vòng lặp vô tận, các công cụ bị gián đoạn, các luồng dự phòng (fallback paths) kích hoạt, và bản thân logic khôi phục cũng thất bại.

Mức độ trưởng thành của hệ thống không thể được đánh giá bằng việc hệ thống nghe có vẻ giống con người như thế nào khi hoạt động trơn tru; nó phải được đánh giá bằng việc các thất bại trông có giống như hành vi được kiểm soát của hệ thống hay không. Điểm mạnh của Claude Code ở đây là không giả vờ rằng lỗi là hiếm gặp. Mã nguồn liên tục phản ánh một giả định điềm tĩnh: lỗi là một phần của luồng chính, và khôi phục phải là cơ chế runtime được thiết kế sẵn.

## 6.2 `prompt too long` xảy ra theo chu kỳ, không phải là ngoại lệ

Đối với các Agent phiên làm việc dài (long-session agents), lỗi prompt quá dài (`prompt too long`) không phải là một trường hợp biên (edge case). Đó là một chu kỳ tất yếu sẽ đến. Coi nó là một ngoại lệ hiếm gặp là một lời mời để môi trường sản xuất sửa sai cho bạn.

File `query.ts` của Claude Code không coi đó là sự cố ngẫu nhiên. Nó có thể tạm thời giữ lại các lỗi này thay vì hiển thị ngay lập tức. Trong quá trình truyền luồng (streaming), logic giữ lại lỗi sẽ xác định các loại lỗi có thể khôi phục được bao gồm:

- prompt too long (prompt quá dài)
- media size error (lỗi kích thước phương tiện)
- max output tokens (lượng token đầu ra tối đa)

Ý nghĩa là: một số lỗi nên được đưa vào cơ chế khôi phục trước, sau đó chỉ hiển thị ra ngoài nếu quá trình khôi phục thất bại. Người dùng thường ít quan tâm đến loại lỗi thô hơn là việc liệu công việc có thể tiếp tục hay không.

Riêng đối với lỗi prompt quá dài, đầu tiên Claude Code sẽ thử phương án khôi phục ít tốn kém và ít phá hủy hơn. Nếu tính năng thu gọn context (context collapse) được bật, đầu tiên nó sẽ gọi `recoverFromOverflow()` để giải phóng các phần thu gọn đã được chuẩn bị sẵn (staged collapse); chỉ khi không đủ hiệu quả thì nó mới gọi `reactiveCompact.tryReactiveCompact()`. Quá trình khôi phục được phân tầng: dọn dẹp các phần tồn đọng đã biết trước, sau đó mới thực hiện nén context (compaction) toàn phần nặng hơn.

Trình tự này cực kỳ thực tế. Một cơ chế khôi phục tốt không giải quyết mọi lỗi bằng một chiếc búa khổng lồ duy nhất. Nó cố gắng bảo toàn context chi tiết trước và chỉ leo thang khi thực sự cần thiết.

## 6.3 Reactive compact: cơ chế khôi phục không được trở thành cỗ máy lặp vô hạn

Một sai lầm phổ biến trong các hệ thống khôi phục vừa ngây thơ vừa tốn kém: một khi lỗi được coi là "có thể khôi phục được", hệ thống cứ liên tục thử lại cho đến khi việc khôi phục biến thành một thảm họa tiêu tốn tài nguyên.

Claude Code phòng thủ rất rõ ràng trước điều này. Hai nơi trong `query.ts` chứng minh điều đó.

Đầu tiên là biến `hasAttemptedReactiveCompact`. Một khi nén phản ứng (reactive compact) đã được thử nghiệm, các thất bại cùng loại sẽ không được thử lại một cách mù quáng nữa. Nếu việc nén không giúp ích gì, việc lặp lại nén thường chỉ tái hiện lại cùng một thất bại dưới một hình thức khác.

Thứ hai là các cơ chế bảo vệ vòng lặp vô tận của stop-hook (stop-hook dead-loop guards). Các bình luận trong mã nguồn rất trực diện: nếu các stop hook chạy sau khi trạng thái prompt quá dài không thể khôi phục, vòng xoáy tử thần (death spirals) sẽ khả thi:

error -> hook blocking -> retry -> error -> hook blocking

Đây không phải là ngôn từ văn học; đó là kỹ thuật thực tế tàn nhẫn. Những lỗi nguy hiểm nhất thường là những nhánh nơi thất bại và khôi phục bắt đầu tự tái tạo lẫn nhau.

Vì vậy, khi lỗi prompt quá dài không thể khôi phục, Claude Code sẽ hiển thị lỗi trực tiếp và bỏ qua các stop hook. Việc tiếp tục quy trình chính thức ở đó chỉ đang nghi thức hóa thất bại.

## 6.4 `max_output_tokens`: khôi phục nên ưu tiên việc tiếp tục công việc

Nhiều sản phẩm mô hình xử lý việc bị cắt ngắn bằng sự lãng phí lịch sự: "Xin lỗi, tôi đã bị ngắt lời, để tôi tóm tắt lại." Nghe thì hay nhưng chẳng giúp ích được gì nhiều.

Hành vi của Claude Code sau dòng `src/query.ts:1185` hướng tới kỹ thuật hơn nhiều. Đầu tiên nó thử cách khôi phục chi phí thấp hơn: nếu giới hạn hiện tại là dè dặt, hãy tăng `maxOutputTokensOverride` và chạy lại chính yêu cầu đó. Không tin nhắn meta (meta message), không lời mở đầu lịch sự, chỉ là thêm một cơ hội nữa để hoàn thành nhiệm vụ.

Nếu giới hạn cao hơn vẫn thất bại, nó sẽ leo thang lên tầng thứ hai: đính kèm một tin nhắn meta của người dùng (meta user message) ngắn gọn nói rằng, trên thực tế:

continue directly; no apology; no recap; if cut mid-sentence, continue from that half sentence; split remaining work into smaller chunks.

Chỉ thị này mang tính hướng dẫn rất cao. Claude Code coi việc khôi phục là để duy trì tính liên tục của tác vụ, chứ không phải để giữ vẻ lịch sự xã giao. Trong các tác vụ dài, sự khác biệt này là rất lớn. Mỗi lần tóm tắt phần bị cắt bớt (truncation recap) sẽ đốt thêm ngân sách và làm tăng sự trôi lệch ngữ nghĩa (semantic drift). Cuối cùng, hệ thống dành nhiều lượt để tự tóm tắt chính mình thay vì thực hiện tác vụ.

Đối với lỗi `max_output_tokens`, khôi phục tốt thường là ưu tiên tiếp tục trước. Claude Code tối ưu hóa rõ ràng cho điều đó.

## 6.5 Auto-compact circuit breaker: hệ thống khôi phục cũng cần được quản trị

Các phần trước nói về "cách khôi phục một thất bại đơn lẻ." File `src/services/compact/autoCompact.ts` giải quyết một tầng khác: điều gì xảy ra nếu bản thân cơ chế khôi phục liên tục thất bại?

Câu trả lời trong mã nguồn rất đơn giản và chính xác: ngừng thử lại mãi mãi.

`AutoCompactTrackingState` theo dõi `consecutiveFailures` (các thất bại liên tiếp). Một khi số lần thất bại vượt quá ngưỡng, ngay cả khi `shouldAutoCompact` báo hiệu đã đến lúc cần nén, hệ thống vẫn sẽ bỏ qua việc nén trực tiếp. Các bình luận trong mã nguồn đề cập đến sự lãng phí lịch sử: các phiên làm việc từng đốt một lượng lớn cuộc gọi API cho việc tự động nén thất bại lặp đi lặp lại, vì vậy cần phải có một cầu dao tự ngắt (circuit breaker).

Kích hoạt cầu dao tự ngắt có nghĩa là thừa nhận phương pháp khôi phục hiện tại không hiệu quả trong trạng thái hiện tại. Các hệ thống trưởng thành không chỉ ghi lại các chỉ số thành công; chúng phải biết khi nào nên lùi bước trước thất bại lặp đi lặp lại. Hệ thống khôi phục không có phanh giống như những chiếc xe không phanh.

Nguyên tắc Kỹ thuật Harness ở đây rất cứng rắn và rõ ràng: bất kỳ sự khôi phục tự động nào cũng phải đếm được, bị giới hạn tần suất (rate-limited) và có thể ngắt được (breakable).

### Các bất biến của cầu dao tự ngắt (Circuit-breaker invariants)

```
assert withheld_error ∈ {prompt_too_long, media_size, max_output_tokens}  # recoverable set is fixed
assert hasAttemptedReactiveCompact ⇒ skip further reactive compact        # no self-loop
assert consecutiveFailures < MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES          # breaker engaged
assert compact aborted by user ⇏ summary_success                           # abort ≠ success
assert every withheld recoverable_error surfaces iff recovery exhausted    # withheld must exit
```

### Ma trận thất bại trên đường khôi phục (Recovery-path failure matrix)

| Thứ tự sự kiện | Trạng thái trước (Pre-state) | Tác nhân kích hoạt (Trigger) | Hành động tiếp theo (Next) | Ngưỡng (Threshold) |
|---|---|---|---|---|
| PTL → collapse | `stagedCollapse > 0` | `prompt_too_long` | `recoverFromOverflow()` | — |
| PTL → compact | `stagedCollapse = 0` | `prompt_too_long` | `tryReactiveCompact()` | một lần mỗi lượt (once per turn) |
| PTL → surface | `hasAttemptedReactiveCompact` | `prompt_too_long` | surface directly; skip stop hooks | — |
| compact PTL | compact input too long | inner `prompt_too_long` | `truncateHeadForPTLRetry()` | loại bỏ các vòng gọi API ban đầu theo phân đoạn (chunks) |
| MOT → cap↑ | cap < MAX | `max_output_tokens` | raise `maxOutputTokensOverride` | giới hạn ∈ {conservative, max} |
| MOT → continue | cap = MAX | `max_output_tokens` | append meta user msg, continue | không tóm tắt lại, không xin lỗi |
| autocompact streak | `consecutiveFailures` ≥ threshold | kích hoạt tiếp theo | bỏ qua nén, hiển thị lỗi trực tiếp | `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3` |
| user abort | đang truyền luồng với `tool_use` đang chờ xử lý | Esc | tiêu thụ dữ liệu còn lại + kết quả công cụ giả lập (`tool_result`) | sổ cái phải được đóng (ledger must close) |

## 6.6 Bản thân việc nén cũng có thể thất bại, vì vậy hành động khôi phục cần sự khôi phục của riêng nó

Hàm `compactConversation()` chứa một khoảnh khắc rất thực tế: bản thân các yêu cầu nén cũng có thể gặp lỗi prompt quá dài (`prompt too long`).

Có một sự hài hước đen tối ở đây. Hệ thống gửi các yêu cầu tóm tắt để giảm bớt context, sau đó các yêu cầu tóm tắt lại thất bại vì context quá lớn. Nhiều thiết kế che giấu tình huống này vì nó gây bối rối. Nhưng các hệ thống kỹ thuật ưu tiên sự sống sót hơn sự thanh lịch.

Claude Code xử lý việc này bằng hàm `truncateHeadForPTLRetry()` trong file `compact.ts`. Khi đầu vào nén quá lớn, nó sẽ cắt bỏ các vòng gọi API cũ hơn theo từng phân đoạn từ phần đầu (head) và thử lại việc nén, ngăn người dùng bị mắc kẹt trong vòng lặp "không thể nén phần nén".

Sự đánh đổi ở đây là rõ ràng: giải pháp dự phòng này gây mất mát dữ liệu và có thể làm mất lịch sử, nhưng nó ưu tiên việc không làm tắc nghẽn trải nghiệm của người dùng. Các bình luận trong mã nguồn mô tả đây là lối thoát hiểm cuối cùng (last-resort escape hatch).

Giá trị của lựa chọn này: nó không phủ nhận các giới hạn cứng. Khi hệ thống đang nghẹn thở, ưu tiên hàng đầu là khôi phục hơi thở, sau đó mới là bảo toàn lịch sử với độ chính xác cao.

![Các nhánh quyết định khôi phục của Claude Code](diagrams/diag-ch06-01-recovery-decision-paths.png)

![Các giải pháp dự phòng nén của Claude Code](diagrams/diag-ch06-02-compact-fallbacks.png)

## 6.7 Ngữ nghĩa hủy bỏ: ngắt quãng là một phần của khôi phục

Nhiều đội ngũ chỉ phân loại việc hủy bỏ (abort) vào phần trải nghiệm người dùng (UX). Về mặt runtime, các ngắt quãng (interrupts) là các trạng thái thất bại yêu cầu đóng ngữ nghĩa (semantic closure) một cách chính xác.

Claude Code xử lý việc này ở hai tầng. Trong `query.ts`, việc ngắt luồng truyền dữ liệu sẽ tiêu thụ `StreamingToolExecutor.getRemainingResults()` và tạo ra các kết quả công cụ giả lập cho các cuộc gọi đã phát ra nhưng chưa hoàn thành, ngăn chặn các cam kết lơ lửng. Trong `compact.ts`, bộ điều khiển hủy bỏ nén (compact abort controller) được truyền vào Agent nhánh (forked agent) và lỗi `APIUserAbortError` được xử lý rõ ràng, ngăn việc "nén bị hủy bởi phím Esc của người dùng" được tính là một lần tóm tắt thành công.

Sự ngắt quãng không đơn thuần là "người dùng ngừng đọc"; đó là một quá trình chuyển đổi trạng thái đòi hỏi sự đóng lại đúng đắn. Việc khôi phục xử lý các ngoại lệ nhưng bỏ qua sự ngắt quãng sẽ để lại các vết thực thi (execution traces) bị phá vỡ một nửa về mặt ngữ nghĩa.

## 6.8 Xử lý lỗi bảo vệ tính nhất quán mạch lạc của quá trình thực thi

Triết lý khôi phục của Claude Code có một mục tiêu thường bị bỏ qua: bảo vệ tính nhất quán mạch lạc của quá trình thực thi (narrative consistency of execution) — liệu hệ thống có còn khả năng giải thích những gì nó đã cố gắng làm, tại sao nó thất bại, đường dẫn khôi phục nào đã được sử dụng, và liệu bây giờ nó đang tiếp tục, dừng lại hay chuyển hướng hay không.

Các trường dữ liệu như `transition.reason`, `maxOutputTokensRecoveryCount`, `hasAttemptedReactiveCompact`, ranh giới nén (compact boundaries), và các tin nhắn lỗi tổng hợp trong `query.ts` tồn tại để giữ cho mạch tự sự này không bị đứt quãng — chúng là các cơ chế chống mất trí nhớ (anti-amnesia mechanisms). Không có tính nhất quán mạch lạc, các hệ thống liên tục đưa ra văn bản trong khi bên trong đang phân rã: người dùng nhìn thấy nội dung rác, bộ phận vận hành thấy các vòng lặp thử lại hook và thử lại nén với mối quan hệ nhân quả không rõ ràng, và các đội ngũ không còn giải thích được hệ thống thực sự đã trải qua những gì. Việc khôi phục không chỉ sửa các lỗi mà còn sửa cả khả năng tự giải thích (self-explainability) của hệ thống; một khi khả năng tự giải thích bị phá vỡ, đối tượng kỹ thuật sẽ bị suy thoái thành phép thuật mơ hồ.

## 6.9 Nguyên tắc thứ sáu rút ra từ mã nguồn

Chương này có thể được nén lại thành một câu duy nhất:

> Một hệ thống Agent thể hiện độ tin cậy của mình bằng cách duy trì một trình tự thực thi có thể giải thích được, có ranh giới và có thể tiếp tục được sau khi xảy ra lỗi.

Mã nguồn của Claude Code hỗ trợ điều này thông qua các điểm mấu chốt:

- `query.ts` giữ lại các lỗi có thể khôi phục để biến đổi ở cấp độ nhánh (branch-level transformation) trước khi đưa lên bề mặt
- Việc khôi phục prompt quá dài phân tầng giải phóng thu gọn (collapse drain) trước nén phản ứng, sắp xếp theo chi phí và mức độ phá hủy
- Biến `hasAttemptedReactiveCompact` và cơ chế bảo vệ stop-hook ngăn ngừa các vòng lặp khôi phục vô hạn
- Việc xử lý `max_output_tokens` leo thang giới hạn trước và ưu tiên tiếp tục trực tiếp hơn là tóm tắt lại một cách lịch sự
- File `autoCompact.ts` theo dõi các thất bại liên tiếp và thực thi ngắt mạch
- File `compact.ts` bao gồm giải pháp dự phòng cho thất bại do prompt quá dài của chính quá trình nén

Các nguyên tắc có thể mang theo: phân tầng các đường dẫn khôi phục thay vì sử dụng một chiếc búa nặng nề duy nhất; logic khôi phục phải an toàn với vòng lặp; khôi phục tự động cần bộ đếm và cầu dao tự ngắt; sau khi bị cắt ngắn, tiếp tục tốt hơn tóm tắt lại; ngắt quãng là trạng thái thất bại ngữ nghĩa yêu cầu đóng lại; độ tin cậy được chứng minh bằng việc hệ thống có còn tự giải thích được sau lỗi hay không.

Chương tiếp theo sẽ chuyển sang một nhóm vấn đề khó hơn: đa Agent và xác thực. Khi hệ thống chuyển từ "một Agent tự khôi phục chính mình" sang "một Agent giao việc và Agent khác xác thực," lỗi và khôi phục không còn thuần túy là mối bận tâm của một luồng đơn lẻ nữa mà trở thành thiết kế tổ chức.
