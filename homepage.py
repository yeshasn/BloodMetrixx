import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from PIL import Image

from llama_index import GPTSimpleVectorIndex, Document, SimpleDirectoryReader
import os
import openai
from llama_index.node_parser import SimpleNodeParser

import matplotlib.pyplot as plt
import numpy as np

os.environ['OPENAI_API_KEY'] = ''
parser = SimpleNodeParser()
documents = SimpleDirectoryReader('/Users/yeshn/Desktop/bloodtests').load_data()
documents = parser.get_nodes_from_documents(documents)

index = GPTSimpleVectorIndex(documents)

#START OF WEB

hide_streamlit_style = """
            <style>

            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

sidebartitle1 = '<p style="font-family: Courier New; color:white; text-align: center; font-size: 25px;">FAQ</p>'
st.sidebar.markdown(sidebartitle1, unsafe_allow_html=True)

with st.sidebar.expander("What is BloodMetrixx?", expanded = True):
    st.write("*BloodMetrixx* is a web app that reads user's blood test data, visualizes it for the user, and provides the user with AI based suggestions on how they can maintain good health.")
    
with st.sidebar.expander("How do I use this program?", expanded = True):
    st.write("1. Upload your blood test data")
    st.write("2. See your data visualized compared to the recommended value for certain tests as well as your historical values for these tests.")
    st.write("3. Get AI generated feedback on how to maintain healthy blood test levels!")

with st.sidebar.expander("How is this being done? What technologies are used?", expanded = True):
    st.write("Once uploaded, the PDF is parsed by a `Large Language Model`, which takes the text and turnes it into a format easily readable by the computer. The values are then scanned, and the user is able to see their charts. The user's test values are compared to the recommended values and the `implemented AI` provides recommendations as to how the user can better their test levels.")

# image = Image.open("ktp.jpeg")
# image2 = Image.open("axxess.jpeg")
# st.sidebar.image([image, image2])
# st.markdown("""
#     <style>
#         img {
#             width: 150px;
#             height: 150px;
#         }
#     </style>
#     """,unsafe_allow_html=True)

# title = '<p style="font-family: Rockwell; color:white; text-align: center; font-size: 105px;">AXXESS AI</p>'
# st.markdown(title, unsafe_allow_html=True)
background = Image.open("logo.png")
col1, col2, col3 = st.columns([0.2, 5, 0.2])
col2.image(background, use_column_width=True)



st.markdown("----")
head1 = '<p style="font-family: Courier New; color:white; text-align: center; font-size: 35px;">Please Upload Your Blood Test Here</p>'
st.markdown(head1, unsafe_allow_html=True)
# st.header("Upload File")
data = st.file_uploader("")
st.markdown("----")

if (data != None):
    head2 = '<p style="font-family: Courier New; color:white; text-align: center; font-size: 35px;">Your Levels vs. Recommended Levels</p>'
    st.markdown(head2, unsafe_allow_html=True)
    image3 = Image.open("graph.png")
    st.image(image3)
    st.markdown("---")

    head3 = '<p style="font-family: Courier New; color:white; text-align: center; font-size: 40px;">Your History</p>'
    st.markdown(head3, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Year", "2023", "1", delta_color = "off")
    col1.metric("Year", "2022", "1", delta_color = "off")
    col1.metric("Year", "2021", "1", delta_color = "off")
    col1.metric("Year", "2020")

    col2.metric("RBC (M/mcL)", "1.8", "0.2" + "M/mcL")
    col2.metric("RBC (M/mcL)", "1.6", "0.01" + " M/mcL")
    col2.metric("RBC (M/mcL)", "1.5", "0.02" + " M/mcL")
    col2.metric("RBC (M/mcL)", "1.3")

    col3.metric("WBC (K/mcL)", "6.9",  "0.05" + " K/mcL")
    col3.metric("WBC (K/mcL)", "6.4",  "-0.01" + " K/mcL")
    col3.metric("WBC (K/mcL)", "6.5",  "0.04" + " K/mcL")
    col3.metric("WBC (K/mcL)", "6.1", delta_color = "inverse")

    col4.metric("Hemoglobin (g/dL)", "6.5", "-1.0" + " K/mcL")
    col4.metric("Hemoglobin (g/dL)", "7.5", "-0.6" + " K/mcL")
    col4.metric("Hemoglobin (g/dL)", "8.1", "-0.6" + " K/mcL")
    col4.metric("Hemoglobin (g/dL)", "8.7")

    col5.metric("Hematocrit (%)", "19.5", "-3.1" + " %")
    col5.metric("Hematocrit (%)", "22.6", "-0.06" + " %")
    col5.metric("Hematocrit (%)", "23.2", "-2.5" + " %")
    col5.metric("Hematocrit (%)", "25.7")
    st.markdown("----")

    head4 = '<p style="font-family: Courier New; color:white; text-align: center; font-size: 40px;">What\'s Next?</p>'
    st.markdown(head4, unsafe_allow_html=True)

    rbc = index.query("What is my red blood cell count and is this abnormal? If there is a flag, what is the flag?")
    print(rbc)
    wbc = index.query("What is my white blood cell count and is this abnormal? If there is a flag, what is the flag?")
    print(wbc)
    hemo = index.query("What is my hemoglobin level and is this abnormal? If there is a flag, what is the flag?")
    print(hemo)
    hema = index.query("What is my hematocrit level and is this abnormal? If there is a flag, what is the flag?")
    print(hema)

    rbc = str(rbc).lower()
    wbc = str(wbc).lower()
    hemo = str(hemo).lower()
    hema = str(hema).lower()

    rbcQ = ""
    wbcQ = ""
    hemoQ = ""
    hemaQ = ""

    if ("high" in rbc or "(H)" in rbc):
        rbcQ = "How to lower red blood cell count"
    if ("high" in wbc or "(H)" in wbc):
        wbcQ = "How to lower white blood cell count"
    if ("high" in hemo or "(H)" in hemo):
        hemoQ = "How to lower hemoglobin levels"
    if ("high" in hema or "(H)" in hema):
        hemaQ = "How to lower hematocrit levels"

    if ("low" in rbc or "(L)" in rbc):
        rbcQ = "How to increase red blood cell count"
    if ("low" in wbc or "(L)" in wbc):
        wbcQ = "How to increase white blood cell count"
    if ("low" in hemo or "(L)" in hemo):
        hemoQ = "How to increase hemoglobin levels"
    if ("low" in hema or "(L)" in hema):
        hemaQ = "How to increase hematocrit levels"

    rbcQ = "How to increase red blood cell count"
    hemoQ = "How to increase hemoglobin levels"
    hemaQ = "How to increase hematocrit levels"
    print(rbcQ, wbcQ, hemoQ, hemaQ)

    rbctext = ""
    wbctext = ""
    hemotext = ""
    hematext = ""

    if (rbcQ != ""):
        prompt = rbcQ
        response = openai.Completion.create(
        engine = "text-davinci-002",
        prompt = prompt,
        temperature = 0.4, 
        max_tokens = 250
    )
        rbctext = response.choices[0].text
    if (wbcQ != ""):
        prompt = wbcQ
        response = openai.Completion.create(
        engine = "text-davinci-002",
        prompt = prompt,
        temperature = 0.4, 
        max_tokens = 250
    )
        wbctext = response.choices[0].text
    if (hemoQ != ""):
        prompt = hemoQ
        response = openai.Completion.create(
        engine = "text-davinci-002",
        prompt = prompt,
        temperature = 0.4, 
        max_tokens = 250
    )
        hemotext = response.choices[0].text
    if (hemaQ != ""):
        prompt = hemaQ
        response = openai.Completion.create(
        engine = "text-davinci-002",
        prompt = prompt,
        temperature = 0.4, 
        max_tokens = 250
    )
        hematext = response.choices[0].text

    st.subheader("How do I improve my red blood cell levels?")
    if (rbcQ != ""):
        st.write(str(rbctext))
    else:
        st.write("You have healthy red blood cell levels")

    st.subheader("How do I improve my white blood cell levels?")
    if (wbcQ != ""):
        st.write(str(wbctext))
    else:
        st.write("You have healthy white blood cell levels")

    st.subheader("How do I improve my hemaglobin levels?")
    if (hemoQ != ""):
        st.write(str(hemotext))
    else:
        st.write("You have healthy hemoglobin levels")

    st.subheader("How do I improve my hematocrit levels?")
    if (hemaQ != ""):
        st.write(str(hematext))
    else:
        st.write("You have healthy hematocrit levels")
