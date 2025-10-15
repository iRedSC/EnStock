import time
import docker
import psycopg2

# Constants
POSTGRES_IMAGE = "postgres:15"
CONTAINER_NAME = "python-embedded-postgres"
POSTGRES_USER = "user"
POSTGRES_PASSWORD = "pass"
POSTGRES_DB = "appdb"
HOST_PORT = 5435

client = docker.from_env()

# Clean up any old container with the same name
try:
    old = client.containers.get(CONTAINER_NAME)
    print("Removing old container...")
    old.remove(force=True)
except docker.errors.NotFound:
    pass

# Run Postgres container
print("Starting new Postgres container...")
container = client.containers.run(
    POSTGRES_IMAGE,
    name=CONTAINER_NAME,
    detach=True,
    ports={"5432/tcp": HOST_PORT},
    environment={
        "POSTGRES_USER": POSTGRES_USER,
        "POSTGRES_PASSWORD": POSTGRES_PASSWORD,
        "POSTGRES_DB": POSTGRES_DB,
    },
)

# Wait for Postgres to be ready
time.sleep(5)

# Connect and test it
dsn = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{HOST_PORT}/{POSTGRES_DB}"
print("Connecting to:", dsn)

with psycopg2.connect(dsn) as conn:
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS test(id SERIAL PRIMARY KEY, name TEXT)")
        cur.execute("INSERT INTO test(name) VALUES ('Managed by Python')")
        conn.commit()

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM test")
        print("Rows:", cur.fetchall())

# Optionally stop and remove container when done
print("Stopping and removing container...")
container.stop()
container.remove()
print("Done ✅")