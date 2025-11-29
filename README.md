This project fetches the live price of a cryptocurrency (BTCUSDT by default) from the Binance Public API every 2 minutes.
It also calculates:
Minimum price so far
Maximum price so far
Biggest % increase (“max fly”)
Biggest % decrease (“min fly”)
Stores all data into a CSV file for later analysis

It’s a simple project to understand how to work with APIs, JSON data, loops, and real-time price tracking.

 What This Project Does:
✔ Connects to Binance API
✔ Gets the live price every 120 seconds
✔ Saves data (timestamp + price) into price_log.csv
✔ Shows these stats on every update:

Latest price
Lowest price since start
Highest price since start
Biggest percentage rise between two samples
Biggest percentage drop between two samples

Technologies Used:
Python 3
Requests (API calls)
CSV (logging data)
Datetime (timestamps)

Purpose of This Project:
This project was created to practice:
Using APIs
Collecting real-time data
Working with loops
Logging and analyzing price movement
