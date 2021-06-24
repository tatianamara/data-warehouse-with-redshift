import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

IAM_ROLE_ARN = config.get('IAM_ROLE', 'ARN')
SONG_DATA = config.get('S3','SONG_DATA')
LOG_DATA = config.get('S3','LOG_DATA')
LOG_JSONPATH = config.get('S3','LOG_JSONPATH')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS song cascade;"
artist_table_drop = "DROP TABLE IF EXISTS artist;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE staging_events 
                        (
                          artist_name        VARCHAR NULL,
                          auth               VARCHAR NOT NULL,
                          first_name         VARCHAR NULL,
                          gender             CHAR NULL,
                          iteminSession      INT NULL,
                          last_name          VARCHAR NULL,
                          length             FLOAT NULL,
                          level              VARCHAR NOT NULL,
                          location           VARCHAR NULL,
                          method             VARCHAR NULL,
                          page               VARCHAR NULL,
                          registration       FLOAT NULL,
                          sessionId          INT NOT NULL,
                          song               VARCHAR NULL,
                          status             INT NULL,
                          ts                 double precision NOT NULL,
                          userAgent          VARCHAR NULL,
                          userId             INT NULL
                        );
""")

staging_songs_table_create = ("""CREATE TABLE staging_songs 
                        (
                          user_id            INT NULL,
                          artist_id          VARCHAR NULL,
                          artist_latitude    FLOAT NULL,
                          artist_longitude   FLOAT NULL,
                          artist_location    VARCHAR NULL,
                          artist_name        VARCHAR NULL,
                          song_id            VARCHAR NOT NULL,
                          title              VARCHAR NOT NULL,
                          duration           FLOAT NULL,
                          year               INT NULL
                        );
""")

songplay_table_create = ("""CREATE TABLE songplay 
                        (
                          songplay_id    INT IDENTITY NOT NULL,
                          start_time     TIMESTAMP NOT NULL sortkey,
                          user_id        INT NOT NULL,
                          level          VARCHAR NOT NULL,
                          song_id        VARCHAR NOT NULL distkey,
                          artist_id      VARCHAR NOT NULL,
                          session_id     INT NOT NULL,
                          location       VARCHAR NULL,
                          user_agent     VARCHAR NULL
                        );            
""")

user_table_create = ("""CREATE TABLE users 
                        (
                          user_id        INT NOT NULL sortkey,
                          first_name     VARCHAR NULL,
                          last_name      VARCHAR NULL,
                          gender         CHAR NULL,
                          level          VARCHAR NOT NULL
                        )
                        diststyle all;    
""")

song_table_create = ("""CREATE TABLE song 
                        (
                          song_id        VARCHAR NOT NULL sortkey distkey,
                          title          VARCHAR NOT NULL,
                          artist_id      VARCHAR NOT NULL,
                          year           INT NULL,
                          duration       FLOAT NULL
                        );    
""")

artist_table_create = ("""CREATE TABLE artist 
                        (
                          artist_id      VARCHAR NOT NULL sortkey,
                          name           VARCHAR NULL,
                          location       VARCHAR NULL,
                          lattitude      FLOAT NULL,
                          longitude      FLOAT NULL
                        )
                        diststyle all;  
""")

time_table_create = ("""CREATE TABLE time 
                        (
                          start_time     TIMESTAMP NOT NULL sortkey,
                          hour           INT NOT NULL,
                          day            INT NOT NULL,
                          week           INT NOT NULL,
                          month          INT NOT NULL,
                          year           INT NOT NULL,
                          weekday        INT NOT NULL
                        )
                        diststyle all;  
""")

# STAGING TABLES

staging_events_copy = ("""copy staging_events from {}
credentials 'aws_iam_role={}'
region 'us-west-2'
json {};
""").format(LOG_DATA,IAM_ROLE_ARN,LOG_JSONPATH)

staging_songs_copy = ("""copy staging_songs from {}
credentials 'aws_iam_role={}'
region 'us-west-2'
json 'auto';
""").format(SONG_DATA,IAM_ROLE_ARN)

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplay (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
                            SELECT 
                                timestamp 'epoch' + staging_events.ts * interval '0.001 second' as start_time, 
                                staging_events.userId as user_id, 
                                staging_events.level, 
                                staging_songs.song_id, 
                                staging_songs.artist_id, 
                                staging_events.sessionId as session_id, 
                                staging_events.location, 
                                staging_events.userAgent as user_agent
                            FROM staging_events, staging_songs
                            WHERE staging_events.page = 'NextSong' 
                            	AND staging_events.song = staging_songs.title 
                                AND staging_events.artist_name = staging_songs.artist_name;
                            
""")

user_table_insert = ("""INSERT INTO users \
                        SELECT DISTINCT userId as user_id, first_name, last_name, gender, level  \
                        FROM staging_events \
                        WHERE page = 'NextSong';
""")

song_table_insert = ("""INSERT INTO song \
                        SELECT DISTINCT song_id, title, artist_id, year, duration \
                        FROM staging_songs;
""")

artist_table_insert = ("""INSERT INTO artist \
                        SELECT DISTINCT artist_id, \
                        artist_name as name, \
                        artist_location as location, \
                        artist_latitude as latitude, \
                        artist_longitude as longitude \
                        FROM staging_songs;
""")

time_table_insert = ("""INSERT INTO time
                        SELECT DISTINCT timestamp 'epoch' + ts * interval '0.001 second' as start_time,
                        extract(hour from timestamp 'epoch' + ts * interval '0.001 second') as hour,
                        extract(day from timestamp 'epoch' + ts * interval '0.001 second') as day,
                        extract(week from timestamp 'epoch' + ts * interval '0.001 second') as week,
                        extract(month from timestamp 'epoch' + ts * interval '0.001 second') as month,
                        extract(year from timestamp 'epoch' + ts * interval '0.001 second') as year,
                        extract(weekday from timestamp 'epoch' + ts * interval '0.001 second') as weekday
                        FROM staging_events
                        WHERE page = 'NextSong';
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert,song_table_insert,artist_table_insert,time_table_insert,songplay_table_insert]
