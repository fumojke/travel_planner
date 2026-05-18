import requests

ART_INSTITUTE_BASE_URL = "https://api.artic.edu/api/v1/artworks"

def check_place_exists(external_id: str) -> bool:
    """
    Makes a request to the Art Institute of Chicago API
    to check whether a painting/location with the given ID exists.
    """
    url = f"{ART_INSTITUTE_BASE_URL}/{external_id}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        return False
    except requests.RequestException:
        return False