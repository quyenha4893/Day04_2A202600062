# TravelBuddy - Trợ lý Du lịch Thông minh

Chatbot tư vấn du lịch Việt Nam sử dụng LangGraph ReAct Agent, tích hợp các tool tìm chuyến bay, khách sạn và tính ngân sách.

## Kiến trúc

```
User → Agent Node → LLM (GPT-4o-mini)
                      ↓ (tool calls)
                  Tool Node → search_flights / search_hotels / calculate_budget
                      ↓ (tool results)
                  Agent Node → Final Response
```

## Cài đặt

```bash
pip install -r requirements.txt
```

## Cấu hình

Tạo file `.env` từ template:

```bash
cp .env.example .env
```

Điền API key của bạn vào file `.env`:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Chạy

```bash
python agent.py
```

## Tools

| Tool | Mô tả |
|------|--------|
| `search_flights` | Tìm chuyến bay giữa hai thành phố |
| `search_hotels` | Tìm khách sạn theo thành phố và ngân sách |
| `calculate_budget` | Tính toán và kiểm tra ngân sách chuyến đi |

## Các tuyến bay hỗ trợ

- Hà Nội ↔ Đà Nẵng
- Hà Nội ↔ Phú Quốc
- Hà Nội ↔ Hồ Chí Minh
- Hồ Chí Minh ↔ Đà Nẵng
- Hồ Chí Minh ↔ Phú Quốc

## Thành phố có khách sạn

Đà Nẵng, Phú Quốc, Hồ Chí Minh