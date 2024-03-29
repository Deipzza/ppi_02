from .database.mongodatabase import *
from .functions_utils import *

def get_metrics(driver = None):
    """Retrieves the academic metrics for the user.

    Inputs:
    driver -> Selenium driver object.

    Returns:
    list with the metrics.
    """

    pag_academic_history = get_page_academic_history(driver)
    page_soup = BeautifulSoup(pag_academic_history, 'html5lib')
    metrics = page_soup.find(
        "span", {"class": "promedios"}
    ).find_all(
        "span", {"class": "promedio-general"}
    )

    result = ["", "", ""]
    for metric in metrics:
        tipo = metric.find("span", {"class": "promedios-texto"}).text
        valor = metric.find("span", {"class": "promedios-valor"}).text

        if "P.A.P.A" in tipo:
            result[0] = valor
        else:
            result[1] = valor
    result[2] = page_soup.find("span", id = "pt1:r1:2:i12:0:pgl42").text
        
    return result


def metrics(username, data):
    """Adds or updates the metrics of a user.

    Inputs:
    username -> string of the student's username.
    data -> data to be added or updated.
    """

    query = {"username": username}
    results = mongo_db.metrics.count_documents(query)
    data = [username] + data

    # Verify if there's data already in the database.
    if results == 0: # If there's no data, add it.
        add_metrics_user(data)
    else: # If there's data, update it.
        update_metrics_user(data)


def add_metrics_user(data):
    """Inserts the data scraped to the database.

    Inputs:
    data -> data to be inserted.
    """

    # Get or create collection
    collection = mongo_db["metrics"]

    # Organize and insert the data
    document = {
        "username": data[0],
        "papa": data[1],
        "promedio": data[2],
        "avance": data[3],
    }
    collection.insert_one(document)


def update_metrics_user(data):
    """Updates the metrics for a user.

    Inputs:
    data -> data to be updated.
    """

    collection = mongo_db["metrics"]
    username = data[0]
    data = data[1:]

    query = {"username": username}
    update = {"$set": {
        "papa": data[0],
        "promedio": data[1],
        "avance": data[2],
    }}
    collection.update_one(query, update)
