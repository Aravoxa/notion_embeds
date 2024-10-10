import os
import json
import yfinance as yf
from datetime import datetime

# Define the folder structure and time intervals
intervals = ['1min', '5min', '15min', 'daily', 'weekly']

# Function to fetch stock data from Yahoo Finance
def fetch_data(ticker, start_date):
    data = {}
    stock = yf.Ticker(ticker)
    
    # Define time intervals in yfinance format
    yf_intervals = {
        '1min': '1m',
        '5min': '5m',
        '15min': '15m',
        'daily': '1d',
        'weekly': '1wk'
    }
    
    # Fetch historical data for each interval
    for interval in intervals:
        df = stock.history(start=start_date, interval=yf_intervals[interval])
        # Save as JSON (open, high, low, close)
        data[interval] = df[['Open', 'High', 'Low', 'Close']].to_dict('records')
    
    return data

# Function to create the folder structure and files
def create_trade_folder(ticker, date):
    folder_name = f"{ticker}_{date.replace('/', '-')}"
    
    # Create the main folder
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Create the 'data' folder
    data_folder = os.path.join(folder_name, 'data')
    os.makedirs(data_folder, exist_ok=True)
    
    # Fetch the data
    start_date = datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
    data = fetch_data(ticker, start_date)
    
    # Create HTML and data files for each interval
    for interval in intervals:
        # Write HTML file
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{interval} Chart - {ticker}</title>
            <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
        </head>
        <body>
            <div id="chart" style="width: 100%; height: 400px;"></div>

            <script>
                fetch('./data/{interval}.json')
                .then(response => response.json())
                .then(data => {{
                    const chart = LightweightCharts.createChart(document.getElementById('chart'), {{
                        width: 600,
                        height: 400,
                    }});
                    const lineSeries = chart.addLineSeries();
                    lineSeries.setData(data);
                }})
                .catch(error => console.error('Error fetching the data:', error));
            </script>
        </body>
        </html>
        """
        with open(os.path.join(folder_name, f"{interval}.html"), "w") as html_file:
            html_file.write(html_content)
        
        # Write data JSON file
        with open(os.path.join(data_folder, f"{interval}.json"), "w") as json_file:
            json.dump(data[interval], json_file, indent=4)

# Main function to run the script
def main():
    ticker = input("Enter ticker symbol (e.g., AAPL): ").upper()
    date = input("Enter date (dd/mm/yyyy): ")
    
    create_trade_folder(ticker, date)
    print(f"Trade folder for {ticker} on {date} has been created successfully.")

if __name__ == "__main__":
    main()
