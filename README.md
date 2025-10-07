# uni_project_bot

Before to run the project, you must create .env file and fill out this

--.env

 BOT_TOKEN=TOKEN

 DB_URL=postgresql+asyncpg://user:password@db:5432/db_name 

 POSTGRES_USER=user 

 POSTGRES_PASSWORD=password 

 POSTGRES_DB=db_name

----

Then just build this with Doker
Run this code in terminal


--cmd


docker-compose up -d --build

# !!!!!!!!!!!!!!!!!!!!!!!!!!

# You should have admin rights to write something directly to the bot. Because, that bot was created to public use. (without admin rights bot will ignore all your messages)

- add this bot in your telegram group
- send '/admin@(your_telegram_bot_username)' to have access to personal chat of bot


# !!!!!!!!!!!!!!!!!!!!!!!!!!
p.s i removed the administrator check, because of some misunderstandings.

all of telegram users capable to ro write a private messages to the bot 


----


# ALL COMMANDS

/start - to reset bot

/list - list of audios

/list (tag) - list of audios with tags


just send them audio file to save it, mention bot if you send it in group









# If you want run this code without Docker
Download 'ffmpeg-release-essentials.zip' from this site
https://www.gyan.dev/ffmpeg/builds/

'bin/' consist .exe files, copy and past these to 'app/ffmpeg/'

----
Download all from requirements.txt

--cmd

pip install -r requirements.txt

----
And download 'audioop-lts'

--cmd

pip install audioop-lts

----

In .env change parameters and add new

From

DB_URL=postgresql+asyncpg://user:password@db:5432/db_name 

----
On

DB_URL=postgresql+asyncpg://user:password@localhost:5432/db_name

WITHOUT_DOCKER=True

----

I DON'T RECOMMEND TO RUNNING THIS CODE WITHOUT DOCKER.
This way so difficult and something can be wrong




