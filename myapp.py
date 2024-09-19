import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

# Set page layout to wide mode
st.set_page_config(layout="wide")

# Title of the app
st.write("# Player Analysis Web App")

# Subtitle
st.write("# T 99")

# Sidebar input for user to select year
st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2023, 2024))))

# Load and display the player data
player_df = pd.read_csv("tolu_clean.csv")

# Drop the "Unnamed: 0" column if it exists
if "Unnamed: 0" in player_df.columns:
    player_df = player_df.drop("Unnamed: 0", axis=1)

# Reset the index and make it start from 1
player_df = player_df.reset_index(drop=True)
player_df.index = player_df.index + 1

# Title for the data section
st.title("Player Data")

# Display the DataFrame
st.dataframe(player_df)

# Calculate total minutes and average minutes per game
total_minutes = player_df['Min'].sum()
average_minutes = player_df['Min'].mean()

# Display total and average minutes
st.write(f"### Total Minutes Played: {total_minutes}")
st.write(f"### Average Minutes per Game: {average_minutes:.2f}")

# Calculate total goals and average goals per game
total_goals = player_df['Gls'].sum()
average_goals = player_df['Gls'].mean()

# Display total and average goals
st.write('# Goals')
st.write(f"### Total Goals: {total_goals}")
st.write(f"### Average Goals per Game: {average_goals:.2f}")

# Compare Expected Goals (xG) with Actual Goals
avg_xg = player_df['xG'].mean()
avg_goals = player_df['Gls'].mean()
st.write(f"### Expected Goals (xG): {avg_xg:.2f} vs Actual Goals (aG): {avg_goals:.2f}")

# Investigate performance based on venue
# Ensure 'Venue' and 'Gls' columns are properly formatted
player_df['Venue'] = player_df['Venue'].astype(int)  # Convert 'Venue' to integer
player_df['Gls'] = pd.to_numeric(player_df['Gls'], errors='coerce')  # Ensure 'Gls' is numeric

# Split the data into home and away games
home_games = player_df[player_df['Venue'] == 1]
away_games = player_df[player_df['Venue'] == 0]

# Calculate average goals scored at home and away
avg_goals_home = home_games['Gls'].mean()
avg_goals_away = away_games['Gls'].mean()

# Display average goals scored at home and away
st.write(f"### Average Goals Scored at Home: {avg_goals_home:.2f}")
st.write(f"### Average Goals Scored Away: {avg_goals_away:.2f}")

# Calculate total assists and average assists per game
total_assists = player_df['Ast'].sum()
average_assists = player_df['Ast'].mean()

# Display total and average assists
st.write('# Assists')
st.write(f"### Total Assists: {total_assists}")
st.write(f"### Average Assists per Game: {average_assists:.2f}")

# Goal/Assist Contribution
contribution_per_game = (player_df['Gls'] + player_df['Ast']).mean()
st.write('# Goal/Assist Contribution')
st.write(f"### Goal Contribution per Game: {contribution_per_game:.2f}")

# Shooting Accuracy
total_shots = player_df['Sh'].sum()
total_shots_target = player_df['SoT'].sum()

# Calculate shooting accuracy per row
player_df['Shooting_Accuracy'] = np.where(
    player_df['Sh'] > 0, 
    player_df['SoT'] / player_df['Sh'] * 100, 
    0
)

# Calculate the average shooting accuracy
average_shooting_accuracy = player_df['Shooting_Accuracy'].mean()

# Display shooting statistics
st.write('# Shooting Accuracy')
st.write(f"### Total Shots: {total_shots}")
st.write(f"### Total Shots on Target: {total_shots_target}")
st.write(f"### Shooting Accuracy: {average_shooting_accuracy:.2f}%")
