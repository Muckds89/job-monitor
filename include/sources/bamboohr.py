from urllib.parse import urlparse, urlunparse
import posixpath
def parse(response, source):
    """
    response: the object returned by requests.get(url) for this source
    source:   the configuration dictionary for this company

    Returns: a list of dictionaries in the normalized format,
             i.e., id, title, url, location.

    
    Qui dentro decidi tu:
      - dove sta la lista nella risposta, e cosa fai se non c'e'
      - come si chiamano i campi in questa sorgente
      - come costruisci l'url se la sorgente non te lo da'
      - come appiattisci la sede quando e' annidata o sporca
    """
    data = response.json()
    if "result" not in data:
        raise Exception(f"Unexpected response from API: {data}")
    fetched_result = data.get("result", [])
    # normalize the data into a list of dictionaries with the required fields
    cleaned_data = []
    for result in fetched_result:
        cleaned_result = {
            "id": result.get("id"),
            "title": result.get("jobOpeningName"),
            "url": urlunparse(urlparse(source["api_url"])._replace(path=posixpath.join(posixpath.split(urlparse(source["api_url"]).path)[0], str(result.get("id"))))),
            "location": result.get("location")
        }
        cleaned_data.append(cleaned_result)


    return cleaned_data