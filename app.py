import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="SDV Verification Pipeline", layout="wide")

st.title("🚗 Software-Defined Vehicle (SDV) Trust Verification Gate")
st.markdown("**Domain:** Automotive Manufacturing | **System:** Automated CI/CD Safety Validation")
st.markdown("---")

st.sidebar.header("⚙️ Simulation Controls")
test_count = st.sidebar.slider("Number of Test Scenarios", min_value=10, max_value=100, value=25)
fault_mode = st.sidebar.toggle("Inject Software Fault (Brake Delay / Sensor Bug)")
fault_type = st.sidebar.selectbox("Select Fault Type", [
    "Brake Delay (Over-speed Risk)", 
    "Lane Departure Logic Error", 
    "Synthetic Sensor Noise"
])

run_btn = st.sidebar.button("🚀 Run Pipeline Verification", type="primary")

if run_btn:
    st.subheader("1. AI Synthetic Scenario & Risk Generation")
    np.random.seed(42)
    speeds = np.random.randint(50, 130, size=test_count)
    distances = np.random.randint(10, 60, size=test_count)
    
    df = pd.DataFrame({
        "Scenario ID": [f"TEST_{i+1:03d}" for i in range(test_count)],
        "Vehicle Speed (km/h)": speeds,
        "Obstacle Distance (m)": distances,
        "Mock ECU Status": ["ACTIVE"] * test_count
    })
    
    st.dataframe(df.head(5), use_container_width=True)
    
    st.subheader("2. Executing Simulation & Safety Gate Test")
    progress_bar = st.progress(0)
    status_list = []
    failed_count = 0
    
    for i in range(test_count):
        time.sleep(0.01)
        progress_bar.progress((i + 1) / test_count)
        
        speed = df.loc[i, "Vehicle Speed (km/h)"]
        dist = df.loc[i, "Obstacle Distance (m)"]
        
        if fault_mode and speed > 85 and dist < 30:
            status_list.append("FAILED ❌")
            failed_count += 1
        else:
            status_list.append("PASSED ✅")
            
    df["Result"] = status_list
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Scenarios Evaluated", test_count)
    col2.metric("Passed Tests", test_count - failed_count)
    col3.metric("Safety Regressions (Bugs)", failed_count, delta_color="inverse")
    
    st.subheader("3. Risk Coverage & Scenario Plot")
    fig, ax = plt.subplots(figsize=(9, 3.5))
    colors = ['#2ecc71' if r == "PASSED ✅" else '#e74c3c' for r in df["Result"]]
    
    ax.scatter(df["Vehicle Speed (km/h)"], df["Obstacle Distance (m)"], c=colors, s=70)
    ax.set_xlabel("Vehicle Speed (km/h)")
    ax.set_ylabel("Obstacle Distance (m)")
    ax.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig)
    
    st.subheader("4. CI/CD OTA Release Gate Decision")
    if failed_count > 0:
        st.error(f"❌ **OTA UPDATE REJECTED!** Injected Fault Detected: [{fault_type}]. Deployment halted to avoid vehicle crash risk.")
    else:
        st.success("✅ **OTA UPDATE APPROVED!** All automated risk scenarios passed. Ready to deploy to vehicle fleet.")
else:
    st.info("👈 Left side-la irukkura '🚀 Run Pipeline Verification' button-a click panni simulation-a start pannunga!")