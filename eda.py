import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def visualize_price_carat(df):
    """Plots the relationship between carat weight and price."""
    sns.relplot(x='Carat Weight', y='Price', data=df, hue='Report', kind='line', 
                palette=['#ffea04', '#fe3a9e'], col='Cut', col_wrap=3, height=4)
    plt.grid(alpha=0.5)
    plt.show()

if __name__ == "__main__":
    df = pd.read_excel("data.xlsx")
    visualize_price_carat(df)
