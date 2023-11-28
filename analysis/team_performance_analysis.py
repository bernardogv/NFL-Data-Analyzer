import pandas as pd
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

def load_data():
    return pd.read_csv('../team_data/preprocessed_data/offense_preprocessed.csv')

def standardize_stats(data):
    scaler = StandardScaler()
    numeric_data = data.select_dtypes(include=['float64', 'int64'])
    data[numeric_data.columns] = scaler.fit_transform(numeric_data)
    return data

def plot_comparison(data):
    plt.figure(figsize=(12, 10))
    sns.heatmap(data.set_index('team_name').T, annot=True, cmap='coolwarm')
    plt.title('Standardized Offensive Stats Comparison')
    plt.show()

def main():
    offense_data = load_data()
    offense_data = standardize_stats(offense_data)
    plot_comparison(offense_data)

if __name__ == '__main__':
    main()
