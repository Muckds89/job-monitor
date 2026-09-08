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

    pass