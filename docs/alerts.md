# Template Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert 1

- Tên: High Latency (P95 Latency > 3000ms)
- Severity: warning
- Duration: 5m
- Kênh thông báo: Slack (#alerts-llmops)
- SLI/SLO liên quan: `fast_successful_requests` (SLO P95 latency <= 3000ms)
- Điều kiện và thời gian duy trì: `latency_p95_ms > 3000` duy trì trong 5 phút
- Ảnh hưởng tới người dùng: Người dùng bị chậm khi nhận câu trả lời từ hệ thống, trải nghiệm chat bị gián đoạn hoặc giật lag.
- Ba bước kiểm tra đầu tiên:
  1. Mở Dashboard kiểm tra panel `Latency percentiles and TTFT` để xác nhận P95/P99 latency và TTFT có đồng loạt tăng không.
  2. Lọc file `data/logs.jsonl` tìm các event `response_sent` có `latency_ms > 3000` trong khoảng thời gian diễn ra alert để lấy sample `correlation_id`.
  3. Mở Langfuse UI tra cứu trace bằng `correlation_id` đó để xem waterfall, đối chiếu xem độ trễ chủ yếu đến từ span `retrieval` hay `generation`.
- Mitigation tạm thời: Bật cache cho retrieval, giảm độ dài document context, hoặc chuyển hướng traffic sang model nhẹ hơn / fallback endpoint.
- Owner: oncall-llmops

## Alert 2

- Tên: High Error Rate (Error Rate > 2%)
- Severity: critical
- Duration: 5m
- Kênh thông báo: Slack (#alerts-llmops)
- SLI/SLO liên quan: Guardrail `error_rate_pct_max: 2` và `fast_successful_requests`
- Điều kiện và thời gian duy trì: `error_rate_pct > 2%` duy trì trong 5 phút
- Ảnh hưởng tới người dùng: Người dùng nhận thông báo lỗi HTTP 500, không nhận được câu trả lời từ assistant.
- Ba bước kiểm tra đầu tiên:
  1. Kiểm tra panel `Error rate and retrieval success` trên Dashboard để xem tỷ lệ lỗi và breakdown theo `error_type`.
  2. Tìm trong `data/logs.jsonl` các dòng `request_failed`, kiểm tra `payload.detail` và trích xuất `correlation_id`.
  3. Vào Langfuse tìm trace tương ứng để kiểm tra span gặp exception (retrieval lỗi hay prompt/generation timeout).
- Mitigation tạm thời: Trả về câu trả lời graceful fallback ("Hệ thống đang quá tải, vui lòng thử lại sau"), hoặc khởi động lại instance lỗi.
- Owner: oncall-llmops

## Alert 3

- Tên: Retrieval Success Rate Degradation (< 90%)
- Severity: warning
- Duration: 10m
- Kênh thông báo: Slack (#alerts-llmops)
- SLI/SLO liên quan: Guardrail `retrieval_success_rate_pct_min: 90`
- Điều kiện và thời gian duy trì: `retrieval_success_rate_pct < 90%` duy trì trong 10 phút
- Ảnh hưởng tới người dùng: Assistant trả lời chung chung hoặc hallucination do không truy xuất được tài liệu liên quan từ kho tri thức.
- Ba bước kiểm tra đầu tiên:
  1. Kiểm tra panel `Error rate and retrieval success` (chỉ số retrieval success rate) và panel `Quality proxy`.
  2. Lọc log sự kiện có `tool_success == false` hoặc `quality_score < 0.75` và lấy `correlation_id`.
  3. Mở Langfuse trace để kiểm tra span `retrieval`: xem vector store connection, latency và `doc_count`.
- Mitigation tạm thời: Chuyển sang fallback tài liệu mặc định (default corpus) hoặc tạm thời chuyển mode sang direct answer kèm disclaimer.
- Owner: oncall-llmops
