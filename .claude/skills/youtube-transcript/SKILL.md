---
name: youtube-transcript
description: Use this skill when retrieving or analyzing YouTube video transcripts/captions. Guides transcript retrieval and analysis workflow.
---

# YouTube Transcript Skill

Use this skill when working with video transcripts/captions.

## When to Use

- Getting video transcript for content analysis
- Extracting spoken content from videos
- Searching within video content
- Summarizing video content

## Tool Usage

### Primary Tool: `youtube_get_transcript`

**Parameters:**

- `video_id` (required): 11-character YouTube video ID
- `language` (optional, default "en"): Language code (e.g., en, es, fr, de)

## Workflow

1. Get video ID from URL or user input
2. Call `youtube_get_transcript` with appropriate language
3. Check if captions are available
4. If transcript text is available, analyze as requested
5. If only metadata is available (due to API limitations), inform user

## Language Codes

Common codes:
- `en`: English
- `es`: Spanish
- `fr`: French
- `de`: German
- `ja`: Japanese
- `ko`: Korean
- `zh`: Chinese

## Limitations

- Full transcript text may require additional processing
- Some videos may not have captions
- Auto-generated captions may have errors
- Manual captions are typically more accurate

## Analysis Options

Once you have transcript data, you can:
- Summarize content
- Extract key points
- Identify topics discussed
- Search for specific terms
- Create notes from the content
