import requests
from bs4 import BeautifulSoup


def get_wikipedia_current_events(date_str):
    """
    Fetches and parses the Wikipedia Current Events portal for a specific date to extract the list of events.

    Args:
        date_str: A string representing the date in the format 'YYYY_MM_DD'.
    Returns:
        A list of events for the specified date.
    """
    # Construct the URL
    url = f"https://en.wikipedia.org/wiki/Portal:Current_events/{date_str}"

    # Fetch the HTML content
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to retrieve data from Wikipedia."

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    events_div = soup.find("div", {"id": f"{date_str.replace('_', ' ')}"})

    if not events_div:
        return "No events found for this date."

    # Extract the events
    events = []
    for heading in events_div.find_all("p", recursive=False):
        category = heading.get_text().strip()
        for event in heading.find_next_sibling("ul").find_all("li", recursive=False):
            event_text = event.get_text().strip()
            events.append(f"{category}: {event_text}")

    return events


# Example usage
date_str = "2024_January_9"  # Format: YYYY_MonthName_DD
events = get_wikipedia_current_events(date_str)
print(events)
