import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

# Custom styling
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
            color: white;
        }
        .css-1v0mbdj.edgvbvh3 {  # Sidebar style
            background-color: #1c1e26 !important;
        }
        h1, h2, h3, h4 {
            color: #f63366;
        }
        .stButton>button {
            color: white;
            background-color: #f63366;
            border-radius: 8px;
        }
        .stButton>button:hover {
            background-color: #e02e5a;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
# WhatsApp icon and title in one row using columns
col1, col2 = st.sidebar.columns([0.2, 0.8])
with col1:
    st.image("https://img.icons8.com/color/48/whatsapp--v1.png", width=50)  # reduced size for better alignment
with col2:
    st.markdown("<h3 style='line-height: 1.6; margin-top: 6px;'>WhatsApp Chat Analyzer</h3>", unsafe_allow_html=True)

st.sidebar.markdown("Upload your exported chat file (without media) and explore insightful analytics ✨")

uploaded_file = st.sidebar.file_uploader("📁 Upload a WhatsApp chat file (.txt)")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("👤 Select user to analyze", user_list)

    if st.sidebar.button("🔍 Show Analysis"):

        st.markdown("## 📈 Top Statistics")
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Messages", num_messages)
        with col2:
            st.metric("Total Words", words)
        with col3:
            st.metric("Media Shared", num_media_messages)
        with col4:
            st.metric("Links Shared", num_links)

        st.markdown("---")
        st.markdown("## 🗓️ Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='lime')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.markdown("## 📅 Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='cyan')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.markdown("## 📊 Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔁 Busiest Days")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='violet')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.markdown("### 📆 Busiest Months")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.markdown("### 🧠 Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap, cmap='YlGnBu')
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.markdown("## 👥 Most Active Users")
            x, new_df = helper.most_busy_users(df)
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.markdown("## 🌥️ WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.markdown("## 📝 Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='teal')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.markdown("## 😄 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
