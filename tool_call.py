from langchain_core.tools import Tool, tool
from langchain_core.messages import ToolMessage
from langchain_ollama import ChatOllama

#=======================================
#Tool 1 : Multiply
#===================================
@tool
def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers together.

    """
    return a * b

#=======================================
# Tool 2 : calculate Percentage
#=======================================
@tool
def calculate_percentage(obtained: float, total: float) -> float:
    """
    Calculate the percentage of obtained marks out of total marks.

    """
    return (obtained / total) * 100

#=======================================
#Tool 3 : Attendance Percentage
#======================================

@tool
def attendance_percentage(attended: int, total_classes: int )-> float:
    """
    Calculate the attendance percentage based on attended classes and total classes.

    """
    return (attended / total_classes) * 100

#=======================================
# Tool 4 : Electricity Bill
#=======================================

@tool
def electricity_bill(units: int,) -> float:
    """
    Calculate the electricity bill based on the number of units consumed.

    """
    if units <= 100:
        return units * 5
    elif units <= 200:
        return (100*5) + ((units - 100) * 7)
    else:
        return (100*5) + (100*7) + ((units - 200) * 10)


#======================================
# Tool 5 : Simple Interest
#======================================
@tool
def simple_interest(principal: float, rate: float, time: float) -> float:
    """
    Calculate the simple interest based on principal, rate, and time.

    """
    return (principal * rate * time) / 100

#======================================
# Tool 6 : Compound Interest
#======================================
@tool
def compound_interest(principal: float, rate: float, time: float) -> float:
    """
    Calculate the compound interest based on principal, rate, and time.

    """
    amount=principal * ((1 + rate / 100) ** time)
    return amount - principal

#======================================
# Local Model
#======================================



model = ChatOllama(
    model="qwen3:1.7b",
    temperature=0,
    thinking=False
)

#======================================
# Bind Tools
#======================================

model_with_tools=model.bind_tools([
    multiply,
    calculate_percentage,
    attendance_percentage,
    electricity_bill,
    simple_interest,
    compound_interest])

#======================================
# Main Loop
#======================================
while True:
    query = input("\nEnter your question (or type 'exit' to quit): ")
    if query.lower() == "exit":
        print("Good Bye!")
        break
    messages = [
        ("human", query)
    ]
    response = model_with_tools.invoke(messages)
    print("\nAI Response:")
    print(response)
    messages.append(response)

    for call in response.tool_calls:
        if call["name"] == "multiply":
            result = multiply.invoke(call["args"])
        elif call["name"] == "calculate_percentage":
            result = calculate_percentage.invoke(call["args"])
        elif call["name"] == "attendance_percentage":
            result = attendance_percentage.invoke(call["args"])
        elif call["name"] == "electricity_bill":
            result = electricity_bill.invoke(call["args"])
        elif call["name"] == "simple_interest":
            result = simple_interest.invoke(call["args"])
        elif call["name"] == "compound_interest":
            result = compound_interest.invoke(call["args"])
        else:
            continue
        print("\nTool Call Result:")
        print(result)
        print(result)
        messages.append(
                ToolMessage(
                    content=str(result),
tool_call_id=call["id"]
                )
            )

final_response = model_with_tools.invoke(messages)
print("\nFinal Answer:")
print(final_response.content)
