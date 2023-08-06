import asyncio
import datetime

from typing import Optional

from context_helper import ctx

from graphql_service_framework import Schema, field

from hypercorn.config import Config
from hypercorn.asyncio import serve
from hypercorn.middleware import AsyncioWSGIMiddleware


class UTCTime(Schema):

    @field
    def now(self) -> Optional[str]:
        raise NotImplementedError()


class TimeOffset(Schema):

    @field
    def now(self, offset: int) -> Optional[str]:
        raise NotImplementedError()


class TimeOffsetService(TimeOffset):

    @field
    def now(self, offset: int) -> Optional[str]:
        utc_time: UTCTime = ctx.services.utc_time
        now = datetime.datetime.fromisoformat(utc_time.now())
        return str(now + datetime.timedelta(seconds=offset))


app = TimeOffsetService(config={
    "services": {
        "utc_time": UTCTime(
            url="https://europe-west2-parob-297412.cloudfunctions.net/"
                "utc_time"
        )
    }
}).create_app()

app = AsyncioWSGIMiddleware(app, max_body_size=2**32)

if __name__ == "__main__":
    asyncio.run(serve(app, Config()))
