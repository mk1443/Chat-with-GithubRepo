import subprocess
import os
import streamlit as st 
import openai

st.set_page_config(layout='wide')
st.markdown("""

                <h3 style='text-align: center; color: black;'>MakAi-Chat-with-Github</h3>""", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
                <h5 style='text-align: center; color: black;'>Github-Repo</h5>""", unsafe_allow_html=True)
    openai.api_key = st.text_input("OpenAI API Key", type="password")
    if openai.api_key:
        github_id=st.text_input("Enter your github-repo-id")
    # Cloning Github Repo 
        subprocess.call(f"git clone {github_id}")
        if github_id:
                st.info("Github repo Downloaded")

    # Reading file Github 
                files = []

                def list_files(startpath):
                    for root, dirs, filenames in os.walk(startpath):
                        for filename in filenames:
                            paths = os.path.join(root, filename)
                            files.append(paths)
                    return files


                if github_id:
                    git_id = github_id.split('/')[-1].split('.', 1)[0]
                    file = list_files(git_id)
                    with col1:
                        selected_file = st.selectbox("Select a file",file,index=None,placeholder="Select a file...")
                    if selected_file:
                        with open (selected_file) as file:
                            file_read = file.read()
                        with col2:
                            st.markdown("""
                                <h5 style='text-align: center; color: blue;'>File Viewer</h5>""", unsafe_allow_html=True)
                            st.code(file_read)
                        with col1: 
                            query = st.text_input("Enter your Query")
                            if query :
                                st.chat_message("user").markdown(query)
                                user_input = query+file_read
                                res_box = st.empty()
                                report = []
                                for resp in openai.Completion.create(model='text-davinci-003',
                                                                    prompt=user_input,
                                                                    max_tokens=1000, 
                                                                    temperature = 0.8,
                                                                    stream = True):
                                    # join method to concatenate the elements of the list 
                                    # into a single string, 
                                    # then strip out any empty strings
                                    report.append(resp.choices[0].text)
                                    result = "".join(report).strip()
                                    result = result.replace("\n", "")        
                                    res_box.markdown(f'*{result}*') 
                                    res_box.chat_message("assistant").markdown(f'*{result}*')