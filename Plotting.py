import pandas as pd
import psycopg2
import urllib.parse as up
import plotnine as p9
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import ggplot, aes, geom_bar, theme, element_text, labs


class Plotting:

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def display_menu(self):
        print("Available plot options:")
        print("1. Violin Plot")
        print("2. Histogram")
        print("3. Correlation Heatmap")
        print("4. Choropleth Map")
        print("5. Line Plot")

    def select_plot(self):
        self.display_menu()
        choice = input("Enter the number of the plot you want to create: ")
        if choice == '1':
            self.violinplot_menu()
        elif choice == '2':
            self.histogram()
        elif choice == '3':
            self.heatmap_menu()
        elif choice == '4':
            self.plot_choropleth()
        elif choice == '5':
            self.plot_line_menu()
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

    def violinplot_menu(self):
        columns = input("Enter the columns to plot (comma-separated, no space): ").split(",")
        title = input("Enter the title for the plot: ")
        xlabel = input("Enter the xlabel for the plot: ")
        ylabel = input("Enter the ylabel for the plot: ")
        self.violinplot(columns, title=title, xlabel=xlabel, ylabel=ylabel)

    def violinplot(self, columns, title="", xlabel="", ylabel=""):
        plt.figure(figsize=(12, 8))
        sns.violinplot(data=self.dataframe[columns], inner='quartile', palette='muted')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.show()

    def histogram(self):
        numeric_cols = self.dataframe.select_dtypes(include=['number']).columns
        num_cols = len(numeric_cols)
        num_rows = (num_cols + 1) // 2  # Ensures at least 2 rows

        # Create subplots
        fig, axes = plt.subplots(num_rows, 3, figsize=(12, 6 * num_rows))
        axes = axes.flatten()

        # Plot histograms for numeric columns
        for i, col in enumerate(numeric_cols):
            ax = axes[i]
            ax.hist(self.dataframe[col], bins=30, color='skyblue', edgecolor='black')
            ax.set_title(f'Distribution of {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequency')
            ax.grid(True)

        # Remove unused subplots
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()
        plt.show()

    def heatmap_menu(self):
        question = int(input("Do you want the corr of all or of specific columns? [1 = All, 2 = Specific]"))
        if question == 1:
            column_df = self.df.select_dtypes(include =['number', 'float', 'integer'])
            correlation_matrix = column_df.corr()
        elif question == 2:
            column_list = input("Enter the columns for correlation of interest (comma-separated, no space): ").split(",")
            column_df = self.df[column_list]
            correlation_matrix = column_df.corr()
        else:
            print("invalid input. Try again")
        self.heatmap(correlation_matrix)

    def heatmap(self, correlation_matrix):
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, vmin=-1, vmax=1)
        plt.title("Correlation Heatmap")
        plt.show()

    def plot_choropleth(self):
        fig = px.choropleth(self.dataframe,
                            locations='country',
                            locationmode='country names',
                            color='count',
                            color_continuous_scale='Viridis',
                            range_color=(0, self.dataframe['count'].max()),
                            title="Artist Heritage",
                            hover_name='country',
                            hover_data='count',
                            labels={'country': 'count'})
        fig.update_geos(projection_type="orthographic", showcoastlines=True, coastlinecolor='Black',
                        showland=True, landcolor='LightGreen', showocean=True)
        fig.show()

    def plot_line_menu(self):
        x = input("Enter the name of the column for x-axis: ")
        y = input("Enter the name of the column for y-axis: ")
        title = input("Enter the title for the plot: ")
        xlabel = input("Enter the xlabel for the plot: ")
        ylabel = input("Enter the ylabel for the plot: ")
        self.plot_line(x, y, title=title, xlabel=xlabel, ylabel=ylabel)

    def plot_line(self, x, y, title="", xlabel="", ylabel=""):
        plt.figure(figsize=(10, 6))
        plt.plot(self.dataframe[x], self.dataframe[y])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()