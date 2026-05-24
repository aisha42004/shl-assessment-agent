import requests
import os


API_URL = "http://127.0.0.1:8000/chat"


# ---------------------------------
# Parse markdown traces
# ---------------------------------

def extract_messages(text):

    messages = []

    lines = text.split("\n")

    i = 0

    while i < len(lines):

        line = lines[i].strip()

        # ---------------------------------
        # USER BLOCK
        # ---------------------------------

        if line == "**User**":

            # find next non-empty line
            j = i + 1

            while j < len(lines):

                candidate = lines[j].strip()

                if candidate.startswith(">"):

                    content = candidate.replace(
                        ">",
                        ""
                    ).strip()

                    messages.append({
                        "role": "user",
                        "content": content
                    })

                    break

                j += 1

        # ---------------------------------
        # AGENT BLOCK
        # ---------------------------------

        elif line == "**Agent**":

            assistant_lines = []

            j = i + 1

            while j < len(lines):

                future = lines[j].strip()

                # stop at next section
                if (
                    future == "**User**"
                    or future == "**Agent**"
                    or future.startswith("### Turn")
                ):
                    break

                # skip metadata
                if (
                    "recommendations:" in future
                    or "end_of_conversation" in future
                ):
                    j += 1
                    continue

                if future:

                    assistant_lines.append(
                        future
                    )

                j += 1

            combined = " ".join(
                assistant_lines
            ).strip()

            if combined:

                messages.append({
                    "role": "assistant",
                    "content": combined
                })

        i += 1

    return messages


# ---------------------------------
# Evaluate one trace
# ---------------------------------

def evaluate_trace(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

    messages = extract_messages(text)

    print("\n" + "=" * 60)

    print("TRACE:",
          os.path.basename(file_path))

    print("=" * 60)

    print("\nEXTRACTED MESSAGE COUNT:")
    print(len(messages))

    if len(messages) == 0:

        print("\nNO MESSAGES EXTRACTED")
        return

    payload = {
        "messages": messages
    }

    response = requests.post(
        API_URL,
        json=payload
    )

    print("\nSTATUS CODE:")
    print(response.status_code)

    if response.status_code != 200:

        print("\nFAILED RESPONSE:")
        print(response.text)

        return

    data = response.json()

    print("\nREPLY:\n")

    print(data["reply"])

    print("\nRECOMMENDATIONS:\n")

    for item in data["recommendations"]:

        print("-", item["name"])

    print("\nSCHEMA VALID:")

    schema_valid = (
        "reply" in data and
        "recommendations" in data and
        "end_of_conversation" in data
    )

    print(schema_valid)


# ---------------------------------
# Run all traces
# ---------------------------------

def run_all():

    folder = "sample_conversations"

    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".md")
    ]

    for file_path in sorted(files):

        evaluate_trace(file_path)


if __name__ == "__main__":

    run_all()