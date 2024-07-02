import streamlit as st

import os 

my_secret = st.secrets['my_secret']

st.title("I love secrets!")


st.write("I wouldn't normally write my secret but its that i love..........")
st.write(my_secret)


