Hawaii Climate API
This project provides a Flask-based API for accessing Hawaii climate data stored in a SQLite database. It serves precipitation, weather station, and temperature observation data via multiple endpoints. The project also demonstrates optional improvements such as error handling, unit testing, and deployment instructions.

File Structure
A typical folder structure for the project is as follows:

SurfsUp/  
├── Resources/  
│   └── hawaii.sqlite         # SQLite database with 
│   └── app.py                # **Completed Flask application and API  
│   └── app.source.py         # old py file
├── ipynb_checkpoints         # source folder
├── README.md                 # Project documentation  

  
Setup & Installation  
1. Ensure Python 3.x is installed  
2. Install required packages:  
pip install flask sqlalchemy numpy pandas


Run the application:  
python app.py
  
## API Routes  
- `/` : Home page, lists all available routes  
- `/api/v1.0/precipitation` : Last 12 months of precipitation data  
- `/api/v1.0/stations` : List of weather stations  
- `/api/v1.0/tobs` : Temperature observations from most active station  
- `/api/v1.0/<start>` : Temperature stats from start date (YYYY-MM-DD)  
- `/api/v1.0/<start>/<end>` : Temperature stats for date range  
  
## Data Analysis Features  
- SQLAlchemy ORM for database interaction  
- Date filtering for precipitation analysis  
- Statistical calculations (min, avg, max temperatures)  
- JSON formatted responses  
  
## Error Handling  
- Date format validation (YYYY-MM-DD)  
- Invalid route handling  
- Database connection error handling  
  
## Testing  
Run the application locally and verify each endpoint returns expected JSON data.  
  
## Dependencies  
- Flask  
- SQLAlchemy  
- NumPy  
- Pandas  