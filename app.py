import streamlit as st
from openai import OpenAI

# Set up clean page structure
st.set_page_config(page_title="Mahi-hem Logic", page_icon="👶", layout="centered")

st.title("👶 Mahi-hem Logic")
st.subheader("Dismantling toddler tantrums with high-level formal debate tactics.")
st.caption("Spoiler alert: You cannot reason someone out of a position they didn't reason themselves into.")

# 1. Check for API key in Streamlit Secrets
if "OPENAI_API_KEY" not in st.secrets:
    st.error("🔑 OpenAI API Key missing! Please add it to your Streamlit Community Cloud app settings under App Secrets.")
    st.stop()

# Initialize the OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 2. Define the Fallacies from the PRD
fallacies = {
    "Because I said so (Circular Reasoning)": "Proving your point by just repeating your point in different words.",
    "Everyone else is doing it (Bandwagon Appeal)": "Arguing that something is right or good because it is popular.",
    "We always did it (Appeal to Tradition)": "Arguing that we must do something a certain way simply because that’s how we’ve always done it.",
    "Bait and switch (Red Herring)": "Introducing a completely unrelated topic to distract from the real argument."
}

# 3. Build UI Components
tantrum_input = st.text_area(
    "1. Enter the Toddler's Grievance / Argument:",
    placeholder="e.g., My grilled cheese is cut into triangles, but I wanted rectangles!"
)

fallacy_choice = st.selectbox(
    "2. Choose the Debate Captain's Weapon of Choice:",
    options=list(fallacies.keys())
)

# Display a quick tooltip helper
st.info(f"💡 **Fallacy Definition:** {fallacies[fallacy_choice]}")

# 4. Trigger the Debate
if st.button("Dismantle Toddler Logic", type="primary"):
    if not tantrum_input.strip():
        st.warning("Please type a toddler complaint first!")
    else:
        with st.spinner("The Debate Captain is adjusting his tie and preparing a flawless refutation..."):
            
            # Anchor prompt strictly following the PRD
            system_prompt = (
                "You are the Captain of the Harvard Debate Team. You are cold, analytical, flawlessly dressed, "
                "and deeply concerned with the structural integrity of arguments. You are currently debating a 3-year-old child. "
                "Your goal is to win the argument at all costs using formal debate tactics and specifically weaponizing the logical fallacy provided. "
                "You must treat the toddler's grievance with the gravity of a geopolitical crisis.\n\n"
                "Structure your response exactly in three parts:\n"
                "1. THE REBUTTAL: A formal, multi-point refutation of the toddler's premise using the assigned logical fallacy. Name the fallacy explicitly with corporate arrogance.\n"
                "2. THE BREAKDOWN: A brief, analytical note on why your logic is bulletproof.\n"
                "3. THE DEFEAT (Toddler Response): Describe the toddler's physical, entirely irrational counter-move that completely invalidates your logic (e.g., screaming, throwing a shoe, lying flat on the floor). Show your internal despair at this tactical maneuver."
            )
            
            user_prompt = f"Toddler's Grievance: \"{tantrum_input}\"\nAssigned Fallacy: {fallacy_choice}"
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.8
                )
                
                # Render results nicely
                st.success("Transcript Generated Successfully!")
                st.markdown("---")
                st.markdown(response.choices[0].message.content)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
