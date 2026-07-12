
import json, os, re, requests
from bs4 import BeautifulSoup
from pathlib import Path

HUB_URL = "https://topdeck.gg/hubs/5p6FS9av9zQagvbQECo51VQLz9c2"
WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

state_file = Path("data/state.json")
state = json.loads(state_file.read_text())

html = requests.get(HUB_URL, timeout=30).text

# Generic extraction; may need adjustment if TopDeck changes markup.
matches = sorted(set(re.findall(r'/event/([A-Za-z0-9_-]+)', html)))
new_events = [m for m in matches if m not in state["seen_events"]]

for event_id in new_events:
    if WEBHOOK:
        requests.post(
            WEBHOOK,
            json={
                "embeds": [{
                    "title": "New TopDeck Event Detected",
                    "description": f"https://topdeck.gg/event/{event_id}"
                }]
            },
            timeout=30
        )

state["seen_events"] = sorted(set(state["seen_events"] + matches))
state_file.write_text(json.dumps(state, indent=2))
print(f"Found {len(new_events)} new events")
