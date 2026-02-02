# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-01-29

### Added
- Official website link to pyproject.toml and README.md

## [0.1.x] - 2025-01

### Added
- YouTube transcript integration using youtube-transcript-api
- Comprehensive test suite for YouTube MCP Server
- Environment configuration support (.env)
- MCP CLI wrapper for proper async execution (cli_main)
- Tools: YouTube search, video details, transcripts, playlists, comments, channel
- Claude MCP configuration examples (claude mcp add support)

### Fixed
- Async execution issues with MCP server
- Remove unused files and redundant scripts
- Correct test logic and type annotations

### Changed
- Simplified README to focus on user usage
- Updated installation instructions (pipx instead of pip)
- MCP plugin terminology corrected to MCP server
- Skills examples moved to docs/examples/skills

### Docs
- Added comprehensive testing design plan
- Restructured technical documentation
- Multiple README improvements for clarity
