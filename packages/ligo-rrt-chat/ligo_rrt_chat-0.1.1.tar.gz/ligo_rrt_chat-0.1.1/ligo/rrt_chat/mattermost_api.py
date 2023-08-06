import json
import requests


class MMApi:
    """Mattermost API v4 bindings."""

    def __init__(self, url):
        self._url = url
        self._bearer = None
        self._headers = requests.utils.default_headers()
        self._my_user_agent = "RRT"
        self._headers.update({"User-Agent": self._headers["User-Agent"]+" " +
                              self._my_user_agent})

    def _get(self, endpoint, params=None):
        """
        Do a get-request.
        Args:
            endpoint (string): API-Endpoint to call
            params (dict, optional): url-parameters-dict
        Returns:
            dict: requested data.
        """
        res = requests.get(self._url + endpoint,
                           headers=self._headers,
                           params=params)
        return res

    def _post(self, endpoint, params=None, data=None):
        """
        Do a post-request.
        Args:
            endpoint (string): API-Endpoint to call
            params (dict, optional): url-parameters-dict
            data (dict, optional): json-data to post, if any
        Returns:
            dict: requested data.
        """
        if data is not None:
            data = json.dumps(data)

        res = requests.post(self._url + endpoint,
                            headers=self._headers,
                            params=params,
                            data=data)
        return res

    def _delete(self, endpoint, params=None, data=None):
        """
        Do a delete-request.
        Args:
            endpoint (string): API-Endpoint to call
            params (dict, optional): url-parameters-dict
            data (dict, optional): json-data to delete
        Returns:
            dict: requested data.
        """
        res = requests.delete(self._url + endpoint,
                              headers=self._headers,
                              params=params,
                              data=json.dumps(data))
        return res

    def login(self, bearer=None):
        """
        Login to the corresponding (self._url).
        """
        self._bearer = bearer
        if bearer is not None:
            self._headers.update({"Authorization": "Bearer "+self._bearer})
        res = requests.get(self._url + "users/me", headers=self._headers)
        return res

    def logout(self, **kwargs):
        """
        This will end the session at the server and invalidate MMApi-object.
        """
        return self._post("users/logout", **kwargs)

    def create_channel(self, team_id, name, display_name,
                       purpose=None, header=None,
                       chan_type="O", **kwargs):
        """
        Create a new channel.
        Args:
            team_id (string): The team ID of the team to create the channel on.
            name (string): The unique handle for the channel.
                           Look API web for name limiations
            purpose (string, optional): Purpose of the channel
            header (string, optional): Text to display in the header
            chan_type (string, default: public): Public/Private
        Returns:
            response: created Channel Response
        """

        return self._post("channels", data={
            "team_id": team_id,
            "name": name,
            "display_name": display_name,
            **({"purpose": purpose} if purpose else {}),
            **({"header": header} if header else {}),
            "type": chan_type,
        }, **kwargs)

    def delete_channel(self, channel_id, **kwargs):
        """
        Deletes a channel

        Args:
            channel_id (String): The id of the channel to delete.
        Returns:
            response
        """

        return self._delete("channels/" + channel_id, **kwargs)

    def search_channel_by_name(self, team_id, channel_name, **kwargs):
        """
        Check if the channel is present and return its info

        Args:
            channel_name (String): Name of the channel to search
        Returns:
            response: Channel info Response
        """

        return self._get("teams/"+team_id+"/channels/name/"+channel_name,
                         **kwargs)

    def search_user(self, username, team_id, **kwargs):
        """
        Find the user in the team and get ifo

        Args:
            username (String): albert.einstein
        Returns:
            response: User info response
        """
        return self._post("users/search", data={
            "term": username,
            "team_id": team_id
        }, **kwargs)

    def add_user_to_a_channel(self, channel_id, user_id, **kwargs):
        """
        Add a user to a channel

        Args:
            channel_id (String): ID of the channel to add user to
            user_id (String) : ID of the user to add to
        Returns:
            response: channel info with user id Response
        """
        return self._post("channels/"+channel_id+"/members", data={
            "user_id": user_id
        }, **kwargs)

    def post_in_channel(self, channel_id, message, file_id=None, **kwargs):
        """
        Post in a channel

        Args:
            channel_id (String): ID of the channel to post
            message (String) : Message to be posted
            file_id (list) : A list of file IDs to associate with the post
        Returns:
            response: post creation response
        """
        return self._post("posts", data={
            "channel_id": channel_id,
            "message": message,
            **({"file_id": file_id} if file_id else {})
        }, **kwargs)
