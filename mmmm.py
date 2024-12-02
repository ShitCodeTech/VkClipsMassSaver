import requests
import json

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


counter = 0
huyaunter = 0
with open('links.txt') as links:
    links = links.readlines()
    links = [link.strip() for link in links]
    print(links)
for link in links:
    json_data = {
        'url': link,
    }

    response = requests.post('https://api.get-save.com/api/v1/vidinfo', headers=headers, json=json_data)
    data = json.loads(response.content)
    latest_url = []
    for item in data["sizes"]:
        if item.get("resolution") == "audio only" and item.get("ext") == "m4a":
            latest_url.append(item["url"])  # Overwrites with the latest match
    main_url = str(latest_url[-1])        
    print(main_url)
    session = requests.Session()

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    })

    name = (link.split('/')[3])[:-4]
    response = session.get(main_url)
    if response.status_code == 200:
        counter +=1
        with open(f"{name}.m4a", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        huyaunter +=1

