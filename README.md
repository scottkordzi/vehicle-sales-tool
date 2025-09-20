# vehicle-sales-tool

## Project Goals

1. Create a centralized dashboard for consumers with up-to-date information on vehicle market trends.
2. Create a predictive model that provides an estimate for consumers on vehicles that they're either looking to purchase or sell.

## Dashboard Features

- Average selling price of vehicles over the years
    - Broken down by luxury and non-luxury vehicles
- Difference in selling price across different brands
- Average selling price with regards to state, condition, and odometer

## Model Methodology and Feature Inputs

Vehicle Sales Tool
Overview
The Vehicle Sales Tool is a web-based application designed to empower consumers with insights into the vehicle market. It provides a centralized dashboard displaying up-to-date market trends and a predictive model to estimate vehicle prices for buying or selling. The tool aims to simplify decision-making by offering data-driven insights into vehicle pricing based on various factors such as brand, condition, odometer reading, and location.
Project Goals

Centralized Dashboard: Create an intuitive dashboard that provides consumers with real-time information on vehicle market trends.
Predictive Model: Develop a machine learning model to estimate vehicle prices for consumers looking to purchase or sell, based on historical and current market data.

## Dashboard Features

Average Selling Price Trends:
Historical data on vehicle prices over the years.
Segmented by luxury and non-luxury vehicles for detailed insights.


Brand Comparison:
Visualize differences in selling prices across various vehicle brands.


Price Analysis by Factors:
Average selling price broken down by:
State: Regional pricing differences.
Condition: New, used, or certified pre-owned vehicles.
Odometer: Impact of mileage on vehicle value.





## Technologies Used

Frontend: HTML, CSS, JavaScript, Dash (e.g., React for the dashboard)
Backend: Python (e.g., Flask or Django for API and data processing)
Data Analysis: Pandas, NumPy
Machine Learning: Scikit-learn for the predictive model
Data Visualization: Plotly, D3.js, or Chart.js
Database: SQLite or PostgreSQL for storing vehicle data
Data Sources: Public APIs or datasets

## Installation
To set up the project locally, follow these steps:

Clone the Repository:
git clone https://github.com/scottkordzi/vehicle-sales-tool.git
cd vehicle-sales-tool


Set Up a Virtual Environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Set Up the Database:

Configure your database connection in config.py (e.g., SQLite or PostgreSQL).
Run the database initialization script:python init_db.py




Run the Application:
python app.py


Access the dashboard at http://localhost:5000 in your browser.



## Usage

Dashboard Access:

Open the application in your web browser to view the dashboard.
Explore interactive charts showing average vehicle prices, brand comparisons, and more.


Price Prediction:

Input vehicle details (e.g., make, model, year, condition, odometer, state) into the prediction tool.
Receive an estimated price based on the predictive model.


Customization:

Filter data by luxury/non-luxury vehicles or specific brands.
Adjust parameters to analyze trends in specific states or conditions.


This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or feedback, please contact the project maintainer:

GitHub: scottkordzi
Email: [Your email address, if you'd like to include it]

Footer
© 2025 Scott Kordzi. Powered by GitHub.
