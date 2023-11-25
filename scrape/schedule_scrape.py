import requests

# URL of the ESPN NFL schedule for a specific week and year
url = "https://www.espn.com/nfl/schedule/_/week/12/year/2023/seasontype/2"

# Set a User-Agent header to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

try:
    # Sending a GET request to the URL
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the HTML content from the response
        html_content = response.text

        # Save the HTML content to a file
        with open("espn_schedule.html", "w", encoding="utf-8") as file:
            file.write(html_content)

        print("HTML content saved to espn_schedule.html")
    else:
        print(f"Failed to access the website. Status code: {response.status_code}")
except requests.RequestException as e:
    # Handle any exceptions that occur during the request
    print(f"An error occurred: {e}")

