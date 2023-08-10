import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title='Dashboard', layout='wide')

def sheet():
    st.title('Crie um monstro/Atualize um Monstro')
    uploaded_file = st.file_uploader('Crie um novo monstro, ou atualize os dados de um', type='csv')
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data)
        if st.button('Salvar monstrão'):
            if not os.path.exists('monstros'):
                os.makedirs('monstros')
            data.to_csv(os.path.join('monstros', uploaded_file.name), index=False)
            st.success('File saved successfully!')
        if st.button('Download File'):
            csv = data.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{uploaded_file.name}">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)

def evolution():
    st.title('Evolução')
    files = [f for f in os.listdir('monstros') if f.endswith('.csv')]
    file = st.selectbox('Choose a CSV file', files)
    if file:
        data = pd.read_csv(os.path.join('monstros', file))
        date_column = data.columns[0]
        y_column = st.selectbox('Choose a column for the y-axis', data.columns[1:])
        if date_column and y_column:
            fig, ax = plt.subplots()
            ax.plot(data[date_column], data[y_column], label=file)
            ax.legend()
            st.pyplot(fig)

PAGES = {
    'Crie/Atualize um monstro': sheet,
    'Evolução': evolution
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio('Go to', list(PAGES.keys()))
page = PAGES[selection]
page()
