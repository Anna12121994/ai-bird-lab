import psycopg2


def connect_db():
    connection = psycopg2.connect(
        host="localhost",
        database="bird_lab",
        user="postgres",
        password="Nesk.121294",
        port="5433"
    )

    return connection


def create_table():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bird_analysis (
            id SERIAL PRIMARY KEY,
            image_name TEXT,
            predicted_species TEXT,
            confidence FLOAT,
            analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            extra_info TEXT
        )
    """)

    connection.commit()

    cursor.close()
    connection.close()


def save_result(
    image_name,
    predicted_species,
    confidence,
    description,
    extra_info
):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO bird_analysis (
            image_name,
            predicted_species,
            confidence,
            description,
            extra_info
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (
        image_name,
        predicted_species,
        confidence,
        description,
        extra_info
    ))

    result_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return result_id


def get_history():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            image_name,
            predicted_species,
            confidence,
            analysis_date
        FROM bird_analysis
        ORDER BY id
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def search_bird(name):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            image_name,
            predicted_species,
            confidence,
            analysis_date,
            description,
            extra_info
        FROM bird_analysis
        WHERE LOWER(predicted_species) LIKE LOWER(%s)
        ORDER BY id
    """, (f"%{name}%",))

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def delete_result(result_id):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM bird_analysis
        WHERE id = %s
    """, (result_id,))

    connection.commit()

    deleted = cursor.rowcount

    cursor.close()
    connection.close()

    return deleted