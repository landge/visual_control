# Create streamlit app to display images and visually control the content

from dis import dis
from hashlib import new
import streamlit as st
import pickle
from pathlib import Path
st.title('Control stroke masks!')
# Initialize the session state

if 'image_paths_key' not in st.session_state:
    st.session_state.image_paths_key = 0

if 'wrong_mask' not in st.session_state:
    st.session_state.wrong_mask = []
    
# Load paths to images
images = list(Path('/tmp/panel/').glob('**/*.png'))
images_dict = {}
for image in images:
    subject = image.name.split('_')[0]
    images_dict[subject] = image

def display_subject(key):
    subject = images[key].name.split('_')[0]
    st.write(subject)
    st.image(images[key].as_posix())

def display_subject_dict(subject_id):
    subject = images_dict[subject_id].name.split('_')[0]
    st.write(subject)
    st.image(images_dict[subject_id].as_posix())

def increment_image_paths_key():
    st.session_state.image_paths_key += 1
    st.session_state.mask_error = False

def add_subject_if_wrong_mask():
    subject = images[st.session_state.image_paths_key].name.split('_')[0]
    open_file = open('/tmp/panel/wrong_mask.pkl', 'w+b')
    st.session_state.wrong_mask.append(subject)
    pickle.dump(st.session_state.wrong_mask, open_file)
    open_file.close()


display_subject(st.session_state.image_paths_key)

wrong_mask = st.checkbox('Wrong mask!', value=False, key="mask_error")
if wrong_mask:
    add_subject_if_wrong_mask()

st.button('Next', on_click=increment_image_paths_key)
new_subject_id = st.text_input('Subject_id:  ')
if new_subject_id:
    display_subject_dict(new_subject_id)
    