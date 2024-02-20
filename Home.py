
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
            try:
                title = driver.find_element(By.CSS_SELECTOR, '.story-info-right h1').text
            except NoSuchElementException:
                title = 'N/A'
            try:
                genres = [genre.text for genre in driver.find_elements(By.CSS_SELECTOR, '.story-info-right .variations-tableInfo tr:nth-child(4) .table-value a')]
            except NoSuchElementException:
                genres = []
            try:
                updated = driver.find_element(By.CSS_SELECTOR, '.story-info-right-extent p:nth-child(1) .stre-value').text
            except NoSuchElementException:
                updated = 'N/A'
            try:
                view = driver.find_element(By.CSS_SELECTOR, '.story-info-right-extent p:nth-child(2) .stre-value').text
                view = convert_view(view)
            except NoSuchElementException:
                view = 'N/A'

            data.append([title, ', '.join(genres), updated, view])

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
        writer.writerow(['Title', 'Genres', 'Updated', 'Views'])
        for item in data:
            writer.writerow(item)

def convert_view(view):
    if view.endswith('M'):
        return float(view[:-1]) * 1000000
    elif view.endswith('K'):
        return float(view[:-1]) * 1000
    else:
        return view

@st.cache_data()
def load_data():
    return pd.read_csv('manga_info.csv')

if __name__ == "__main__":
    st.title("Manga Scraper")
    st.sidebar.title("Settings")
    num_pages = st.sidebar.slider("Number of Pages to Scrape", 1, 10, 1)
    st.sidebar.text("You selected: " + str(num_pages))
    if st.sidebar.button("Scrape"):
        main(num_pages)
        st.success("Scraping complete! Check manga_info.csv for the data.")

    df = load_data()

    # Split genres into individual columns
    genres_list = [
        'Action', 'Romance', 'Sci fi', 'Shounen',
        'Comedy', 'Horror', 'Mystery', 'Seinen',
        'Adventure', 'Drama', 'Fantasy', 'Slice of life', 'Manhwa',
        'Martial arts', 'Sports', 'Supernatural', 'Harem', 'Isekai',
        'School life', 'Shounen ai', 'Webtoons', 'Yaoi', 'Smut', 'Mature'
    ]
    for genre in genres_list:
        df[genre] = df['Genres'].apply(lambda x: 1 if isinstance(x, str) and genre in x else 0)

    # Display the main table
    st.write("## Manga Data")
    st.write(df)

    # Perform EDA and display plots
    st.write("## Exploratory Data Analysis")

    # Plot genre counts
    genre_counts = df[genres_list].sum().sort_values(ascending=False)
    fig = px.bar(x=genre_counts.index, y=genre_counts.values, title='Genre Counts')
    fig.update_layout(xaxis_title='Genre', yaxis_title='Count', xaxis_tickangle=-45)
    st.plotly_chart(fig)

    # Plot genre counts
    genre_counts = df[genres_list].sum().sort_values(ascending=False)
    fig = px.pie(values=genre_counts.values, names=genre_counts.index, title='Genre Counts')
    st.plotly_chart(fig)


    # Plot Views Distribution
    fig = px.scatter(df, x='Title', y='View', title='Views Distribution')
    fig.update_layout(xaxis_title='Title', yaxis_title='Views')
    st.plotly_chart(fig)