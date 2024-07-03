import streamlit as st
import requests
import numpy as np
import math
from datetime import datetime as dt 
import pytz
from enum import Enum

st.set_page_config(layout="wide")

THRESHOLD_DANGER = 35
THRESHOLD_WARNING = 31

URL_TEMPERATURE = "https://api.data.gov.sg/v1/environment/air-temperature"
URL_HUMIDITY = "https://api.data.gov.sg/v1/environment/relative-humidity"

status_message = [
    (
        "Current environment might be dangerous.", "🚨",
        """
            Some actions you can take to stay safe:
            - Move to a location with air conditioning. If you are outdoors, stay under any available shelter.
            - Stay hydrated.
            - Observe your body for symptoms of discomfort and consult a doctor if you feel unwell.
        """
    ), (
        "Current environment might be unsafe.", "⚠️",
        """
            The current Wet-Bulb temperature poses a high risk of heat stress. Consider these actions to minimise your risk of injury:
            - Avoid outdoor activity and stay under shelter.
            - Observe your body for discomfort.
            - Hydrate frequently. 
        """
    ), (
        "Current environment is safe.", "✅",
        """
            The current Wet-Bulb temperature puts you at low risk of injury. Even so, stay on the alert for any signs of discomfort.
            - Hydrate regularly.
            - Take shelter in between prolonged outdoor activity.
        """
    )
]

class Status(Enum):
    DANGER = 0
    WARNING = 1
    SAFE = 2
    NONE = 3

@st.cache_data
def display_intro():
    st.title("Live Wet-Bulb temperature in Singapore")
    st.info("DISCLAIMER: this site does not substitute professional medical advice and is for educational purposes only.")

@st.cache_data
def get_temp_rh(for_datetime):
    """
        Calls the public data.gov API to get the current temperature and 
        relative humidity.

        Parameters:
            for_datetime (datetime): The timestamp for which to retrieve the 
            temperature and relative humidity.

        Returns:
            (dict): The current data on temperature.
            (dict): The current data on relative humidity.
    """
    params = {"date_time": for_datetime}
    
    res_temp = requests.get(URL_TEMPERATURE, params=params).json()

    res_rh = requests.get(URL_HUMIDITY, params=params).json()
    
    return res_temp, res_rh

@st.cache_data
def agg_values(temp, rh):
    avg_temp = np.mean([i["value"] for i in 
                        temp.get("items", -1)[0]["readings"]])

    avg_rh = np.mean([i["value"] for i in rh.get("items", -1)[0]["readings"]])

    return avg_temp, avg_rh

@st.cache_data
def calc_wetbulb(temp, rh):
    """
        Uses the formula from the American Meteorological Society journal to 
        calculate the Wet-Bulb temperatre.

        Params:
            temp (numpy.float64): The average temperature.
            rh (numpy.float64): The average relative humidity.
    """
    return (temp * math.atan(0.151977 * math.sqrt(rh + 8.313659))) \
        + math.atan(temp + rh) \
        - math.atan(rh - 1.676331) \
        + (0.00391838 * (math.sqrt(rh) ** 3)) * math.atan(0.023101 * rh) \
        - 4.686035

@st.cache_data
def check_status(wb_temp):
    """
        Evaluates if the current Wet-Bulb temperature is dangerous using 
        guidelines from the references and retrieves the interpretation of the 
        results.

        Params:
            wb_temp (numpy.float64): The current Wet-Bulb temperature
        
        Returns:
            (Status): The evaluated status of the current Wet-Bulb 
            temperature. Corresponds to the Status enum defined above.
            (tuple): The status message, icon and actions to display to the user
            based on the current status.
    """
    status = Status.NONE
    if wb_temp >= THRESHOLD_DANGER:
        status = Status.DANGER
    elif wb_temp >= THRESHOLD_WARNING:
        status = Status.WARNING
    else:
        status = Status.SAFE
    return status, status_message[status.value]

@st.cache_data
def display_output(temp, rh, wetbulb):
    """
        Presents a dashboard of the current temperature, humidity and Wet-Bulb
        temperature with actionable insights on how to interpret the results.

        Params:
            temp (numpy.float64): The average temperature.
            rh (numpy.float64): The average relative humidity.
            wetbulb (numpy.float64): The current Wet-Bulb temperature.
    """
    left, centre, right = st.columns(3)

    with left.container(height=170, border=True):
        st.subheader("Current temperature:")
        st.subheader(f"{round(temp, 2)} °C")

    with left.container(height=170, border=True):
        st.subheader("Current relative humidity:")
        st.subheader(f"{round(rh, 2)} %")

    with centre.container(height=356, border=True):
        st.subheader("Wet-Bulb Temperature:")
        st.header(f"{round(wetbulb, 2)} °C")

    status, msg = check_status(wetbulb)
    with right.container(height=356, border=True):
        st.subheader("What this means:")
        if status == Status.DANGER:
            st.error(msg[0], icon=msg[1])
        elif status == Status.WARNING:
            st.warning(msg[0], icon=msg[1])
        elif status == Status.SAFE:
            st.success(msg[0], icon=msg[1])
        st.markdown(msg[2])

@st.cache_data
def display_info():
    st.header("About Wet-Bulb temperature (WBT)")
    st.markdown(
        """
        WBT is the lowest temperature that an environment can take after 
        adjusting for evaporation. Since our sweat evaporates, it can be used 
        as a measure of how cool the air surrounding our body can get after 
        accounting for sweating. 

        Evaporation, and therefore sweat evaporation, is higher when relative 
        humidity is low. This means that an area which is hot but dry might 
        be safer than an area that might be cooler but very humid because 
        people in the hot, dry area can cool off better by sweating.

        At high WBTs, the body finds it hard to avoid overheating, increasing 
        the risk of 
        [heat-related illnesses](http://www.weather.gov.sg/learn-heat-stress/).
        """
    )

    st.header("Sources and further reading")
    st.markdown(
        """
        Information on WBT:
        - [Meteorological Service Singapore (MSS)](http://www.weather.gov.sg/heat-stress/)
        - [*Why you need to worry about the 'wet-bulb temperature'*, The Guardian](https://www.theguardian.com/science/2022/jul/31/why-you-need-to-worry-about-the-wet-bulb-temperature)

        Real-time data on air temperature and humidity in Singapore:
        
        - [Air Temperature across Singapore](https://beta.data.gov.sg/datasets/d_5b1a6d3688427dd41e2c234fe42fb863/view) from the National Environment Agency, via data.gov under the Open Data License.
        - [Relative Humidity across Singapore](https://beta.data.gov.sg/datasets/d_a64cbc762227d00a5a7fc7fc7fdb762b/view) from the National Environment Agency, via data.gov under the Open Data License.

        Formula used to calculate WBT:

        Stull, R. (2011). Wet-Bulb Temperature from Relative Humidity and Air
        Temperature. Journal of Applied Meteorology and Climatology, 50(11), 
        2267-2269. https://doi.org/10.1175/JAMC-D-11-0143.1
        """
    )

if __name__ == "__main__":
    display_intro()

    # call NEA's API to get the temperature and relative humidity
    tz = pytz.timezone("Asia/Singapore")
    live_datetime = dt.now(tz=tz).strftime("%Y-%m-%dT%H:%M:%S")
    temp, rh = get_temp_rh(live_datetime)

    # aggregate the results and calculate WBT
    avg_temp, avg_rh = agg_values(temp, rh)
    wetbulb = calc_wetbulb(avg_temp, avg_rh)

    # show the results as a dashboard
    display_output(avg_temp, avg_rh, wetbulb)
    st.button("Refresh")

    # show information and sources
    display_info()

