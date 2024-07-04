### Setting up and running locally:


1. Clone the repo with `git clone`
2. Rename .env.example to .env and input a discord bot token for Theta to connect to
3. Install requirements with `pip install -r requirements.txt`, I recommend setting up a [virtual environment](https://docs.python.org/3/library/venv.html) first.
4. In ./theta/staticdata, create a file titled trusted.json, you can simply rename trusted.json.exmaple and input your own Discord user id
5. Using the [prisma cli](https://www.prisma.io/docs/orm/tools/prisma-cli), run `prisma db push —schema ./data/schema.prisma`to create the database
6. If you have docker, run the docker-compose file with `docker compose up`, if you do not have docker please download it, it’s well worth the learning curve and much easier than it looks at first
7. Once the bot is up and running, go to a channel it has access to and run `!sync-all` (if development mode is on) or `$sync-all` (if development mode is off) to sync slash commands to Discord
8. Enjoy!

## Why a rewrite?📮

ScrimBoard v1 was not built with scale in mind, it lacks persistence, is slow to update, lacks extensibility should we offer future integrations with other projects, and has a lot of overhead for possible performance optimization and UX improvements.

## Features 🧱

Expecting a magic bullet? We have a brick. It's not even close.

1. Now interacts with message IDs directly meaning it doesn’t need anywhere near as many perms
2. Rest API allowing for web integration
3. Persistent posts and data via SQLite to reduce the impact of outages (which should hopefully never happen due to digital Ocean hosting it)
4. Queue system with Redis to update posts in order at a high speed and integrate with APIs (imagine a co-worker coming over to your desk and leaving a pile of paperwork with no other context, that’s what we’re doing here to ScrimBoard)

# User workflows 🔥

### Setup the bot

Command: /setup

Options: “use-this-channel” OR “ create-new-channel ” OR “create-new-category”

**Use this channel /  New channel (Basic setup)**

Sends posts to that specific channel, in house scrims are not available. By default, only an all-posts channel will be needed because you can now create scrim posts in any channel that allows bot commands, and a majority of servers do not have enough members / focus on scrims to warrant supporting in-house scrims everywhere.

**New Category (Full setup)**

Creates a category with three channels:

how-to-use (also used for sending announcements / updates)

in-house-scrims (in server scrims only)

global-Scrims (scrims from every server)

### Making a post

Command: /scrim-**new**

Options: “Team name” “Skill level / LUTI Division” “More Information” “Screen OK?” “Expiration (default ~3 days, TBD)” “Destination (all-servers or this server)

/scrim-new makes a post object, sets an expiration, and deletes it after that period using async.io

If ScrimBoard goes down for any reason, upon restart it can check the DB and set the timeouts appropriately.

**Accepting a post**

Find a scrim you like? Just click accept.

**Change your mind?**

Hit cancel.

**Want to delete it?**

The author can hit cancel to look for another team (if one was already found), which will change the cancel button to a delete button. The author can then hit delete.

### Viewing a post

Command: /scrim-**view**

Shows your current post to you as an ephemeral message, with the accepter’s info attached if relevant alongside the options to cancel or delete your post.

# Data structures 🌉

Ok but like ehh how do the thing store the value? Objects? What am I, Json Borne?

**Instance Disk Storage** (.csv, not accessible to anyone without local system access)

- Banned user IDs (split between two files)
    - Partners
    - Local
- Trusted user IDs
    - Partners
    - Developers
- Logs
    - Post actions (CRUD + status + reason)
    - Server state changes

---

__ScrimBoard Core Data (Accessible w/ open APIs via Fast API (tbd), auth token required)__

- Servers = {
    - ScrimBoard Category = [category_id : int]
    - All-post channels = [global_scrims_id : int]
    - In-server-post channels = [local_scrims_id: int]
    - How-to-use channels = [how_to_use_id : int] }
- SP-Author discord ID  = {
    - Author = {
        - Display name
        - Discord UID
        - PFP URL
        - Origin Server }
    - Acceptor = {

      Is accepted is implied because Discord ID will be set to None if false and a normal 9-digit ID if true

        - Display name
        - Discord ID
        - PFP URL
        - Origin Server }
    - StaticScrimInfo = {
        - Team name
        - Skill level / Division
        - Time / Map List
        - Screen OK?
    - Expiration period (2-120 hrs) = INT (default 72)
    - Post Message IDs = [] }
- BTN-IDs = [button id, button id2, etc]

**Buttons!** 🎛️

- Buttons on embeds will have IDs equal to the poster’s UID snowflake followed by -accept, -cancel, or -delete. For example, user ID 4559 would have an accept button ID of 4559-accept

## API Routes 🔗
```Still a work in progress, routes and strcutures are NOT final!```

* __✒️GetAllPosts (GET):__ /scrims/ => 200 / 400 /401 (OK, Bad Request, Unauthorized)
  * authtoken
* __✒️GetPost (GET):__ /scrims/author_user_id => 200 / 204 / 400 /401 (OK, No Content, Bad Request, Unauthorized)
  * authtoken
* __✒️Create (POST):__ /scrims/create/ => 201 / 208 / 400 / 401 (Created, Already Reported (duplicate), Bad Request, Unauthorized)
  * scrim = {} (see above scrim model)
  * authtoken
  

# Data flows ⛵

**setupNewServer{minimal|local|how-to|complete}()**

1. Check if server is already setup using “not in” to be performant
2. pin the tail on the donke- I mean upsert. We use upsert. We throw it on the end of the pile if it doesn’t exist and update it if it does.

**updateDiscordPost**()

1. If async updates list full or matching POST ID in system

*Then*

1. Add to updates list
2. [Async.io](http://Async.io) update 5+ servers at once (switch case for CRUD, eg discordPostCreate, discordPostUpdate, discordPostDelete, etc)
3. Remove from updates list returns a list of message IDs which are attached to the post object (or success for delete)

**/**scrim = new post

**postCreate()**

- Check if banned
- Check if post
- Create DB object (returns discord embed data + snowflake)
- discordPostUpdate()

**postAccept()**

- Check if banned
- Get post by button ID
- Update post DB object
- Contact both parties
- Queue post update with updateDiscordPost()

postCancel(), delete setup, and postDelete() perform inverse actions in the same order, __delete setup (now known as 
unlink setup) only removes channels from the database and does NOT delete the channels on Discord__