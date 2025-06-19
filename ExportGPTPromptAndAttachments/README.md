# ExportGPTPromptAndAttachments

Extracts prompts and file attachment references from exported ChatGPT conversation folders. This tool is designed to assist with organizing and archiving GPT chat session data when manual exports include prompts and uploaded files.

---

## 📦 What It Does

* Identifies user prompts from markdown-formatted ChatGPT exports
* Detects and lists references to file attachments
* Structures extracted data for use in external logging, tracking, or prompt analysis workflows

---

## 📁 Usage Context

Place this tool folder inside your working GPT export project. Currently, this folder contains example prompts and a framework for formatting attachment metadata manually or via a companion tool.

> 📌 Note: This tool does not yet include a processing script. It provides prompt and attachment examples as a model for use in scripting or pipeline builds.

---

## 📂 Contents

* `example_prompt.md` – A formatted GPT export snippet with embedded prompt and attachment data
* `README.md` – This documentation file

---

## 💡 Next Steps

This module is intended to be expanded with:

> ⚠️ A parser may not be necessary for well-structured exports, but could become useful if formatting drifts or attachment handling becomes more complex.

* Python/Node CLI tools for parsing `.md` exports
* Optional automation for tracking filenames, timestamps, and prompt hashes
* Export options for `.csv`, `.json`, or `.txt`

---

## 📜 License

Part of the GPT Tools suite. Distributed under [CC BY-NC-SA 4.0](../../LICENSE.md)
