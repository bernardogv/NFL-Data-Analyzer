import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    offense = pd.read_csv('../team_data/preprocessed_data/offense_preprocessed.csv')
    defense = pd.read_csv('../team_data/preprocessed_data/defense_preprocessed.csv')
    special_teams = pd.read_csv('../team_data/preprocessed_data/special-teams_preprocessed.csv')
    combined_data = offense.merge(defense, on='team_name').merge(special_teams, on='team_name')
    return combined_data

def perform_eda(data):
    # Perform exploratory data analysis here
    # Display descriptive statistics
    print(data.describe())

    # Correlation heatmap - including only numeric columns
    numeric_data = data.select_dtypes(include=[float, int])
    plt.figure(figsize=(10, 8))
    sns.heatmap(numeric_data.corr(), annot=True, fmt='.2f', cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.show()

    # Additional EDA code...


def main():
    data = load_data()
    perform_eda(data)

if __name__ == '__main__':
    main()
