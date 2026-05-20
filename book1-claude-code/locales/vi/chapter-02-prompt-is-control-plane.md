# Chương 2 Prompt không phải là Tính cách, Prompt là Mặt phẳng Kiểm soát

## 2.1 Coi prompt là tính cách (persona) là một sự hiểu lầm phổ biến

Khi mọi người nghe nói đến "system prompt", trước tiên họ nghĩ đến những lời hoa mỹ quen thuộc: bạn là ai, bạn giỏi cái gì, lý tưởng nhất là có một tính cách ổn định. Cách đóng khung đó chỉ đủ cho các hệ thống chỉ trò chuyện (chat-only system) và rõ ràng là không đủ cho một tác nhân đọc tệp, gọi công cụ, chạm vào shell, xử lý quyền hạn và thực thi qua nhiều lượt. Tính cách (persona) trả lời cho câu hỏi "nó trông như thế nào"; mặt phẳng kiểm soát (control plane) trả lời cho câu hỏi "nó có thể làm gì, khi nào, điều gì xảy ra khi thất bại, ai chịu trách nhiệm dự phòng (fallback)". Chúng thuộc các lớp khác nhau.

Việc triển khai Claude Code cho thấy điều này một cách trực tiếp: system prompt của nó là một tập hợp phân lớp các khối hành vi — gần với một giao thức runtime (runtime protocol) hơn là tiểu sử của một nhân vật.

## 2.2 Trong nguồn, prompt của Claude Code được phân lớp ngay từ đầu

Trong `getSystemPrompt()` tại `src/constants/prompts.ts:444`, Claude Code trả về một mảng các phần (section), chứ không phải là một chuỗi hoàn chỉnh. Chi tiết này rất quan trọng. Một khi prompt trở thành đa khối (multi-block), hệ thống chính thức thừa nhận các ràng buộc khác biệt bên trong với những nhiệm vụ khác nhau.

Những phần này bao gồm ít nhất một vài danh mục.

Đầu tiên là danh tính và nhiệm vụ. Tại `src/constants/prompts.ts:175`, hệ thống tuyên bố nó là một tác nhân tương tác sử dụng các công cụ có sẵn để hoàn thành các tác vụ kỹ nghệ phần mềm, bao gồm cả các ràng buộc an toàn như không tự ý đoán các URL.

Tiếp theo là các quy tắc cấp hệ thống. Bắt đầu từ `src/constants/prompts.ts:186`, hệ thống định nghĩa rõ ràng:

- Người dùng có thể nhìn thấy đoạn văn bản nào
- Các lượt gọi công cụ có thể kích hoạt sự phê duyệt quyền hạn (permission approval)
- Các hành động bị từ chối không được thử lại một cách máy móc
- Các lời nhắc hệ thống có thể xuất hiện bên trong kết quả công cụ và tin nhắn của người dùng
- Ngữ cảnh có thể tự động được nén (compact)

Các quy tắc này chia sẻ một đặc tính rõ ràng: chúng không quan tâm liệu mô hình "trông giống một trợ lý thông minh" hay không. Chúng quan tâm liệu nó có phải là một trình thực thi có kỷ luật hay không. Đó là giọng điệu của mặt phẳng kiểm soát (control plane); sứ mệnh chính của nó là định nghĩa ranh giới.

Sau đó, bắt đầu từ `src/constants/prompts.ts:199`, là các hướng dẫn kỹ thuật để làm việc: không thêm yêu cầu một cách tùy tiện, không tối ưu hóa vượt quá thẩm quyền, không che giấu việc xác nhận (validation) thất bại chỉ để trông có vẻ trau chuốt, và không tự ý bịa ra các lớp trừu tượng nếu không cần thiết. Chúng có vẻ giống như các hướng dẫn về phong cách viết, nhưng chúng được liên kết chặt chẽ với các ràng buộc kỹ thuật. Một mô hình "tối ưu hóa mọi thứ một cách đầy thiện chí" có thể trông có vẻ nhiệt tình ở góc độ sản phẩm nhưng vẫn nguy hiểm ở góc độ kỹ thuật.

Vì vậy, chỉ riêng cấu trúc mã nguồn đã chỉ ra điều này: prompt của Claude Code được thiết kế để giữ hành vi của mô hình trong các ranh giới ở môi trường runtime phức tạp.

## 2.3 Giá trị của prompt không phải là bản thân văn bản, mà là cấu trúc ưu tiên

Nếu prompt chỉ tồn tại dưới dạng văn bản, điều đó vẫn chưa chứng minh được vị thế mặt phẳng kiểm soát của nó. Điều quyết định điều đó là thứ tự ưu tiên nghiêm ngặt (strict precedence).

Bạn có thể thấy điều này trong `buildEffectiveSystemPrompt()` tại `src/utils/systemPrompt.ts:28`, nơi các nguồn prompt được cấu thành theo thứ tự rõ ràng:

1. override system prompt (prompt hệ thống ghi đè)
2. coordinator system prompt (prompt hệ thống điều phối)
3. agent system prompt (prompt hệ thống tác nhân)
4. custom system prompt (prompt hệ thống tùy chỉnh)
5. default system prompt (prompt hệ thống mặc định)

Sau đó `appendSystemPrompt` (prompt hệ thống nối thêm) được nối thêm một cách đồng nhất.

Việc xử lý chế độ chủ động (proactive-mode) thậm chí còn trực tiếp hơn. Sau `src/utils/systemPrompt.ts:99`, khi prompt tác nhân và chế độ chủ động cùng tồn tại, prompt tác nhân không còn thay thế prompt mặc định nữa; nó được nối thêm vào phía sau. Một hiến pháp chung có thể được mở rộng bởi bản mô tả công việc, nhưng không được phép bị bản mô tả công việc đó xóa bỏ.

### Bộ khung: chuỗi ưu tiên lắp ráp prompt

```
// bộ khung: buildEffectiveSystemPrompt()  (src/utils/systemPrompt.ts:28)
sources = [override, coordinator, agent, custom, default]
base = first_present(sources)           // mức ưu tiên cao hơn sẽ thay thế hoàn toàn mặc định
if proactive_mode and agent:
    base = default + agent              // trường hợp đặc biệt: phân lớp, không thay thế
return base + appendSystemPrompt        // nối thêm luôn ở cuối cùng

assert exists unique base in sources                # baseline phải là duy nhất
assert precedence(override) > precedence(default)   # thứ tự được hardcode, không phải "bản ghi cuối cùng thắng"
assert appendSystemPrompt never replaces base       # append chỉ có thể nối thêm
```

Vi phạm bất kỳ điều nào trong số các ràng buộc bất biến (invariant) này và prompt sẽ xuống cấp thành một bảng vẽ bậy, nơi bất kỳ ai viết cuối cùng sẽ nắm quyền kiểm soát.

## 2.4 Prompt không phải là bản sao tĩnh; nó được kết nối với các hệ thống bộ nhớ

Nếu những điều trên đã nghe giống như một cuốn sổ tay hướng dẫn runtime, cách xử lý bộ nhớ (memory) và `CLAUDE.md` của Claude Code thậm chí còn làm rõ hơn: prompt ở đây là một điểm đầu vào (entry point) cho việc quản trị ngữ cảnh đầy đủ, chứ không chỉ là "một đoạn văn hiển thị cho mô hình".

Trong `getClaudeMds()` tại `src/utils/claudemd.ts:1153`, hệ thống thu thập các hướng dẫn dự án (project instructions), hướng dẫn cục bộ (local instructions), bộ nhớ đội ngũ (team memory) và bộ nhớ tự động (auto memory) vào một định dạng thống nhất rồi sau đó hợp nhất chúng vào ngữ cảnh liền kề prompt. Nó thậm chí còn gắn nhãn nguồn gốc một cách rõ ràng: hướng dẫn cấp dự án, hướng dẫn dự án riêng tư của người dùng, bộ nhớ đội ngũ được chia sẻ, hoặc bộ nhớ tự động được lưu trữ lâu dài qua các phiên (cross-session persisted auto memory).

Trong `buildMemoryLines()` tại `src/memdir/memdir.ts:187`, hệ thống biến chính các quy tắc ghi bộ nhớ thành một phần của prompt:

- Bộ nhớ là một hệ thống lưu trữ lâu dài dựa trên tệp (file-based persistence system)
- `MEMORY.md` là một chỉ mục (index), không phải phần thân văn bản
- Frontmatter nên được viết theo định dạng cụ thể
- Một số thông tin nhất định không được lưu lại
- Các kế hoạch và tác vụ không được lạm dụng làm các mục lưu trữ bộ nhớ

Điều này rất quan trọng. Nó mở rộng nhiệm vụ của prompt từ "ràng buộc hành vi hiện tại" sang "ràng buộc cách thức tri thức tương lai được lắng đọng". Điều này vượt ra ngoài kỹ nghệ prompt thông thường và gần hơn với một giao thức quản trị tri thức (knowledge-governance protocol) cho các bên tham gia môi trường runtime.

Nói cách khác, Claude Code không chỉ sử dụng prompt để định nghĩa "cách nói chuyện trong lượt này". Nó sử dụng prompt để định nghĩa "cách hình thành bộ nhớ tồn tại lâu dài". Một khi một hệ thống đạt đến giai đoạn này, prompt không còn đơn thuần là tông giọng nữa; nó trở thành quy chế (institution).

## 2.5 Một mặt phẳng kiểm soát thực sự phải bao gồm việc lưu đệm và chi phí tính toán

Hầu hết các cuộc thảo luận về prompt đều bỏ qua hiệu năng. Ý tưởng phổ biến là: prompt chỉ là văn bản được đưa vào mô hình, nên cứ viết là xong. Claude Code thực tế hơn: prompt cũng là chi phí tính toán (compute cost). Nó càng phức tạp và dễ biến động thì tỷ lệ trúng bộ đệm (cache hit rate) càng tệ, và runtime càng trở nên đắt đỏ cũng như chậm chạp.

Trong `src/constants/systemPromptSections.ts:16` và các dòng dưới, các phần prompt được chia thành:

- `systemPromptSection` có thể lưu đệm (cacheable)
- `DANGEROUS_uncachedSystemPromptSection` làm hỏng bộ đệm (cache-breaking)

`resolveSystemPromptSections()` ưu tiên tái sử dụng bộ đệm và chỉ tính toán lại khi cần thiết. `clearSystemPromptSections()` xóa trạng thái phần sau khi chạy lệnh `/clear` hoặc `/compact`.

Điều này có vẻ giống như việc tối ưu hóa, nhưng nó vẫn là thiết kế mặt phẳng kiểm soát (control-plane design). Một hệ thống prompt trong môi trường sản xuất không thể chỉ tối ưu hóa khả năng biểu đạt mà bỏ qua băng thông (throughput), độ trễ (latency) và hành vi của bộ đệm (cache behavior). Trong `getSystemPrompt()`, Claude Code thậm chí còn đặt các ranh giới rõ ràng giữa các phân đoạn prompt tĩnh và động sau `src/constants/prompts.ts:560`. That means design explicitly assumes some content is turn-stable while other content changes per turn; they must not be mixed in a way that burns cache.

Một khi hệ thống bắt đầu hỏi "phần nào của prompt làm vô hiệu hóa bộ đệm (invalidate cache)", nó đã ngừng coi prompt như một công việc viết lách (copywriting). Viết lách tối ưu hóa sự hoàn chỉnh của biểu đạt. Mặt phẳng kiểm soát tối ưu hóa khả năng quản trị, khả năng tái sử dụng và chi phí hành vi có thể dự đoán trước.

## 2.6 Người dùng có thể ghi đè prompt, nhưng không thể bỏ qua cấu trúc này

Claude Code không khóa chặt người dùng vào prompt mặc định. CLI hỗ trợ rõ ràng việc ghi đè (override) và nối thêm (append).

Sau `src/main.tsx:1342`, hệ thống xử lý các tùy chọn như `--system-prompt`, `--system-prompt-file`, `--append-system-prompt`, và `--append-system-prompt-file`. Người dùng hoàn toàn có thể đưa vào các quy tắc tùy chỉnh.

But one key point remains: regardless of override or append, final assembly still goes through `buildEffectiveSystemPrompt()`. So customization is allowed, order is not abandoned. Users can change content; system retains structure.

Tùy chỉnh không có cấu trúc thường suy thoái thành sự trôi dạt tùy tiện: một phần được thêm vào hôm nay, một phần khác bị loại bỏ ngày mai, và một tác nhân nào đó thay thế các ràng buộc cơ bản vào ngày kia. Hành vi khi đó bắt đầu trông giống như những thông báo truyền miệng tùy tiện (ad hoc). Claude Code chọn một con đường khác: cho phép người dùng sửa đổi, nhưng buộc các sửa đổi phải đi qua sự phân lớp và thứ tự ưu tiên cố định.

## 2.7 Tại sao prompt ở đây gần với hiến pháp hơn là các lời thoại hội thoại

Tổng hợp các phần trước lại và kết luận đã rõ ràng:

Prompt của Claude Code giống như một bản hiến pháp.

Lời thoại là những gì các nhân vật nói trên sân khấu. Một bản hiến pháp định nghĩa các ranh giới quyền lực, các mối quan hệ nghĩa vụ và việc xử lý ngoại lệ. Prompt của Claude Code gần với điều sau hơn vì nó thỏa mãn các điều kiện cấu trúc:

- Nó được phân lớp, không phải là một khối duy nhất (monolithic)
- Nó có thứ tự ưu tiên, chứ không phải "bản ghi mới nhất thắng"
- Nó tạo thành một mặt phẳng kiểm soát đầy đủ cùng với bộ nhớ, `CLAUDE.md`, các hướng dẫn tác nhân (agent instructions) và các hướng dẫn MCP (MCP instructions)
- Nó có cơ chế bộ đệm và phần động, chứ không phải là việc nối chuỗi văn bản tùy tiện
- Nó được liên kết chặt chẽ với runtime, chứ không phải lơ lửng bên ngoài hệ thống như đồ trang trí

Đó cũng là lý do tại sao việc "viết một prompt tốt" một cách cô lập có giá trị hạn chế. Câu hỏi khó hơn là prompt nằm ở đâu trong kiến trúc hệ thống, nó phối hợp với những module nào, và liệu nó có tham gia vào việc quản trị quyền hạn, trạng thái, ngữ cảnh và bộ nhớ dài hạn hay không. Nếu không có những câu trả lời đó, một cái gọi là prompt tốt thường chỉ chính xác tạm thời trong một kịch bản suôn sẻ duy nhất.

## 2.8 Nguyên lý thứ hai có thể trích xuất từ nguồn

Chương này có thể được nén lại trong một câu:

> Prompt chỉ có giá trị khi nó được tích hợp vào cấu trúc kiểm soát rõ ràng.

Mã nguồn Claude Code chứng minh điều này qua nhiều module:

- `constants/prompts.ts` cấu trúc prompt dưới dạng các khối kiểm soát được phân đoạn thay vị một lời tuyên bố duy nhất
- `utils/systemPrompt.ts` định nghĩa thứ tự ưu tiên nguồn nghiêm ngặt
- `utils/claudemd.ts` tích hợp dự án và bộ nhớ dài hạn vào việc lắp ráp ngữ cảnh
- `memdir/memdir.ts` sử dụng prompt để định nghĩa giao thức ghi bộ nhớ dài hạn
- `constants/systemPromptSections.ts` biến prompt thành các đối tượng runtime có thể lưu đệm, có thể vô hiệu hóa và có thể tính toán lại theo từng phần

Vì vậy, trong các hệ thống tác nhân trưởng thành, prompt không nên được hiểu là "những câu mở đầu để đưa mô hình vào vai". Nó là một văn bản quy chế sống động. Văn bản quy chế có thể rõ ràng, nhưng đặc tính quyết định của nó là tính thực thi (enforceability).

Chương tiếp theo sẽ chuyển sang một phần xương máu cấu trúc thậm chí còn khó hơn: vòng lặp truy vấn (query loop). Ngay cả mặt phẳng kiểm soát tốt nhất cuối cùng cũng phải hạ cánh bên trong các chu kỳ thực thi. Prompt định nghĩa ranh giới; vòng lặp quyết định số phận. Hệ thống cuối cùng trở thành cái gì thường được bộc lộ qua cách mỗi lượt tiếp tục, ngắt quãng và phục hồi.
