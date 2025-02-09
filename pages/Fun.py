 # Visualization
import streamlit as st




def fun():
    st.title("🌍 Climate Change Quiz")
    st.write("Test your knowledge and earn eco-bragging rights!")

    # Initialize session state for quiz
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'score' not in st.session_state:
        st.session_state.score = 0

    # Quiz questions and answers
    questions = [
        {
            "question": "What is the main greenhouse gas responsible for recent climate change?",
            "options": ["Carbon Dioxide (CO₂)", "Methane", "Nitrous Oxide", "Water Vapor"],
            "answer": "Carbon Dioxide (CO₂)"
        },
        {
            "question": "How much has global sea level risen since 1900?",
            "options": ["5-10 cm", "15-20 cm", "25-30 cm", "Over 50 cm"],
            "answer": "15-20 cm"
        },
        {
            "question": "Which food has the highest carbon footprint per kilogram?",
            "options": ["Beef", "Cheese", "Chicken", "Tofu"],
            "answer": "Beef"
        },
        {
            "question": "What percentage of Arctic sea ice has disappeared since 1979?",
            "options": ["10%", "30%", "50%", "70%"],
            "answer": "50%"
        },
        {
            "question": "Which renewable energy source grew the fastest in the last decade?",
            "options": ["Solar Power", "Wind Power", "Hydropower", "Geothermal"],
            "answer": "Solar Power"
        },
        {
            "question": "How many climate change records were broken in 2023?",
            "options": ["12", "27", "34", "Over 50"],
            "answer": "Over 50"
        },
        {
            "question": "Which country is the largest emitter of CO₂ historically?",
            "options": ["USA", "China", "Russia", "India"],
            "answer": "USA"
        },
        {
            "question": "What's the 'safe' limit of global warming agreed in the Paris Agreement?",
            "options": ["1°C", "1.5°C", "2°C", "2.5°C"],
            "answer": "1.5°C"
        },
        {
            "question": "Which animal is most threatened by melting sea ice?",
            "options": ["Polar Bears", "Penguins", "Seals", "Arctic Foxes"],
            "answer": "Polar Bears"
        },
        {
            "question": "How much food is wasted globally each year?",
            "options": ["10%", "20%", "30%", "40%"],
            "answer": "30%"
        },
        {
            "question": "Which city is sinking fastest due to climate change?",
            "options": ["Venice", "Jakarta", "Miami", "Shanghai"],
            "answer": "Jakarta"
        },
        {
            "question": "What percentage of global electricity comes from renewables?",
            "options": ["10%", "20%", "30%", "40%"],
            "answer": "30%"
        },
        {
            "question": "Which industry emits the most CO₂?",
            "options": ["Transportation", "Energy Production", "Agriculture", "Manufacturing"],
            "answer": "Energy Production"
        },
        {
            "question": "How many trees would we need to plant to offset current emissions?",
            "options": ["1 billion", "5 billion", "50 billion", "1.6 trillion"],
            "answer": "1.6 trillion"
        },
        {
            "question": "What's the biggest carbon capture system on Earth?",
            "options": ["Amazon Rainforest", "Ocean Phytoplankton", "Canadian Boreal Forest", "Sahara Desert"],
            "answer": "Ocean Phytoplankton"
        }
    ]

    # Display questions
    user_answers = []
    for i, q in enumerate(questions):
        st.subheader(f"Question {i+1}: {q['question']}")
        answer = st.radio("Choose your answer:", q["options"], key=f"q{i}")
        user_answers.append(answer)
        st.markdown("---")

    # Calculate score
    if st.button("Submit Quiz"):
        st.session_state.quiz_submitted = True
        st.session_state.score = sum(1 for i, q in enumerate(questions) if user_answers[i] == q["answer"])
        
    if st.session_state.quiz_submitted:
        st.balloons() if st.session_state.score >= 9 else st.snow()
        st.subheader(f"Your Score: {st.session_state.score}/15 ({st.session_state.score/15:.0%})")
        
        # Celebration or encouragement
        if st.session_state.score >= 9:
            st.success("🎉 Climate Champion! You're ready to lead the green revolution!")
            st.image("https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif")
        else:
            st.warning("🌱 Keep Learning! The planet needs informed heroes!")
            st.image("https://media.giphy.com/media/l3V0j3ytFyGHqiV7W/giphy.gif")
        
        # Show explanations
        st.markdown("---")
        st.subheader("Learn More:")
        for i, q in enumerate(questions):
            with st.expander(f"Question {i+1}: {q['question']}"):
                st.write(f"**Correct Answer:** {q['answer']}")
                st.write(f"**Your Answer:** {user_answers[i]}")
                if user_answers[i] != q["answer"]:
                    st.error("❌ Let's learn why:")
                    # Add fun facts/explanations
                    fun_facts = [
                        "CO₂ accounts for 76% of greenhouse gas emissions!",
                        "Oceans absorb 30% of our CO₂ emissions - but it's making them acidic!",
                        "Beef production creates 60kg CO₂ per kg - 60x more than peas!",
                        "The Arctic could be ice-free in summer by 2030! 😱",
                        "Solar panel costs dropped 82% in the last decade! ☀️",
                        "A single tree can absorb 21kg CO₂ per year! 🌳",
                        "The energy sector emits 73% of global CO₂! ⚡",
                        "Food waste creates 8% of global emissions - more than airlines! ✈️",
                        "1.6 trillion trees = 1,000 trees for every person on Earth!",
                        "Phytoplankton produce 50% of Earth's oxygen! 🌊"
                    ]
                    st.info(fun_facts[i % len(fun_facts)])
        
        # Reset button
        if st.button("🔄 Try Again"):
            st.session_state.quiz_submitted = False
            st.session_state.score = 0
            st.experimental_rerun()

        # Social sharing
        st.markdown("---")
        st.write("**Challenge your friends!**")
        st.code(f"I scored {st.session_state.score}/15 on the Climate Quiz! Can you beat me? 🌍 #ClimateAction")

