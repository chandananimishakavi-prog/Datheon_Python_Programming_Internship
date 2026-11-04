import json
import re
from pathlib import Path
FAQ_FILE = Path(__file__).with_name("sample_faq.json")
EXIT_COMMANDS = {"bye", "goodbye", "exit", "quit"}
FALLBACK_MESSAGE = (
    "I'm sorry, I couldn't understand that question. "
    "Please ask about business hours, internship project submission, "
    "or certificate status."
)
INTENT_KEYWORDS = {
    "hours": [
        r"\b(hours?|timings?|working hours?|office hours?|open|close|"
        r"opening time|closing time|business hours?|operation time)\b"
    ],
    "project": [
        r"\b(internship project|project submission|submit my project|"
        r"submit project|upload my project|github|repository|repo link)\b"
    ],
    "certificate": [
        r"\b(certificates?|certificate status|certificate issue|"
        r"when.*certificate|receive.*certificate|code review)\b"
    ],
}
def normalize(text):
    """Convert input to lowercase and normalize whitespace."""
    return re.sub(r"\s+", " ", text.lower().strip())
def load_faq_data():
    """Load and validate the FAQ JSON file."""
    try:
        with FAQ_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError("The JSON root must be an object.")
        greetings = data.get("greetings", [])
        faqs = data.get("faqs", [])
        if not isinstance(greetings, list) or not isinstance(faqs, list):
            raise ValueError("'greetings' and 'faqs' must be lists.")
        valid_faqs = []
        for item in faqs:
            if (
                isinstance(item, dict)
                and isinstance(item.get("question"), str)
                and isinstance(item.get("answer"), str)
            ):
                valid_faqs.append(item)
        if not valid_faqs:
            raise ValueError("No valid FAQ question-and-answer entries found.")
        return greetings, valid_faqs
    except FileNotFoundError:
        print(f"Error: FAQ file not found: {FAQ_FILE}")
        print("Place sample_faq.json in the same folder as chatbot.py.")
        return [], []
    except json.JSONDecodeError as error:
        print(f"Error: Invalid JSON in FAQ file: {error}")
        return [], []
    except (OSError, ValueError) as error:
        print(f"Error loading FAQ data: {error}")
        return [], []
def is_greeting(message, greetings):
    """Recognize a greeting without matching words such as 'this'."""
    greeting_patterns = [
        rf"^{re.escape(normalize(greeting))}[!.?,\s]*$"
        for greeting in greetings
        if isinstance(greeting, str) and greeting.strip()
    ]
    return any(re.search(pattern, message) for pattern in greeting_patterns)
def split_into_queries(message):
    """Split messages that contain multiple questions or requests."""
    parts = re.split(
        r"\s*(?:[?.!,;]|\band\b|\balso\b)\s*",
        message,
        flags=re.IGNORECASE,
    )
    return [part.strip() for part in parts if part.strip()]
def identify_intents(message):
    """Return all recognized FAQ intent names in the user's message."""
    found = []
    for intent, patterns in INTENT_KEYWORDS.items():
        if any(re.search(pattern, message, re.IGNORECASE) for pattern in patterns):
            found.append(intent)
    return found
def answer_query(message, faqs):
    """Match recognized intents to FAQ entries and return their answers."""
    intent_names = identify_intents(message)
    # Map the FAQ entries by their question text.
    faq_by_intent = {}
    for faq in faqs:
        question = normalize(faq["question"])
        if "hours of operation" in question:
            faq_by_intent["hours"] = faq
        elif "internship project" in question:
            faq_by_intent["project"] = faq
        elif "certificate" in question:
            faq_by_intent["certificate"] = faq
    answers = []
    for intent in intent_names:
        faq = faq_by_intent.get(intent)
        if faq:
            answers.append(faq["answer"])
    return answers
def main():
    greetings, faqs = load_faq_data()
    if not faqs:
        print("Chatbot could not start because the FAQ data is unavailable.")
        return
    print("\n==============================================")
    print("       RULE-BASED CUSTOMER SUPPORT BOT")
    print("==============================================")
    print("Type 'bye', 'exit', or 'quit' to end the chat.")
    print("You can ask about working hours, project submission,")
    print("or certificates.\n")
    greeted = False
    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Thank you for chatting. Goodbye!")
            break
        message = normalize(user_input)
        if not message:
            print("Bot: Please enter a question so I can help you.")
            continue
        if message in EXIT_COMMANDS:
            print("Bot: Thank you for chatting. Have a great day!")
            break
        if is_greeting(message, greetings):
            print("Bot: Hello! Welcome to customer support. How can I help you?")
            greeted = True
            continue
        # Support a greeting followed by a question in the same message.
        message = re.sub(
            r"^(hello|hi|hey|good morning|good afternoon)\b[\s,!.]*",
            "",
            message,
            flags=re.IGNORECASE,
        )
        if not message:
            if not greeted:
                print("Bot: Hello! How can I help you today?")
            continue
        queries = split_into_queries(message)
        responses = []
        for query in queries:
            responses.extend(answer_query(query, faqs))
        # Also check the complete message so multi-intent requests are not missed.
        if not responses:
            responses = answer_query(message, faqs)
        # Remove duplicate answers while preserving their order.
        unique_responses = list(dict.fromkeys(responses))
        if unique_responses:
            for response in unique_responses:
                print(f"Bot: {response}")
        else:
            print(f"Bot: {FALLBACK_MESSAGE}")
if __name__ == "__main__":
    main()