## LMNH Plant Sensors Dashboard


LNMH wants to be able to visualise the data that is being collected. They want to be able to see the data in real time and be able to see the data over time.
This is the lowest priority of LNMH and so you should only attempt this once you have completed the other deliverables.

The requirements are:

- To be able to view the data in real-time
- View graphs of the latest temperature and moisture readings for every plant
- To be able to view the data from the long-term storage


### Dependencies

The following libraries are required to run the dashboard:

```python3
pandas
altair
sqlalchemy
streamlit
pytest
pylint
ipykernel
python-dotenv
```

### Usage

- Extracts data from RDS from past 24 hours
- Creates dataframes for time series of temperature and moisture
- Creates streamlit dashboard
- TODO: dockerise and deploy
