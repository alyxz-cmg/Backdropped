# Product Requirements Document (PRD) For LLM Context

## Product Name: Backdropped

### Version: v1 MVP + Long-Term Product Vision

### Platform: macOS Desktop (initial), future Windows, possible mobile/web companion

### Version: 1.1

---

# 1. Executive Summary

## Product Vision

Backdropped is an AI-powered desktop video recording and background replacement application that enables users to record themselves with real-time person segmentation and automatic green screen compositing—without needing a physical green screen.

The long-term vision is to evolve Backdropped from a “Zoom blur + recording” tool into a lightweight creator studio for:

* Content creators
* Remote workers
* Educators
* Streamers
* Interview prep
* Product demos

Backdropped should eventually combine:

* Live AI segmentation
* Virtual backgrounds
* Video background replacement
* Post-production cleanup tools
* Layer-based editing
* Export tools
* Potential live streaming integrations

---

# 2. Problem Statement

## User Problem

Current tools often fail in one or more ways:

* Zoom-style background blur is low quality
* Green screens require physical setup
* Professional editing tools are expensive and overkill
* Segmentation artifacts (hair edges, moving hands) reduce quality
* Post-recording correction is difficult
* Few lightweight desktop apps specialize in “record + fix + replace background”

## Core Pain Points

1. Users want professional-looking background replacement
2. Users need low setup friction
3. Users need correction tools for imperfect AI masks
4. Users may want static, green, blurred, or video backgrounds
5. Users need creator-grade exports without full Premiere/After Effects complexity

---

# 3. Product Goals

## Primary Goal (MVP)

Enable users to:

### Record webcam video with real-time AI subject isolation and green-screen replacement.

## Secondary Goals

* Replace green screen with custom static images
* Replace with looping or uploaded video backgrounds
* Save alpha masks for later correction
* Enable post-processing mask cleanup
* Improve segmentation quality over time

## Business/Strategic Goals

* Build a niche creator utility
* Potential SaaS/premium export features
* Marketplace for templates/background packs
* Plugin architecture

---

# 4. Target Users

## Primary Personas

### A. Creator / Streamer

* Wants quick branded background
* May use OBS later
* Needs quality + speed

### B. Professional / Remote Worker

* Wants polished presentation videos
* Needs simplicity

### C. Educator

* Records lessons with cleaner visuals
* May overlay slides/videos later

### D. Technical User / Power User

* Wants manual correction and advanced controls

---

# 5. MVP Scope (Version 1)

## Must-Have Features

### 5.1 Live Camera Feed

* Webcam device detection
* Start/stop camera
* Resolution settings (720p, 1080p)
* FPS target: 24–30

### 5.2 Real-Time Person Segmentation

* AI person/background separation
* Replace background with:

  * Pure green screen
  * Blur
  * Solid color
* Edge smoothing
* Hair refinement baseline

### 5.3 Recording

* Start/Stop recording
* Save composited output
* Save original source optionally
* Save segmentation mask optionally
* MP4 export

### 5.4 Basic UI

* Preview window
* Background mode selector
* Record button
* Status indicator
* Settings panel

### 5.5 Performance Controls

* Adjustable quality/performance mode
* Frame skipping fallback
* CPU/GPU selection if available

---

# 6. Post-MVP (Version 2)

## Editing Layer

### 6.1 Timeline Editor

* Scrub timeline
* Frame preview
* Re-render export

### 6.2 Manual Mask Cleanup

* Brush erase background artifacts
* Brush restore removed subject areas
* Feather controls
* Keyframe corrections across frames

### 6.3 Background Replacement

* Static image insertion
* Video layer insertion
* Parallax options
* Blur intensity slider

### 6.4 Layer Stack

* Subject layer
* Background layer
* Overlay graphics
* Text
* Watermark

---

# 7. Long-Term Vision (Version 3+)

## Advanced Features

### AI Enhancements

* Better hair/hand segmentation
* Multi-person support
* Object retention (chairs, instruments, pets)
* Depth estimation
* Lighting adaptation
* Shadow synthesis

### Creator Tools

* OBS virtual camera output
* Twitch/YouTube live background replacement
* Scene templates
* Motion graphics packs

### Collaboration

* Cloud project saves
* Presets sync
* Team branding kits

### ML Personalization

* User-specific mask refinement
* Fine-tuned segmentation profiles

---

# 8. Functional Requirements

## FR-1 Camera Input

* System camera detection
* External webcam support
* Device switching

## FR-2 Segmentation Engine

* Real-time mask generation
* Adjustable threshold
* Confidence map
* Temporal smoothing

## FR-3 Rendering Pipeline

* Composite foreground + selected background
* Render under 100ms latency target

## FR-4 Recording Engine

* Encode MP4 (H.264 initially)
* Audio sync future support

## FR-5 Project Save System

* Save:

  * Raw video
  * Composite video
  * Mask frames
  * Metadata

---

# 9. Non-Functional Requirements

## Performance

* MVP Target: 24 FPS @ 720p on modern MacBook
* Stretch: 30 FPS @ 1080p

## Reliability

* Crash recovery
* Auto-save sessions

## UX

* Beginner friendly
* Minimal clicks

## Security

* Local-only processing by default
* No cloud dependency for MVP

---

# 10. Technical Architecture

## Suggested Stack

### Frontend/UI:

* PySide6

### Video Processing:

* OpenCV
* NumPy

### ML Segmentation:

* MediaPipe initially
* Future:

  * TensorFlow Lite
  * ONNX Runtime
  * SAM-style segmentation exploration

### Encoding:

* FFmpeg

### Data:

* JSON project configs
* Local cache

---

# 11. System Pipeline

## Live Mode

Camera Feed → Frame Capture → Segmentation → Mask Refinement → Background Composite → Preview → Record/Save

## Edit Mode

Recorded Video + Saved Mask → Manual Corrections → New Background → Re-render → Export

---

# 12. UX Requirements

## Main Dashboard

### Sections:

* Live Preview
* Background Selector
* Recording Controls
* Performance Meter
* Settings

## Future Editing Dashboard

* Timeline
* Brush Tool
* Layers Panel
* Export Panel

---

# 13. Risks & Challenges

## Technical Risks

### High:

* Hair edge quality
* Motion blur artifacts
* CPU bottlenecks
* Large file storage

## Product Risks

* Competing with free tools
* User expectations vs ML quality

## Mitigation

* Performance mode
* Quality mode
* Manual correction tools
* Modular ML upgrades

---

# 14. Success Metrics

## MVP Metrics

* App launches successfully
* Live preview latency <150ms
* Recording success >95%
* Segmentation acceptable in standard indoor lighting

## Product Metrics

* Weekly retention
* Export frequency
* Session duration
* Upgrade to advanced features

---

# 15. Milestone Roadmap

## Milestone 1: Foundation

* Repo setup
* Camera preview
* UI shell

## Milestone 2: AI Segmentation

* Live masking
* Green screen
* Blur

## Milestone 3: Recording

* MP4 export
* Basic settings

## Milestone 4: Quality

* Edge smoothing
* Better controls

## Milestone 5: Editor

* Timeline
* Manual cleanup
* Background layers

## Milestone 6: Creator Suite

* OBS
* Live streaming
* Presets

---

# 16. Nice-to-Have Features

* Auto framing
* Eye contact correction
* Teleprompter overlay
* AI lighting correction
* Noise suppression
* Chroma spill correction
* Gesture-triggered recording

---

# 17. Out of Scope (For Now)

* Mobile-first build
* Browser-based editing suite
* Full Adobe competitor feature set
* Enterprise cloud collaboration

---

# 18. Competitive Advantage

## Backdropped Differentiator:

### “Fast, local-first AI background replacement + creator-grade correction.”

Unlike Zoom:

* Better recording focus
* Editing tools
* Background replacement depth

Unlike Premiere:

* Faster
* Simpler
* Real-time first

---

# 19. Launch Strategy

## Initial Launch

* macOS desktop beta
* Indie creator / student audience
* Reddit / creator communities

## Future

* Windows release
* Premium templates
* Pro editing suite

---

# 20. Final Product Philosophy

Backdropped should feel like:

### “OBS + Zoom Background + CapCut Lite for AI background isolation.”

Core principle:

## Instant recording now, deeper correction later.

This ensures:

* Fast MVP
* Technical feasibility
* Sustainable roadmap
* Feature expansion without rebuilding core architecture
