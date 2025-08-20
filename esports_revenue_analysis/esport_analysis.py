import pandas as pd

# Load the datasets from the CSV files
players_df = pd.read_csv('C:\\Users\\durki\\OneDrive\\Desktop\\Python-Portfolio-Project\\highest_earning_players.csv')
teams_df = pd.read_csv('C:\\Users\\durki\\OneDrive\\Desktop\\Python-Portfolio-Project\\highest_earning_teams.csv')

# Set a pandas display option to format currency nicely
pd.set_option('display.float_format', lambda x: f'${x:,.2f}')

# Analysis 1: Summary Statstics for Earnings
print("--- Analysis 1: Summary Statistics for Earnings ---")

# Use the .describe()metod to get key stats for player earnings
print("\nPlayer Earnings Statistics:")
print(players_df['TotalUSDPrize'].describe())

# Use the .describe() method for team earnings
print("\nTeam Earnings Statistics:")
print(teams_df['TotalUSDPrize'].describe())
print("-" * 50)


# Analysis 2: Top 5 Highest Earnings (Players, Teams, Games)
print("\n--- Analysis 2: Top 5 Highest Earners ---")

# Use the .nlargest() method to efficiently get the top 5 players
print("\nTop 5 Highest Earning Players:")
print(players_df.nlargest(5, 'TotalUSDPrize')[['CurrentHandle', 'TotalUSDPrize', 'Game']])

# Use .nlargest() again for the top 5 teams
print("\nTop 5 Highest Earning Teams:")
print(teams_df.nlargest(5, 'TotalUSDPrize')[['TeamName', 'TotalUSDPrize', 'Game']])

# Group by game, sum the prize money, and then find the nlargest
print("\nTop 5 Most Lucrative Games (by total players earnings):")
top_games = players_df.groupby('Game')['TotalUSDPrize'].sum().nlargest(5)
print(top_games)
print("-" * 50)


# Analysis 3: Players and Game Counts by Genre
print("\n--- Analysis 3: Player and Game Counts by Genre ---")

# Group by genre and aggregate two different columns:
# - Count the number of players (using PlayerID)
# - Count the number of unique games (using Game)
genre_counts = players_df.groupby('Genre').agg(
    NumberOfPlayers=('PlayerId', 'count'),
    NumberOfUniqueGames=('Game', 'nunique')
).sort_values(by='NumberOfPlayers', ascending=False)
print("\nNumber of Top Players and Unique Games per Genre:")
print(genre_counts)
print("-" * 50)


# Analysis 4: Detailed Earnings Breakdown by Genre
print("\n--- Analysis 4: Detailed Earnings Breakdown by Genre")

# Group by genre and aggregate multiple statistics for the prize money
genre_earnings_summary = players_df.groupby('Genre')['TotalUSDPrize'].agg(
    ['sum', 'mean', 'median', 'max', 'min']
).sort_values(by='sum', ascending=False)

# Rename the columns for a cleaner final table
genre_earnings_summary.rename(columns={
    'sum': 'TotalEarnings',
    'mean': 'AverageEarnings',
    'median': 'MedianEarnings',
    'max': 'MaxPlayerEarnings',
    'min': 'MinPlayerEarnings'
}, inplace=True)
print("\nSummary Of Player Earnings by Game Genre:")
print(genre_earnings_summary)
print("-" * 50)