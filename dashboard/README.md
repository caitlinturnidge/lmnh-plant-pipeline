# LMNH Plant Sensors Dashboard

This repository contains the code for the LMNH Plant Sensors Dashboard, a real-time data visualisation tool for the Liverpool Natural History Museum. The dashboard provides real-time and historical data on plant health, allowing the museum staff to monitor and manage their gardens effectively.


#### Here's what it looks like...

 <video width="600" controls>
 <source src="plant-dashboard-demo.mp4" type="video/mp4">
 Your browser does not support the video tag.
 </video>
 <figcaption>Plant Health Tracker Demo</figcaption>


## 📋 Requirements

The dashboard should meet the following requirements:

- Display data in real-time.
- Show graphs of the latest temperature and moisture readings for every plant.
- Provide access to data from long-term storage.

## 🗂️ File Overview

This repository contains the following files:

- `main.py`: The main script that builds and runs the dashboard on Streamlit.
- `data_utils.py`: Contains functions to read in image and origin data (imported in main.py).
- `db_functions.py`: Functions that interact with the database (imported into main.py).
- `create_mock_data.py`: Creates mock 24hr data from one API reading (for use with chart exploration).
- `playground.ipynb`: An exploratory notebook to test visualisation elements.
- `config.toml`: A Streamlit configuration file that sets the custom theme for the dashboard.
- `Dockerfile`: Builds the container image to be deployed.
- `.env`: Stores environment variables needed to deploy the dashboard on AWS and access the database.

## ✅ Dependencies

The following libraries are required to run the dashboard:

```python3
- pandas
- altair
- sqlalchemy
- streamlit
- pytest
- pylint
- ipykernel
- python-dotenv
```

Install these dependencies using the command `pip install -r requirements.txt`.

## 📊 Usage

The dashboard extracts data from RDS for the past 24 hours, creates dataframes for the time series of temperature and moisture, and then generates the Streamlit dashboard.

## 🐳 Building the Docker Image

To build the Docker image for this application, follow these steps:

1. Navigate to the root directory of this repository.
2. Run the command `docker build -t lmnh-plant-sensors .` to build the Docker image. Replace `lmnh-plant-sensors` with the desired name for your Docker image.
3. After the build process completes, you can run the Docker image using the command `docker run -p 8501:8501 lmnh-plant-sensors`.

The application will now be accessible at `http://localhost:8501`.

## 📞 Contact

For any queries or issues, please contact the team. 
🦋