# Chương 7 Công việc Đa Agent và Xác minh: Quản lý sự Không ổn định thông qua Phân công Lao động

## 7.1 Vượt qua một giới hạn nhất định, câu hỏi không phải là "liệu một agent có thể làm được không" mà là "công việc nên được phân chia như thế nào"

Sự ma sát khi sử dụng một agent đơn lẻ (single-agent friction) có thể được che giấu bằng sự kiên nhẫn, nhưng một khi các tác vụ lớn dần lên, các khâu nghiên cứu (research), triển khai (implementation) và xác minh (verification) sẽ dồn hết vào một chuỗi ngữ cảnh (context chain) duy nhất, cạnh tranh nhau về ngân sách (budget), sự chú ý và trung tâm cốt truyện. Đa agent (multi-agent) trông có vẻ là một câu trả lời hiển nhiên, nhưng nó không hề rẻ: tính song song không bị ràng buộc chỉ sao chép lại sự hỗn loạn của một agent đơn lẻ. Khó khăn thực sự là cô lập sự không ổn định của từng agent trong khi vẫn kết hợp các kết quả đầu ra một cách mạch lạc.

Mã nguồn Claude Code rất thực tế ở điểm này: nó không coi các subagent (agent phụ) như là "một cửa sổ chat khác". Nó coi chúng như các tiến trình thực thi được quản lý (managed execution processes) với các ranh giới bộ đệm (cache boundaries), ranh giới trạng thái (state boundaries) rõ ràng, cùng các nhiệm vụ xác minh và trách nhiệm dọn dẹp.

## 7.2 Nguyên lý đầu tiên của các agent phân nhánh (forked agents) là an toàn bộ đệm (cache safety)

Ở phần đầu của file `src/utils/forkedAgent.ts`, một chú thích đã nêu chính xác các nhiệm vụ tiện ích của agent phân nhánh:

1. chia sẻ các tham số quan trọng đối với cache (cache-critical params) với parent để đảm bảo tỷ lệ trúng bộ đệm prompt (prompt-cache hits)
2. theo dõi mức độ sử dụng trong toàn bộ vòng lặp truy vấn (query loop)
3. ghi lại các chỉ số đo lường (metrics)
4. cô lập trạng thái có thể thay đổi (mutable state) để tránh làm ảnh hưởng đến vòng lặp parent

Trong số đó, việc chia sẻ các tham số quan trọng đối với cache xuất hiện đầu tiên. Điều đó không phải là ngẫu nhiên. Nó có nghĩa là việc phân nhánh (fork) là một sự rẽ nhánh được kiểm soát bởi runtime. Nếu đó là sự rẽ nhánh, các tham số bắt buộc phải giữ tính nhất quán với parent là vô cùng quan trọng; nếu không, việc tái sử dụng cache của prompt (prompt-cache) sẽ thất bại, kéo theo cả chi phí lẫn độ trễ đều trở nên tồi tệ hơn.

Các thuộc tính của đối tượng `CacheSafeParams` bao gồm rõ ràng:

- systemPrompt
- userContext
- systemContext
- toolUseContext
- forkContextMessages

Mã nguồn cũng cảnh báo việc thay đổi tùy tiện `maxOutputTokens`, vì cấu hình tư duy (thinking configuration) có thể thay đổi và cấu hình tư duy là một phần của các khóa cache (cache keys).

Điều này cho thấy đa agent trước hết là một bài toán kinh tế học runtime. Nếu mỗi agent con (child agent) đốt lại ngữ cảnh của parent từ đầu, những gì trông giống như sự tăng tốc song song thực chất là một sự lãng phí song song. Mối quan tâm hàng đầu của Claude Code trong các lộ trình phân nhánh (fork paths) là duy trì kỷ luật bộ đệm (cache discipline).

### Khung xương (Skeleton): forkAgent()

```
// skeleton: forkAgent()  (src/utils/forkedAgent.ts, src/utils/createSubagentContext.ts)
params = CacheSafeParams {
    systemPrompt, userContext, systemContext,
    toolUseContext, forkContextMessages        // phải khớp với parent để duy trì prompt-cache hits
}
ctx = createSubagentContext(parent):
    readFileState  := clone(parent.readFileState)              // được cô lập theo mặc định
    abortController := new ChildAbortController(parent)        // bộ kiểm soát con được liên kết với parent
    getAppState    := wrap(parent.getAppState, suppress_prompt)
    setAppState    := noop                                     // chỉ đọc theo mặc định
    nestedMemoryAttachmentTriggers := new Set()
    loadedNestedMemoryPaths         := new Set()
if opt_in.shareAbortController:  ctx.abortController := parent.abortController
if opt_in.shareSetAppState:      ctx.setAppState      := parent.setAppState
hooks.fire(SubagentStart, { agent_id, agent_type })
track_usage(parent, child)
defer hooks.fire(SubagentStop,  { agent_transcript_path })     // vòng đời phải được đóng lại
```

### Các bất biến (Invariants)

```
assert child.CacheSafeParams == parent.CacheSafeParams         # việc phân nhánh không làm hỏng prompt cache
assert child.mutable_state isolated unless opt_in.share_*       # việc chia sẻ phải rõ ràng và có chủ ý
assert parent.abort ⇒ propagate(child.abort)                    # parent dừng, child dừng theo
assert SubagentStart fired ⇒ SubagentStop fired eventually      # vòng đời được đóng lại
assert verification_worker ≠ implementation_worker              # vai trò xác minh và triển khai phải tách biệt
```

## 7.3 Cô lập trạng thái (State isolation): Giảm thiểu ô nhiễm trước khi chia sẻ bất cứ điều gì

Chìa khóa thứ hai là hàm `createSubagentContext()`: theo mặc định, tất cả các trạng thái có thể thay đổi (mutable state) đều được cô lập để tránh gây can thiệp đến parent. Các cài đặt mặc định sẽ sao chép `readFileState`, tạo ra các bộ kiểm soát hủy tiến trình con (child abort controllers), bao bọc `getAppState` để ngăn chặn các câu hỏi yêu cầu phân quyền, biến `setAppState` thành một hàm rỗng (no-op) và tái tạo các tập hợp như `nestedMemoryAttachmentTriggers` và `loadedNestedMemoryPaths`. Việc chia sẻ chỉ xảy ra thông qua các cờ chọn tham gia (opt-in flags) rõ ràng như `shareSetAppState`, `shareSetResponseLength`, `shareAbortController`.

Lý do của việc này rất quan trọng: giá trị cốt lõi của các agent con là giữ cho sự hỗn loạn cục bộ tránh xa luồng chính (main thread). Những phán đoán nghiên cứu sai sót, các quan sát tệp tạm thời, các nhánh suy luận mang tính chất khám phá và các quyết định công cụ đang thực thi không nên được tự động ghi đè trở lại luồng chính. Lập trường của Claude Code rất dứt khoát: chia sẻ cần có sự đồng ý (consent), cô lập là đạo đức mặc định (default ethics) — điều này gần gũi với thiết kế cơ sở dữ liệu giao dịch (transactional database) hơn là các ứng dụng trò chuyện đồ chơi.

## 7.4 Chế độ Điều phối viên (Coordinator mode): Tổng hợp là năng lực khan hiếm

Trong file `src/coordinator/coordinatorMode.ts`, các kỳ vọng đối với điều phối viên (coordinator) được quy định chặt chẽ:

- giúp người dùng đạt được mục tiêu
- chỉ đạo các worker làm nghiên cứu, triển khai và xác minh
- tổng hợp các kết quả tìm kiếm và giao tiếp với người dùng
- trả lời trực tiếp khi không cần thiết phải ủy quyền (delegation)

Dòng quan trọng nhất trong phần 5 của prompt là: **Luôn luôn tổng hợp (Always synthesize)**. Khi các worker trả về kết quả tìm kiếm, điều phối viên phải tiêu hóa và chuyển đổi chúng thành các prompt cụ thể; nó không được chuyển tiếp trực tiếp các kết quả thô và một lần nữa thuê ngoài việc thấu hiểu (outsource understanding).

Đây là nút thắt cổ chai của thiết kế đa agent. Năng lực khan hiếm không phải là sản phẩm đầu ra chạy song song; đó là việc nén lại các kiến thức cục bộ phân tán thành các bước tiếp theo khả thi và có thể xác minh được. Nếu không có lớp này, đa agent sẽ biến tướng thành việc chuyển tiếp tác vụ một cách lịch sự. Claude Code xử lý vấn đề này ở cấp độ prompt: nghiên cứu và tổng hợp được tách biệt, điều phối viên sở hữu quyền giải thích và các prompt tiếp theo phải đề cập đến các tệp, vị trí và thay đổi cụ thể thay vì nói chung chung kiểu "dựa trên kết quả trên". Nghiên cứu có thể phân tán; nhưng sự hiểu biết phải hội tụ.

## 7.5 Xác minh phải độc lập, nếu không việc hoàn thành triển khai sẽ mạo danh vấn đề đã được giải quyết

File `coordinatorMode.ts` cũng chứa một phần rất đáng để chắt lọc tinh thần. Nó chia nhỏ dòng chảy tác vụ thông thường thành:

- Nghiên cứu (Research)
- Tổng hợp (Synthesis)
- Triển khai (Implementation)
- Xác minh (Verification)

Và nêu rõ ràng rằng xác minh phải chứng minh được tính hiệu quả, chứ không chỉ đơn thuần là sự tồn tại của mã nguồn:

- chạy các bài kiểm thử khi tính năng đã được bật
- điều tra các lỗi thay vì bỏ qua chúng như thể không liên quan
- luôn giữ thái độ hoài nghi
- kiểm thử độc lập, không phê duyệt một cách máy móc (rubber-stamp)

Điều này cho thấy Claude Code coi xác minh là chốt chặn chất lượng lớp thứ hai (second-layer quality gate), chứ không phải là tác dụng phụ của việc triển khai: prompt chồng các bước tự kiểm tra triển khai kết hợp với một worker xác minh độc lập một cách rõ ràng.

Tại sao điều này quan trọng: "Tôi đã thay đổi mã nguồn" và "thay đổi đó là chính xác" được ngăn cách bởi một con sông rộng, và các mô hình lại rất giỏi trong việc xây những cây cầu giấy bắc qua sông — các thay đổi, giải thích, các kết quả đầu ra trông giống như bài kiểm thử hợp lý, nhưng không có gì trong số đó đảm bảo tính chính xác thực tế. Xác minh độc lập sẽ ngăn chặn hành vi "có thể sửa đổi mã" mạo danh "có thể mang lại kết quả"; trong công việc đa agent, sự phân tách vai trò này là cốt lõi.

## 7.6 Các hook và vòng đời tác vụ: Tạo ra một subagent mới chỉ là điểm khởi đầu

Trong các hệ thống đa agent, một thực tế thường bị bỏ qua là việc khởi tạo (spawn) chỉ là điểm bắt đầu, chứ không phải điểm kết thúc.

File `src/utils/hooks/hooksConfigManager.ts` định nghĩa các hook `SubagentStart` và `SubagentStop`. Các sự kiện bắt đầu bao gồm `agent_id` và `agent_type`. Các sự kiện dừng bao gồm `agent_transcript_path`, và thậm chí cho phép mã thoát bằng 2 (exit code 2) để lỗi tiêu chuẩn (stderr) có thể được phản hồi lại và giúp subagent tiếp tục.

Điều này có nghĩa là các subagent là các đối tượng vòng đời rõ ràng trong Claude Code. Điểm bắt đầu có thể được quan sát, điểm trước khi dừng (pre-stop) có thể được chặn lại, các đường dẫn bản ghi hội thoại (transcript paths) có thể truy vết được. "Sự kết thúc của subagent" tự nó là một sự kiện được quản lý.

Ở một lớp khác, hàm `registerAsyncAgent()` trong file `src/tasks/LocalAgentTask/LocalAgentTask.tsx` cho thấy mỗi agent bất đồng bộ (async agent) đều có các trình xử lý dọn dẹp (cleanup handlers). Tín hiệu hủy từ parent (parent aborts) được lan truyền tới các bộ kiểm soát hủy của child (child abort controllers). Khi hoàn thành tác vụ, các kết quả đầu ra có thể bị loại bỏ (evicted), trạng thái được cập nhật và các callback dọn dẹp được hủy đăng ký.

Điều này tương tự như việc kiểm soát vòng đời của hệ điều hành, chứ không phải các thẻ trò chuyện (chat tabs):

- agent có còn đang chạy hay không
- child có nên kết thúc khi parent kết thúc hay không
- các sản phẩm đầu ra có nên được giữ lại hay không
- các trình xử lý dọn dẹp có bị rò rỉ (leaked) hay không

![Claude Code Multi-Agent Runtime Lifecycle](diagrams/diag-ch07-01-multi-agent-lifecycle.png)

Nhiều bản demo đa agent chỉ dừng lại ở mức "Tôi có thể khởi động một agent khác". Claude Code tiến thêm một bước quan trọng: nó coi các agent là các thực thể runtime có thể rò rỉ tài nguyên, để lại cặn bã trạng thái và trở thành các tiến trình mồ côi (orphans) sau khi parent dừng.

### Ma trận lỗi vòng đời subagent (Subagent lifecycle failure matrix)

| Trật tự sự kiện | Trạng thái trước | Tác nhân kích hoạt | Bước tiếp theo | Ngưỡng |
|---|---|---|---|---|
| parent hủy + child đang chạy | child chưa xong | parent hủy | lan truyền `child.abort`, chờ dọn dẹp | không cho phép tiến trình mồ côi |
| child gặp lỗi đột ngột | child thoát bất thường | `SubagentStop` thoát ≠ 0 | loại bỏ đầu ra, kích hoạt stop hook | mã thoát 2 nạp lại stderr để tiếp tục |
| child quá giờ | child chạy quá lâu | `registerAsyncAgent` quá giờ | hủy child, ghi kết quả tổng hợp | — |
| trôi lệch khóa cache | `CacheSafeParams` bị thay đổi | phân nhánh (fork) | từ chối fork hoặc dựng lại cache | phải khớp hoàn toàn |
| chia sẻ không khai báo | opt-in chưa bật | child ghi vào `setAppState` | no-op, parent không bị ảnh hưởng | cô lập là mặc định |
| xung đột bộ nhớ cũ | bộ nhớ không khớp thực tế | đọc bản ghi cũ | tin tưởng thực tế; cập nhật/xóa bộ nhớ | xác minh trước |
| rò rỉ trình dọn dẹp | tác vụ kết thúc mà không hủy đăng ký | hoàn tất | ép buộc hủy đăng ký + loại bỏ | không để lại trình xử lý lửng lơ |

## 7.7 Xác minh áp dụng cho cả bộ nhớ và khuyến nghị, không chỉ dành cho mã nguồn

Xác minh đa agent không chỉ là một hoạt động diễn ra sau khi thay đổi mã nguồn. File `src/memdir/memoryTypes.ts` cảnh báo rõ ràng: các bản ghi bộ nhớ có thể trở nên lỗi thời; trước khi đưa ra các khuyến nghị từ bộ nhớ, hãy xác minh trạng thái hiện tại; khi bộ nhớ xung đột với thực tế hiện tại, hãy tin tưởng vào trạng thái quan sát được hiện tại và cập nhật hoặc xóa bộ nhớ đã lỗi thời.

Thực tế rộng lớn hơn: xác minh là thói quen cơ bản của hệ thống chống lại sự trôi lệch theo thời gian và ngữ cảnh (temporal and context drift). Nếu một hệ thống chỉ xác minh mã nguồn mới viết nhưng không xác minh bộ nhớ cũ, các giả định hoặc chỉ mục, lịch sử vẫn sẽ dẫn dắt nó đi chệch hướng. Xác minh vừa là một kỹ năng vừa là một kỷ luật tổ chức: bạn có thể ủy quyền công việc, lưu trữ thông tin và để các agent khác chạy trước, nhưng trước khi người dùng thực hiện các hành động trên kết quả đầu ra, ai đó phải quay lại thực tế hiện tại và xác thực lại.

## 7.8 Đa agent thực sự giải quyết việc phân chia sự không chắc chắn

Thiết kế đa agent của Claude Code tập trung vào một mục tiêu rõ ràng: phân chia sự không chắc chắn (partition uncertainty). Các worker nghiên cứu sẽ khám phá trong các ngữ cảnh cục bộ, các worker triển khai tập trung vào việc chỉnh sửa mã, các worker xác minh chuyên trách về sự hoài nghi, và điều phối viên đứng ở giữa để hội tụ thông tin và giao tiếp.

Lợi ích chính là phân định rõ ràng trách nhiệm, nhờ đó các lỗi có thể được định vị: liệu khâu nghiên cứu có bỏ lỡ một tín hiệu quan trọng, khâu tổng hợp có thất bại trong việc tiêu hóa kết quả tìm kiếm, khâu triển khai có đưa vào các lỗi (defects), khâu xác minh có kiểm tra chưa đủ kỹ? Một agent đơn lẻ cung cấp "một bát súp đặc lẫn lộn" sẽ không thể được gỡ lỗi theo từng lớp. Giá trị của đa agent ít nằm ở tốc độ hơn là nằm ở việc đặt các sự không chắc chắn khác nhau vào các thùng chứa khác nhau, sau đó kết hợp lại chúng thông qua sự tổng hợp của điều phối viên.

## 7.9 Nguyên lý thứ bảy có thể trích xuất từ mã nguồn

Chương này có thể được tóm gọn trong một câu duy nhất:

> Các hệ thống đa agent phụ thuộc vào sự phân công lao động rõ ràng: nghiên cứu, triển khai, xác minh và tổng hợp phải chạy dưới các thùng chứa ràng buộc khác nhau, sau đó được điều phối viên khâu nối lại thành các kết quả có thể bàn giao.

Mã nguồn Claude Code cùng hỗ trợ luận điểm này:

- `forkedAgent.ts` ưu tiên các tham số an toàn cho cache, theo dõi sử dụng và cô lập trạng thái, biến việc phân nhánh trước hết thành một vấn đề kiểm soát của runtime
- `createSubagentContext()` cô lập các trạng thái có thể thay đổi theo mặc định và chỉ chia sẻ thông qua opt-in rõ ràng
- `coordinatorMode.ts` yêu cầu sự tổng hợp thay vì chuyển tiếp thô, để sự thấu hiểu không bị thuê ngoài
- việc xác minh được tách biệt rõ ràng khỏi việc triển khai và phải chứng minh tính hiệu quả một cách độc lập
- `hooksConfigManager.ts` cung cấp `SubagentStart` and `SubagentStop`, làm cho các subagent trở thành các đối tượng vòng đời có thể quan sát được
- `LocalAgentTask.tsx` xử lý việc lan truyền hủy bỏ từ parent, dọn dẹp và loại bỏ đầu ra

Là những nguyên lý kỹ thuật có thể mang đi được: phân nhánh trước hết là vì các ranh giới bộ đệm và ranh giới trạng thái, sau đó mới là vì "chuyên môn hóa vai trò" (persona specialization); cô lập các agent con theo mặc định và chỉ chia sẻ thông qua khai báo rõ ràng; nghiên cứu có thể được ủy quyền, tổng hợp thì không; xác minh phải được phân tách vai trò với triển khai; vòng đời của agent phải có thể quan sát, có thể ngắt và có thể thu hồi; giá trị song song thực sự là trách nhiệm rõ ràng hơn, chứ không phải là tốc độ thô.

Chương tiếp theo sẽ chuyển từ thiết kế runtime sang thiết kế tổ chức: cách `CLAUDE.md`, các kỹ năng, sự phê duyệt, các hook và bộ nhớ trở thành các thể chế nhóm có thể tái sử dụng thay vì chỉ là các mẹo cá nhân của chuyên gia.
