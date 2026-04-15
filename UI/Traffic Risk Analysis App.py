import oracledb
import streamlit as st
from pathlib import Path

# --- DATABASE SETUP ---
LIB_DIR = bytes(Path(__file__).parent.parent.joinpath("instantclient-basiclite-windows.x64-23.26.1.0.0","instantclient_23_0"))

# * Replace with user, pass, and dsn of the actual database
DB_USER = "Traffic_Accident_Risk_analysis"
DB_PASS = "Traffic123"
DB_DSN = "127.0.0.1:1521/xe"

# Initialize Oracle Client for Thick Mode
@st.cache_resource
def init_db():
    if LIB_DIR:
        try:
            oracledb.init_oracle_client(lib_dir=LIB_DIR)
        except Exception as e:
            st.error(f"Error initializing Oracle Client: {e}")

init_db()

def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)

#Run query given and write a table with the resulting data
def QueryTable(query):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        conn.close()
        if(data):
            return data
        else:
            st.info("No Records Found")
    except Exception as e:
        st.error(f"Error {e}")

# Streamlit UI
st.title("Traffic Analysis Risk Database")
st.subheader("Patterns in Traffic Accidents")

# Page browsing via clicking buttons
menu = ["Home","Accident ID", "Vehicle ID", "Count"]
choice = st.sidebar.radio("Search", menu)

match choice:
    case "Home":
        st.markdown("""
        ## Credits
        Database Designer: Brandon Bachoco\n
        UI Developer: Kallie Mendez\n
        
        ## Data Sources
        - https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents
        - https://www-fars.nhtsa.dot.gov/States/StatesCrashesAndAllVictims.aspx
        """)
        
    # * Accident ID
    case "Accident ID":
        # Instructions for page
        st.markdown("Get the **Vehicle Type**, **Report Timestamp**, **Weather Condition**, and **Accident Date** from an **Accident ID**")
        id = st.text_input("Enter the Accident ID")

        #Perform Search Query
        if st.button("Search"):
            query = f"""
                select v.VEHICLE_TYPE, ar.REPORT_TIMESTAMP, a.ACCIDENT_DATE, w.CONDITION_TYPE 
                from accident a 
                left join ACCIDENT_VEHICLE av 
                on a.ACCIDENT_ID = av.ACCIDENT_ID 
                left join vehicle v 
                on av.VEHICLE_ID = v.vehicle_ID 
                left join WEATHER_CONDITION w 
                on a.WEATHER_ID = w.WEATHER_ID 
                left join ACCIDENT_REPORT ar 
                on a.ACCIDENT_ID = ar.ACCIDENT_ID 
                where a.Accident_ID = {id}
                """
            data = QueryTable(query)
            st.dataframe(data, column_config={
                "0": "Vehicle Type",
                "1": "Report Timestamp",
                "2": "Accident Date",
                "3": "Weather Condition"
            })
                
    # * Vehicle ID
    case "Vehicle ID":
        st.html('<p style="font-size: 15.6239px;">Get the <b>Location ID</b>, <b>Accident Date</b>, and <b>Severity Level</b> for all accidents that a specifc <b>Vehicle ID</b> has been in </p>')
        id = st.text_input("Enter the Vehicle ID")

        #Perform Search Query
        if st.button("Search"):
            query = "select l.LOCATION_ID, a.ACCIDENT_DATE, a.SEVERITY_LEVEL "
            query += "from vehicle v "
            query += "left join accident_vehicle av "
            query += "on v.VEHICLE_ID = av.VEHICLE_ID "
            query += "left join accident a "
            query += "on av.ACCIDENT_ID = a.ACCIDENT_ID "
            query += "left join location l "
            query += "on a.LOCATION_ID = l.LOCATION_ID "
            query += f"WHERE v.VEHICLE_ID = {id} " 
            query += "ORDER BY l.LOCATION_ID "
            data = QueryTable(query)
            st.dataframe(data, column_config={
                "0": "Location ID",
                "1": "Accident Date",
                "2": "Severity Level"
            })
    # * Count
    case "Count":
        countMenu = ["", "Vehicle Type", "Vehicle ID", "Weather Condition"]
        countChoice = st.selectbox("Get count of all accidents per", countMenu)

        match countChoice:
            # * Vehicle Type
            case "Vehicle Type":
                query = "select v.vehicle_type, count(av.accident_id) as \"# of Accidents\" "
                query += "from vehicle v "
                query += "left join ACCIDENT_VEHICLE av "
                query +="on v.VEHICLE_ID = av.VEHICLE_ID "
                query += "group by v.VEHICLE_TYPE "
                query += "Order by \"# of Accidents\" desc"
                data = QueryTable(query)
                st.dataframe(data, column_config={
                    "0": "Vehicle Type",
                    "1": "# of Accidents"
                })
            case "Vehicle ID":
                id = st.text_input("Enter the Vehicle ID")
                if st.button("Search"):
                    query = "select count(av.ACCIDENT_ID) as \"#_of_Accidents\" "
                    query += "from ACCIDENT_VEHICLE av "
                    query += f"where av.vehicle_ID = {id}"
                    data = QueryTable(query)
                    st.dataframe(data, column_config={
                        "value": "# of Accidents"
                    })
            case "Weather Condition":
                query = "select w.CONDITION_TYPE, count(a.ACCIDENT_ID) as \"NUM_ACCIDENTS\" "
                query += "from WEATHER_CONDITION w "
                query += "left join ACCIDENT a "
                query += "on w.WEATHER_ID = a.WEATHER_ID "
                query += "group by w.CONDITION_TYPE "
                query += "order by NUM_ACCIDENTS DESC"
                data = QueryTable(query)
                st.dataframe(data, column_config={
                    "0": "Weather",
                    "1": "# of Accidents"
                })



