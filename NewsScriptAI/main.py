from transformers import T5Tokenizer, T5ForConditionalGeneration
from datetime import datetime
import os

# Load T5 model and tokenizer
model = T5ForConditionalGeneration.from_pretrained("t5-base")
tokenizer = T5Tokenizer.from_pretrained("t5-base")

# Summarize using T5
def summarize_with_t5(text):
    input_text = "summarize: " + text.strip().replace("\n", " ")
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=60, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Read your full news .txt file
def read_articles(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Split on your previous separator
    return [a.strip() for a in content.split("■" * 100) if len(a.strip()) > 100]

# Format the full YouTube script
def generate_full_script(summaries):
    script = ""

    # Add intro only once
    script += "🎬 [Intro]\n"
    script += "Welcome back to Daily News Digest! Here are today’s top stories:\n\n"

    # Add each summary with title
    for i, (title, summary) in enumerate(summaries, 1):
        script += f"📰 Headline {i}: {title.strip()}\n"
        script += f"📌 {summary.strip()}\n\n"

    # Add outro only once
    script += "🧾 [Outro]\n"
    script += "Thanks for watching! Don’t forget to like, share, and subscribe for more daily updates.\n"

    return script

# Save final script to a file
def save_to_file(script_text):
    filename = f"youtube_script_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(script_text)
    print(f"\n✅ YouTube script saved to: {os.path.abspath(filename)}")

# Main
if __name__ == "__main__":
    input_file = "news.txt"  # Replace with your actual file

    print("📄 Reading articles...")
    articles = read_articles(input_file)

    summaries = []

    for i, article in enumerate(articles, 1):
        print(f"\n🔁 Summarizing article {i}/{len(articles)}...")
        lines = article.splitlines()
        title = lines[0] if lines else f"Story {i}"
        body = "\n".join(lines[4:])  # Skip metadata

        try:
            summary = summarize_with_t5(body)
            summaries.append((title, summary))
            print("✅ Summary generated.")
        except Exception as e:
            print(f" Failed to summarize: {e}")

    if summaries:
        final_script = generate_full_script(summaries)
        save_to_file(final_script)
    else:
        print(" No valid summaries generated.")
