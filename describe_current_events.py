import wikipediaapi
import datetime

# Create a Wikipedia object
wikipedia = wikipediaapi.Wikipedia(
    language="en", user_agent="MyCustomUserAgent/1.0 (myemail@example.com)"
)


# Function to get Wikipedia page for a specific day
def get_wikipedia_page_for_day(month, day):
    page_title = f"{month} {day}"
    page = wikipedia.page(page_title)
    return page.text if page.exists() else "Page not found"


# Specify the date you're interested in
date_of_interest = (
    datetime.date.today()
)  # or use a specific date like datetime.date(2024, 1, 8)
month = date_of_interest.strftime("%B")
day = date_of_interest.day

# Get the article
article_text = get_wikipedia_page_for_day(month, day)

# Save the article to a file
with open(f"Wikipedia_Article_{month}_{day}.txt", "w", encoding="utf-8") as file:
    file.write(article_text)
