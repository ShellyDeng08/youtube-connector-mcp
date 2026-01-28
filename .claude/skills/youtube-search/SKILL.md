---
name: youtube-search
description: Use this skill when searching YouTube for videos, channels, or playlists. Guides search workflow with filters and result interpretation.
---

# YouTube Search Skill

Use this skill when you need to search YouTube content.

## When to Use

- Finding videos on a topic
- Looking for channels related to a subject
- Discovering playlists
- Researching YouTube content

## Tool Usage

### Primary Tool: `youtube_search`

**Parameters:**

- `query` (required): Search terms
- `max_results` (optional, default 10): Number of results (1-50)
- `order` (optional, default "relevance"): Sort by relevance, date, viewCount, rating
- `type` (optional, default "video"): Resource type - video, channel, or playlist

**Common Orders:**

- `relevance`: Most relevant results
- `date`: Most recent
- `viewCount`: Most viewed
- `rating`: Highest rated

## Workflow

1. Clarify user's search intent
2. Construct appropriate query
3. Apply filters if needed (duration, date, type)
4. Call `youtube_search` tool
5. Present results with key information (title, channel, views, date)
6. Offer follow-up actions (get video details, comments, transcript)

## Result Interpretation

For videos, highlight:
- Title and description
- Channel name
- View count and publication date
- Thumbnail URL

For channels, highlight:
- Channel name
- Subscriber count
- Description

For playlists, highlight:
- Playlist title
- Channel
- Video count
