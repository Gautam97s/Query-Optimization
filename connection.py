import pymysql
import time

servername = "localhost"
username = "root"
password = "root"
dbname = "chinook"

def get_explain_data(conn, query_text):
    with conn.cursor() as cursor:
        cursor.execute(f"EXPLAIN {query_text}")
        return cursor.fetchone()

def calculate_final_cost(explain_data, execution_time):
    rows_scanned = explain_data[0]
    return round((execution_time * 1000) + (rows_scanned * 0.001), 5)

def calculate_cost_and_time(conn, query_text):
    start_time = time.time()
    with conn.cursor() as cursor:
        cursor.execute(query_text)
        results = cursor.fetchall()
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time, results

def main():
    optimized_query = input("Enter the optimized query: ")
    unoptimized_query = input("Enter the unoptimized query: ")

    conn = pymysql.connect(
        host=servername,
        user=username,
        password=password,
        database=dbname
    )

    print("\nRunning EXPLAIN and queries...")
    optimized_explain_data = get_explain_data(conn, optimized_query)
    unoptimized_explain_data = get_explain_data(conn, unoptimized_query)

    optimized_time, optimized_results = calculate_cost_and_time(conn, optimized_query)
    unoptimized_time, unoptimized_results = calculate_cost_and_time(conn, unoptimized_query)

    optimized_cost = calculate_final_cost(optimized_explain_data, optimized_time)
    unoptimized_cost = calculate_final_cost(unoptimized_explain_data, unoptimized_time)

    print("\n--- Results ---")
    print(f"Optimized Query Time: {round(optimized_time, 5)} seconds")
    print(f"Unoptimized Query Time: {round(unoptimized_time, 5)} seconds")
    print(f"Optimized Query Cost: {optimized_cost}")
    print(f"Unoptimized Query Cost: {unoptimized_cost}")

    conn.close()

if __name__ == "__main__":
    main()
