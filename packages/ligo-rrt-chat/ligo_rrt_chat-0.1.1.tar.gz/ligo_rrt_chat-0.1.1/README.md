# Chat

Create a mattermost chat for discussing superevents.

## Usage

This current version uses a superevent_id information
to make mattermost channels. It only works if the .netrc 
file has a "mattermost-bot" login with appropiate token as password. 

If the channel creation succeedes, the new channel 
name will be `RRT O4 {superevent_id}`. A post will be 
made in this channel with a corresponding 
grace_db url. Raises exceptions in case of failures.

```
from ligo.rrt_chat import channel_creation
import json

channel_creation.rrt_channel_creation(superevent_id, gracedb_url)

```
