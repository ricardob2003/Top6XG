from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import matplotlib.pyplot as plt
import pandas as pd

def extract_data(URL, TEAMS):
    # Setup headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    # Initialize the WebDriver with options
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Navigate to the webpage (replace URL_OF_THE_PAGE with the actual URL)
    driver.get("https://xgscore.io/xg-statistics/epl")
    # Define the TEAMS constant
    # Wait for the div that contains the table to be present
    wait = WebDriverWait(driver, 10)
    standings_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "xgs-xg-standings")))
    # Locate the table within the div
    xg_table = standings_div.find_element(By.TAG_NAME, "table")
    # Now, you can iterate over the rows of the table and extract the data
    rows = xg_table.find_elements(By.TAG_NAME, "tr")[1:]  # Skipping the header row
    team_data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if cols:
            # Use try-except to catch any potential errors if the structure is different
            try:
                team_name_column = cols[1].find_element(By.TAG_NAME, "span").text.strip()
                if team_name_column in TEAMS:
                    gs = cols[6].text.split('\n')[0].strip()  # Split string and keep only the main figure
                    xg = cols[7].text.split('\n')[0].strip()
                    pts = cols[10].text.split('\n')[0].strip()
                    xPTS = cols[-1].text.split('\n')[0].strip()

                    team_data.append({
                        "Team": team_name_column,
                        "xG": xg,
                        "gs": gs,
                        "xPTS": xPTS,
                        "pts": pts
                    })
            except Exception as e:
                print(f"An error occurred while processing the row: {e}")
    # Do not forget to quit the driver at the end of your script to free resources
    driver.quit()
    return team_data

def display_data(data, team_colors):
    # Extracting the team names and their respective data
    teams = [team['Team'] for team in data]
    xG = [float(team['xG']) for team in data]
    gs = [float(team['gs']) for team in data]
    pts = [float(team['pts']) for team in data]
    xPTS = [float(team['xPTS']) for team in data]

    # Creating a figure and axes for the bar charts
    fig, axs = plt.subplots(1, 4, figsize=(20, 5), gridspec_kw={'wspace': 0.75}) # Adjust 'wspace' for space between subplots
    fig.suptitle('Team Performance Metrics')
    colors = [team_colors[team] for team in teams]
    # Function to create bar charts
    def create_bar_chart(ax, data, title, teams, team_colors, bar_width=0.8):
        n_teams = len(teams)
        index = range(n_teams)
        colors = [team_colors[team] for team in teams]
        ax.bar(index, data, color=colors, width=bar_width)
        ax.set_xticks(index)
        ax.set_xticklabels(teams, rotation=45, ha='right')
        ax.set_title(title)

    # Plotting bar charts for each category

    create_bar_chart(axs[0], xG, 'Expected Goals (xG)', teams, team_colors)
    create_bar_chart(axs[1], gs, 'Goals Scored (GS)', teams, team_colors)
    create_bar_chart(axs[2], pts, 'Points (PTS)', teams, team_colors)
    create_bar_chart(axs[3], xPTS, 'Expected Points (xPTS)', teams, team_colors)

    # Manually adjust the first subplot to add left margin space
    pos1 = axs[0].get_position() # get the original position of the first subplot
    axs[0].set_position([pos1.x0 + 0.025, pos1.y0, pos1.width, pos1.height]) # Increase the x0 position
    # Show the plots
    plt.show()

def create_sorted_tables(data):
    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(data)

    # Convert numerical columns to float to ensure proper sorting
    numeric_cols = ['xG', 'gs', 'pts', 'xPTS']
    df[numeric_cols] = df[numeric_cols].astype(float)

    # Create separate DataFrames for each sorting metric
    df_sorted_by_points = df[['Team', 'pts']].sort_values('pts', ascending=False)
    df_sorted_by_xpoints = df[['Team', 'xPTS']].sort_values('xPTS', ascending=False)
    df_sorted_by_goals = df[['Team', 'gs']].sort_values('gs', ascending=False)
    df_sorted_by_xgoals = df[['Team', 'xG']].sort_values('xG', ascending=False)

    # Set the index to start from 1 instead of 0 for all the tables
    df_sorted_by_points.index = range(1, len(df_sorted_by_points) + 1)
    df_sorted_by_xpoints.index = range(1, len(df_sorted_by_xpoints) + 1)
    df_sorted_by_goals.index = range(1, len(df_sorted_by_goals) + 1)
    df_sorted_by_xgoals.index = range(1, len(df_sorted_by_xgoals) + 1)

    # Print the tables
    print("Teams sorted by Points:")
    print(df_sorted_by_points)
    print("\nTeams sorted by Expected Points:")
    print(df_sorted_by_xpoints)
    print("\nTeams sorted by Goals Scored:")
    print(df_sorted_by_goals)
    print("\nTeams sorted by Expected Goals:")
    print(df_sorted_by_xgoals)

    # Return the sorted DataFrames if you need to use them later
    return df_sorted_by_points, df_sorted_by_xpoints, df_sorted_by_goals, df_sorted_by_xgoals


# The TEAMS constant is defined outside the function
TEAMS = ["Chelsea", "Man City", "Arsenal", "Man United", "Liverpool", "Tottenham"]
TEAM_COLORS = {
    'Chelsea': 'blue',
    'Man City': 'lightblue',
    'Liverpool': 'red',
    'Man United': 'darkred',
    'Tottenham': 'grey',  # Using grey because white won't show on a white background
    'Arsenal': 'black'
}
# Example usage:
URL = "https://xgscore.io/xg-statistics/epl" # Replace with the actual URL
data = extract_data(URL, TEAMS)
display_data(data, TEAM_COLORS)
sorted_tables = create_sorted_tables(data)