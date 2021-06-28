# Neo4j database connection string
DATABASE_URL = 'bolt://neo4j:12345@localhost:7687'
# The initial account identifier.
ROOT_NAME = "shailyn.abdullah.3"
# How 'far' away from the root node the scraper will go to.
DEPTH = 0
# Wherever the cookies file is stored.
COOKIE_FILE = 'cookies.json'
# Delay between each scraping attempt. A random integer between SLEEP_INTERVAL[0] and SLEEP_INTERVAL[1] seconds.
SLEEP_INTERVAL = (10, 30)
