import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import seaborn as sns
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re

# Function to open the dataset
def open_file(file_path):
    df = pd.read_csv(file_path)
    return df

# Function to get all relevant columns for a given year
def get_columns_for_year(df, year):
    # Use regex to find relevant columns for each year based on known patterns
    columns = {
        'HDI ': [col for col in df.columns if re.match(f"Human Development Index \({year}\)", col)],
        'Life Expectancy': [col for col in df.columns if re.match(f"Life Expectancy at Birth \({year}\)", col)],
        'Expected Schooling': [col for col in df.columns if re.match(f"Expected Years of Schooling \({year}\)", col)],
        'Mean Schooling': [col for col in df.columns if re.match(f"Mean Years of Schooling \({year}\)", col)],
        'GNI': [col for col in df.columns if re.match(f"Gross National Income Per Capita \({year}\)", col)],
        'GDI': [col for col in df.columns if re.match(f"Gender Development Index \({year}\)", col)],
        'HDI female ': [col for col in df.columns if re.match(f"HDI female \({year}\)", col)],
        'Life Expectancy Female': [col for col in df.columns if re.match(f"Gross Life Expectancy at Birth, female \({year}\)", col)],
        'Expected Schooling Female ': [col for col in df.columns if re.match(f"Expected Years of Schooling, female \({year}\)", col)],
        'Mean Schooling Female': [col for col in df.columns if re.match(f"Mean Years of Schooling, female \({year}\)", col)],
        'GNI Female': [col for col in df.columns if re.match(f"Gross National Income Per Capita, female \({year}\)", col)],
        'HDI male ': [col for col in df.columns if re.match(f"HDI male \({year}\)", col)],
        'Life Expectancy Male': [col for col in df.columns if re.match(f"Gross Life Expectancy at Birth, male \({year}\)", col)],
        'Expected Schooling Male ': [col for col in df.columns if re.match(f"Expected Years of Schooling, male \({year}\)", col)],
        'Mean Schooling Male': [col for col in df.columns if re.match(f"Mean Years of Schooling, male \({year}\)", col)],
        'GNI Male': [col for col in df.columns if re.match(f"Gross National Income Per Capita, male \({year}\)", col)],
        'HDI Adjusted': [col for col in df.columns if re.match(f"Inequality-adjusted Human Development Index \({year}\)", col)],
        'Inequality': [col for col in df.columns if re.match(f"Coefficient of human inequality \({year}\)", col)],
        'Loss': [col for col in df.columns if re.match(f"Overall loss \(\%\)  \({year}\)", col)],
        'GNI': [col for col in df.columns if re.match(f"Gross National Income Per Capita \({year}\)", col)],
        'GNI': [col for col in df.columns if re.match(f"Gross National Income Per Capita \({year}\)", col)],
        'GNI': [col for col in df.columns if re.match(f"Gross National Income Per Capita \({year}\)", col)],
        # Add more categories if needed (like GDI, HDI, etc.)
    }
    return columns

# Function to plot any two variables (X and Y) for the selected year
def plot_generic(df, x_col, y_col, ax, xlim, ylim, annotations):
    # Check if the columns exist in the dataset
    if x_col not in df.columns or y_col not in df.columns:
        print(f"Data for {x_col} or {y_col} is not available.")
        return

    # Filter the dataset for valid data points (non-null values for the selected columns)
    valid_data = df.dropna(subset=[x_col, y_col])

    # Clear the current plot and re-plot for the new data
    ax.clear()

    # Create a scatter plot with regression line
    sns.regplot(x=x_col, y=y_col, data=valid_data, 
                scatter_kws={'alpha': 0.8, 's': 40},
                line_kws={'linewidth': 2}, ci=None, ax=ax)

    # Title and labels
    ax.set_title(f'{y_col} vs {x_col}', fontsize=18)
    ax.set_xlabel(x_col, fontsize=14)
    ax.set_ylabel(y_col, fontsize=14)
    
    # Set the axis limits to be constant across all years
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    # Redraw the plot with the updated year
    plt.draw()

# Function to initialize the plot with an interactive slider and dynamic dropdowns
def interactive_plot(df):
    # Set a predefined style
    plt.style.use('seaborn-v0_8-pastel')  # You can choose any style like 'ggplot', 'seaborn-v0_8-pastel', etc.

    # Create the figure and axis for the plot
    fig, ax = plt.subplots(figsize=(12, 8))

    # Tkinter UI setup for the main window
    root = tk.Tk()
    root.title("Interactive Plot with Variable Selection")

    style = ttk.Style(root)
    style.theme_use('alt')

    # Canvas to display the matplotlib plot inside the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)  
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Create a frame for the controls (dropdowns and slider)
    controls_frame = tk.Frame(root)
    controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # Create the slider widget for year selection
    year_slider_widget = tk.Scale(controls_frame, from_=1990, to_=2021, orient=tk.HORIZONTAL)
    year_slider_widget.set(2020)
    year_slider_widget.pack(side=tk.LEFT)

    # Dropdown for selecting X and Y variables
    def update_dropdowns(year):
        columns = get_columns_for_year(df, year)
        available_columns = []
        for category in columns.values():
            available_columns.extend(category)

        # Update X-axis dropdown values, if it's the first initialization
        if not x_dropdown['values']:
            x_dropdown.set('')
        else:
            x_dropdown.set(re.sub(r'\(\d{4}\)', "(" + str(year) + ")", x_dropdown.get()))
        x_dropdown['values'] = available_columns

        # Update Y-axis dropdown values, if it's the first initialization
        if not y_dropdown['values']:
            y_dropdown.set('')
        else:
            y_dropdown.set(re.sub(r'\(\d{4}\)', "(" + str(year) + ")", y_dropdown.get()))
        y_dropdown['values'] = available_columns
    # Function to handle dropdown selection and update the plot
    def update_plot():
        year = year_slider_widget.get()
        x_col = x_dropdown.get()
        y_col = y_dropdown.get()

        x_maxes = []
        x_mins = []
        y_maxes = []
        y_mins = []
        for year_col in range(1990, 2022):
            x_maxes.append(df[re.sub(r'\(\d{4}\)', "(" + str(year_col) + ")", x_col)].max())
            y_maxes.append(df[re.sub(r'\(\d{4}\)', "(" + str(year_col) + ")", y_col)].max())
            x_mins.append(df[re.sub(r'\(\d{4}\)', "(" + str(year_col) + ")", x_col)].min())
            y_mins.append(df[re.sub(r'\(\d{4}\)', "(" + str(year_col) + ")", y_col)].min())

        # Dynamically set xlim and ylim based on the data for the selected year
        x_data = df[x_col].dropna()
        y_data = df[y_col].dropna()

        # Adding leeway (e.g., 10%) to the axis limits
        x_margin = 0.01 * (max(x_maxes) - min(x_mins))  # 10% margin
        y_margin = 0.01 * (max(y_maxes) - min(y_mins))  # 10% margin

        # Calculate new limits with leeway
        xlim = (min(x_mins) - x_margin, max(x_maxes) + x_margin)
        ylim = (min(y_mins) - y_margin, max(y_maxes) + y_margin)

        # Plot the selected data
        plot_generic(df, x_col, y_col, ax, xlim, ylim, [])
        canvas.draw()

    # Create X and Y dropdown menus
    x_label = tk.Label(controls_frame, text="Select X-axis Variable:")
    x_label.pack(side=tk.LEFT)

    x_dropdown = ttk.Combobox(controls_frame)
    x_dropdown.pack(side=tk.LEFT)

    y_label = tk.Label(controls_frame, text="Select Y-axis Variable:")
    y_label.pack(side=tk.LEFT)

    y_dropdown = ttk.Combobox(controls_frame)
    y_dropdown.pack(side=tk.LEFT)

    # Create the update button
    update_button = tk.Button(controls_frame, text="Update Plot", command=update_plot)
    update_button.pack(side=tk.LEFT)

    # Update dropdowns when year slider is moved
    def update_slider(val):
        update_dropdowns(int(val))

        # Get the selected values for X and Y, and update the plot accordingly
        update_plot()

    # Connect the year slider to update function
    year_slider_widget.config(command=update_slider)
    
    # Initial plot setup for year 2020
    update_dropdowns(2020)
    plot_generic(df, 'Expected Years of Schooling (2020)', 'Life Expectancy at Birth (2020)', ax, (0, 20), (40, 90), [])

    # Mainloop to start the Tkinter application
    root.mainloop()


# Load the data and create the interactive plot
print("loading database")
df = open_file('data.csv')  # Replace with the path to your data file
interactive_plot(df)
