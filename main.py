import streamlit as st
from openai import OpenAI
import os

st.title("My first Streamlit app")
st.write("Welcome to my first streamlit app")

st.button("Reset", type="primary")

if st.button("Say Hello"):
    st.write("Why say hello?")
else:
    st.write("Goodbye")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def story_gen(prompt):
    system_prompt = """
    You are a world-renowned author for young adult fiction short stories.
    Given a concept, generate a short story relevant to the themes of the story.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=1.6,
        max_tokens=2000,
    )
    return response.choices[0].message.content


def art_gen(prompt):
    response = client.images.generate(model="dall-e-2",
                                      prompt=prompt,
                                      size="1024x1024",
                                      quality="standard",
                                      n=1)
    return response.data[0].url


def design_gen(prompt):
    system_prompt = """
    You will be given a short story. Generate a prompt for cover art that is suitable for the story.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=1.3,
        max_tokens=2000,
    )
    return response.choices[0].message.content


prompt = st.text_input("Enter a prompt: ")

if st.button("Generate"):

    story = story_gen(prompt)
    design = design_gen(story)
    art = art_gen(design)

    st.caption(design)
    st.divider()
    st.write(story)
    st.divider()
    st.image(art)
    
