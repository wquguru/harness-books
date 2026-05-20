# Phụ lục A Bản đồ Mã nguồn: Những Tệp làm Cơ sở Chính cho bài So sánh này

Phụ lục này chỉ thực hiện một việc duy nhất: nó chỉ ra các nhận định trong mỗi chương chủ yếu dựa trên các tệp nào. Đây không phải là một thư mục sao chép lại mã nguồn, cũng không có nghĩa là cuốn sách đi kèm với mã nguồn cùng với các lập luận của nó.

Ranh giới tương tự cũng được áp dụng ở đây:

- chỉ sử dụng các trích dẫn kỹ thuật tối thiểu và vị trí mô-đun
- phần thân triển khai của Claude Code hay Codex không bị sao chép lại
- không cung cấp các đoạn trích dẫn mã nguồn dài dòng

## A.1 Các tham chiếu chính phía Claude Code

Mặt phẳng điều khiển và prompt toàn cục:

- `src/constants/prompts.ts`
- `src/utils/systemPrompt.ts`
- `src/utils/claudemd.ts`
- `src/memdir/memdir.ts`

Vòng lặp runtime và khôi phục:

- `src/query.ts`
- `src/QueryEngine.ts`
- `src/services/compact/autoCompact.ts`
- `src/services/compact/compact.ts`

Công cụ và phân quyền:

- `src/services/tools/toolOrchestration.ts`
- `src/services/tools/toolExecution.ts`
- `src/services/tools/StreamingToolExecutor.ts`
- `src/hooks/useCanUseTool.tsx`
- `src/tools/BashTool/prompt.ts`
- `src/tools/BashTool/bashPermissions.ts`

Công việc đa agent, kỹ năng và hook:

- `src/utils/forkedAgent.ts`
- `src/coordinator/coordinatorMode.ts`
- `src/tasks/LocalAgentTask/LocalAgentTask.tsx`
- `src/tools/SkillTool/SkillTool.ts`
- `src/tools/SkillTool/prompt.ts`
- `src/utils/hooks/hooksConfigManager.ts`

## A.2 Các tham chiếu chính phía Codex

Khung xương mô-đun cốt lõi:

- `core/src/lib.rs`
- `tools/src/lib.rs`
- `skills/src/lib.rs`
- `hooks/src/lib.rs`

Các phân đoạn hướng dẫn (instruction fragments) và sự can thiệp của người dùng (user injection):

- `instructions/src/lib.rs`
- `instructions/src/fragment.rs`
- `instructions/src/user_instructions.rs`
- `docs/agents_md.md`

Công cụ, phê duyệt và chính sách thực thi:

- `tools/src/local_tool.rs`
- `tools/src/agent_tool.rs`
- `execpolicy/src/lib.rs`
- `docs/execpolicy.md`
- `docs/sandbox.md`

Luồng (threads) và trạng thái:

- `sdk/typescript/src/thread.ts`
- `core/src/lib.rs`
- `core/src/thread_manager.rs`
- `core/src/rollout.rs`
- `core/src/state_db_bridge.rs`
- `core/src/message_history.rs`

Cơ chế sự kiện hook:

- `hooks/src/engine/mod.rs`

## A.3 Ánh xạ Chương sang Tệp

Chương 1:

- `query.ts` và `toolOrchestration.ts` của Claude Code
- `core/src/lib.rs` của Codex

Chương 2:

- Lắp ráp prompt và `CLAUDE.md` của Claude Code
- `fragment.rs` và `user_instructions.rs` của Codex

Chương 3:

- Vòng lặp truy vấn và `QueryEngine` của Claude Code
- `thread.ts` của Codex, cùng các mô-đun để lộ xung quanh `thread_manager`, `rollout` và `state_db_bridge`

Chương 4:

- Điều phối công cụ, các hạn chế đối với Bash và ngữ nghĩa phân quyền của Claude Code
- `tools/src/lib.rs`, `local_tool.rs` và `execpolicy/src/lib.rs` của Codex

Chương 5:

- Kỹ năng, hook và hệ thống bộ nhớ của Claude Code
- Hệ thống kỹ năng và cơ chế hook của Codex

Chương 6:

- Thiết kế forked-agent và kỷ luật xác minh của Claude Code
- Tập hợp công cụ agent (agent-tool set) cùng cấu trúc luồng / triển khai / trạng thái của Codex

Chương 7:

- nhận định tích lũy được tạo ra bởi toàn bộ tập hợp tệp ở trên
