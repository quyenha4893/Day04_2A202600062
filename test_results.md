# Test Results

## Test Case 1
D:\porjects\assignments\lab4_agent\venv\Lib\site-packages\langchain_core\_api\deprecation.py:25: UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.
  from pydantic.v1.fields import FieldInfo as FieldInfoV1
\============================================================
TravelBuddy - Trợ lý Du lịch Thông minh
   Gõ 'quit', 'exit' hoặc 'q' để thoát
\============================================================

Bạn: Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Chào bạn! Rất vui được hỗ trợ bạn lên kế hoạch cho chuyến đi sắp tới. Việt Nam mình có nhiều địa điểm đẹp lắm, bạn muốn đi đâu, vào khoảng thời gian nào và ngân sách dự kiến của bạn là bao nhiêu để mình có thể tư vấn cụ thể hơn nhé?

## Test Case 2
Bạn: Tìm giúp tôi chuyến bay từ Hà Nội đến Đà Nẵng

TravelBuddy đang suy nghĩ...
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
Trả lời trực tiếp

TravelBuddy: Tuyệt vời! Có một vài lựa chọn cho bạn đây:

Chuyến bay:
- Vietnam Airlines | 06:00 -> 07:20 | Giá: 1.450.000₫ (economy)
- Vietnam Airlines | 14:00 -> 15:20 | Giá: 2.800.000₫ (business)
- VietJet Air | 08:30 -> 09:50 | Giá: 890.000₫ (economy)
- Bamboo Airways | 11:00 -> 12:20 | Giá: 1.200.000₫ (economy)

Bạn muốn chọn chuyến nào và có muốn tìm khách sạn ở Đà Nẵng luôn không? Nếu có, cho mình biết ngân sách mỗi đêm của bạn nhé!

## Test Case 3
Bạn: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

TravelBuddy đang suy nghĩ...
Gọi tool: search_flights({'destination': 'Phú Quốc', 'origin': 'Hà Nội'})
Gọi tool: search_hotels({'max_price_per_night': 1950000, 'city': 'Phú Quốc'})
Gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 'vé máy bay: 1100000, khách sạn: 400000'})
--- Đang tính toán ngân sách cho các khoản: vé máy bay: 1100000, khách sạn: 400000 ---
Trả lời trực tiếp

TravelBuddy: Chào bạn, với ngân sách 5 triệu cho chuyến đi Phú Quốc 2 đêm từ Hà Nội, mình có gợi ý này nhé:

Chuyến bay:
*   VietJet Air | 16:00 -> 18:15 | Giá: 1.100.000₫ (economy)

Khách sạn:
*   9Station Hostel (2⭐) | Giá: 200.000₫/đêm (cho 2 đêm là 400.000₫) | Khu vực: Dương Đông | Đánh giá: 4.5

Tổng chi phí ước tính: 1.100.000₫ (vé máy bay) + 400.000₫ (khách sạn 2 đêm) = 1.500.000₫.
Bạn còn dư 3.500.000₫ để ăn uống, đi lại và vui chơi đó!

Gợi ý thêm: 9Station Hostel ở khu vực Dương Đông khá trung tâm, tiện đi lại và khám phá chợ đêm Phú Quốc. Bạn có thể thưởng thức hải sản tươi ngon ở đây nhé!

## Test Case 4
Bạn: Tôi muốn đặt khách sạn

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Bạn muốn đặt khách sạn ở thành phố nào và ngân sách của bạn cho mỗi đêm là bao nhiêu?

## Test Case 5
Bạn: Giải giúp tôi bài toán lập trình Python về linked list

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Chào bạn, rất tiếc mình chỉ có thể hỗ trợ bạn về các vấn đề liên quan đến du lịch, đặt phòng, đặt vé thôi. Mình không chuyên về lập trình nên không giúp bạn giải bài toán này được rồi.