import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="code_quality_db",
        user="postgres",
        password="Shanu",
        host="localhost",
        port="5433"
    )

def save_analysis(features, prediction, user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO analyses (
            user_id,
            lines_of_code,
            num_functions,
            num_loops,
            num_conditionals,
            nested_loop_depth,
            avg_function_length,
            cyclomatic_complexity,
            predicted_label
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        user_id,
        features["lines_of_code"],
        features["num_functions"],
        features["num_loops"],
        features["num_conditionals"],
        features["nested_loop_depth"],
        features["avg_function_length"],
        features["cyclomatic_complexity"],
        prediction
    ))

    conn.commit()
    cur.close()
    conn.close()