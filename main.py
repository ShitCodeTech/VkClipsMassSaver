import requests
import json


def fetch_video_formats(link):
    """
    Fetches available video formats for the given link.
    """
    headers = {
        'accept': 'application/json',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://ru.get-save.com',
        'priority': 'u=1, i',
        'referer': 'https://ru.get-save.com/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    payload = {'url': link}

    try:
        response = requests.post('https://api.get-save.com/api/v1/vidinfo', headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching video formats: {e}")
        return None


def display_and_choose_format(formats):
    """
    Displays available formats and lets the user choose one.
    """
    idx = 0
    resolution_urls = []
    print("Available video formats:")

    for smth, item in enumerate(formats.get("sizes", [])):
        if item.get("ext") == "mp4" and item.get("protocol") == "https" and item.get('acodec') != 'none':
            print(f'{idx}) Height: {item.get("height")}p')
            resolution_urls.append(item.get("url"))
            idx += 1

    if not resolution_urls:
        print("No suitable formats found.")
        return None

    while True:
        try:
            choice = int(input("Choose a resolution by entering its number: "))
            if 0 <= choice < len(resolution_urls):
                return resolution_urls[choice]
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def download_video(video_url, link):
    """
    Downloads the video from the given URL and saves it locally.
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    })

    file_name = f"{link.split('/')[3][:-4]}.m4a"
    successful_downloads = 0
    failed_downloads = 0

    try:
        response = session.get(video_url, stream=True)
        if response.status_code == 200:
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            successful_downloads += 1
        else:
            failed_downloads += 1
    except requests.RequestException as e:
        print(f"Error downloading video: {e}")
        failed_downloads += 1

    print(f"Successfully saved: {successful_downloads}, Failed downloads: {failed_downloads}")


def main():
    link = input("Enter the video link:\n")
    formats = fetch_video_formats(link)

    if not formats:
        print("Failed to retrieve video formats. Exiting.")
        return

    video_url = display_and_choose_format(formats)
    if video_url:
        download_video(video_url, link)


if __name__ == "__main__":
    main()