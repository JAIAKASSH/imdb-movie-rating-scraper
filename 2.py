import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# -------- SETTINGS ----------
HEADLESS_MODE = False   # True = no browser window
TOP_MOVIES = 25        # Number of movies to extract
OUTPUT_FILE = r"C:\Users\jaisa\OneDrive\Desktop\project\imdb_top_movies.csv"
# ----------------------------


def setup_driver():
    options = Options()
    if HEADLESS_MODE:
        options.add_argument("--headless")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def scrape_imdb():
    driver = setup_driver()

    print("🎬 Opening IMDb Top Rated Movies page...")
    driver.get("https://www.imdb.com/chart/top/")

    # Wait until movie list loads
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//ul[contains(@class,'ipc-metadata-list')]"))
    )

    movies = driver.find_elements(By.XPATH, "//li[contains(@class,'ipc-metadata-list-summary-item')]")[:TOP_MOVIES]

    data = []

    for movie in movies:
        try:
            title = movie.find_element(By.XPATH, ".//h3").text
            rating = movie.find_element(By.XPATH, ".//span[contains(@class,'ipc-rating-star')]").text
            year = movie.find_element(By.XPATH, ".//span[contains(@class,'cli-title-metadata-item')]").text

            data.append([title, year, rating])

        except Exception as e:
            print("Movie skipped:", e)

    driver.quit()

    df = pd.DataFrame(data, columns=["Title", "Year", "IMDb Rating"])
    return df


def save_to_csv(df):
    df.to_csv(OUTPUT_FILE, index=False)
    print("\n✅ Data successfully saved to:")
    print(os.path.abspath(OUTPUT_FILE))


if __name__ == "__main__":
    print("📊 Fetching IMDb Top Rated Movies...\n")

    df = scrape_imdb()

    if not df.empty:
        print(df.head())
        save_to_csv(df)
    else:
        print("⚠ No data extracted.")