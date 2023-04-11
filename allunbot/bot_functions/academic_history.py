import time
import os

import pandas as pd
import prettytable as pt

from bs4 import BeautifulSoup

from .database.manage_database import *
from .utils import *
# from login import *

db = 'allunbot.db'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
temp = os.path.join(BASE_DIR, 'bot_functions/temp')

def get_academic_history(driver=None):
    pag_academic_history = get_page_academic_history(driver)
    page_soup = BeautifulSoup(pag_academic_history, 'html5lib')
    table = page_soup.find("div", id = "pt1:r1:1:t10::db").find("table")
    result = process_table(table)
    return result


def create_table_academic_history():
    query = """
        CREATE TABLE academic_history(
            username TEXT PRIMARY KEY, 
            disc_op TEXT NOT NULL,
            fund_ob TEXT NOT NULL,
            fund_op TEXT NOT NULL,
            dis_ob TEXT NOT NULL,
            libre_eleccion TEXT NOT NULL,
            trabajo_grado TEXT NOT NULL,
            total TEXT NOT NULL,
            nivelacion TEXT NOT NULL,
            total_estudiante TEXT NOT NULL
        );
        """
    create_table(db,"academic_history",query)


def add_academic_history_user(data):
    sql="""
        INSERT INTO
            academic_history
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
    insert_values_by_query([data], db, sql)


def update_academic_history_user(data):
    sql="""
        UPDATE academic_history
            SET
            disc_op = ?,
            fund_ob = ?,
            fund_op = ?,
            dis_ob = ?,
            libre_eleccion = ?,
            trabajo_grado = ?,
            total = ?,
            nivelacion = ?,
            total_estudiante = ?
            WHERE username = ?
        """
    username = data[0]
    data = data[1:]
    data.append(username)
    select_data_query(sql, db, data)


def academic_history(username, data):
    sql = "SELECT * FROM academic_history WHERE username = ?;"
    result = select_data_query(sql, db, [username])
    
    data = pd.DataFrame(data)
    data = data.transpose()
    data = [
                username, "-".join(data[0]), 
                "-".join(data[1]), "-".join(data[2]), 
                "-".join(data[3]), "-".join(data[4]), 
                "-".join(data[5]), "-".join(data[6]),
                "-".join(data[7]), "-".join(data[8])
            ]

    if len(result) == 0:
        add_academic_history_user(data)
    else:
        update_academic_history_user(data)


def generete_academic_history_user(username):
    sql = "SELECT * FROM academic_history WHERE username = ?"
    result = select_data_query(sql, db, [username])

    if len(result) == 0:
        return False
    else:
        table = pt.PrettyTable(['','Exigidos', 'Aprobados', 'Pendientes', 'Inscritos', 'cursados'])
        data = [item.split("-") for item in result[0][1:]]
        table.add_rows(data)
    
    return table

def generate_academic_history_img(username):
    import matplotlib.pyplot as plt

    sql = "SELECT * FROM academic_history WHERE username = ?"
    result = select_data_query(sql, db, [username])

    if len(result) == 0:
        return False
    
    column_headers = ('Exigidos', 'Aprobados', 'Pendientes', 'Inscritos', 'cursados')
    data = [item.split("-") for item in result[0][1:]]
    fig, ax = plt.subplots()

    # Pop the headers from the data array
    row_headers = [x.pop(0) for x in data]
    ax.table(cellText=data,
                      rowLabels=row_headers,
                      colLabels=column_headers,
                      loc='center')
    
    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    fig.tight_layout()

    filename= os.path.join(temp, f'{username}-academic-history.png')
    plt.savefig(filename, bbox_inches='tight',dpi=150)

    return filename


#--------------------------

def process_table(table):
    
    content = table.find("tbody")
    result = []

    for row in content.find_all("tr"):
        cells = row.findAll("td")

        data_row = []

        if len(cells) > 2:
            for cell in cells:
                data_row.append(cell.find("span").text)

            result.append(data_row)

    return result


# create_table_academic_history()