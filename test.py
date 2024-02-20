# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px

# # # Load the data
# # @st.cache_data()
# # def load_data():
# #     return pd.read_csv('manga_info.csv')

# # df = load_data()

# # # Display the main table
# # st.write("## Manga Data")
# # st.write(df)

# # # Perform EDA and display plots
# # st.write("## Exploratory Data Analysis")

# # # Plot 1: Top 10 Genres
# # fig = px.bar(df['Genres'].value_counts().head(10), x='Genres', y='Genres', title='Top 10 Genres')
# # st.plotly_chart(fig)

# # # Plot 2: Status Distribution
# # fig = px.pie(df, names='Status', title='Status Distribution')
# # st.plotly_chart(fig)

# # # Plot 3: Rating Distribution
# # fig = px.histogram(df, x='Rating', title='Rating Distribution')
# # st.plotly_chart(fig)

# # # Plot 4: Updated Distribution
# # fig = px.histogram(df, x='Updated', title='Updated Distribution')
# # st.plotly_chart(fig)

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException
# import csv

# def main(num_pages):
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     base_url = 'https://manganato.com/genre-all/'
#     driver.get(base_url + '1')
#     # Wait for the page to load
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, '.panel-content-genres .content-genres-item'))
#     )

#     current_page = 1
#     data = []
#     visited_urls = set()

#     while current_page <= num_pages:
#         manga_urls = []

#         # Get the URLs of all manga items
#         elements = driver.find_elements(By.CSS_SELECTOR, '.panel-content-genres .content-genres-item .genres-item-img.bookmark_check')
#         for element in elements:
#             manga_url = element.get_attribute('href')
#             if manga_url not in visited_urls:
#                 manga_urls.append(manga_url)
#                 visited_urls.add(manga_url)

#         for manga_url in manga_urls:
#             driver.get(manga_url)
#             # No need to wait for the page to load explicitly
#             # Extract information and save to data list
#             title = driver.find_element(By.CSS_SELECTOR, '.story-info-right h1').text
#             alternative = driver.find_element(By.CSS_SELECTOR, '.story-info-right .variations-tableInfo tr:nth-child(1) .table-value').text
#             status = driver.find_element(By.CSS_SELECTOR, '.story-info-right .variations-tableInfo tr:nth-child(3) .table-value').text
#             genres = [genre.text for genre in driver.find_elements(By.CSS_SELECTOR, '.story-info-right .variations-tableInfo tr:nth-child(4) .table-value a')]
#             updated = driver.find_element(By.CSS_SELECTOR, '.story-info-right-extent p:nth-child(1) .stre-value').text
#             view = driver.find_element(By.CSS_SELECTOR, '.story-info-right-extent p:nth-child(2) .stre-value').text
#             try:
#                 author = driver.find_element(By.CSS_SELECTOR, '.story-info-right .variations-tableInfo tr:nth-child(2) .table-value a').text
#             except NoSuchElementException:
#                 author = 'N/A'

#             rating = driver.find_element(By.CSS_SELECTOR, '.story-info-right-extent p:nth-child(3) .stre-value em').text

#             data.append([title, alternative, author, status, ', '.join(genres), updated, view, rating])

#             # Go back to the previous page
#             driver.back()

#         try:
#             current_page += 1
#             driver.get(base_url + str(current_page))
#             # Wait for the page to load, adjust the wait time as needed
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, 'group-page'))
#             )
#         except:
#             break

#     driver.quit()
#     save_to_csv(data)

# def save_to_csv(data):
#     with open('manga_info.csv', 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Title', 'Alternative', 'Author(s)', 'Status', 'Genres', 'Updated', 'View', 'Rating'])
#         for item in data:
#             writer.writerow(item)

# # Streamlit App
# st.title("Manga Scraper")
# st.sidebar.title("Settings")
# num_pages = st.sidebar.slider("Number of Pages to Scrape", 1, 10, 1)
# st.sidebar.text("You selected: " + str(num_pages))
# if st.sidebar.button("Scrape"):
#     main(num_pages)
#     st.success("Scraping complete! Check manga_info.csv for the data.")

# # Load the data
# @st.cache_data()
# def load_data():
#     return pd.read_csv('manga_info.csv')

# if st.sidebar.checkbox("Show Data Table"):
#     df = load_data()
#     st.write("## Manga Data")
#     st.write(df)

#     # Perform EDA and display plots
#     st.write("## Exploratory Data Analysis")

#     # Plot 1: Top 10 Genres
#     fig = px.bar(df['Genres'].value_counts().head(10), x='Genres', y='Genres', title='Top 10 Genres')
#     st.plotly_chart(fig)

#     # Plot 2: Status Distribution
#     fig = px.pie(df, names='Status', title='Status Distribution')
#     st.plotly_chart(fig)

#     # Plot 3: Rating Distribution
#     fig = px.histogram(df, x='Rating', title='Rating Distribution')
#     st.plotly_chart(fig)

#     # Plot 4: Updated Distribution
#     fig = px.histogram(df, x='Updated', title='Updated Distribution')
#     st.plotly_chart(fig)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import csv
import streamlit as st
import pandas as pd
import plotly.express as px

def main(num_pages):
    driver = webdriver.Chrome()
    driver.maximize_window()
    base_url = 'https://manganato.com/genre-all/'
    driver.get(base_url + '1')
    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.panel-content-genres .content-genres-item'))
    )

    current_page = 1
    data = []
    visited_urls = set()

    while current_page <= num_pages:
        manga_urls = []

        # Get the URLs of all manga items
        elements = driver.find_elements(By.CSS_SELECTOR, '.panel-content-genres .content-genres-item .genres-item-img.bookmark_check')
        for element in elements:
            manga_url = element.get_attribute('href')
            if manga_url not in visited_urls:
                manga_urls.append(manga_url)
                visited_urls.add(manga_url)

        for manga_url in manga_urls:
            driver.get(manga_url)
            # No need to wait for the page to load explicitly
            # Extract information and save to data list
            title = driver.find_element(By.CSS_SELECTOR, '.story-info-right h1').text
            status = driver.find_element(By.CSS_SELECTOR, '.story-info-right .variations-tableInfo tr:nth-child(3) .table-value').text
            genres = [genre.text for genre in driver.find_elements(By.CSS_SELECTOR, '.story-info-right .variations-tableInfo tr:nth-child(4) .table-value a')]
            updated = driver.find_element(By.CSS_SELECTOR, '.story-info-right-extent p:nth-child(1) .stre-value').text
            view = driver.find_element(By.CSS_SELECTOR, '.story-info-right-extent p:nth-child(2) .stre-value').text

            rating = driver.find_element(By.CSS_SELECTOR, '.story-info-right-extent p:nth-child(3) .stre-value em').text

            data.append([title, status, ', '.join(genres), updated, view, rating])

            # Go back to the previous page
            driver.back()

        try:
            current_page += 1
            driver.get(base_url + str(current_page))
            # Wait for the page to load, adjust the wait time as needed
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'group-page'))
            )
        except:
            break

    driver.quit()
    save_to_csv(data)

def save_to_csv(data):
    with open('manga_info.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Status', 'Genres', 'Updated', 'View', 'Rating'])
        for item in data:
            writer.writerow(item)

# Load the data
@st.cache_data()
def load_data():
    return pd.read_csv('manga_info.csv')

def main_app():
    st.title("Manga Scraper")
    st.sidebar.title("Settings")
    num_pages = st.sidebar.slider("Number of Pages to Scrape", 1, 10, 1)
    st.sidebar.text("You selected: " + str(num_pages))
    if st.sidebar.button("Scrape"):
        main(num_pages)
        st.success("Scraping complete! Check manga_info.csv for the data.")

    df = load_data()

    # Display the main table
    st.write("## Manga Data")
    st.write(df)

    # Perform EDA and display plots
    st.write("## Exploratory Data Analysis")

    # Plot 1: Top 10 Genres
    fig = px.bar(df['Genres'].value_counts().head(10), x='Genres', y='Genres', title='Top 10 Genres')
    st.plotly_chart(fig)

    # Plot 2: Status Distribution
    fig = px.pie(df, names='Status', title='Status Distribution')
    st.plotly_chart(fig)

    # Plot 3: Rating Distribution
    fig = px.histogram(df, x='Rating', title='Rating Distribution')
    st.plotly_chart(fig)

    # Plot 4: Updated Distribution
    fig = px.histogram(df, x='Updated', title='Updated Distribution')
    st.plotly_chart(fig)

if __name__ == "__main__":
    main_app()
