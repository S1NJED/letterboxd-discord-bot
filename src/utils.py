import asqlite

async def db_query(db_path: str, query: str, params: tuple = (), fetch: str = None):
    """
    Execute a query safely with a new connection each time.
    
    fetch: "one", "all", or None (for insert/update/delete)
    """
    async with asqlite.connect(db_path) as conn:
        async with conn.execute(query, params) as cursor:
            if fetch == "one":
                return await cursor.fetchone()
            elif fetch == "all":
                return await cursor.fetchall()
        await conn.commit()
