import streamlit as st
from openai import OpenAI

# 1. Page Configuration & Styling
st.set_page_config(page_title="Mahi-hem Logic", page_icon="🏛️", layout="centered")

st.markdown("""
<style>
.main-title { font-size: 2.8rem; font-weight: 800; text-align: center; color: #1E3A8A; margin-bottom: 0px; }
.tagline { text-align: center; font-style: italic; color: #6B7280; margin-bottom: 30px; }
.section-header { color: #1E3A8A; font-weight: 700; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏛️ Mahi-hem Logic</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Where formal debate goes to die.</div>', unsafe_allow_html=True)

# 2. Sidebar Fallacy Guide with the custom definitions
with st.sidebar:
st.header("📚 Weaponized Fallacy Guide")
st.markdown("**Because I Said So:** Proving your point by just repeating your point in different words.")
st.markdown("**Everyone Else is Doing It:** Using global peer pressure on a toddler who couldn't care less about what's popular.")
st.markdown("**We Always Did It:** Treating basic household routines like ancient, unshakeable laws.")
st.markdown("**Bait and Switch:** Introducing a completely unrelated topic/shiny object to distract from the real argument.")

# 3. User Inputs
st.subheader("Step 1: What is the grievance?")

# Preset Buttons
preset_clicked = None
col1, col2, col3, col4 = st.columns(4)
with col1:
if st.button("🧼 Bath is too wet"): preset_clicked = "The bath is too wet!"
with col2:
if st.button("😡 Angry water"): preset_clicked = "The blue cup makes the water taste angry!"
with col3:
if st.button("🔺 Wrong toast shapes"): preset_clicked = "My toast is cut into triangles, but I wanted rectangles!"
with col4:
if st.button("☀️ Sun is looking at me"): preset_clicked = "The sun is looking at me!"

# Text Input (Defaults to preset if clicked)
initial_text = preset_clicked if preset_clicked else ""
toddler_input = st.text_input("Or type your own toddler argument here:", value=initial_text, placeholder="e.g., The banana is too yellow...")

st.subheader("Step 2: Weapon of Choice")
fallacy = st.selectbox("Select a tactical fallacy for the Debate Captain to use:",
["Because I Said So", "Everyone Else is Doing It", "We Always Did It", "Bait and Switch"])

# 4. Trigger the AI Debate
if st.button("🔥 Initiate Debate", type="primary"):
if not toddler_input:
st.warning("Please enter a toddler argument or click a preset first!")
elif not st.secrets.get("OPENAI_API_KEY"):
st.error("Missing OpenAI API Key! Please add it to your Streamlit App Secrets.")
else:
with st.spinner("Debate Captain is adjusting his tie and consulting the lexicon..."):
try:
# Initialize OpenAI client with secure secret key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

system_prompt = """You are the Captain of the Harvard Debate Team. You are cold, analytical, flawlessly dressed, and deeply concerned with the structural integrity of arguments. You are currently debating a 3-year-old child.

Your goal is to win the argument at all costs using formal debate tactics, but you are forced to weaponize the highly absurd custom fallacy rule provided by the user. You must treat the toddler's grievance with the gravity of a geopolitical crisis and deliver your argument with intense, corporate arrogance.

Here are the specific rules for the fallacies you must use:
1. "Because I Said So": Prove your point entirely by tautology—just repeating your point over and over using increasingly complex, pompous vocabulary.
2. "Everyone Else is Doing It": Argue that something is correct because it is popular. Apply massive global statistics or societal peer pressure to a toddler who completely layout does not care. (e.g., '90% of kids in the US accept the transition into jammies by 7 PM...')
3. "We Always Did It": Argue that a minor household routine is an ancient, sacred tradition that cannot be broken without violating historical laws. (e.g., 'For many many years and seven hundred days our family has placed the car seat...')
4. "Bait and Switch": When logic completely fails, introduce a totally unrelated topic or sudden external observation to distract the toddler, hoping they won't notice the primary argument is lost. (e.g., 'While you argue the tag on your shirt is scratchy... let's look at the broader reality: there is a dog outside. Look at that dog.')

Structure your response cleanly using these exact Markdown headers:
### 👔 THE REBUTTAL
[A formal, multi-point refutation of the toddler's premise using the assigned fallacy framework. Explicitly name the tactic with corporate arrogance.]

### 🧐 THE ANALYTICAL BREAKDOWN
[A brief, arrogant note explaining why your structural application of this specific strategy is flawless.]

### 🧸 THE INEVITABLE DEFEAT
[Describe the toddler's physical, entirely irrational counter-move—like screaming, throwing a shoe, going completely limp on the floor, or blowing a bubble with their spit—that totally bypasses your logic, leaving the Debate Captain in absolute internal despair.]"""

user_prompt = f"Toddler Grievance: '{toddler_input}'\nAssigned Fallacy to use: {fallacy}"

response = client.chat.completions.create(
model="gpt-4o-mini",
messages=[
{"role": "system", "content": system_prompt},
{"role": "user", "content": user_prompt}
],
temperature=0.8
)

# Output the result beautifully
st.markdown("---")
st.markdown(response.choices[0].message.content)
st.markdown("---")

except Exception as e:
st.error(f"An error occurred: {str(e)}")
