import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

# Set page layout to wide mode
st.set_page_config(layout="wide")

# Title of the app
st.markdown("<h1 style='text-align: center;'> Player Analysis Web App</h1>", unsafe_allow_html=True)

# Define a mapping between player and CSV file path
file_mapping = {
    'Tolu Arokodare': 'tolu_clean.csv',
    'Yira Sor': 'yira_clean.csv'
}

# Sidebar input for user to select year
st.sidebar.header('Select Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2023, 2024))))
selected_player = st.sidebar.selectbox('Player', list(file_mapping.keys()))

# Check if a player has been selected
if selected_player:
    file_path = file_mapping[selected_player]
    player_df = pd.read_csv(file_path)

    # Drop the "Unnamed: 0" column if it exists
    if "Unnamed: 0" in player_df.columns:
        player_df = player_df.drop("Unnamed: 0", axis=1)

    # Reset the index and make it start from 1
    player_df = player_df.reset_index(drop=True)
    player_df.index = player_df.index + 1

    # Ensure 'Date' column is in datetime format
    player_df['Date'] = pd.to_datetime(player_df['Date'])

    # Display the selected player’s name on the main page
    st.markdown(f"<h1 style='text-align: center; color: Blue; font-size: 4em'> {selected_player}</h1>", unsafe_allow_html=True)

    # Title for the data section
    st.markdown(f"<h2 style='text-align: center;'>Player Data for {selected_year}</h2>", unsafe_allow_html=True)

    # Metrics
    total_minutes = player_df['Min'].sum()
    average_minutes = player_df['Min'].mean()
    st.write(f'# Minutes')
    st.write(f"### Total Minutes Played: {total_minutes}")
    st.write(f"### Average Minutes per Game: {average_minutes:.2f}")

    total_goals = player_df['Gls'].sum()
    average_goals = player_df['Gls'].mean()
    st.write('# Goals')
    st.write(f"### Total Goals: {total_goals}")
    st.write(f"### Average Goals per Game: {average_goals:.2f}")

    # Performance by Venue
    player_df['Venue'] = pd.to_numeric(player_df['Venue'], errors='coerce')
    player_df['Gls'] = pd.to_numeric(player_df['Gls'], errors='coerce')

    home_games = player_df[player_df['Venue'] == 1]
    away_games = player_df[player_df['Venue'] == 0]
    avg_goals_home = home_games['Gls'].mean()
    avg_goals_away = away_games['Gls'].mean()
    st.write(f"### Average Goals Scored at Home: {avg_goals_home:.2f}")
    st.write(f"### Average Goals Scored Away: {avg_goals_away:.2f}")

    avg_xg = player_df['xG'].mean()
    st.write(f"### Expected Goals (xG): {avg_xg:.2f} vs Actual Goals (aG): {average_goals:.2f}")

    # Assists
    total_assists = player_df['Ast'].sum()
    average_assists = player_df['Ast'].mean()
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
    player_df['Shooting_Accuracy'] = np.where(player_df['Sh'] > 0, player_df['SoT'] / player_df['Sh'] * 100, 0)
    average_shooting_accuracy = player_df['Shooting_Accuracy'].mean()
    st.write('# Shooting Accuracy')
    st.write(f"### Total Shots: {total_shots}")
    st.write(f"### Total Shots on Target: {total_shots_target}")
    st.write(f"### Shooting Accuracy: {average_shooting_accuracy:.2f}%")

    # Expected Goals vs Actual Goals Plot
    st.write("# Expected Goals vs Actual Goals Over Time")
    plt.figure(figsize=(10, 5))
    plt.plot(player_df['Date'], player_df['xG'], label='Expected Goals (xG)', marker='o')
    plt.plot(player_df['Date'], player_df['Gls'], label='Actual Goals', marker='x')
    plt.xlabel('Date')
    plt.ylabel('Goals')
    plt.title('Expected Goals vs Actual Goals')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

    # Goals by Opponent
    st.write("## Goals Scored Against Opponents")
    goals_by_opponent = player_df.groupby('Opponent')['Gls'].sum().reset_index()
    plt.figure(figsize=(12, 6))
    plt.bar(goals_by_opponent['Opponent'], goals_by_opponent['Gls'], color='skyblue')
    plt.xlabel('Opponent')
    plt.ylabel('Total Goals')
    plt.title('Total Goals Scored Against Each Opponent')
    plt.xticks(rotation=45, ha='right')
    plt.gca().tick_params(axis='x', pad=5)
    plt.tight_layout()
    st.pyplot(plt)

    # Download button for the CSV file
    csv = player_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{selected_player}_data_{selected_year}.csv",
        mime='text/csv',
        key='download-csv'
    )
else:
    st.write("Please select a player to view their data.")
