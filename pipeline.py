import streamlit as st
from ingest import get_facts
from prompt_engine import call_model
import os
import json
from datetime import datetime

# Set up page
st.set_page_config(page_title="🧠 Fun Fact Prompt Playground", page_icon="💬")
st.title("🧠 Fun Fact Prompt Playground")
st.write("Click the button to ingest 10 fun facts. Then enter your own instruction for each (e.g., explain, summarize, rephrase).")

# Initialize session state
if "facts" not in st.session_state:
    st.session_state.facts = []

# Button to ingest new facts
if st.button("🚀 Ingest 10 New Fun Facts"):
    st.session_state.facts = get_facts(10)

# Helper: save each interaction to its own file
def save_single_to_json(data, folder="data/processed"):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"interaction_{timestamp}.json"
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return filepath

# Display facts and allow custom instructions
if st.session_state.facts:
    for i, original_fact in enumerate(st.session_state.facts):
        st.markdown("---")
        st.subheader(f"🧩 Fact #{i + 1}")

        # Editable fact
        user_fact = st.text_input(f"Edit Fact", value=original_fact, key=f"fact_{i}")

        # Instruction input
        user_instruction = st.text_input(
            f"Instruction (e.g. explain, summarize)",
            placeholder="Enter your instruction",
            key=f"instruction_{i}"
        )

        # Automatically generate and save when instruction is provided
        if user_instruction.strip():
            full_prompt = f"{user_instruction.strip().capitalize()}: {user_fact.strip()}"
            model_response = call_model(full_prompt)

            st.markdown("**🧠 Insight:**")
            st.success(model_response)

            # Save immediately
            record = {
                "fact": user_fact.strip(),
                "instruction": user_instruction.strip(),
                "prompt": full_prompt,
                "response": model_response
            }
            path = save_single_to_json(record)
            st.info(f"💾 Auto-saved to `{path}`")
