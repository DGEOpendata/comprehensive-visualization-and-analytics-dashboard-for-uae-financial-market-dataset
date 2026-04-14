python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template, request

# Load dataset
data = pd.read_excel('Trading_Summary_by_Investor_Type_March.xlsx')

# Initialize Flask App
app = Flask(__name__)

# Route for homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route for data visualization
@app.route('/visualize', methods=['GET', 'POST'])
def visualize():
    investor_type = request.args.get('investor_type', 'All')
    start_date = request.args.get('start_date', data['Date'].min())
    end_date = request.args.get('end_date', data['Date'].max())

    # Filter data based on user inputs
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    if investor_type != 'All':
        filtered_data = filtered_data[filtered_data['Investor Type'] == investor_type]

    # Generate a line plot for buy/sell values
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=filtered_data, x='Date', y='Buy Value', label='Buy Value', marker="o")
    sns.lineplot(data=filtered_data, x='Date', y='Sell Value', label='Sell Value', marker="o")
    plt.title(f'Trading Values for {investor_type} from {start_date} to {end_date}')
    plt.xlabel('Date')
    plt.ylabel('Value (AED)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('static/trading_plot.png')

    return render_template('visualization.html', 
                           image_url='static/trading_plot.png', 
                           start_date=start_date, 
                           end_date=end_date,
                           investor_type=investor_type)

if __name__ == '__main__':
    app.run(debug=True)
