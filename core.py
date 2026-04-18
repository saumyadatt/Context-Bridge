from dotenv import load_dotenv
load_dotenv()
from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def summarize_chunk(chunk_text):
    """Summarize a single chunk of conversation — lightweight call."""
    prompt = f"""Briefly summarize the key points from this portion of a conversation in bullet points.
Focus on: decisions made, work completed, tools used, and any problems encountered.
Keep it concise — max 150 words.

Conversation chunk:
{chunk_text}

Summary:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    return response.choices[0].message.content


def chunk_and_summarize(conversation_text, chunk_size=2500):
    """Split long conversations into chunks, summarize each, return combined summary."""
    words = conversation_text.split()

    if len(words) <= chunk_size:
        return conversation_text

    chunks = [
        " ".join(words[i: i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]

    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        summary = summarize_chunk(chunk)
        chunk_summaries.append(f"[Part {i+1}]\n{summary}")

    return "\n\n".join(chunk_summaries)


def generate_handoff(conversation_text, mode="Continue working"):
    """Generate a structured handoff card from a conversation."""

    words = conversation_text.split()
    if len(words) > 2500:
        conversation_text = chunk_and_summarize(conversation_text)

    prompt = f"""Summarize this AI conversation into a handoff card using EXACTLY this format:

CONTEXTBRIDGE HANDOFF CARD
━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 GOAL
[1-2 sentences on the user's ultimate objective]

✅ PROGRESS SO FAR
[Bullet points of completed decisions or work]

🔧 TOOLS & TECH
[Languages, libraries, APIs, frameworks]

📍 LAST POINT REACHED
[Where the conversation ended — be specific]

⏭️ IMMEDIATE NEXT STEP
[The single next action]

❓ OPEN QUESTIONS
[Unresolved items or pending decisions]

💬 HOW TO CONTINUE
Paste this card and say: "{mode} from where I left off."
━━━━━━━━━━━━━━━━━━━━━━━━━━

Conversation:
{conversation_text}

Be specific and concise. No extra commentary."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )
        return response.choices[0].message.content

    except Exception as e:
        error_msg = str(e)
        if "rate_limit_exceeded" in error_msg or "413" in error_msg:
            words = conversation_text.split()
            conversation_text = " ".join(words[:500] + ["...[trimmed]..."] + words[-500:])
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
            )
            return response.choices[0].message.content
        raise