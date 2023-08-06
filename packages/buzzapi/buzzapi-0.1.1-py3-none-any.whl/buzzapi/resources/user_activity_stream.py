from urllib.parse import urlencode


class UserActivityStream:
    def get_user_activity_stream(self, userid: int, enrollmentid: int):
        activities = []
        r = self.get_user_activity_stream_limited(userid, enrollmentid, {})
        response = r.json()
        activity = response["response"]["activities"]["activity"]
        activities = activities + activity
        print(response)
        endkeyPresent = "endkey" in response["response"]["activities"]
        while endkeyPresent:
            startkey = response["response"]["activities"]["endkey"]
            r = self.get_user_activity_stream_limited(
                userid, enrollmentid, {"startkey": startkey}
            )
            response = r.json()

            endkeyPresent = "endkey" in response["response"]["activities"]

            if endkeyPresent:
                startkey = response["response"]["activities"]["endkey"]
                activity = response["response"]["activities"]["activity"]
                activities = activities + activity
            else:
                print(response)

        return activities

    def get_user_activity_stream_limited(
        self, userid: int, enrollmentid: int, params: dict
    ):
        query = {
            "cmd": "getuseractivitystream",
            "userid": userid,
            "enrollmentid": enrollmentid,
            "limit": 1,
            **params,
        }
        return self.get(urlencode(query))
