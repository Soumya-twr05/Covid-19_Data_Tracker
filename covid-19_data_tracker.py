import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sn
import requests

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Covid-19 Data Tracker", page_icon="🦠", layout="wide")
st.title("🦠 COVID-19 Data Tracker")

# --- Global Data ---
st.header("🌍 Global COVID-19 Summary")
global_url = "https://disease.sh/v3/covid-19/all"
global_data = requests.get(global_url).json()

st.metric("Total Cases", global_data['cases'])
st.metric("Total Deaths", global_data['deaths'])
st.metric("Total Recovered", global_data['recovered'])

# --- Country-Wise Data ---
country_data_url = "https://disease.sh/v3/covid-19/countries"
countries_data = requests.get(country_data_url).json()

df = pd.DataFrame(countries_data)
df = df[['country', 'cases', 'todayCases', 'deaths', 'todayDeaths', 'recovered', 'active']]

# --- Top 10 Countries ---
st.header("📊 Top 10 Countries by Total Cases")
top_10 = df.sort_values(by='cases', ascending=False).head(10)

fig1, ax1 = plt.subplots(figsize=(20,4))
sn.barplot(x='cases', y='country', data=top_10, palette='viridis', ax=ax1)
ax1.set_title('Top 10 Countries by Total COVID-19 Cases')
st.pyplot(fig1)

# --- Historical Data for India ---
st.header("📈 India's COVID-19 Trend (From 2-08-2023 to 3-09-2023) Last data that available")
india_history_url = "https://disease.sh/v3/covid-19/historical/India?lastdays=30"
history = requests.get(india_history_url).json()

cases = history['timeline']['cases']
dates = list(cases.keys())
values = list(cases.values())

fig2, ax2 = plt.subplots(figsize=(14,2))
ax2.plot(dates, values, marker='o', color='red')
ax2.set_title("COVID-19 Cases in India (Last 30 Days)")
ax2.set_xlabel("Date")
ax2.set_ylabel("Cases")
plt.xticks(rotation=45)
st.pyplot(fig2)

# --- Country-Specific Input ---
st.header("🔍 Search COVID-19 Stats by Country")
country = st.text_input("Enter Country Name:", "India")
if country:
    try:
        country_info = requests.get(f"https://disease.sh/v3/covid-19/countries/{country}").json()
        st.write(f"**Country**: {country_info['country']}")
        st.write(f"**Total Cases**: {country_info['cases']}")
        st.write(f"**Deaths**: {country_info['deaths']}")
        st.write(f"**Recovered**: {country_info['recovered']}")
        st.image(country_info['countryInfo']['flag'], width=100)
        st.header("🛡️ Stay Safe – COVID-19 Safety Tips")
        st.markdown("""
            ### ✅ Basic Prevention Measures:
            - 😷 **Wear a mask** in crowded or indoor places
            - 🧼 **Wash your hands frequently** with soap for at least 20 seconds
            - ↔️ **Maintain social distancing** (at least 6 feet)
            - 💉 **Get vaccinated** and keep up with booster doses
            - 🧴 **Use hand sanitizer** when soap and water aren't available
            - 🏠 **Stay home if you're feeling sick**



            ### 🚨 Be Aware of Symptoms:
            - Fever, cough, sore throat
            - Loss of taste or smell
            - Shortness of breath
            - Body aches and fatigue

            📝 If you have symptoms, **get tested and self-isolate**.



            ### 📢 Stay Informed:
            - Follow updates from the [World Health Organization](https://www.who.int/)
            - Check your local health department's announcements
            - Beware of **misinformation** and verify news from trusted sources
        """)

        
    except:
        st.error("Country not found or API error.")
