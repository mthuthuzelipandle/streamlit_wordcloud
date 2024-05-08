import mysql.connector
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import base64
from io import BytesIO

# Connection
# conn = mysql.connector.connect(
#     host="localhost",
#     port="8889",
#     user="root",
#     passwd="root",
#     db="radar_dbs01"
# )
conn = mysql.connector.connect(
     host="mysql.radardat.com",
    # port="8889",
     user="radar_data",
     passwd="h~-ccQLYBf,_V%5",
     db="radar_dbs01"
 )

c = conn.cursor()

# Fetch data
def view_all_data():
    c.execute('select * from discussioncontent order by ID asc')
    data = c.fetchall()
    return data

# Fetch data
result = view_all_data()
df = pd.DataFrame(result, columns=["ID", "Discussion_Content_Zulu", "Discussion_Content_English", "Time_Stamp", "Time_Stamp_End", "Audio_Link", "Extra_Data"])

st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")
st.header("ANALYTICAL PROCESSING, TRENDS & PREDICTIONS")
st.markdown("##")

# Sidebar
st.sidebar.header("Please filter")
dates = st.sidebar.multiselect(
    "Select date",
    options=df["Extra_Data"].unique(),
    default=df["Extra_Data"].unique(),
)

df_selection = df.query(
    "Extra_Data==@dates"
)

# Define phrases
phrase_list = [
    "Loadshedding", "Load shedding", "Eskom", "Power cuts", "Stage 1", "stage 2",
    "Cooking", "Dinner", "Cook", "Dinner", "Lunch", "Breakfast", "take-out", "fast food",
    "Bathing", "Shower", "Showering",
    "Laundry", "Cleaning Clothes", "clothing",
    "Solar", "Battery",
    "Paraffin", "Candle", "candles", "Charcoal", "Gas",
    "Checkers", "Shoprite", "Woolworths", "Spar", "Boxer", "Makro", "Pick and Pay", "Dischem", "Clicks", "Spaza", "shop", "tradeport", "Discount store",
    "Bathing", "Showering", "lotion", "cream", "petroleum Jelly", "roll on", "toothpaste", "deodorant", "deo", "antiperspirant", "antiperspirant", "shampoo", "handwash", "haircare", "skincare", "facewash", "bodywash", "soap",
    "Affordability", "inflation", "hyperinflation", "hyperinflation", "price increases", "price rise", "price hike", "Inflation hike", "price surge", "inflation peak", "bargain", "discount", "low cost", "budget", "stokvel", "Cheaper Pack Sizes", "Cheaper Brands"
]

# Function to filter sentences containing the specified phrases
def filter_sentences(text, phrases):
    sentences = text.split(".")
    filtered_sentences = []
    for sentence in sentences:
        if any(phrase.lower() in sentence.lower() for phrase in phrases):
            filtered_sentences.append(sentence.strip())
    return filtered_sentences

# Combine all English text into a single string
english_text = ' '.join(df['Discussion_Content_English'].dropna())

# Filter sentences containing the specified phrases
filtered_sentences = filter_sentences(english_text, phrase_list)

# Combine filtered sentences into a single string
filtered_text = '. '.join(filtered_sentences)

# Create word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(filtered_text)

# Convert word cloud image to base64
img_data = BytesIO()
wordcloud.to_image().save(img_data, format='PNG')
encoded_img = base64.b64encode(img_data.getvalue()).decode()

# Display word cloud as HTML
cloud_html = f'<img src="data:image/png;base64,{encoded_img}" alt="Word Cloud">'
st.markdown(cloud_html, unsafe_allow_html=True)

st.header("Transcripts")
st.markdown("##")

with st.expander("Tabular", expanded=True):
    showData = st.multiselect('Filter: ', df_selection.columns, default=[])
    st.write(df_selection[showData]) 
