from langchain_ollama import ChatOllama
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)
from langchain_core.tools import tool


# ============================================================
# 1. CREATE TOOLS
# ============================================================

@tool
def get_career_path(career: str) -> str:
    """
    Returns a recommended learning path for a particular career.
    """

    careers = {
        "backend developer": [
            "Python or Node.js",
            "REST APIs",
            "SQL",
            "Git",
            "Docker",
            "Authentication",
            "System Design"
        ],

        "frontend developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Git",
            "REST APIs",
            "Frontend Testing"
        ],

        "data scientist": [
            "Python",
            "Statistics",
            "Pandas",
            "NumPy",
            "Machine Learning",
            "Data Visualization",
            "Deep Learning"
        ],

        "ai engineer": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "LLMs",
            "Prompt Engineering",
            "Embeddings",
            "RAG",
            "AI Agents"
        ]
    }

    career = career.lower()

    if career in careers:
        return "\n".join(
            f"- {skill}"
            for skill in careers[career]
        )

    return "Career path not available."


@tool
def calculate_skill_score(
    completed_skills: str,
    total_skills: int
) -> str:
    """
    Calculates percentage of completed skills.
    """

    completed = len(
        [x for x in completed_skills.split(",") if x.strip()]
    )

    percentage = (completed / total_skills) * 100

    return f"Skill completion: {percentage:.1f}%"


@tool
def get_learning_resources(topic: str) -> str:
    """
    Returns suggested learning resources for a topic.
    """

    resources = {
        "python": [
            "Python official documentation",
            "Python practice problems",
            "Build CLI applications"
        ],

        "sql": [
            "Practice SELECT queries",
            "Learn JOINs",
            "Learn indexes",
            "Practice database design"
        ],

        "docker": [
            "Learn Docker images",
            "Learn containers",
            "Write Dockerfiles",
            "Learn Docker Compose"
        ],

        "machine learning": [
            "Learn supervised learning",
            "Learn unsupervised learning",
            "Practice with datasets"
        ]
    }

    topic = topic.lower()

    if topic in resources:
        return "\n".join(
            f"- {item}"
            for item in resources[topic]
        )

    return "No specific resources found."


# ============================================================
# 2. CREATE MODEL
# ============================================================

model = ChatOllama(
    model="qwen3:1.7b",
    temperature=0,
    think=False
)


# ============================================================
# 3. BIND TOOLS
# ============================================================

tools = [
    get_career_path,
    calculate_skill_score,
    get_learning_resources
]

model_with_tools = model.bind_tools(tools)


# ============================================================
# 4. SYSTEM PROMPT
# ============================================================

system_message = SystemMessage(
    content="""
You are a friendly Career Guidance AI Agent.

Your job is to help students choose careers
and create learning plans.

Rules:

1. Ask questions when you need more information.
2. Use tools when they can provide useful information.
3. Do not invent career paths when a tool can provide one.
4. Explain concepts in simple language.
5. Remember information from the current conversation.
6. Give practical advice suitable for IT students.
"""
)


# ============================================================
# 5. CONVERSATION MEMORY
# ============================================================

conversation = [
    system_message
]


# ============================================================
# 6. TOOL MAP
# ============================================================

tool_map = {
    "get_career_path": get_career_path,
    "calculate_skill_score": calculate_skill_score,
    "get_learning_resources": get_learning_resources
}


# ============================================================
# 7. CHAT LOOP
# ============================================================

print("======================================")
print("       Career Guidance AI Agent")
print("======================================")
print("Type 'quit' to exit.\n")


while True:

    user_text = input("You: ")

    if user_text.lower() == "quit":
        print("Agent: Goodbye!")
        break


    # --------------------------------------------------------
    # Add user message
    # --------------------------------------------------------

    conversation.append(
        HumanMessage(content=user_text)
    )


    # --------------------------------------------------------
    # Ask model
    # --------------------------------------------------------

    response = model_with_tools.invoke(
        conversation
    )


    # --------------------------------------------------------
    # Save AI response
    # --------------------------------------------------------

    conversation.append(response)


    # --------------------------------------------------------
    # Check if AI wants to use a tool
    # --------------------------------------------------------

    if response.tool_calls:

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            tool_args = tool_call["args"]

            print(
                f"\n[Agent is using tool: {tool_name}]"
            )

            print(
                f"[Arguments: {tool_args}]"
            )

            # Find tool
            selected_tool = tool_map[tool_name]

            # Execute tool
            tool_result = selected_tool.invoke(
                tool_args
            )

            print(
                f"[Tool Result: {tool_result}]\n"
            )


            # ------------------------------------------------
            # Add tool result to conversation
            # ------------------------------------------------

            from langchain_core.messages import ToolMessage

            conversation.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                )
            )


        # ----------------------------------------------------
        # Ask model again using tool result
        # ----------------------------------------------------

        final_response = model_with_tools.invoke(
            conversation
        )

        conversation.append(
            final_response
        )

        print(
            "Agent:",
            final_response.content
        )

    else:

        print(
            "Agent:",
            response.content
        )