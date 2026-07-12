import requests

HUB_ID = "5p6FS9av9zQagvbQECo51VQLz9c2"

def fetch_events():
    url = f"https://topdeck.gg/api/event-filter/{HUB_ID}"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://topdeck.gg",
        "Referer": f"https://topdeck.gg/hubs/{HUB_ID}",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(
        url,
        json={},
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    events = []

    for event in data.get("currEvents", []):
        events.append({
            "id": event["id"],
            "title": event["name"],
            "game": event["game"],
            "format": event["format"],
            "date": event["start"],
            "location": event.get("location") or "",
            "url": f"https://topdeck.gg/event/{event['id']}"
        })

    return events
