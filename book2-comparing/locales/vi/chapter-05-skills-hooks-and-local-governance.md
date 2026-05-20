# Chapter 5 Kỹ năng (Skills), Hook và Quy tắc Địa phương (Local Rules): Cách Hệ thống Học cách Tôn trọng Luật Làng

![Local Governance Comparison](diagrams/diag-04-local-governance-comparison.png)

## 5.1 Bất kỳ Agent nào có thể triển khai (deployable agent) đều trở thành địa phương

Bất kỳ Agent lập trình đa năng (general-purpose coding agent) nào khi bắt đầu công việc thực tế cho một đội ngũ đều va chạm với cùng một thực tế: các công ty, kho lưu trữ (repositories), thư mục và con người đều có những quy tắc và thói quen riêng. Một hệ thống không thể tiếp thu các thể chế địa phương (local institutions) đó sẽ mãi bị mắc kẹt trong môi trường demo. Claude Code và Codex đều đưa ra câu trả lời theo các hướng khác nhau.

## 5.2 Claude Code: Thể chế địa phương dưới dạng bộ nhớ thực địa (field memory)

Khả năng bản địa hóa nằm ở `CLAUDE.md`, các kỹ năng (skills), hook và bộ nhớ phiên (session memory) — cùng nhau, chúng mang lại cảm giác giống như kinh nghiệm thực địa tích lũy: `CLAUDE.md` nêu rõ những gì được coi là kiến thức thông thường (common sense) trong kho lưu trữ (repo), thư mục và đội ngũ này; kỹ năng đóng gói các quy trình làm việc có thể lặp lại; hook gắn quản trị của đội ngũ vào các thời điểm trong vòng đời (lifecycle points); bộ nhớ phiên giữ cho mỗi lượt chạy không phải bắt đầu lại từ con số không. Đặc điểm chung là sự gần gũi với bối cảnh nhiệm vụ — đưa các quy tắc vào phiên hiện tại và lượt thực thi hiện tại, thay vì một hiến pháp vĩnh cửu duy nhất ngay từ đầu. Claude Code giống như một kỹ sư ghi chép lại các phong tục địa phương ở bất cứ nơi nào họ đi qua — cực kỳ thực tế trên các dự án, thư mục và các ràng buộc địa phương, nhưng nếu không được dọn dẹp, kiến thức sẽ phình to dưới dạng các bản vá thực địa (field patches).

## 5.3 Codex: Thể chế địa phương dưới dạng tiêm cấu trúc (structured injection) và hệ thống sự kiện (event systems)

Codex cũng có các kỹ năng, quy tắc địa phương và hook, nhưng tính chất mang tính thể chế hơn. Kỹ năng: `skills/src/lib.rs` cài đặt các kỹ năng hệ thống vào `CODEX_HOME/skills/.system` và theo dõi chúng bằng dấu vân tay (fingerprint) — một kỹ năng là một tài sản được cài đặt, quản lý và có thể đánh số phiên bản (versionable asset), chứ không phải là văn bản được đọc lại một cách tình cờ khi khởi động. `install_system_skills()` chỉ cài đặt lại khi nhãn đánh dấu (marker) không khớp. `AGENTS.md` mang phạm vi và phân cấp hơn là mang ý nghĩa "đọc một ghi chú địa phương" — các quy tắc địa phương mang các mối quan hệ vị trí chứ không chỉ là nội dung. Hook: `hooks/src/engine/mod.rs` chia nhỏ các sự kiện thành `session_start`, `pre_tool_use`, `post_tool_use`, `user_prompt_submit`, `stop`, và mỗi trình xử lý (handler) có `event_name`, bộ khớp (matcher), thời gian chờ (timeout), thông báo trạng thái (status message), đường dẫn nguồn (source path), thứ tự hiển thị (display order) — giống một hệ thống sự kiện vòng đời chính thức (formal lifecycle event system) hơn là mô hình "thả một hàm gọi lại (callback) ở bất cứ nơi nào thuận tiện". Engine tách biệt các đường dẫn `preview_*` khỏi các đường dẫn `run_*` (xem trước các trình xử lý nào sẽ kích hoạt trước khi thực thi), và trên Windows sẽ vô hiệu hóa `codex_hooks` bằng một cảnh báo rõ ràng khi hỗ trợ chưa hoàn thiện — khả năng của hook được làm cho có thể giải thích được.

## 5.4 Claude Code tiếp thu kinh nghiệm; Codex gắn kết các thể chế (mounts institutions)

Quản trị địa phương (local governance) của Claude Code liên tục tiếp thu kinh nghiệm thực địa vào vùng lân cận của vòng lặp chính (main loop) — mạnh mẽ trong việc giúp Agent nhanh chóng học hỏi cách thức hoạt động ở đây. Codex gắn kết các quy tắc địa phương vào một mặt phẳng điều khiển (control plane) và hệ thống vòng đời rõ ràng — mạnh mẽ trong việc phân loại, sắp xếp, cài đặt và kích hoạt các quy tắc. Cảm nhận về đội ngũ có sự khác biệt: thực thể trước giống như một nhân viên lâu năm biết cách ứng xử phù hợp hoàn cảnh (read the room); thực thể sau là một người mới đến với bản năng thể chế mạnh mẽ, người sẽ dán các quy tắc lên trước, sau đó mới điều phối công việc.

### Skeleton: Vòng đời hook của Codex

```
// bộ khung (skeleton): Codex hook engine  (src: hooks/src/engine/mod.rs)
events = [session_start, user_prompt_submit, pre_tool_use, post_tool_use, stop]
for ev in events:
    handlers = preview_handlers(ev, ctx)        // xem trước các bộ khớp trước
    emit(preview_event { ev, handlers })
    for h in handlers sorted by display_order:
        if match(h.matcher, ctx) and not timed_out(h.timeout):
            run_handler(h)                      // thực sự kích hoạt
        else:
            log_skip(h, reason)
on platform == windows: disable(codex_hooks); warn("incomplete support")
```

### Bất biến (Invariants): Thứ tự sự kiện hook

```
assert session_start fires once per thread before any tool_use
assert pre_tool_use fires immediately before execution; post_tool_use after
assert stop fires exactly once per thread termination path
assert preview_* path never executes handlers; only run_* does
assert each handler has {event_name, matcher, timeout, source_path, display_order}
assert stable display_order ⇒ replayable ordering across runs
assert skill fingerprint mismatch ⇒ reinstall; match ⇒ skip  (skills/src/lib.rs)
```

## 5.5 Các hệ quả khác nhau đối với khả năng tái lặp của tổ chức (organizational reproducibility)

Một hệ thống dựa trên kinh nghiệm thực địa được tiêm (injected field experience) sẽ thích ứng nhanh hơn với các kho lưu trữ mới và duy trì hiệu quả trong bối cảnh địa phương dày đặc. Nhưng khi nó lan rộng ra các đội ngũ, nó thường cần sự dọn dẹp biên tập — nếu không, mọi người đều tự viết `CLAUDE.md` của riêng họ và phát minh ra các kỹ năng của riêng họ, và tổ chức sẽ kết thúc bằng việc in sách giáo khoa theo từng tỉnh. Một hệ thống dựa trên tiêm cấu trúc và gắn kết vòng đời (structured injection and lifecycle mounting) có nhiều tiềm năng mở rộng hơn: các quy tắc dễ dàng được phân phối đồng nhất, đánh số phiên bản và kiểm toán hơn. Cái giá phải trả là học tập: đội ngũ trước tiên phải chấp nhận nhiều thể chế rõ ràng hơn. Sự đánh đổi cổ điển — gần gũi hơn với bối cảnh mang lại sự đàn hồi (elasticity), thể chế hóa nhiều hơn mang lại khả năng tái lặp (reproducibility). Điều quyết định kết quả là đội ngũ thực sự cần sự ổn định nào.

## 5.6 Kết luận chương

Chương này có thể được tóm tắt như sau:

> Claude Code có xu hướng biến quản trị địa phương thành bộ nhớ thực địa và tiêm lúc chạy (runtime injection), trong khi Codex có xu hướng biến quản trị địa phương thành các tài sản có cấu trúc và hệ thống sự kiện vòng đời.

Đó không chỉ là một cách nói khác của việc "cả hai đều hỗ trợ kỹ năng và hook."

Sự khác biệt là Claude Code đặt câu hỏi, "Làm thế nào để chúng ta làm cho Agent hoạt động ở đây giống như một người địa phương hơn?" trong khi Codex hỏi, "Làm thế nào để chúng ta đưa các quy tắc địa phương vào một khung thể chế có thể quản trị được?"

Chương tiếp theo sẽ chuyển sang một lớp có rủi ro cao hơn: công việc đa Agent (multi-agent work), xác minh, trạng thái bền vững (persistent state) và phục hồi. Khi nhiều Agent bắt đầu hoạt động cùng một lúc, chỉ riêng các quy tắc là không đủ; trách nhiệm cũng phải được phân chia.
