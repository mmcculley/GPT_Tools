""" 
ChatGPT Conversation Exporter

Parses a ChatGPT `conversations.json` file and exports each conversation into
Markdown files, grouped optionally by date. Also generates metadata indexes
and statistics summaries.

Author: Michael McCulley
Version: 1.2.0
License: MIT

Contact: me@michaelmcculley.com

Features:
- Group by year/month
- Set file creation timestamps
- Emoji or plain speaker labels
- Generate .csv and .md summary files
- Optional verbose output for tracking progress

Usage:
  python parse_conversations.py --group-by-date --generate-index --generate-stats --verbose
"""

__author__ = "Michael McCulley"
__version__ = "1.2.0"

import json
import re
import os
import sys
import time
import csv
import argparse
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

# ---------- Helpers ----------

def sanitize_filename(name):
    name = re.sub(r'[<>:"/\\|?*\n\r]', '_', name)
    name = re.sub(r'\s+', '_', name)
    return name.strip('_')[:100]

def get_year_month(timestamp):
    try:
        if isinstance(timestamp, str):
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        elif isinstance(timestamp, (float, int)):
            dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        else:
            return "Unknown"
        return dt.strftime("%Y-%m")
    except Exception:
        return "Unknown"

def set_file_timestamps(path, timestamp):
    try:
        os.utime(path, (timestamp, timestamp))
        if os.name == "nt":
            import ctypes
            from ctypes.wintypes import FILETIME
            wintime = int((timestamp + 11644473600) * 10000000)
            low = wintime & 0xFFFFFFFF
            high = wintime >> 32
            create_time = FILETIME(low, high)
            CreateFile = ctypes.windll.kernel32.CreateFileW
            SetFileTime = ctypes.windll.kernel32.SetFileTime
            CloseHandle = ctypes.windll.kernel32.CloseHandle
            handle = CreateFile(str(path), 0x0100, 0, None, 3, 0, None)
            if handle != -1:
                SetFileTime(handle, ctypes.byref(create_time), None, None)
                CloseHandle(handle)
    except Exception as e:
        print(f"⚠️ Failed to set timestamps on {path}: {e}", file=sys.stderr)

def write_index(index_data, output_root):
    index_file = Path(output_root) / "conversations_index.csv"
    with open(index_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Title", "Date", "Archived", "Memory Scope", "Model", "Message Count", "Word Count", "Folder", "File Name", "Conversation ID"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in index_data:
            writer.writerow(row)

def write_stats(index_data, output_root):
    stats_file = Path(output_root) / "conversations_stats.csv"
    total_convos = len(index_data)
    archived = sum(1 for row in index_data if row["Archived"])
    active = total_convos - archived
    total_messages = sum(int(row["Message Count"]) for row in index_data)
    total_words = sum(int(row["Word Count"]) for row in index_data)
    avg_messages = round(total_messages / total_convos, 2) if total_convos else 0
    avg_words = round(total_words / total_convos, 2) if total_convos else 0
    model_stats = defaultdict(lambda: {"convos": 0, "messages": 0, "words": 0})
    for row in index_data:
        model = row.get("Model", "unknown")
        model_stats[model]["convos"] += 1
        model_stats[model]["messages"] += int(row["Message Count"])
        model_stats[model]["words"] += int(row["Word Count"])
    with open(stats_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total Conversations", total_convos])
        writer.writerow(["Archived", archived])
        writer.writerow(["Active", active])
        writer.writerow(["Total Messages", total_messages])
        writer.writerow(["Total Word Count", total_words])
        writer.writerow(["Avg. Messages per Conversation", avg_messages])
        writer.writerow(["Avg. Words per Conversation", avg_words])
        writer.writerow([])
        writer.writerow(["Model", "Conversations", "Messages", "Words"])
        for model, data in model_stats.items():
            writer.writerow([model, data["convos"], data["messages"], data["words"]])

def write_summary(index_data, output_root):
    from collections import Counter
    summary_file = Path(output_root) / "SUMMARY.md"
    total = len(index_data)
    archived = sum(1 for row in index_data if row["Archived"])
    active = total - archived
    messages = sum(int(row["Message Count"]) for row in index_data)
    words = sum(int(row["Word Count"]) for row in index_data)
    avg_msgs = round(messages / total, 2) if total else 0
    avg_words = round(words / total, 2) if total else 0
    by_month = Counter(row["Folder"] for row in index_data)
    by_model = Counter(row.get("Model", "unknown") for row in index_data)
    sample_files = [row["File Name"] for row in index_data[:10]]
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# ChatGPT Export Summary\n\n")
        f.write(f"**Total Conversations:** {total}\n")
        f.write(f"**Archived:** {archived}\n")
        f.write(f"**Active:** {active}\n")
        f.write(f"**Total Messages:** {messages}\n")
        f.write(f"**Total Word Count:** {words}\n")
        f.write(f"**Avg. Messages/Conversation:** {avg_msgs}\n")
        f.write(f"**Avg. Words/Conversation:** {avg_words}\n\n")
        f.write("---\n\n")
        f.write("## 📅 Conversations by Month\n\n")
        for month, count in sorted(by_month.items()):
            f.write(f"- {month}: {count}\n")
        f.write("\n---\n\n")
        f.write("## 🤖 Conversations by Model\n\n")
        for model, count in sorted(by_model.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- {model}: {count}\n")
        f.write("\n---\n\n")
        f.write("## 🗃️ Sample Files\n\n")
        for name in sample_files:
            f.write(f"- {name}\n")

# ---------- Core Parsing ----------

def load_conversations(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def parse_conversation(convo, use_emojis=True):
    parsed = {
        "id": convo.get("id", "unknown"),
        "title": convo.get("title", "Untitled"),
        "create_time": convo.get("create_time", "Unknown"),
        "memory_scope": convo.get("memory_scope", "unknown"),
        "default_model_slug": convo.get("default_model_slug", "unknown"),
        "conversation_id": convo.get("conversation_id", "unknown"),
        "is_archived": convo.get("is_archived", False),
        "messages": []
    }
    if use_emojis:
        mapping = {"user": "👤", "assistant": "🤖", "system": "⚙️"}
    else:
        mapping = {"user": "User", "assistant": "Assistant", "system": "System"}
    for message in convo.get("mapping", {}).values():
        message_data = message.get("message")
        if not message_data:
            continue
        role = message_data.get("author", {}).get("role", "unknown")
        parts = message_data.get("content", {}).get("parts", [])
        content = parts[0].get("text", "") if parts and isinstance(parts[0], dict) else (str(parts[0]) if parts else "")
        parsed["messages"].append({
            "role": mapping.get(role, role),
            "content": content.strip()
        })
    return parsed

# ---------- Export Core ----------

def export_conversations(parsed_conversations, output_root="parsed_conversations", grouped=False, set_dates=False, verbose=False):
    output_path = Path(output_root)
    output_path.mkdir(exist_ok=True)
    folder_counters = {}
    index_data = []
    for convo in parsed_conversations:
        year_month = get_year_month(convo['create_time']) if grouped else "."
        folder = output_path / year_month
        folder.mkdir(parents=True, exist_ok=True)
        folder_counters.setdefault(year_month, 0)
        folder_counters[year_month] += 1
        index_num = folder_counters[year_month]
        safe_title = sanitize_filename(convo['title'] or "Untitled")
        filename = folder / f"{index_num:03d}_{safe_title}.md"
        if verbose:
            print(f"Writing: {filename}")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {convo['title']}\n")
            f.write(f"**Created:** {convo['create_time']}\n\n")
            for msg in convo["messages"]:
                f.write(f"{msg['role']}: {msg['content']}\n\n")
        if set_dates:
            try:
                dt = datetime.fromisoformat(convo['create_time'].replace("Z", "+00:00"))                     if isinstance(convo['create_time'], str)                     else datetime.fromtimestamp(convo['create_time'], tz=timezone.utc)
                set_file_timestamps(filename, dt.timestamp())
            except Exception:
                pass
        word_count = sum(len(msg['content'].split()) for msg in convo["messages"])
        index_data.append({
            "Title": convo['title'],
            "Date": (
                datetime.fromtimestamp(convo['create_time'], tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
                if isinstance(convo['create_time'], (int, float)) else
                convo['create_time'].replace("T", " ").replace("Z", "")
            ),
            "Archived": convo.get('is_archived', "unknown"),
            "Memory Scope": convo.get("memory_scope", "unknown"),
            "Model": convo.get("default_model_slug", "unknown"),
            "Message Count": len(convo["messages"]),
            "Word Count": word_count,
            "Folder": year_month,
            "File Name": filename.name,
            "Conversation ID": convo.get('conversation_id', "unknown")
        })
    return index_data

# ---------- CLI Entry Point ----------

def main():
    parser = argparse.ArgumentParser(
        description="📦 ChatGPT Conversation Exporter",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--group-by-date", action="store_true", help="Group conversations by year and month")
    parser.add_argument("--no-emojis", action="store_true", help="Use plain speaker labels instead of emojis")
    parser.add_argument("--set-file-dates", action="store_true", help="Set file timestamps from creation time")
    parser.add_argument("--generate-index", action="store_true", help="Generate conversations_index.csv")
    parser.add_argument("--generate-stats", action="store_true", help="Generate statistics and SUMMARY.md")
    parser.add_argument("--verbose", action="store_true", help="Print progress while exporting")
    parser.add_argument("--input", default="conversations.json", help="Input JSON file")
    parser.add_argument("--output", default="parsed_conversations", help="Output folder")
    parser.add_argument("--version", action="version", version="ChatGPT Conversation Exporter v1.2.0")
    args = parser.parse_args()

    conversations_data = load_conversations(args.input)
    parsed_conversations = [
        parse_conversation(c, use_emojis=not args.no_emojis)
        for c in conversations_data if isinstance(c, dict)
    ]
    index_data = export_conversations(
        parsed_conversations,
        output_root=args.output,
        grouped=args.group_by_date,
        set_dates=args.set_file_dates,
        verbose=args.verbose
    )
    if args.generate_index:
        write_index(index_data, args.output)
    if args.generate_stats:
        write_stats(index_data, args.output)
        write_summary(index_data, args.output)

if __name__ == "__main__":
    main()
