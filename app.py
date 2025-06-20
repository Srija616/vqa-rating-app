import streamlit as st
import pandas as pd
import os

# Load data
DATA_PATH = "data_native.csv"
RATING_PATH = "rated_native.csv"

df = pd.read_csv(DATA_PATH)
if os.path.exists(RATING_PATH):
    rated_df = pd.read_csv(RATING_PATH)
    rated_ids = set(rated_df['id'])
else:
    rated_df = pd.DataFrame(columns=['id', 'rating'])
    rated_ids = set()

# Filter unrated
df_unrated = df[~df['id'].isin(rated_ids)]

st.title("VQA Output Rating")
st.write("Rate the model output as: 0 = Incorrect, 1 = Acceptable, 2 = Correct")

if df_unrated.empty:
    st.success("🎉 All examples have been rated!")
else:
    row = df_unrated.iloc[0]

    st.image(row['image_path'], width=400)
    st.markdown(f"**Question:** {row['question']}")
    st.markdown(f"**Model Answer:** {row['model_answer']}")
    st.markdown(f"**Correct Answer:** {row['correct_answer']}")

    rating = st.radio("Your rating:", [0, 1, 2], horizontal=True)

    if st.button("Submit Rating"):
        new_row = pd.DataFrame([{'id': row['id'], 'rating': rating}])
        rated_df = pd.concat([rated_df, new_row], ignore_index=True)
        rated_df.to_csv(RATING_PATH, index=False)
        st.experimental_rerun()
