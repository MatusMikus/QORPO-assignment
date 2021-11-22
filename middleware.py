# @web.middleware
# async def middleware(request: web.Request,
#                      handler: Callable[[web.Request], Awaitable[web.Response]]):
#     conn = request.config_dict["db_connect"]
#     await conn.execute("BEGIN")
#     try:
#         resp = await handler(request)
#         await conn.execute("COMMIT")
#         return resp
#     except Exception:
#         await conn.execute("ROLLBACK")
#         raise