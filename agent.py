from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
# Import các tools đã viết ở Phần 2
from tools import search_flights, search_hotels, calculate_budget 
from dotenv import load_dotenv

# 0. Load biến môi trường
load_dotenv()

# 1. Đọc System Prompt từ file đã tạo ở Phần 1
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State (Trạng thái của Agent)
class AgentState(TypedDict):
    # add_messages giúp cộng dồn lịch sử chat thay vì ghi đè
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và kết nối với Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0,
)
llm_with_tools = llm.bind_tools(tools_list)

# 4. Định nghĩa Agent Node (Nút xử lý chính)
def agent_node(state: AgentState):
    messages = state["messages"]
    
    # Nếu tin nhắn đầu tiên không phải SystemMessage, chèn nó vào đầu
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    response = llm_with_tools.invoke(messages)

    # === LOGGING để quan sát Agent suy nghĩ ===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"Gọi tool: {tc['name']}({tc['args']})")
    else:
        print(f"Trả lời trực tiếp")
        
    return {"messages": [response]}

# 5. Xây dựng Graph (Đồ thị luồng công việc)
builder = StateGraph(AgentState)

# Thêm các nút (Nodes)
builder.add_node("agent", agent_node)
tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# TODO: Sinh viên khai báo edges (Các đường nối luồng)
# builder.add_edge(START, ...)
builder.add_edge(START, "agent")
# builder.add_conditional_edges("agent", tools_condition)
builder.add_conditional_edges("agent", tools_condition)
# builder.add_edge("tools", ...)
builder.add_edge("tools", "agent")

graph = builder.compile()

# 6. Chat loop (Vòng lặp tương tác người dùng)
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy - Trợ lý Du lịch Thông minh")
    print("   Gõ 'quit', 'exit' hoặc 'q' để thoát")
    print("=" * 60)
    
    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
            
        print("\nTravelBuddy đang suy nghĩ...")
        # Chạy graph với đầu vào từ người dùng
        result = graph.invoke({"messages": [("human", user_input)]})
        
        # Lấy tin nhắn cuối cùng trong danh sách phản hồi
        final = result["messages"][-1]
        # Kiểm tra nếu nội dung là chuỗi văn bản thuần túy
        if isinstance(final.content, str):
            print(f"\nTravelBuddy: {final.content}")
        # Nếu Gemini trả về dạng list (parts), lấy phần text đầu tiên
        elif isinstance(final.content, list):
            text_content = next((part['text'] for part in final.content if 'text' in part), str(final.content))
            print(f"\nTravelBuddy: {text_content}")