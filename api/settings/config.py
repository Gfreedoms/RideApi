SECRET_KEY = "ride_api_key"

rideslist = [
    {"id": 1, "user_id": 2, "from": "kampala", "to": "masaka kavule",
     "dept_date": "14/05/2018", "time": "08:30", "spots": 5,
     "description": "this is the first ride"}
    ]


# each ride request contains the id of the ride, the id of the
# person requesting and the acceptance status
# 0 for pending 1 for accepted and 2 for rejected
ride_requests = [
    {"id": 1, "ride_id": 2, "user_id": 1, "status": 0},
    {"id": 1, "ride_id": 3, "user_id": 2, "status": 0}
                ]
