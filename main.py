import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Set up the main app title and sidebar
st.title("\U0001F4CA Sentiment Analysis of Tweets")
st.sidebar.title("\U0001F50E Sentiment Analysis Options")

st.markdown("This is a **Streamlit application** for visualizing airline tweet sentiments! \u2708\ufe0f")
st.sidebar.markdown("Filter and explore tweet sentiments using the sidebar. \U0001F6E0\ufe0f")

# Load the data
@st.cache(persist=True)
def load_data():
    data = pd.read_csv("Tweets.csv")
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

# Display a random tweet based on sentiment
st.sidebar.subheader("\U0001F3B2 Random Tweets")
random_sentiment = st.sidebar.radio("Choose Sentiment", ('positive', 'neutral', 'negative'))
random_tweet = data.query('airline_sentiment == @random_sentiment')[["text"]].sample(n=1).iat[0, 0]
st.sidebar.markdown(f"### Random Tweet: {random_tweet}")

# Visualization of tweet counts
st.sidebar.subheader("\U0001F4CA Number of Tweets")
viz_type = st.sidebar.selectbox("Choose Visualization Type", ['Histogram', 'Pie Chart'], key='viz')

sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count_df = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

if not st.sidebar.checkbox("Hide Chart", True):
    st.markdown("### Number of Tweets by Sentiments")
    if viz_type == "Histogram":
        fig = px.bar(sentiment_count_df, x='Sentiment', y='Tweets', color='Tweets', title="Histogram of Sentiments")
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count_df, values='Tweets', names='Sentiment', title="Pie Chart of Sentiments")
        st.plotly_chart(fig)

# Time-based analysis
st.sidebar.subheader("\u23F0 Tweet Timing")
hour_filter = st.sidebar.slider("Hour of Day", 0, 23)
filtered_data = data[data['tweet_created'].dt.hour == hour_filter]

if not st.sidebar.checkbox("Close Map", True, key='time'):
    st.markdown(f"### Tweets by Location between {hour_filter}:00 and {(hour_filter + 1) % 24}:00")
    st.map(filtered_data)

# Airline sentiment comparison
st.sidebar.subheader("\u2708\ufe0f Airline Tweets by Sentiment")
selected_airlines = st.sidebar.multiselect('Choose Airlines', data['airline'].unique())

if selected_airlines:
    airline_data = data[data['airline'].isin(selected_airlines)]
    fig_airline = px.histogram(airline_data, x='airline', y='airline_sentiment', histfunc='count',
                               color='airline_sentiment', facet_col='airline_sentiment',
                               title="Sentiment by Airline", height=600, width=800)
    st.plotly_chart(fig_airline)

# Word Cloud
def generate_wordcloud(sentiment):
    df = data[data['airline_sentiment'] == sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'https' not in word and not word.startswith('@') and word != 'RT'])
    return WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)

st.sidebar.subheader("\u2601\ufe0f Word Cloud")
word_sentiment = st.sidebar.radio("Sentiment Type", ('positive', 'neutral', 'negative'))

if not st.sidebar.checkbox("Hide Word Cloud", True, key='wc'):
    st.markdown(f"### Word Cloud for {word_sentiment.capitalize()} Sentiment")
    wordcloud = generate_wordcloud(word_sentiment)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt.gcf())
