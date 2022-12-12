from aiohttp import web
async def logger_middleware(app, handler):
    async def middleware_handler(request):
        print(f"Received request: {request.method} {request.path}")
        try:
            response = await handler(request)
        except Exception as e:
            ''' Handle the exception and return a 500 Internal Server Error response'''
            print(f"Exception occurred: {e}")
            response = web.Response(status=500)
        print(f"Returning response: {response.status}")
        return response

    return middleware_handler
