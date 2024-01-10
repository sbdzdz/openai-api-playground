import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser
from datetime import datetime


def get_wikipedia_current_events(date_str):
    """
    Fetch and parse the list of world events from Wikipedia for the specified date.

    Args:
        date_str: A string representing the date in the format 'YYYY_Month_D'.
    Returns:
        A list of events for the specified date.
    """
    # Construct the URL
    year, month, _ = date_str.split("_")
    url = (
        f"https://en.wikipedia.org/wiki/Portal:Current_events/{month}_{year}#{date_str}"
    )

    # Fetch the HTML content
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to retrieve data from Wikipedia."

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    events_div = soup.find("div", {"id": date_str})

    if not events_div:
        return "No events found for this date."

    ul_tags = events_div.find_all("ul")
    for ul_tag in ul_tags:
        li_tags = ul_tag.find_all("li", recursive=False)
        for li_tag in li_tags:
            process_li_tag(li_tag)


def process_li_tag(li_tag):
    """Output the text of the tag if it's a leaf node and contains more than a single link.
    Args:
        li_tag: A list item tag.
    Returns:
        None.
    """
    if li_tag.find("li"):
        return
    if len(li_tag.contents) == 1 and li_tag.find("a", recursive=False):
        return
    # Remove the reporting agency info
    for a_tag in li_tag.find_all("a", recursive=False):
        tag_class = a_tag.get("class", [])
        if "external" in tag_class and "text" in tag_class:
            a_tag.decompose()
    event_text = li_tag.get_text(separator=" ", strip=True)
    print(fix_formatting(event_text))


def fix_formatting(event_text):
    """Fix some formatting issues in the event text."""
    event_text = event_text.replace(" ,", ",")
    event_text = event_text.replace(" .", ".")
    event_text = event_text.replace(" :", ":")
    event_text = event_text.replace(" ;", ";")
    event_text = event_text.replace(" )", ")")
    event_text = event_text.replace("( ", "(")
    return event_text


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--date",
        help="Date in the format YYYY_Month_D",
        default=datetime.now().strftime("%Y_%B_%d"),
    )
    args = parser.parse_args()
    get_wikipedia_current_events(args.date)
