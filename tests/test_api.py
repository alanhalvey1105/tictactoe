import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db import db


@pytest.mark.asyncio
async def test_api_flow():
    # Ensure DB is connected before the test
    await db.connect()

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:

        # ---- Create game ----
        create_resp = await client.post("/games", json={"player_name": "A"})
        assert create_resp.status_code == 200

        game = create_resp.json()
        gid = game["id"]

        # ---- Join game ----
        join_resp = await client.post(f"/games/{gid}/join", json={"player_name": "B"})
        assert join_resp.status_code == 200

        # ---- Make a move ----
        move_resp = await client.post(
            f"/games/{gid}/move",
            json={"player_name": "A", "position": 0},
        )
        assert move_resp.status_code == 200
