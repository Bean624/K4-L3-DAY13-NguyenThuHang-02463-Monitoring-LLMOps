# Báo cáo cá nhân — K4-L3A Day 13 Monitoring & LLMOps

> Mỗi học viên hoàn thiện một file duy nhất này. Khi dẫn evidence, dùng đường dẫn tương đối, ví dụ `evidence/07-trace-waterfall.png`.

## 1. Thông tin học viên

- **Họ và tên:** Nguyễn Thu Hằng
- **MSSV:** 2A202602463
- **Lớp:** K4-L3A
- **Repository URL:** https://github.com/Bean624/K4-L3-DAY13-NguyenThuHang-02463-Monitoring-LLMOps
- **Commit SHA cuối:**
- **Challenge ID:** day13-k4-l3a-monitoring-llmops-v1
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
| `validate_logs.py` | 30/100 | 100/100 | Đã enrich đầy đủ context, propagation correlation ID và scrub 100% PII |
| `validate_dashboard.py` | 6/6 panel có trong dashboard contract | 6/6 panel hợp lệ | Đầy đủ 6 panel theo chuẩn contract YAML |
| `pytest` | 22 passed | 22 passed | Toàn bộ 22 unit tests vượt qua |
| Số traces hợp lệ | 0 | 15 traces | Đạt yêu cầu tối thiểu (≥ 10 traces trên Langfuse cá nhân) |
| Số PII leak | 4 | 0 | 100% email, phone_vn, CCCD, credit card được redact thành công |
| Latency P95 / TTFT P95 | 1253ms / 50ms | 3635ms / 55ms | Tăng mạnh khi kích hoạt sự cố rag_slow |
| Retrieval success rate | 100% | 100% | Vẫn thành công nhưng bị trễ cao ở vector store |

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
- **Trace ID của mỗi version:**
  - **Version 1 (`production` / `baseline`):** `031027267f9423609922771afec2cdb8` (gắn `correlation_id: req-f3fa8bad`)
  - **Version 2 (`candidate`):** `4f89d3170a254c798933ca553bb1bb5f` (gắn `correlation_id: req-933ca553`)
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

- **Challenge ID:** `day13-k4-l3a-monitoring-llmops-v1`
- **Khoảng thời gian điều tra:** `16:00 - 16:30, 29/09/2026 (Asia/Ho_Chi_Minh)`
- **Triệu chứng từ metrics:** Khi incident `rag_slow` được kích hoạt và chạy workload challenge (`load_test.py --challenge --concurrency 5`), metrics ghi nhận:
  - `latency_p50`: 2963.0ms
  - `latency_p95`: **3635.0ms** (vượt xa ngưỡng threshold 2000ms của challenge và vượt ngưỡng SLO 3000ms)
  - `latency_p99`: 3635.0ms
  - `ttft_p95`: 55.0ms (không bị ảnh hưởng)
  - `traffic`: 5 requests, `error_breakdown`: {} (0% error rate).
- **Log line và correlation ID liên quan:**
  Trong file `data/logs.jsonl`, sự kiện `response_sent` đối với request bị chậm:
  ```json
  {"service": "api", "latency_ms": 3635, "ttft_ms": 50, "tokens_in": 35, "tokens_out": 155, "cost_usd": 0.00243, "quality_score": 0.8, "tool_name": "retrieval", "tool_success": true, "payload": {"answer_preview": "Starter answer. You should improve this output logic and add better quality chec..."}, "event": "response_sent", "correlation_id": "req-f3fa8bad", "session_id": "k4-l3a-challenge-s03", "env": "dev", "user_id_hash": "dc9b2ec8da9d", "model": "claude-sonnet-4-5", "feature": "monitoring", "level": "info", "ts": "2026-09-29T09:03:49.164153Z"}
  ```
  - **Correlation ID đại diện:** `req-f3fa8bad`
- **Trace ID và span gây ảnh hưởng:**
  - **Trace ID:** `031027267f9423609922771afec2cdb8` (gắn `correlation_id: req-f3fa8bad`).
  - Cây quan sát waterfall hiển thị rõ 3 tầng: Root observation `lab-agent-run` (tổng thời gian 3.65s), bên trong gồm 2 child observations:
    - Child span 1: `retrieval` (type `retriever`, thanh xanh lá) chiếm **2.51s** (chiếm phần lớn thời gian và là nguyên nhân chính gây trễ).
    - Child span 2: `generation` (type `generation`) chỉ chiếm **151ms**.
  $\implies$ Span gây ảnh hưởng chính (bottleneck) được định vị chính xác tại child span `retrieval`.
- **Root cause:** Hiện tượng chậm bắt nguồn từ lớp truy xuất dữ liệu RAG (mô phỏng bởi cờ `rag_slow` qua `time.sleep(2.5)` trong `app/mock_rag.py`). Trong hệ thống production thực tế, đây là triệu chứng điển hình của việc Vector Database (Pinecone/Milvus/Qdrant) bị nghẽn I/O, latency mạng cao giữa API và Vector DB, hoặc thiếu index khiến việc tìm kiếm similarity search trên embedding bị chậm nghiêm trọng.
- **Fix action:**
  1. *Ngắn hạn:* Cấu hình timeout tối đa cho vector retrieval client (ví dụ: `timeout=1000ms`). Nếu vượt quá thời gian này, kích hoạt fallback trả về context mặc định hoặc cho LLM trả lời trực tiếp kèm ghi chú disclaimer để đảm bảo SLO độ trễ.
  2. *Trung hạn:* Triển khai semantic cache (Redis Semantic Caching) cho các query phổ biến thuộc feature `monitoring` nhằm giảm tải 70-80% truy vấn trực tiếp vào vector database.
  3. *Dài hạn:* Tối ưu index HNSW/IVF cho kho vector, scale out thêm read replicas cho cụm vector store và đặt cùng VPC/region với backend API để triệt tiêu network latency.
- **Preventive measure:**
  1. Cấu hình Alert Rule `high_latency_p95` (như đã khai báo trong `config/alert_rules.yaml`) gửi thông báo Slack tới team trực oncall khi P95 latency vượt ngưỡng trong 5 phút.
  2. Bổ sung metric giám sát độc lập cho RAG: `retrieval_latency_ms` (P95/P99) và `retrieval_timeout_total` để phát hiện sự cố ở tầng vector DB trước khi ảnh hưởng diện rộng tới người dùng.
  3. Triển khai Circuit Breaker cho service truy xuất tài liệu để ngăn chặn hiện tượng cascading failure làm nghẽn toàn bộ luồng xử lý API.

## 8. Giải thích và tự đánh giá

- **Một quyết định kỹ thuật quan trọng và lý do:** Việc bind và truyền `correlation_id` xuyên suốt từ Middleware HTTP $\to$ Structlog Contextvars $\to$ Metadata của Langfuse Trace. Quyết định này giúp liên kết hai hệ sinh thái giám sát riêng biệt (structured logs cục bộ và distributed traces trên cloud) lại với nhau, biến việc điều tra sự cố từ mơ hồ thành quy trình chuẩn xác chỉ trong vài phút.
- **Một lỗi/blocker đã gặp:** Ban đầu file `data/logs.jsonl` chứa các bản ghi log từ trước khi áp dụng bộ lọc PII và correlation ID mới, khiến công cụ `validate_logs.py` quét toàn bộ file và chấm điểm thấp dù code đã được cập nhật.
- **Cách tìm nguyên nhân và xử lý:** Đọc kỹ cơ chế hoạt động của `scripts/validate_logs.py`, nhận ra script duyệt từ đầu đến cuối file log. Cách xử lý là lưu baseline làm bằng chứng đối chứng, sau đó dọn dẹp log cũ, restart API server và chạy lại load test để sinh ra tập log chuẩn sạch.
- **Cách hiểu luồng Metrics → Logs → Traces:**
  - *Metrics (What/When):* Phát hiện triệu chứng bất thường (ví dụ: Dashboard cảnh báo P95 latency tăng vọt vào thời điểm cụ thể).
  - *Logs (Where/Which):* Thu hẹp phạm vi và xác định những request cụ thể bị ảnh hưởng, trích xuất mã định danh duy nhất `correlation_id`.
  - *Traces (Why/How):* Đi sâu vào bên trong request đó thông qua biểu đồ waterfall để nhìn thấy từng child span (retrieval vs generation), từ đó tìm ra chính xác mắt xích bị chậm/lỗi gây ra sự cố (Root Cause).
- **Vai trò của prompt version, token/cost, SLO hoặc rollback trong vận hành LLM:**
  - *Prompt Versioning & Rollback:* Giúp quản trị prompt chuyên nghiệp như source code, thử nghiệm prompt mới an toàn với nhãn `candidate` và rollback về `baseline` trên production ngay lập tức mà không cần redeploy backend.
  - *Token & Cost:* Chi phí mô hình LLM biến động theo độ dài ngữ cảnh và câu trả lời; việc giám sát token/cost theo thời gian thực giúp ngăn chặn tình trạng tràn context hoặc tấn công vét cạn ngân sách (cost spike).
  - *SLO & Error Budget:* Đưa ra thước đo định lượng giữa tốc độ ra mắt tính năng và độ tin cậy dịch vụ, giúp đội ngũ kỹ thuật quyết định khi nào cần đóng băng tính năng để tối ưu hệ thống.
- **Điều quan trọng nhất đã học:** Tư duy vận hành hệ thống AI toàn diện (LLMOps) theo chuẩn công nghiệp: Từ logging có cấu trúc, che chắn thông tin nhạy cảm (PII Redaction), truy vết phân tán (Distributed Tracing), đến thiết lập hàng rào phòng vệ bằng SLO, Alert và Runbook.
- **Hạn chế hoặc phần chưa hoàn thành, nếu có:** Bộ regex PII hiện tại giải quyết tốt 4 loại dữ liệu định dạng chuẩn (email, SĐT, CCCD, thẻ ngân hàng); trong tương lai có thể mở rộng sang mô hình NER (Named Entity Recognition) để tự động che mờ địa chỉ và tên riêng tự nhiên.

## 9. Checklist trước khi nộp

- [x] Kết quả và evidence thuộc commit SHA cuối.
- [x] Tất cả ảnh/output mở được bằng đường dẫn tương đối.
- [x] Incident evidence nối đúng metric → log → trace.
- [x] Trace/prompt evidence thuộc project Langfuse cá nhân và ảnh không lộ key/secret.
- [x] Repository chạy lại được theo README.
- [x] Không có secret, API key, PII thô hoặc evidence của người khác/lớp khác.
- [x] URL repo và commit SHA cuối đã được nộp trên LMS/Codelabs.

