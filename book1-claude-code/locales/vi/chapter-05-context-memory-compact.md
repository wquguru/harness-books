# Chương 5 Quản trị Ngữ cảnh: Bộ nhớ, CLAUDE.md và Rút gọn (Compact) như một Cơ chế Ngân sách

## 5.1 Khi ngữ cảnh tăng lên, các hệ thống dễ nảy sinh một ảo tưởng cấp thấp

"Nhiều thông tin hơn giúp hệ thống thông minh hơn" là một lầm tưởng nguy hiểm. Các hệ thống agent không phải là thư viện; ngữ cảnh không phải là một kho chứa hàng nơi "lưu trữ" đồng nghĩa với "sở hữu". Đó là một loại ngân sách đắt đỏ, dễ bị lạm phát và tự làm ô nhiễm. Mã nguồn Claude Code không có chỗ cho sự cảm tính về việc này: tải cái gì, cắt ngắn cái gì, bảo tồn cái gì trong dài hạn và tóm tắt cái gì trong ngắn hạn là những quyết định quản trị runtime nghiêm túc.

Vì vậy, chương này đặt câu hỏi: làm thế nào Claude Code tránh bị đè bẹp bởi những gì nó ghi nhớ? "Nhớ nhiều hơn" và "quản trị bộ nhớ" trông có vẻ gần gũi nhưng về mặt kỹ thuật, chúng là hai cơ chế hoàn toàn khác nhau.

## 5.2 Hệ thống CLAUDE.md: Các hướng dẫn tồn tại lâu dài không thể trộn lẫn với cuộc trò chuyện tạm thời

Tại phần đầu của file `src/utils/claudemd.ts`, Claude Code đã định nghĩa rõ ràng các lớp bộ nhớ. Các nguồn hướng dẫn được chia thành:

- bộ nhớ được quản lý (managed memory), ví dụ `/etc/claude-code/CLAUDE.md`
- bộ nhớ người dùng (user memory), ví dụ `~/.claude/CLAUDE.md`
- bộ nhớ dự án (project memory), ví dụ như tệp root `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md`
- bộ nhớ cục bộ (local memory), ví dụ `CLAUDE.local.md`

Các tệp này được tải theo thứ tự ưu tiên và độ gần của thư mục. Các quy tắc dự án nằm gần thư mục làm việc hiện tại hơn sẽ được ưu tiên cao hơn. Các quy tắc riêng tư và cục bộ hơn được tải sau, do đó được đặt gần hơn với tiêu điểm chú ý của mô hình (attention front).

Điều này rất quan trọng. Nó cho thấy Claude Code từ chối pha trộn chính sách cộng tác tồn tại lâu dài với ngữ cảnh trò chuyện tạm thời. Các chuẩn mực của nhóm, sở thích cá nhân và các ràng buộc của kho lưu trữ tồn tại lâu hơn bất kỳ tin nhắn riêng lẻ nào của người dùng. Nếu bạn ép tất cả chúng vào lịch sử trò chuyện, hệ thống sẽ dao động giữa hai thái cực tồi tệ: hoặc là tiêm lại (reinject) mọi thứ ở mỗi lượt (lãng phí ngữ cảnh), hoặc là phụ thuộc vào khả năng tự nhớ lại của mô hình (cuối cùng sẽ thất bại).

File `claudemd.ts` giải quyết vấn đề này bằng cách làm cho các quy tắc ổn định có thể khám phá được, được phân lớp và có thể cấu thành nên các hệ thống hướng dẫn bền vững. Một chi tiết rất đáng chú ý: nó hỗ trợ cú pháp `@include`, nhưng chỉ dành cho các phần mở rộng tệp văn bản được cho phép rõ ràng. Điều này cho thấy thiết kế đang cân bằng giữa sự tiện lợi và một kiểu lỗi phổ biến: vô tình đưa vào các tệp nhị phân (binaries), tài liệu khổng lồ hoặc các sản phẩm phụ gây độc cho prompt (prompt-toxic artifacts).

Đó là sự tiết chế thực tế. Trước tiên, hệ thống sẽ tự hỏi: điều gì xứng đáng được đưa vào bộ nhớ, và điều gì sẽ trở thành ô nhiễm nếu được nhận vào?

## 5.3 MEMORY.md là một chỉ mục, không phải một cuốn nhật ký

Nếu `CLAUDE.md` quản trị lớp chính sách, thì `memdir` quản trị bộ nhớ bền vững ở mức độ chi tiết (fine-grained persistent memory). Trong file `src/memdir/memdir.ts`, một quyết định thiết kế rất đáng để xem xét lại: `ENTRYPOINT_NAME` is `MEMORY.md`, nhưng nó không được thiết kế để đổ trực tiếp nội dung vào. Nó được quy định rõ ràng là một chỉ mục (index).

Hàm `buildMemoryLines()` thiết lập việc ghi nhớ dưới dạng hai bước:

1. ghi nhớ cụ thể vào các tệp chuyên dụng
2. thêm các con trỏ một dòng (one-line pointers) trong tệp `MEMORY.md`

Tại sao lại cần bước bổ dung này? Bởi vì các tệp điểm bắt đầu (entrypoint files) được tải thường xuyên. Một khi chúng bị phình to, ngữ cảnh sẽ dần bị kéo trì lại bởi sức nặng của chỉ mục.

Đó là lý do tại sao `memdir.ts` đặt các giới hạn cứng: `MAX_ENTRYPOINT_LINES = 200` và `MAX_ENTRYPOINT_BYTES = 25_000`. Vượt quá những giới hạn này, runtime sẽ kích hoạt `truncateEntrypointContent()` và nối thêm một cảnh báo rõ ràng: chỉ thực hiện tải một phần; hãy chuyển thông tin chi tiết vào các tệp chủ đề (topic files).

Thiết kế này mang lại cảm giác được tạo ra bởi một người đã chứng kiến quá nhiều chỉ mục bị mất kiểm soát. Nó không tin tưởng rằng tất cả mọi người sẽ luôn giữ nội dung ngắn gọn, vì vậy nó bắt buộc "điểm bắt đầu phải luôn ngắn". Một khi tệp bắt đầu cố gắng vừa làm mục lục vừa làm toàn văn, cuối cùng nó sẽ không thể làm tốt cả hai.

Từ góc độ Kỹ thuật Khung kiểm soát (Harness Engineering), nguyên lý này rất rõ ràng: bộ nhớ dài hạn phải được chia thành điểm bắt đầu (entrypoint) và phần thân (body). Điểm bắt đầu cung cấp khả năng định địa chỉ với chi phí thấp; phần thân mang nội dung dày đặc. Trộn lẫn chúng và điểm bắt đầu sẽ thất bại, khi đó hệ thống bộ nhớ sẽ chỉ còn mang tính chất trang trí.

## 5.4 Bộ nhớ phiên: Tính liên tục ngắn hạn không thể giải quyết bằng cách nhồi nhét nhật ký trò chuyện

Chỉ riêng bộ nhớ dài hạn là không đủ. Vấn đề thực tế khó khăn nhất trong các phiên làm việc của agent thường là "chính xác thì chúng ta đã ở đâu trước lượt này?". Đó là vấn đề duy trì tính liên tục (continuity) bên trong một phiên làm việc.

Claude Code xây dựng các mẫu chuyên dụng cho việc này trong `src/services/SessionMemory/prompts.ts`. Các phần mặc định bao gồm:

- `Current State` (Trạng thái hiện tại)
- `Task specification` (Định nghĩa tác vụ)
- `Files and Functions` (Tệp và Hàm)
- `Workflow` (Quy trình làm việc)
- `Errors & Corrections` (Lỗi & Sửa lỗi)
- `Codebase and System Documentation` (Cơ sở mã nguồn và Tài liệu hệ thống)
- `Learnings` (Bài học kinh nghiệm)
- `Key results` (Kết quả chính)
- `Worklog` (Nhật ký công việc)

Những phần này rõ ràng không phải dùng để ghi nhật ký hành trình. Chúng theo dõi trạng thái, cạm bẫy, các tệp đã thay đổi và các bước hành động tiếp theo để duy trì tính liên tục. Giọng điệu của prompt cập nhật cũng rõ ràng không kém:

- Chỉ sử dụng công cụ Edit để cập nhật tệp ghi chú
- Không nói về bản thân việc ghi chép ghi chú
- Không thay đổi cấu trúc mẫu (template structure)
- Giữ `Current State` đồng bộ với công việc mới nhất
- Giữ cho mỗi phần luôn cô đọng nhưng phải có ý thức về ngân sách (budget-aware)

Điều này có nghĩa là bộ nhớ phiên (session memory) trong Claude Code không phải là "lưu một bản sao khác của lịch sử trò chuyện". Nó chắt lọc phiên làm việc thành một bản tóm tắt vận hành để tiếp tục công việc. Nó không tìm cách phát lại toàn bộ; nó tìm kiếm cấu trúc tối thiểu cần thiết để tiếp tục làm việc.

Ngoài ra còn có một chi tiết mang tính thực tiễn cao: file `prompts.ts` thiết lập `MAX_SECTION_LENGTH = 2000` và `MAX_TOTAL_SESSION_MEMORY_TOKENS = 12000`. Khi vượt quá ngân sách, runtime sẽ yêu cầu cô đọng mạnh mẽ, với sự ưu tiên rõ ràng dành cho `Current State` và `Errors & Corrections`.

Điều này nói lên nhiều điều. Các hệ thống trưởng thành coi việc "bảo tồn những gì hữu ích nhất để tiếp tục" là một phẩm chất. Ngân sách ngữ cảnh là bộ nhớ làm việc (working memory), và bộ nhớ làm việc phải luôn ở trạng thái có thể vận hành được.

## 5.5 Tự động rút gọn (Autocompact): Quản trị ngữ cảnh trước hết là quản trị ngân sách

Đến thời điểm này chúng ta đã có các quy tắc dài hạn, bộ nhớ bền vững và bộ nhớ phiên. Ngữ cảnh vẫn tiếp tục phình to. Vì vậy, trong file `src/services/compact/autoCompact.ts`, Claude Code thừa nhận một thực tế khác: bất kể chất lượng tổ chức ra sao, các phiên làm việc đủ dài sẽ tiếp cận các giới hạn cửa sổ ngữ cảnh (context window).

Hàm `getEffectiveContextWindowSize()` trước tiên sẽ trừ đi ngân sách đầu ra được dự phòng để tạo tóm tắt. `MAX_OUTPUT_TOKENS_FOR_SUMMARY` dự phòng trực tiếp 20.000 token. Runtime giả định rằng chính quá trình rút gọn cũng tiêu tốn ngân sách và không bao giờ đợi cho đến khi lượng oxy gần cạn kiệt.

Sau đó, `getAutoCompactThreshold()` trừ đi thêm `AUTOCOMPACT_BUFFER_TOKENS = 13_000` nữa. Các ngưỡng cảnh báo, ngưỡng lỗi và dự phòng rút gọn thủ công đều có các bộ đệm (buffers) chuyên dụng.

Logic rất đơn giản: quản trị ngữ cảnh phải dự phòng trước chỗ trống cho sự thất bại và khôi phục. Các hệ thống không dự phòng gì có thể trông có vẻ tiết kiệm trong các trường hợp bình thường nhưng thực chất chỉ đang trì hoãn việc thanh toán rủi ro sang các lượt sau.

### Các ngưỡng ngân sách (Budget thresholds)

| Tên | Giá trị | Mục đích | Nguồn |
|---|---|---|---|
| `MAX_ENTRYPOINT_LINES` | 200 | giới hạn dòng cho chỉ mục `MEMORY.md` | `memdir/memdir.ts` |
| `MAX_ENTRYPOINT_BYTES` | 25_000 | giới hạn byte cho tệp chỉ mục | `memdir/memdir.ts` |
| `MAX_SECTION_LENGTH` | 2_000 | giới hạn mỗi phần trong bộ nhớ phiên | `SessionMemory/prompts.ts` |
| `MAX_TOTAL_SESSION_MEMORY_TOKENS` | 12_000 | tổng ngân sách cho bộ nhớ phiên | `SessionMemory/prompts.ts` |
| `MAX_OUTPUT_TOKENS_FOR_SUMMARY` | 20_000 | dự phòng đầu ra cho tóm tắt rút gọn | `compact/autoCompact.ts` |
| `AUTOCOMPACT_BUFFER_TOKENS` | 13_000 | bộ đệm cảnh báo sớm tự động rút gọn | `compact/autoCompact.ts` |
| `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES` | 3 | ngưỡng cầu dao ngắt mạch (circuit-breaker) | `compact/autoCompact.ts` |

Đối tượng `AutoCompactTrackingState` cũng tiết lộ nhiều điều. Nó không chỉ theo dõi trạng thái `compacted` (đã rút gọn), mà còn theo dõi `turnCounter`, `turnId` và `consecutiveFailures`. Do đó, tự động rút gọn là một hành vi runtime được theo dõi sát sao, có thể thất bại và có thể bị giới hạn tần suất (rate-limited).

Mã nguồn thậm chí còn lưu ý một bài học xương máu: một lượng lớn các cuộc gọi API từng bị lãng phí do lỗi tự động rút gọn lặp đi lặp lại, vì thế `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3` đi kèm với một cầu dao ngắt mạch sau đó. Bạn có thể thất bại, nhưng bạn không được phép thất bại vô hạn mà không lưu lại lịch sử.

## 5.6 compactConversation() cho thấy các bản tóm tắt phải xây dựng lại ngữ cảnh làm việc

Nhiều người nghe thấy rút gọn (compact) và cho rằng nó là "tóm tắt lại cuộc trò chuyện trước đó". Claude Code làm được nhiều hơn thế. Trong hàm `compactConversation()` bên trong `src/services/compact/compact.ts`, runtime phân rã ngữ cảnh cũ, tóm tắt, sau đó tiêm lại (reinject) các tệp đính kèm runtime (runtime attachments) cần thiết để xây dựng lại một thế giới sau rút gọn vẫn có thể tiếp tục hoạt động.

Trước tiên, hãy nhìn vào quy trình làm sạch trước khi tóm tắt. Hàm `stripImagesFromMessages()` thay thế hình ảnh và tài liệu bằng các dấu đánh dấu như `[image]` và `[document]`. Hàm `stripReinjectedAttachments()` loại bỏ các tệp đính kèm sẽ được tiêm lại sau đó để tránh lãng phí token. Chỉ riêng hai hành động này đã cho thấy quá trình rút gọn chủ động loại bỏ nội dung có chi phí token cao và giá trị tóm tắt thấp.

Bây giờ, hãy nhìn vào cách xử lý lỗi khi tóm tắt. Mã nguồn bao gồm hàm `truncateHeadForPTLRetry()` cho trường hợp trớ trêu khi chính yêu cầu rút gọn lại gặp phải lỗi prompt quá dài (prompt-too-long). Hệ thống thừa nhận không chỉ lộ trình chính (main path) mới có thể bùng nổ, mà công cụ giải cứu cũng có thể bùng nổ.

Sau khi rút gọn thành công, Claude Code không chỉ giữ lại một dòng tóm tắt duy nhất. Nó còn:

- xóa bỏ trạng thái `readFileState` cũ đã lỗi thời
- tái tạo các tệp đính kèm sau rút gọn (post-compact file attachments)
- tiêm lại các tệp đính kèm kế hoạch (plan attachments)
- tiêm lại các tệp đính kèm chế độ kế hoạch (plan mode attachments)
- tiêm lại các tệp đính kèm kỹ năng đã gọi (invoked-skills attachments)
- tiêm lại các công cụ bị hoãn, danh sách agent và tệp đính kèm MCP instruction delta
- chạy các hook bắt đầu phiên và các hook sau rút gọn
- ghi các tin nhắn ranh giới rút gọn (compact boundary messages) cùng số lượng token trước khi rút gọn và siêu dữ liệu ranh giới

Tóm lại, rút gọn (compact) trong Claude Code là một quá trình khởi động lại có kiểm soát (controlled reboot), chứ không phải là tóm tắt trò chuyện. Ngữ cảnh cũ được dịch sang một lớp nền vận hành mới (operating substrate). Nhiều hệ thống chỉ thực hiện một nửa đầu tiên, sau đó phát hiện ra rằng sau khi rút gọn, chúng chỉ "nhớ mang máng" nhưng đã làm mất đi trạng thái công cụ, trạng thái kế hoạch và trạng thái tệp đính kèm, dẫn đến việc phải mất nhiều lượt hội thoại sau đó để tự định vị lại bản thân.

## 5.7 Quản trị ngữ cảnh là về việc bảo tồn ngữ nghĩa công việc

Nếu bạn đọc nửa sau của file `compact.ts`, một thiên hướng nhất quán sẽ xuất hiện: Claude Code ưu tiên bảo tồn ngữ nghĩa công việc (working semantics).

Nó khôi phục các tệp đính kèm được truy cập gần đây vì chúng mã hóa thực tế công việc tại chỗ. Nó khôi phục chế độ kế hoạch (plan mode) vì nếu không, mô hình có thể quên rằng chúng vẫn đang hoạt động dưới kỷ luật lập kế hoạch. Nó giữ lại nội dung của kỹ năng đã gọi nhưng giới hạn token cho từng kỹ năng để giai đoạn sau rút gọn không bị chiếm đoạt bởi các gói tải trọng kỹ năng (skill payloads).

Một cụm từ trong mã nguồn đã nắm bắt tốt điều này: cắt ngắn từng kỹ năng tốt hơn là loại bỏ hoàn toàn (per-skill truncation beats dropping). Ngây cả khi cắt giảm, hãy giữ lại các ràng buộc dẫn đầu quan trọng (leading constraints) thay vì bỏ đi toàn bộ các khối. Đó là quản trị (governance), không phải là sự hạn chế thô bạo (brute throttling). Sự hạn chế thô bạo sẽ cắt giảm một cách mù quáng. Quản trị quyết định cái gì cần cắt bỏ và cái gì cần giữ lại.

Một bài học lâu bền rút ra là: các hệ thống ngữ cảnh nên ưu tiên bảo tồn ngữ nghĩa hành động (action semantics), chứ không phải bảo tồn lượng thông tin hiển thị cao nhất. Các đặc tính của tệp, kế hoạch hiện tại, các sửa lỗi và các ràng buộc kỹ năng sẽ trực tiếp quyết định liệu hành động tiếp theo có thể chính xác hay không. Lịch sử trò chuyện dài lặp đi lặp lại và dữ liệu runtime dễ dàng truy xuất không xứng đáng có một vị trí vĩnh viễn.

## 5.8 Nguyên lý thứ năm có thể trích xuất từ mã nguồn

Chương này có thể được tóm gọn trong một câu duy nhất:

> Ngữ cảnh là bộ nhớ làm việc. Quản trị tồn tại để giữ cho hệ thống có thể tiếp tục công việc.

Mã nguồn Claude Code hỗ trợ điều này trên nhiều lớp khác nhau:

- `claudemd.ts` tải các hướng dẫn tồn tại lâu dài theo các lớp, tách biệt các quy tắc ổn định khỏi cuộc hội thoại tạm thời
- `memdir.ts` định nghĩa `MEMORY.md` như một chỉ mục và cắt ngắn cứng nó, bắt buộc điểm bắt đầu phải ngắn gọn và có khả năng định địa chỉ
- `SessionMemory/prompts.ts` cấu trúc tính liên tục ngắn hạn bằng mẫu cố định kết hợp với ngân sách cho từng phần và ngân sách toàn cục
- `autoCompact.ts` dự phòng ngân sách tóm tắt, bộ đệm và cầu dao ngắt mạch khi thất bại, xử lý việc vận hành cửa sổ ngữ cảnh như một hoạt động quản lý rủi ro ngân sách
- `compact.ts` khôi phục kế hoạch, tệp tin, kỹ năng, tệp đính kèm công cụ và trạng thái hook sau khi tóm tắt, cho thấy việc rút gọn nhằm xây dựng lại ngữ nghĩa làm việc chứ không chỉ tạo ra các bản tóm tắt đẹp đẽ

Các nguyên lý kỹ thuật có thể di động được: phân lớp các quy tắc dài hạn, bộ nhớ bền vững và duy trì tính liên tục của phiên thay vì trộn lẫn chúng; giữ cho các sản phẩm dạng chỉ mục luôn nhỏ gọn; tóm tắt phiên phục vụ cho việc tiếp tục công việc chứ không phải lưu giữ lại toàn bộ hồi ức; rút gọn là một lộ trình cốt lõi; ngữ cảnh sau rút gọn phải bảo tồn các ngữ nghĩa runtime, chứ không chỉ là bề mặt ngôn ngữ.

Chương tiếp theo sẽ đặt câu hỏi điều gì xảy ra khi hệ thống quản trị này chạm tới các giới hạn cứng: prompt quá dài, số lượng token đầu ra tối đa, các vòng lặp vô hạn của hook và các nhánh khôi phục cạnh tranh nhau. Đó là nơi bạn cuối cùng có thể biết được một hệ thống là đang "hy vọng không có gì đổ vỡ" hay "được thiết kế để tiếp tục hoạt động sau khi đổ vỡ".
