import os
from dotenv import load_dotenv
from fredapi import Fred
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv('FRED_API_KEY')

# Check if the API key was loaded successfully
if not api_key:
    raise ValueError("FRED_API_KEY not found in .env file or environment variables.")

# Initialize the Fred client with my API key
fred = Fred(api_key=api_key)

# Request data from the specified date range
unemployment_data = fred.get_series("UNRATE", observation_start='2016-01-01', observation_end='2024-12-31')
payrolls_data = fred.get_series('PAYEMS', observation_start='2016-01-01', observation_end='2024-12-31')

print ("** Data from FRED API (2020 - 2024) **")

# Print the last 5 entries for the unemployment rate
print("\nLatest Unemployment Rate Data:")
print(unemployment_data.tail())

# Print the last 5 entries for nonfarm payrolls
print("\nLatest Nonfarm Payrolls Data (in thousands)")
print(payrolls_data.tail())

# ** Trend Analysis
cpi_data = fred.get_series('CPIAUCSL', observation_start='2016-01-01')
cpi_pct_change = cpi_data.pct_change(periods=12) * 100

# Create a DataFrame for easier analysis
df = pd.DataFrame({'Inflation': cpi_pct_change})

# Calculate the 3-month moving average
df['3_Month_MA'] = df['Inflation'].rolling(window=3).mean()

# Show the last 6 months for context
print("** Trend Analysis of Inflation Data **")
print(df.tail(6))

# NLP Sentiment (Qualitative Analysis to Verify Bias)

# Using simulated news descriptions from previous analysis
articles = [
    {
        "source": "Fox News",
        "description": "Trump's tariff revenue has skyrocketed in just a few months, soaring past 2024 levels."
    },
    {
        "source": "Yale Budget Lab",
        "description": "US real GDP growth over 2025 and 2026 is -0.5 pp lower each year from all 2025 tariffs."
    },
    {
        "source": "Associated Press",
        "description": "The economy showed surprising resilience, expanding at a 3.0% pace in the latest quarter despite ongoing inflation concerns."
    }
]

print("** NLP Sentiment Analysis of News Content**")
for article in articles:
    blob = TextBlob(article['description'])
    polarity = blob.sentiment.polarity

    # Classify the sentiment
    if polarity > 0.1:
        sentiment = 'Positive'
    elif polarity < -0.1:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    print(f"Source: {article['source']}")
    print(f"Polarity Score: {polarity:.2f} ({sentiment})")

# Visualizations: Visualizing the Economic Trend vs. Noise
plt.style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize=(10, 6))

# Call the 'df' variable directly for plotting
plt.plot(df.index,df['Inflation'], marker='o', linestyle='--', label='Monthly Inflation(Noise)')
plt.plot(df.index, df['3_Month_MA'], marker='', linestyle='-', linewidth=2, label='3-Month Moving Average(Trend)')

plt.title('Economic Analysis: Monthly Inflation vs. Underlying Trend', fontsize=16)
plt.ylabel('Year-over-Year Inflation (%)', fontsize=12)
plt.xlabel('Date', fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout
plt.show()

# Visualizations: Comparing Media Sentiment
sentiment_data = {
    'Source': ['Fox News', 'Yale Budget Lab', 'Associated Press'],
    'Polarity Score': [-0.23, 0.20, 0.60]
}
sentiment_df = pd.DataFrame(sentiment_data)
sentiment_df = sentiment_df.sort_values('Polarity Score')

# Plotting
plt.figure(figsize=(8, 6))
color = ['firebrick' if x < 0 else 'mediumseagreen' for x in sentiment_df['Polarity Score']]

plt.bar(sentiment_df['Source'], sentiment_df['Polarity Score'], color=color)
plt.axhline(0, color='gray', linewidth=0.8) # Add a line at zero for reference

plt.title('Media Sentiment Analysis on Economic News', fontsize=16)
plt.ylabel('Sentiment Polarity Score (-1 to +1)', fontsize=12)
plt.xlabel('News Source', fontsize=12)
plt.tight_layout()
plt.show()