import json
from pathlib import Path

def load_conversations(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def explore_structure(conversations):
    print(f"🔍 Found {len(conversations)} conversation objects.\n")

    for i, convo in enumerate(conversations[:5], 1):  # Limit for brevity
        print(f"📄 Conversation {i} - Top-level keys:")
        for key in convo.keys():
            print(f"   - {key}")
        print()

    # Explore the structure of the first one more deeply
    print("🔬 Sample Conversation Structure (1st entry):")
    print(json.dumps(conversations[0], indent=2)[:2000])  # Truncate for readability

def main():
    input_file = Path("conversations.json")
    if not input_file.exists():
        print("❌ File not found: conversations.json")
        return

    conversations = load_conversations(input_file)
    if not isinstance(conversations, list):
        print("❌ JSON does not appear to be a list of conversations.")
        return

    explore_structure(conversations)

if __name__ == "__main__":
    main()
