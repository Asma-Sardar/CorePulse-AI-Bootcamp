import streamlit as st
import sqlite3
import pandas as pd

# 1. setting up the database
def init_db():
    conn = sqlite3.connect('corepulse.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_profile (
                 user_id INTEGER PRIMARY KEY, Age INTEGER, Gender TEXT, 
                 Weight_kg REAL, Height_m REAL, BMI REAL, Fat_Percentage REAL, 
                 Experience_Level TEXT, Experience_Factor REAL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS daily_logs (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
                 Max_BPM REAL, Avg_BPM REAL, Resting_BPM REAL, 
                 Session_Duration_hours REAL, Calories_Burned REAL, 
                 Workout_Type TEXT, Workout_Frequency_days_week INTEGER,
                 Heart_Stress REAL, Intensity REAL, Training_Load REAL,
                 Weekly_Load REAL, Calorie_Efficiency REAL, Workout_Factor REAL,
                 log_date DATE DEFAULT CURRENT_DATE)''')
    conn.commit()
    conn.close()

init_db()

st.title("CorePulse Full Data Entry")

# 2. setting up the form
with st.form("main_form"):
    #  --> user profile sections
    st.header("User Profile")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        weight = st.number_input("Weight (kg)", value=70.0)
        height = st.number_input("Height (m)", value=1.75)
    with col2:
        bmi = st.number_input("BMI", value=22.8)
        fat_per = st.number_input("Fat Percentage", value=15.0)
        exp_level = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
        exp_factor = st.number_input("Experience Factor", value=1.0)

    st.divider()

    # --> daily log section
    st.header("Daily Log")
    col3, col4 = st.columns(2)
    with col3:
        w_type = st.selectbox("Workout Type", ["Cardio", "Strength", "HIIT", "Yoga"])
        max_bpm = st.number_input("Max BPM", value=180.0)
        avg_bpm = st.number_input("Avg BPM", value=130.0)
        rest_bpm = st.number_input("Resting BPM", value=60.0)
        duration = st.number_input("Session Duration (hours)", value=1.0)
        cals = st.number_input("Calories Burned", value=400.0)
    with col4:
        freq = st.number_input("Workout Frequency (days/week)", value=4)
        stress = st.number_input("Heart Stress", value=0.0)
        intensity = st.number_input("Intensity", value=0.0)
        t_load = st.number_input("Training Load", value=0.0)
        w_load = st.number_input("Weekly Load", value=0.0)
        eff = st.number_input("Calorie Efficiency", value=0.0)
        w_factor = st.number_input("Workout Factor", value=0.0)

    # 3. handling form submission
    submitted = st.form_submit_button("Save Everything")
    
    if submitted:
        conn = sqlite3.connect('corepulse.db')
        c = conn.cursor()
        
        try:
            # Insert into user_profile
            c.execute('''INSERT INTO user_profile 
                         (Age, Gender, Weight_kg, Height_m, BMI, Fat_Percentage, Experience_Level, Experience_Factor) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                      (age, gender, weight, height, bmi, fat_per, exp_level, exp_factor))
            
            # Get the user_id of the person we just added to link the tables
            user_id = c.lastrowid
            
            # Insert into daily_logs
            c.execute('''INSERT INTO daily_logs 
                         (user_id, Max_BPM, Avg_BPM, Resting_BPM, Session_Duration_hours, Calories_Burned, 
                          Workout_Type, Workout_Frequency_days_week, Heart_Stress, Intensity, 
                          Training_Load, Weekly_Load, Calorie_Efficiency, Workout_Factor) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                      (user_id, max_bpm, avg_bpm, rest_bpm, duration, cals, 
                       w_type, freq, stress, intensity, t_load, w_load, eff, w_factor))
            
            conn.commit()
            st.success(" All data saved to both tables!")
        except Exception as e:
            st.error(f" Error saving data: {e}")
        finally:
            conn.close()
st.divider()
st.header(" Database Viewer")

# to select which table to view
table_to_view = st.radio("Select Table:", ["Daily Logs", "User Profiles"], horizontal=True)

conn = sqlite3.connect('corepulse.db')

try:
    if table_to_view == "Daily Logs":
        query = "SELECT * FROM daily_logs"
    else:
        query = "SELECT * FROM user_profile"
    
    df = pd.read_sql_query(query, conn)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        
        # option to download the data as CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Download {table_to_view} as CSV",
            data=csv,
            file_name=f"{table_to_view.lower().replace(' ', '_')}.csv",
            mime='text/csv',
        )
    else:
        st.info(f"The {table_to_view} table is currently empty. Submit the form above to add data!")

except Exception as e:
    st.error(f"Error reading database: {e}")

finally:
    conn.close()
