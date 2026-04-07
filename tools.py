from langchain_core.tools import tool
import re

# =====================================================================
# MOCK DATA - Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases
# =====================================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1450000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2800000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1200000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1350000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1100000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1600000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1300000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3200000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1300000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1800000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1200000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 350000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1500000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2800000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1400000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 800000, "area": "Quận 1", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180000, "area": "Quận 3", "rating": 4.6},
    ],
}

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy chuyến bay, trả về thông báo không có chuyến
    """
    # TODO: Sinh viên tự triển khai
    # - Tra cứu FLIGHTS_DB với key (origin, destination)
    flights = FLIGHTS_DB.get((origin, destination))
    
    # - Nếu không tìm thấy -> thử tra ngược (destination, origin)
    if not flights:
        flights = FLIGHTS_DB.get((destination, origin))
    
    # - Nếu tìm thấy -> format danh sách chuyến bay dễ đọc bao gồm giá tiền
    if flights:
        result = f"Danh sách chuyến bay giữa {origin} và {destination}:\n"
        for f in flights:
            # Gợi ý: format giá tiền có dấu chấm phân cách (1.450.000₫) 
            price_formatted = f"{f['price']:,}₫".replace(",", ".")
            result += f"- {f['airline']} | {f['departure']} -> {f['arrival']} | Giá: {price_formatted} ({f['class']})\n"
        return result
    
    # - Nếu cũng không có -> "Không tìm thấy chuyến bay từ X đến Y"
    return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    - Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    # TODO: Sinh viên tự triển khai
    # - Tra cứu HOTELS_DB[city]
    hotels = HOTELS_DB.get(city)
    if not hotels:
        return f"Không tìm thấy dữ liệu khách sạn tại {city}."

    # - Lọc theo max_price_per_night
    filtered_hotels = [h for h in hotels if h["price_per_night"] <= max_price_per_night]

    # - Sắp xếp theo rating giảm dần
    filtered_hotels.sort(key=lambda x: x["rating"], reverse=True)

    # - Format đẹp. Nếu không có kết quả -> trả về thông báo yêu cầu tăng ngân sách
    if not filtered_hotels:
        # Format giá Y để hiển thị cho đẹp (VD: 500.000)
        price_y = f"{max_price_per_night:,}".replace(",", ".")
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {price_y}/đêm. Hãy thử tăng ngân sách."

    # Nếu có kết quả, trả về danh sách đã format
    result = f"Danh sách khách sạn tại {city} phù hợp với ngân sách của bạn:\n"
    for h in filtered_hotels:
        p_fmt = f"{h['price_per_night']:,}₫".replace(",", ".")
        result += f"- {h['name']} ({h['stars']}⭐) | Giá: {p_fmt}/đêm | Khu vực: {h['area']} | Đánh giá: {h['rating']}\n"
    
    return result

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy, định dạng 'tên_khoản: số_tiền
    """
    # TODO: Sinh viên tự triển khai
    try:
        # 1. Parse chuỗi expenses thành dict {tên: số_tiền}
        # Ví dụ đầu vào: 'vé_máy_bay:890000, khách_sạn:650000'
        print(f"--- Đang tính toán ngân sách cho các khoản: {expenses} ---")
        expense_items = [item.split(":") for item in expenses.split(",")]
        expense_dict = {k.strip(): int(v.strip()) for k, v in expense_items}
        
        # 2. Tính tổng chi phí
        total_spent = sum(expense_dict.values())
        
        # 3. Tính số tiền còn lại = total_budget - tổng chi phí
        remaining = total_budget - total_spent
        
        # Hàm bổ trợ để format tiền tệ 1.000.000₫
        def fmt(n): return f"{n:,}₫".replace(",", ".")

        # 4. Format bảng chi tiết
        lines = ["Bảng chi phí:"]
        for name, amount in expense_dict.items():
            # Chuyển 'vé_máy_bay' thành 'Vé máy bay' để hiển thị đẹp hơn
            display_name = name.replace("_", " ").capitalize()
            lines.append(f"- {display_name}: {fmt(amount)}")
        
        lines.append("---")
        lines.append(f"Tổng chi: {fmt(total_spent)}")
        lines.append(f"Ngân sách: {fmt(total_budget)}")
        lines.append(f"Còn lại: {fmt(remaining)}")
        
        # 5. Nếu âm -> Thông báo vượt ngân sách
        if remaining < 0:
            lines.append(f"Vượt ngân sách {fmt(abs(remaining))}! Cần điều chỉnh.")
            
        return "\n".join(lines)

    except (ValueError, IndexError):
        # 6. Xử lý lỗi: nếu expenses format sai -> trả về thông báo lỗi rõ ràng
        return "Lỗi: Định dạng chuỗi chi phí không hợp lệ. Vui lòng sử dụng 'tên_khoản:số_tiền, ...'"