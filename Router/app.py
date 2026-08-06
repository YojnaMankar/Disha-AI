from langchain_ollama import ChatOllama
from langchain_core.messages import (
SystemMessage,
HumanMessage,
AIMessage
)
# ==========================
# Load Model
# ==========================

model = ChatOllama(
    model="qwen3:1.7b",
    temperature=0,
)

# ==========================
# Study Handler
# ==========================

def study_handler(query):
    print("\nStudy Handler Calling...\n")

    response = model.invoke([
        SystemMessage(
            content="""
You are a friendly teacher.

Explain every topic in very simple language.

Rules:
- Explain in student level English.
- Keep answer short.
- Give example if possible.
"""
        ),
        HumanMessage(content=query)
    ])

    return response


# ==========================
# Practice Handler
# ==========================

def practice_handler(query):
    print("\nPractice Handler Calling...\n")

    response = model.invoke([
        SystemMessage(
            content="""
You    are a coding trainer.

If the user asks for practice,
generate:

1. One practice question
2. Difficulty
3. Hint

Do NOT give solution unless user asks.
"""
        ),
        HumanMessage(content=query)
    ])

    return response


# ==========================
# Weather Handler
# ==========================

def weather_handler(query):
    return "Weather API is not connected yet."


# ==========================
# General Handler
# ==========================

def general_handler(query):
    print("\nGeneral Handler Calling...\n")

    response = model.invoke([
        SystemMessage(
            content="You are a helpful AI assistant."
        ),
        HumanMessage(content=query)
    ])

    return response

#============================
#Career Handler
#=============================
def career_handler(query):
    print("\nCareer Handler Calling....\n")

    response = model.invoke([
        SystemMessage(
            content="""
You are a experienced career counselor.
Help students with:
-career Guidance
-Resume
-Internship
-Jobs
-Interviw Preparation
-Career Rodmap
-Skills
-Higher Studies

Give practical advice.
"""
        ),
        HumanMessage(content=query)
    ])
    return response




#=========================
#IT Support Handler
#=========================
def it_support_handler(query):
    print("\nIT Support Handler Callling... \n")
    response = model.invoke([
        SystemMessage(
            content="""
you are a an IT Support Engineer.
Help user solve:
-windows problems
-Linux program
-Software Installation
-Printer Issues
-Network Problems
-Git and Github Errors
-VS Code Errors
-Python error
-WiFi problems
-Troubleshooting

Explain step by step.
"""
        ),
        HumanMessage(content=query)
    ])
    return response

#===========================
#Traver Handler
#===========================
def travel_hanlder(query):
    print("\nTraver Handler Calling... \n")
    rescopnse = model.invoke([
        SystemMessage(
            content="""
You are a professional travel guide.
Help user with:
-Travel destinations
-Trip Planning
-Tourist places
hotels
-Budget travel
-Transportation
-Travel trips
-Best time to visit
-packing suggestions
Give clear amd practical travel advise.
"""
        ),
        HumanMessage(content=query)
    ])
    return rescopnse


# ==========================
# Router
# ==========================

def classify_query(query):

    categories = """
study
practice
weather
general
career
itsupport
travel
"""

    router_prompt = f"""
You are a query router.

You are Job is to Classify the user's request into exactly ONE category.

Categories:

{categories}

Rules:

study:
Questions asking to understand or learn a topic.

practice:
Coding exercises, quizzes, assignments, practice questions.

weather:
Weather, climate, rain, temperature.

general:
Anything else.

career:
career guidance, resume, jobs, internship, interview prepration, skills.

itsupport:
windows, linux, networking, github, git, vs code, printer, wifi,
software installation, computer trobleshooting, python error.

travel:
travel planning, tourist placesw, trip ideas, hotels, transportation,
vacation, budget travel, best place to visit.

Return ONLY one word.

"""

    response = model.invoke([
        SystemMessage(content=router_prompt),
        HumanMessage(content=query)
    ])

    return response.content.strip().lower()


# ==========================
# Main Program
# ==========================

while True:

    query = input("\nEnter your query (type exit to quit): ")

    if query.lower() == "exit":
        print("Good Bye!")
        break

    category = classify_query(query)

    print("\nDetected Category:", category)

    if category == "study":
        ans = study_handler(query)
        print("\nAnswer:\n")
        print(ans.content)

    elif category == "practice":
        ans = practice_handler(query)
        print("\nAnswer:\n")
        print(ans.content)

    elif category == "weather":
        ans = weather_handler(query)
        print("\nAnswer:\n")
        print(ans)


    elif category == "carrer":
        ans = career_handler(query)
        print("\nAnswer:\n")
        print(ans.content)
    elif category == "itsupport":
        ans = it_support_handler(query)
        print("\nAnswer:\n")
        print(ans.content)

    elif category == "travel":
        ans = career_handler(query)
        print("\nAnswer:\n")
        print(ans.content)

    else:
        ans = general_handler(query)
        print("\nAnswer:\n")
        print(ans.content)