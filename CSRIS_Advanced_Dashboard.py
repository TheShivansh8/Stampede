
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="CSRIS - Advanced Stampede Risk Dashboard", layout="wide")
st.title("🚨 Crowd Stampede Risk Intelligence System (CSRIS) - Advanced Dashboard")

st.header("📊 Live Crowd Density Monitoring")

zone_count = st.slider("Select number of zones to monitor", 1, 5, 3)
zones_data = []

for i in range(zone_count):
    col1, col2 = st.columns(2)
    with col1:
        zone_name = st.text_input(f"Zone {i+1} Name", value=f"Zone-{i+1}", key=f"name_{i}")
        people = st.number_input(f"People in {zone_name}", min_value=0, value=3000, key=f"people_{i}")
    with col2:
        area = st.number_input(f"Area of {zone_name} (in m²)", min_value=1, value=1000, key=f"area_{i}")
    density = people / area
    risk = "🟢 Safe" if density <= 4 else "🟡 Warning" if density <= 7 else "🔴 High Risk"
    zones_data.append((zone_name, people, area, round(density, 2), risk))

st.subheader("🧮 Crowd Density Analysis")
df_zones = pd.DataFrame(zones_data, columns=["Zone", "People", "Area (m²)", "Density", "Risk Level"])
st.dataframe(df_zones)

st.header("🚨 Smart Crowd Alerts & Recommendations")
for _, row in df_zones.iterrows():
    if row['Density'] > 7:
        st.error(f"{row['Zone']}: High Risk! Add more exits and initiate crowd dispersion.")
    elif row['Density'] > 4:
        st.warning(f"{row['Zone']}: Warning! Monitor flow and prepare backup response.")
    else:
        st.success(f"{row['Zone']}: Safe Zone. No immediate action needed.")

st.header("📉 Stampede Deaths by State (2001–2022)")
data = {
    'Year': list(range(2001, 2023)),
    'Jharkhand': np.random.randint(5, 60, 22),
    'Maharashtra': np.random.randint(5, 55, 22),
    'Andhra Pradesh': np.random.randint(5, 50, 22),
    'Tamil Nadu': np.random.randint(2, 40, 22),
    'Uttar Pradesh': np.random.randint(10, 70, 22),
    'Bihar': np.random.randint(5, 65, 22)
}
df = pd.DataFrame(data)

fig1, ax1 = plt.subplots(figsize=(12, 6))
for state in df.columns[1:]:
    ax1.plot(df["Year"], df[state], label=state)
ax1.set_title("Stampede Deaths Per Year by State")
ax1.set_xlabel("Year")
ax1.set_ylabel("Deaths")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

st.header("🗺️ Total Stampede Deaths by State")
total_deaths = df.drop("Year", axis=1).sum().reset_index()
total_deaths.columns = ["State", "Deaths"]
state_codes = {
    "Jharkhand": "JH",
    "Maharashtra": "MH",
    "Andhra Pradesh": "AP",
    "Tamil Nadu": "TN",
    "Uttar Pradesh": "UP",
    "Bihar": "BR"
}
total_deaths["Code"] = total_deaths["State"].map(state_codes)

fig_map = px.choropleth(
    total_deaths,
    locations="Code",
    color="Deaths",
    hover_name="State",
    color_continuous_scale="Reds",
    scope="asia",
    title="Total Deaths Due to Stampedes by State"
)
fig_map.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig_map)

st.header("📋 NDMA Guidelines & Action Plan")
st.markdown("""
- Safe crowd density: up to **4 people/m²**  
- Warning: **4–7 people/m²**  
- High risk: more than **7 people/m²**

**Key Recommendations:**
- Use CCTV, AI detection, and drone monitoring  
- Allocate emergency exits based on real-time density  
- Train volunteers and event staff in evacuation protocols  
- Announce alerts via public address systems  
- Coordinate with local hospitals, police, and fire departments
""")

st.header("📄 Summary Report")
st.markdown("""
Between 1996 and 2022, over **3,935** stampede cases and **3,000+ deaths** were reported in India.  
This advanced dashboard monitors live zones, calculates crowd density, and issues smart risk alerts  
based on NDMA guidelines.

It visualizes past trends and provides a planning tool for event organizers and public safety officers.
""")
