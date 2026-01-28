---
name: youtube-playlist
description: Use this skill when working with YouTube playlists - getting details, listing videos, or finding playlists from a channel.
---

# YouTube Playlist Skill

Use this skill when working with YouTube playlists.

## When to Use

- Getting details about a specific playlist
- Listing videos in a playlist
- Finding playlists from a channel
- Analyzing playlist content

## Tool Usage

### Get Playlist Details: `youtube_get_playlist`

**Parameters:**

- `playlist_id` (required): YouTube playlist ID (from URL)
- `max_results` (optional, default 50): Number of videos (1-50)

### List Channel Playlists: `youtube_list_playlists`

**Parameters:**

- `channel_id` (required): YouTube channel ID
- `max_results` (optional, default 25): Number of playlists (1-50)

## Workflow

### For a specific playlist:

1. Extract playlist ID from URL (usually after `list=`)
2. Call `youtube_get_playlist` with ID
3. Present playlist metadata (title, description, video count)
4. Show video list with key details

### For channel playlists:

1. Get channel ID (from URL or youtube_get_channel)
2. Call `youtube_list_playlists` with channel ID
3. Present available playlists
4. Offer to get details for specific playlists

## ID Extraction

From URL: `https://www.youtube.com/playlist?list=PLAYLIST_ID`
The `PLAYLIST_ID` is what you need.

## Pagination

- Results include `nextPageToken` for more items
- Use `totalResults` to know of full count

## Combined Workflow

Common pattern:
1. `youtube_search` with type="playlist" to find playlists
2. `youtube_get_playlist` to get details
3. `youtube_get_video` for specific video details
