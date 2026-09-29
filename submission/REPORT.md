# Báo cáo cá nhân — K4-L3A Day 13 Monitoring & LLMOps

> Mỗi học viên hoàn thiện một file duy nhất này. Khi dẫn evidence, dùng đường dẫn tương đối, ví dụ `evidence/07-trace-waterfall.png`.

## 1. Thông tin học viên

- **Họ và tên: Nguyễn Thu Hằng** 
- **MSSV: 2A202602463**
- **Lớp:** K4-L3A
- **Repository URL: https://github.com/Bean624/K4-L3-DAY13-NguyenThuHang-02463-Monitoring-LLMOps** 
- **Commit SHA cuối:**
- **Challenge ID:**
- **Tên project Langfuse cá nhân:** `day13-k4-l3a-2A202602463`

## 2. Evidence index

Điền đúng đường dẫn tới evidence thực tế. Có thể đổi tên hoặc dùng nhiều ảnh nếu cần.

| Evidence | Đường dẫn |
|---|---|
| Pytest cuối | `evidence/01-pytest.png` |
| Log validator | `evidence/02-log-validator.png` |
| Dashboard validator | `evidence/03-dashboard-validator.png` |
| Structured log | `evidence/04-structured-log.png` |
| PII redaction | `evidence/05-pii-redaction.png` |
| Trace list | `evidence/06-trace-list.png` |
| Trace waterfall | `evidence/07-trace-waterfall.png` |
| Trace metadata | `evidence/08-trace-metadata.png` |
| Prompt versions | `evidence/09-prompt-versions.png` |
| Prompt rollback | `evidence/10-prompt-rollback.png` |
| Dashboard runtime | `evidence/11-dashboard-overview.png` |
| Incident metric | `evidence/12-incident-metric.png` |
| Incident log | `evidence/13-incident-log.png` |
| Incident trace | `evidence/14-incident-trace.png` |

## 3. Kết quả kỹ thuật

| Nội dung | Baseline | Kết quả cuối | Nhận xét |
|---|---|---|---|
| `validate_logs.py` |30/100 | |Chưa scrub PII, thiếu context fields |
| `validate_dashboard.py` |6/6 panel có trong dashboard contract | |Đã có khung 6 panel |
| `pytest` |22 passed| | |
| Số traces hợp lệ | | | |
| Số PII leak | | | |
| Latency P95 / TTFT P95 | | | |
| Retrieval success rate | | | |

## 4. Logging và PII

- **Cách tạo/nhận và truyền correlation ID:** `CorrelationIdMiddleware` xóa context cũ qua `clear_contextvars()`, kiểm tra header `x-request-id` (nếu hợp lệ định dạng `req-<8-hex>` thì giữ, ngược lại tự động tạo mới `f"req-{uuid.uuid4().hex[:8]}"`). Sau đó bind vào `structlog` contextvars qua `bind_contextvars(correlation_id=correlation_id)` và lưu vào `request.state.correlation_id`. Cuối cùng trả về correlation ID và thời gian xử lý trong header response `x-request-id`, `x-response-time-ms`.
- **Các metadata được ghi vào structured log:** `user_id_hash` (băm SHA256 12 ký tự), `session_id`, `feature`, `model`, `env`, `ts` (ISO UTC), `level`, `service`, `event`, `latency_ms`, `ttft_ms`, `tokens_in`, `tokens_out`, `cost_usd`, `quality_score`, `tool_name`, `tool_success`.
- **Cách bảo đảm PII được scrub trước khi ghi:** Sử dụng structlog processor `scrub_event` đặt trước `JsonlFileProcessor` và `JSONRenderer`. Processor này duyệt đệ quy qua các payload/event và áp dụng regex `scrub_text` để thay thế email, số điện thoại VN, CCCD, thẻ thanh toán thành `[REDACTED_<TYPE>]` trước khi log được serialize hoặc ghi vào file `data/logs.jsonl`.
- **Cách kiểm chứng kết quả:** Xóa log cũ, chạy lại `python scripts/load_test.py` và kiểm tra bằng `python scripts/validate_logs.py` (đạt 100/100, 0 PII leak) cùng test suite `python -m pytest -q`.

## 5. Tracing và prompt versioning

- **Cách xác nhận traces do chính tôi tạo trong project cá nhân:** Các traces hiển thị rõ tên project cá nhân `day13-k4-l3a-<MSSV>` trên Langfuse Cloud, gắn metadata `user_id_hash`, `session_id`, `correlation_id` khớp với request do tôi chạy trong load test.
- **Cấu trúc root/retrieval/generation observations:** Root observation là `lab-agent-run` (type `agent`), bên dưới gồm hai child observations: `retrieval` (type `retriever`) thực hiện tìm kiếm tài liệu và `generation` (type `generation`) gọi LLM nhận đầy đủ model, prompt, token usage và cost.
- **Cách nối trace với log:** Cả structured log và trace đều chia sẻ chung một `correlation_id` duy nhất (được bind từ middleware và truyền vào metadata của trace).
- **Prompt name:** `day13-chat`
- **Version/label baseline:** Version 1 (gắn label `baseline`, ban đầu gắn `production`)
- **Version/label candidate:** Version 2 (gắn label `candidate`)
- **Trace ID của mỗi version:** *(Học viên điền trace ID thực tế lấy từ Langfuse sau khi chạy)*
- **Cách promote và rollback `production`:**
  - Promote: Trong Langfuse UI, chuyển label `production` sang Version 2 rồi gửi request kiểm tra.
  - Rollback: Chuyển lại label `production` về Version 1 và lưu evidence.

## 6. Dashboard, SLO và alerts

- **Dashboard và sáu panel:** Được cấu hình theo chuẩn contract `config/dashboard.yaml` với 6 panel:
  1. `Latency`: P50, P95, P99 và TTFT P95 (đơn vị: ms, threshold P95 <= 3000ms).
  2. `Traffic`: Số lượng request theo phút (đơn vị: requests/min, threshold >= 1).
  3. `Errors`: Tỷ lệ lỗi % và tỷ lệ truy xuất thành công (đơn vị: %, threshold error rate <= 2%).
  4. `Cost`: Chi phí ước tính theo phút và tổng chi phí (đơn vị: USD, threshold <= 2.5$).
  5. `Tokens`: Tổng số input và output tokens (đơn vị: tokens, threshold <= 50000).
  6. `Quality`: Điểm chất lượng trung bình (đơn vị: score 0-1, threshold >= 0.75).
- **SLO và lý do chọn:** Primary SLO `fast_successful_requests` đặt mục tiêu 99.5% requests thành công và có độ trễ <= 3000ms trong chu kỳ 28 ngày. Lý do chọn: Chatbot AI tương tác trực tiếp với người dùng nên độ trễ dưới 3s là ngưỡng quan trọng để giữ chân người dùng và đảm bảo trải nghiệm hội thoại mượt mà.
- **Cách tính error budget:** Error budget = 100% - 99.5% = 0.5% tổng số request. Ví dụ nếu hệ thống phục vụ 100,000 requests trong 28 ngày thì error budget cho phép tối đa 500 requests bị lỗi hoặc chậm (> 3000ms). Khi error budget cạn kiệt, team kỹ thuật sẽ đóng băng việc release tính năng mới để tập trung fix lỗi hệ thống và tối ưu RAG.
- **Ba alert và runbook tương ứng:**
  1. `high_latency_p95`: warning, kích hoạt khi `latency_p95_ms > 3000` trong 5 phút. Runbook: `docs/alerts.md#alert-1`.
  2. `high_error_rate`: critical, kích hoạt khi `error_rate_pct > 2` trong 5 phút. Runbook: `docs/alerts.md#alert-2`.
  3. `retrieval_degradation`: warning, kích hoạt khi `retrieval_success_rate_pct < 90` trong 10 phút. Runbook: `docs/alerts.md#alert-3`.

## 7. Điều tra challenge

- **Challenge ID:**
- **Khoảng thời gian điều tra:**
- **Triệu chứng từ metrics:**
- **Log line và correlation ID liên quan:**
- **Trace ID và span gây ảnh hưởng:**
- **Root cause:**
- **Fix action:**
- **Preventive measure:**

## 8. Giải thích và tự đánh giá

- **Một quyết định kỹ thuật quan trọng và lý do:**
- **Một lỗi/blocker đã gặp:**
- **Cách tìm nguyên nhân và xử lý:**
- **Cách hiểu luồng Metrics → Logs → Traces:**
- **Vai trò của prompt version, token/cost, SLO hoặc rollback trong vận hành LLM:**
- **Điều quan trọng nhất đã học:**
- **Hạn chế hoặc phần chưa hoàn thành, nếu có:**

## 9. Checklist trước khi nộp

- [ ] Kết quả và evidence thuộc commit SHA cuối.
- [ ] Tất cả ảnh/output mở được bằng đường dẫn tương đối.
- [ ] Incident evidence nối đúng metric → log → trace.
- [ ] Trace/prompt evidence thuộc project Langfuse cá nhân và ảnh không lộ key/secret.
- [ ] Repository chạy lại được theo README.
- [ ] Không có secret, API key, PII thô hoặc evidence của người khác/lớp khác.
- [ ] URL repo và commit SHA cuối đã được nộp trên LMS/Codelabs.
