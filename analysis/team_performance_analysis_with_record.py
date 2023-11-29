import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_data():
    standings_path = '../team_data/raw_data/league_standings/nfl_standings_2023.csv'
    offense_path = '../team_data/preprocessed_data/offense_preprocessed.csv'
    defense_path = '../team_data/preprocessed_data/defense_preprocessed.csv'
    special_teams_path = '../team_data/preprocessed_data/special-teams_preprocessed.csv'

    standings_df = pd.read_csv(standings_path)
    offense_df = pd.read_csv(offense_path)
    defense_df = pd.read_csv(defense_path)
    special_teams_df = pd.read_csv(special_teams_path)

    # Rename 'NFL Team' to 'team_name' in standings_df
    standings_df.rename(columns={'NFL Team': 'team_name'}, inplace=True)

    # Strip and transform team names to ensure consistency
    standings_df['team_name'] = standings_df['team_name'].str.replace(r'[^a-zA-Z ]', '').str.strip()
    offense_df['team_name'] = offense_df['team_name'].str.strip()
    defense_df['team_name'] = defense_df['team_name'].str.strip()
    special_teams_df['team_name'] = special_teams_df['team_name'].str.strip()

    return standings_df, offense_df, defense_df, special_teams_df

def merge_data(standings_df, offense_df, defense_df, special_teams_df):
    # Merge the datasets
    combined_df = standings_df
    combined_df = combined_df.merge(offense_df, on='team_name', how='inner')
    combined_df = combined_df.merge(defense_df, on='team_name', how='inner', suffixes=('_off', '_def'))
    combined_df = combined_df.merge(special_teams_df, on='team_name', how='inner')

    return combined_df

def analyze_and_visualize(combined_df):
    # Filter for column names that might be the passing yards from offense data
    potential_columns = [col for col in combined_df.columns if "Pass" in col and "Yds" in col]
    print("Potential Passing Yards Columns:")
    print(potential_columns)

    # You'll need to manually select the correct column from these printed options
    correct_pass_yds_column = 'Pass Yds_x'  # Replace with the actual column name after checking the output

    # Visualization code
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=combined_df, x=correct_pass_yds_column, y='W')
    plt.title(f'Wins vs {correct_pass_yds_column}')
    plt.xlabel(correct_pass_yds_column)
    plt.ylabel('Wins')
    plt.show()
def main():
    standings_df, offense_df, defense_df, special_teams_df = load_data()
    combined_df = merge_data(standings_df, offense_df, defense_df, special_teams_df)
    analyze_and_visualize(combined_df)

if __name__ == '__main__':
    main()
