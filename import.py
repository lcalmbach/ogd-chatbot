import sys
import pandas as pd
import sqlite3

DATABASE = "ogd.db"


def import_file(filename, tablename):
    # Read the CSV file using Pandas
    data = pd.read_csv(f"./data/{filename}", sep=";")

    # Establish a connection to the SQLite database
    conn = sqlite3.connect(DATABASE)

    # Store the data in the SQLite database
    data.to_sql(tablename, conn, if_exists="replace", index=False)

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    import_file(sys.argv[1], sys.argv[2])
