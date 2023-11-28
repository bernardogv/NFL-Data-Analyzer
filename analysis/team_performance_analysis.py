import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def compare_teams(data, team1, team2, stat_type):
    team1_data = data[data['team_name'] == team1]
    team2_data = data[data['team_name'] == team2]

    if team1_data.empty or team2_data.empty:
        print(f"One or both teams not found: {team1}, {team2}")
        return

    # Dropping non-numeric columns for comparison
    team1_data = team1_data.select_dtypes(include=['float64', 'int64'])
    team2_data = team2_data.select_dtypes(include=['float64', 'int64'])

    team1_better_count = 0
    team2_better_count = 0

    print(f"--- {stat_type} Stats Comparison ---")
    for stat in team1_data.columns:
        team1_stat = team1_data[stat].values[0]
        team2_stat = team2_data[stat].values[0]
        if team1_stat > team2_stat:
            winner = team1
            team1_better_count += 1
        else:
            winner = team2
            team2_better_count += 1
        print(f"{stat}: {team1} ({team1_stat}) vs {team2} ({team2_stat}) - Higher: {winner}")

    overall_winner = team1 if team1_better_count > team2_better_count else team2
    print(f"\nOverall {stat_type} Winner: {overall_winner} ({team1_better_count} vs {team2_better_count})\n")

def main():
    # Specify the two teams to compare
    team1 = 'Seahawks'  # Replace with actual team name
    team2 = 'Cowboys'

    # Load and compare offense data
    offense_data = load_data('../team_data/preprocessed_data/offense_preprocessed.csv')
    compare_teams(offense_data, team1, team2, "Offense")

    # Load and compare defense data
    defense_data = load_data('../team_data/preprocessed_data/defense_preprocessed.csv')
    compare_teams(defense_data, team1, team2, "Defense")

    # Load and compare special teams data
    special_teams_data = load_data('../team_data/preprocessed_data/special-teams_preprocessed.csv')
    compare_teams(special_teams_data, team1, team2, "Special Teams")

if __name__ == '__main__':
    main()
