import streamlit as st
import random
import requests
from time import sleep
from streamlit import caching 
from PIL import Image





Languages = ['C', 'C++', 'C#', 'Go', 'Java', 'JavaScript', 'Shell', 'Ruby', 'Python', 'Perl', 'Html', 'CSS', 'null', None]

image777 = Image.open('777.jpg')


def get_random_gist_url():
    id = random.randint(5000, 10000)
    url = "https://api.github.com/gists/" + str(id)
    return url

def get_code_from_gist(url):
    res = requests.get(url)
    try:
        data = res.json()['files']
        language = data[list(data.keys())[0]]['language']
        content = data[list(data.keys())[0]]['content']
    except:
        return False
    else:
        return{
                'language':language,
                'content':content
        }

@st.cache(show_spinner=False)
def random_gist():
    url = get_random_gist_url()
    gist = get_code_from_gist(url)
    while not gist:
        url = get_random_gist_url()
        gist = get_code_from_gist(url)
    return gist

@st.cache
def get_options_list(correct):
    options = random.sample(Languages,4)
    options.append(correct)
    options = list(set(options))
    random.shuffle(options)
    return options

def about_dev():
    st.sidebar.title("About this project")
    st.sidebar.markdown("""
    ### Hi there, I'm Max Mnemo <img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="25px">
    
    #### This app utilizes the github API to output code snippets from github/gists. The user has to identify the programming language at hand. 
     
    #### Try 10 questions and let me know how many languages you managed to identify. There is currently no highscore.  
    #### You can message me on [Instagram](https://www.instagram.com/max_mnemo/)

    #### Best regards!
    ##### Max Mnemo  

    </a> 
    """,unsafe_allow_html=True)

def get_score():
    if 'total' in st.session_state:
        score = str(st.session_state['correct']) + "/" + str(st.session_state['total'])
        return score
    else:
        return '0/0'

def update_score(score):
    if 'total' in st.session_state:
        st.session_state['total'] = st.session_state.total + 1
        st.session_state['correct'] = st.session_state.correct + score
    else:
        st.session_state['total'] =  1
        st.session_state['correct'] = score

if __name__ == "__main__":
    st.set_page_config(page_title="Guess the Code", layout='wide', page_icon="🖥️")
    about_dev()
    st.markdown("<h1 style='text-align: center; color: black;'>Guess the Code Game</h1>", unsafe_allow_html=True)
    st.image(image777)
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    cols = st.columns([.5,.5])
    cols[0].subheader('What programming language is this?')
    cols[1].subheader('Current score : ' + get_score())

    with st.spinner('Generating random code snippet ...'):
        gist = random_gist()
    correct = gist['language']
    options = get_options_list(correct)

    with st.form('quiz'):
        st.code(gist['content'])
        # st.caption(str(correct)) # to show correct answer
        chosen = st.radio('Choose the correct option',  options)
        if st.form_submit_button('Confirm'):
            if chosen == correct:
                st.success('That is Correct!')
                update_score(1)
            else:
                st.error("Sorry that is incorrect, correct answer is " + str(correct))
                update_score(0)
            # wait for .2 seconds before clearing cache and rerunning the app
            sleep(0.2)
            
            st.legacy_caching.clear_cache())
            st.experimental_rerun()
