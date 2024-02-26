from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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



# The TEAMS constant is defined outside the function
TEAMS = ["Chelsea", "Man City", "Arsenal", "Man United", "Liverpool", "Tottenham"]

# Example usage:
URL = "https://xgscore.io/xg-statistics/epl" # Replace with the actual URL
data = extract_data(URL, TEAMS)
for team in data:
    print(team)


def display_data(data):