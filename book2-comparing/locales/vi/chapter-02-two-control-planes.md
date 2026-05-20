# Chương 2: Hai mặt phẳng điều khiển—các lớp prompt động so với các phân mảnh có cấu trúc

![Biểu đồ so sánh mặt phẳng điều khiển](diagrams/diag-01-control-plane-comparison.png)

## 2.1 Điều khiển không phải là về giọng điệu

Coi prompt như một bài tập về giọng điệu (tone) là một sự hiểu lầm. Cả Claude Code và Codex đều coi prompt là một phần của mặt phẳng điều khiển hành vi (behavioral control plane); sự khác biệt nằm ở cơ chế lắp ráp chúng. Claude Code lắp ráp động (dynamic assembly) — văn bản cơ sở, các prompt đính kèm, vai trò của Agent, `CLAUDE.md`, bộ nhớ và các phong cách đầu ra được phủ nhiều lớp trong thời gian chạy (runtime layered) theo ngữ cảnh tác vụ, công cụ và nhóm; nghệ thuật ở đây nằm ở thứ tự ưu tiên, giải quyết xung đột và cách mỗi lớp gập vào lớp tiếp theo. Codex coi các chỉ thị là các phân mảnh có cấu trúc (structured fragments) — `AGENTS.md`, tin nhắn của người dùng và các kỹ năng trở thành các khối có dấu hiệu (markers) rõ ràng, ranh giới bắt đầu/kết thúc và các quy tắc tuần tự hóa (serialization rules), chuyển chỉ thị từ dạng kể chuyện tự do sang các đơn vị ngữ cảnh có thể nhận dạng được.

## 2.2 Dây chuyền lắp ráp bận rộn của Claude Code

Các prompt hệ thống (system prompts) ở đây không phải là tài liệu cố định mà là một dây chuyền sản xuất: các giá trị mặc định tạo nền móng, các prompt đính kèm đưa vào các yêu cầu, các prompt của Agent bổ sung vai trò, `CLAUDE.md` và bộ nhớ đưa vào các điều kiện cục bộ. Sự linh hoạt cho phép một vòng lặp xử lý nhiều tình huống, nhưng thứ tự là tối quan trọng — thứ tự sai sẽ làm loãng các chỉ thị hoặc để các xung đột lọt qua. Do đó, quản trị thời gian chạy là điều thiết yếu: điều khiển liên tục được đưa vào, ghi đè, nén hoặc cắt tỉa khi tác vụ thay đổi, và vòng lặp tính toán lại "điều gì quan trọng lúc này" sau mỗi vòng. Trực giác dẫn dắt ở đây là: điều khiển bám sát hiện trường — nó không thể đóng băng thành các quy tắc tĩnh.

## 2.3 Cách tiếp cận kiểu phòng lưu trữ hồ sơ của Codex

Codex nhấn mạnh vào các phân mảnh có thể nhận dạng được. Những cái tên như `ContextualUserFragmentDefinition` làm nổi bật kiểu dữ liệu, ranh giới, quy tắc bao bọc và chuyển đổi tin nhắn. AGENTS, kỹ năng và chỉ thị người dùng là các đơn vị ngữ cảnh được gắn thẻ mà hệ thống có thể nhận biết và thao tác — tăng khả năng gỡ lỗi (debuggability), và mở ra con đường đến sự quản trị mang tính lập trình hơn vì mọi chỉ thị đều đã khớp với một phân cấp kiểu dữ liệu (type hierarchy).

Và đây không chỉ đơn thuần là việc đặt tên trang nhã. `fragment.rs` định nghĩa các hằng số như `AGENTS_MD_START_MARKER`, `AGENTS_MD_END_MARKER`, `SKILL_OPEN_TAG` và `SKILL_CLOSE_TAG`; `ContextualUserFragmentDefinition::wrap()` và `into_message()` chuyển các phân mảnh đó thành `ResponseItem::Message`. Trong `user_instructions.rs`, `UserInstructions` tuần tự hóa thư mục thành `# AGENTS.md instructions for ...`, trong khi `SkillInstructions` mang các trường `<name>` và `<path>` rõ ràng. Codex cố gắng hết sức để mô hình không phải tự đoán xem một quy tắc bắt nguồn từ đâu.

### Skeleton: Hai quá trình lắp ráp mặt phẳng điều khiển

```
// skeleton: Lắp ráp động Claude Code  (src: constants/prompts.ts, utils/systemPrompt.ts, claudemd.ts)
system_prompt = concat(
    default_prompt,           // cơ sở
    append_prompt,            // các yêu cầu phủ chồng
    agent_prompt,             // vai trò
    claudemd_layers,          // nhóm / cá nhân / dự án
    memory_sections,          // bộ nhớ phiên
    output_style              // kỷ luật diễn đạt
)
// được tính toán lại sau mỗi vòng lặp: nạp trước bộ nhớ, thu gọn, cô đọng vi mô, tự động cô đọng

// skeleton: Lắp ráp phân mảnh Codex  (src: instructions/src/fragment.rs, user_instructions.rs)
for frag in [agents_md, skill, user_instructions]:
    body = ContextualUserFragmentDefinition::wrap(
        START_MARKER, content, END_MARKER,
        meta { source_dir, name, path }
    )
    msg  = frag.into_message()              // -> ResponseItem::Message
    thread.append(msg)
```

### Invariants

```
assert every fragment has matching (START_MARKER, END_MARKER)   # các dấu hiệu ghép cặp
assert fragment.source ∈ {AGENTS_MD, SKILL, USER}              # loại có thể nhận dạng được
assert precedence(project) > precedence(team) > precedence(default)  # độ ưu tiên đơn điệu
assert claudemd_layers overlay order = team → personal → project  # cái sau ghi đè cái trước
assert child_agents_md enabled ⇒ append scope/precedence notes  # phạm vi là tường minh
```

## 2.4 CLAUDE.md so với AGENTS.md

`CLAUDE.md` là một bảng tin cục bộ: nằm gần thư mục tác vụ, đi kèm với bộ nhớ và kỹ năng, thích hợp để đăng ký các kiến thức thông thường (common sense), điều cấm kỵ (taboos) và các quy tắc cục bộ. `AGENTS.md` được đưa vào cuộc thảo luận về phân cấp của Codex — `docs/agents_md.md` nói rằng ngay cả khi không có `AGENTS.md` nào tồn tại, việc bật `child_agents_md` vẫn sẽ đính kèm thêm các ghi chú về phạm vi và thứ tự ưu tiên. Codex không chỉ quan tâm xem các quy tắc có tồn tại hay không, mà còn quan tâm xem khả năng áp dụng và tính kế thừa của chúng có được tuyên bố rõ ràng hay không. Claude Code đưa các quy tắc cục bộ vào cuộc hội thoại; Codex đưa chúng vào thể chế.

## 2.5 Các đánh đổi

Việc lắp ráp trong thời gian chạy rất linh hoạt nhưng khó chính thức hóa, phụ thuộc nhiều vào vòng lặp chính và đánh giá kỹ thuật; một khi các quy tắc nhân lên, sự chồng chéo và sự suy giảm ngữ nghĩa (semantic dilution) trở thành những rủi ro thực sự. Các phân mảnh có cấu trúc thì tường minh nhưng nặng nề hơn: các dấu hiệu, kiểu dữ liệu, tuần tự hóa và tiêm ngữ cảnh đều cần định nghĩa, cộng thêm các quyết định về việc cái gì xứng đáng có trạng thái ưu tiên hàng đầu (first-class status). Cách tiếp cận trước phát triển khả năng kiểm soát dựa trên trải nghiệm, cách tiếp cận sau phát triển khả năng kiểm soát dựa trên thể chế — một bên linh hoạt nhưng thiếu khai báo, bên kia rõ ràng nhưng phải gánh chi phí cấu trúc liên tục.

## 2.6 Kết luận chương này

> Claude Code coi prompt là các bản dựng thời gian chạy động (dynamic runtime builds); Codex coi chỉ thị là các phân mảnh có thể nhận dạng được.

Một bên mang lại cảm giác của một nhà xưởng sản xuất trực tiếp, bên kia mang lại cảm giác của một bộ máy hành chính công vụ. Lựa chọn đúng đắn phụ thuộc vào việc mối bận tâm hàng đầu của bạn là các phiên làm việc dễ biến động hay nguồn gốc quy tắc không rõ ràng. Chương tiếp theo sẽ đi sâu hơn: tính liên tục nằm ở vòng lặp truy vấn hay ở cơ sở hạ tầng luồng, triển khai và trạng thái?
