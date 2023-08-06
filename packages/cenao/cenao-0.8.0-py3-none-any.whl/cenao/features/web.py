import asyncio
from typing import List

from aiohttp import web
from aiohttp.web_runner import TCPSite, AppRunner
from prometheus_client import generate_latest, Counter

from cenao.app import AppFeature
from cenao.view import View


class MetricsView(View):
    ROUTE = '/metrics'

    async def get(self):
        response = generate_latest().decode('utf-8')

        return web.Response(
            status=200,
            text=response,
        )


class WebAppFeature(AppFeature):
    NAME = 'web'

    VIEWS = [MetricsView]

    host: str
    port: int

    aiohttp_app: web.Application
    runner: AppRunner
    _ws: List[web.WebSocketResponse]

    PROMETHEUS_ROUTE_METRIC: Counter

    def on_init(self):
        self.host = self.config.get('host', '0.0.0.0')
        self.port = int(self.config.get('port', 8000))

        self._ws = []

        self.PROMETHEUS_ROUTE_METRIC = Counter(
            'route',
            documentation='Total route calls',
            labelnames=('path', 'method', 'status'),
            namespace=self.app.NAME,
        )

        @web.middleware
        async def prometheus_route_call_count(request: web.Request, handler) -> web.Response:
            resp: web.Response = await handler(request)
            self.PROMETHEUS_ROUTE_METRIC.labels(
                request.match_info.route.resource.canonical,
                request.method,
                resp.status
            ).inc()
            return resp

        self.aiohttp_app = web.Application(
            loop=self.app.loop,
            middlewares=[prometheus_route_call_count]
        )
        routes_len = 0
        for ft in self.app.ft:
            for view in ft.VIEWS:
                view.init(ft)
                self.aiohttp_app.router.add_view(view.ROUTE, view)
                routes_len += 1
        self.logger.info('Registered %d routes', routes_len)

        self.runner = AppRunner(self.aiohttp_app, logger=self.logger)

    async def on_startup(self):
        self.logger.info('Starting on %s:%d', self.host, self.port)
        await self.runner.setup()
        site = TCPSite(
            self.runner,
            self.host,
            self.port,
        )
        await site.start()

    async def on_shutdown(self):
        self.logger.info('Stopping webserver')

        for ws in self._ws:
            await ws.close()

        await self.runner.cleanup()

    def get_websocket_response(self) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        self._ws.append(ws)
        return ws
