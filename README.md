# Wetbulb warnings
This application displays the average real-time temperature, relative humidity and Wet-Bulb Temperature in Singapore with guidelines on how to stay safe in the heat.

This application was built using [streamlit](https://streamlit.io/).

![wetbulb-warnings app demo](/media/app_sample.png)

## Contents
1. [Installation](#installation)
2. [About WBT](#about-wet-bulb-temperature-wbt)
3. [References and data used](#sources-and-further-reading)
4. [Upcoming features](#upcoming-features)

## Installation
Pull the latest Docker image:
```bash
docker image pull ptejasv/wetbulb-status:latest
```

Run the image:
```bash
docker run -d -p 8501:8501 --name "wetbulb-warnings" ptejasv/wetbulb-status:latest
```

Access the local deployment on port 8501 via `http://localhost:8501/`.

## About Wet-Bulb Temperature (WBT)
WBT is the lowest temperature that an environment can take after adjusting for evaporation. Since our sweat evaporates, it can be used as a measure of how cool the air surrounding our body can get after accounting for sweating. 

Evaporation, and therefore sweat evaporation, is higher when relative humidity is low. This means that an area which is hotbut dry might be safer than an area that might be cooler but very humid because people in the hot, dry area can cool off better by sweating.

At high WBTs, the body finds it hard to avoid overheating, increasing the risk of [heat-related illnesses](http://www.weather.gov.sg/learn-heat-stress/).

## Sources and further reading
**Information on WBT**
- [Meteorological Service Singapore (MSS)](http://www.weather.gov.sg/heat-stress/)
- [*Why you need to worry about the 'wet-bulb temperature'*, The Guardian](https://www.theguardian.com/science/2022/jul/31/why-you-need-to-worry-about-the-wet-bulb-temperature)

**Real-time data on air temperature and humidity in Singapore**

- [Air Temperature across Singapore](https://beta.data.gov.sg/datasets/d_5b1a6d3688427dd41e2c234fe42fb863/view) from the National Environment Agency, via data.gov under the Open Data License.
- [Relative Humidity across Singapore](https://beta.data.gov.sg/datasets/d_a64cbc762227d00a5a7fc7fc7fdb762b/view) from the National Environment Agency, via data.gov under the Open Data License.

**Formula used to calculate WBT**

Stull, R. (2011). Wet-Bulb Temperature from Relative Humidity and Air Temperature. Journal of Applied Meteorology and Climatology, 50(11), 2267-2269. https://doi.org/10.1175/JAMC-D-11-0143.1

## Upcoming features
1. live deployment
2. WBT across different areas of Singapore
