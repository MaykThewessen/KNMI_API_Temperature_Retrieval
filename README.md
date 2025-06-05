**🇳🇱 KNMI Temperature Data Exporter**

This script allows you to retrieve hourly temperature data from the KNMI (Royal Netherlands Meteorological Institute) for a selected weather station in the Netherlands. It processes the data and exports it as a .knmi file, useful for further climate analysis, simulations, or energy modeling.

🔧 Features

	•	📍 Select a KNMI weather station in the Netherlands (via station_id)
 
	•	🕒 Retrieve hourly measured temperature data
 
	•	📤 Export data to a .knmi-formatted file
 
	•	📈 Optional visualization with Plotly
 

🗂 File Structure

	•	KNMY_retrieval_v6_plotly.py

📦 Requirements

Install the required Python packages:

	•	pip install pandas plotly requests

🚀 Usage
Open the Python script and configure your station ID and date range:

	•	station_id = '260'  # e.g. 260 for De Bilt
	•	start_year = 2020
	•	end_year = 2024


Run the script:

	•	python KNMY_retrieval_v6_plotly.py


Output:

	•	A .knmi file containing hourly temperature data
 
	•	A Plotly graph (optional)

📁 Output Format

The output .knmi file contains:

	•	Timestamp
 
	•	Hourly temperature in tenths of degrees Celsius

Example:

YYYYMMDDHH,TEMPERATURE

2024010101,45

2024010102,43

...


🗺️ KNMI Station List

You can find a list of available KNMI stations here.

🧑‍💻 Author

Made by Mayk Thewessen for easy access and export of Dutch climate data.
