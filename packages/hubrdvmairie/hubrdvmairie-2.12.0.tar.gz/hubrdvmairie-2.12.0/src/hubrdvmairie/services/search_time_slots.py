import asyncio
import os
import random
from datetime import date

from fastapi import WebSocket

from ..db.utils import get_all_editors, get_all_meeting_points
from ..services.search_meeting_points import search_close_meeting_points


async def search_slots(
    longitude: float,
    latitude: float,
    start_date: date,
    end_date: date,
    radius_km: int,
    reason: str = "CNI",
    documents_number: int = 1,
    websocket: WebSocket = None,
    department_code: str = None,
):
    """function will call 'search_slots_in_editor' that intercat with editors

    Args:
        longitude (float): longitude of the user
        latitude (float): latitude of the user
        start_date (date): the first date choosed by the user
        end_date (date): the end date choosed by the user
        radius_km (int): _description_
        reason (str, optional): _description_. Defaults to "CNI".
        documents_number (int, optional): _description_. Defaults to 1.
        websocket (WebSocket, optional): _description_. Defaults to None.

    Returns:
        [Meeting_point]: all the meeting point of all the editors
        [Errors]: all the errors sendit by the editor.
    """
    all_points = get_all_meeting_points()

    if department_code:
        all_points = [
            point
            for point in all_points
            if point["zip_code"][: len(department_code)] == department_code
        ]

    meeting_points = search_close_meeting_points(
        all_points, latitude, longitude, radius_km
    )

    all_editors_meeting_points = []
    all_editors_errors = []
    no_response_score = random.randint(1, 3)
    if (
        os.environ.get("MOCK_EMPTY_RESPONSE") in ["True", True]
    ) and no_response_score < 2:
        await asyncio.sleep(3)
    else:
        editor_futures = []
        for editor in get_all_editors():
            editor_futures.append(
                asyncio.ensure_future(
                    editor.search_slots_in_editor(
                        meeting_points,
                        start_date,
                        end_date,
                        reason,
                        documents_number,
                        websocket,
                    )
                )
            )
        all_results = await asyncio.gather(*editor_futures)
        for result in all_results:
            all_editors_meeting_points += result[0]
            if result[1]:
                all_editors_errors.append(result[1])
    return all_editors_meeting_points, all_editors_errors
