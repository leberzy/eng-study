# Chengdu Learning Outro Implementation Plan

Goal: append the approved 36-second, four-card original-voice English lesson to the first 22.64-second punctuated preview.

Architecture: a standalone HyperFrames HTML composition places the existing preview at the beginning, then four nine-second learning cards. Original-voice excerpts are separate local audio assets placed on the framework timeline. GSAP controls restrained entrance animations and the listening/practice cues.

Tech stack: HyperFrames, HTML/CSS, GSAP, local H.264/AAC media; FFmpeg for extracting the approved speech excerpts only.

## Global constraints

- Scope is the first segment only; existing files remain available.
- Output is 1280 × 720, 16:9, MP4, approximately 59 seconds.
- Four cards follow the user-approved learning-outro-design.md.
- No generated voice, extra music, or invented source speech.
- English has punctuation; Chinese translations and vocabulary definitions follow the approved copy.
- No TDD for this reversible media artifact. Validate timing, layout, contrast, audio, and final playback.

## Task 1: runnable composition and assets

- [ ] Initialize english-practice/chengdu-learning-outro with HyperFrames blank template.
- [ ] Write BRIEF.md, design.md, and STORYBOARD.md from the approved design.
- [ ] Copy the existing punctuated preview to assets/source.mp4.
- [ ] Extract voice clips from 0.960–2.100, 4.319–6.260, and 20.840–22.620 into three local WAV files.
- [ ] Write index.html with a framework-timed source video, a separate source audio element, four timed study cards, and three timed replay audio elements.

## Task 2: learning preview

- [ ] Run HyperFrames check with snapshots at the source and four learning cards.
- [ ] Fix any runtime, overflow, contrast, or clip-overlap errors.
- [ ] Inspect all card images and verify English, Chinese, and key-word hierarchy.
- [ ] Start the supervised preview and verify it serves the complete composition.
- [ ] Present the finished preview for the render review required by the HyperFrames workflow.

## Task 3: export and delivery

- [ ] Render the approved preview to 01-back-in-china-Learning.mp4.
- [ ] Verify resolution, duration, audio stream, and frame samples at the footage-to-lesson boundary and all cards.
- [ ] Decode the completed file and verify the original-voice replays appear at their planned positions.
- [ ] Deliver the final MP4 and keep the project editable for subsequent segments.
