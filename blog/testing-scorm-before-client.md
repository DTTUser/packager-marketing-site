---
title: How to test a SCORM package before sending it to a client
description: A practical four-stage testing workflow for SCORM packages, designed to catch problems before the client sees them.
og_description: A four-stage testing routine for SCORM packages. Catches the failure that would have embarrassed you.
slug: testing-scorm-before-client
date: 30 June 2026
read_time: 7 minutes
lede: A practical testing routine for SCORM packages. Catches the failure that would otherwise have embarrassed you.
---

## Why this matters

The most expensive moment in any SCORM project is the call from the client that goes "we uploaded it and nothing works". You then spend two hours debugging on a screen-share, the client loses confidence, and the project starts smelling of trouble even if you fix it within the call.

The fix is to test the package thoroughly before it leaves your machine. What follows is the four-stage testing routine I use. It takes about 30 minutes per course, and it catches roughly 95% of the issues that would otherwise surface at the client.

## Stage 1: Local file system test (5 minutes)

The first test is the cheapest. Before anything else, make sure your content actually loads when extracted from the zip.

Unzip your SCORM package into a folder on your desktop. Open the `imsmanifest.xml` and confirm the `href` attribute on the `<resource>` element matches the entry point file (almost always `index.html`).

Now open that entry point file in a browser. Crucially: do not use `file://` URLs. Modern browsers block a lot of behaviour when serving from `file://`, including most ES6 modules, video autoplay, audio, and fetch requests. The result is that local file:// testing tells you almost nothing about how the content will behave when served by an LMS.

Instead, serve the folder over HTTP. Three easy ways:

- **Python:** `cd` to the folder, run `python3 -m http.server 8000`, open `http://localhost:8000` in your browser.
- **Node:** `npx serve` from the folder, open the URL it prints.
- **A dedicated tool:** [Servez](https://greggman.github.io/servez/) is a free drag-and-drop HTTP server, useful on Windows.

Click through the entire course. Does every screen render? Do all images, videos, and audio play? Are there any 404 errors in the browser console? Are there any JavaScript errors?

If anything is broken at this stage, fix it before moving on. The next stages will not magically resolve it.

## Stage 2: SCORM Cloud validation (10 minutes)

[SCORM Cloud](https://cloud.scorm.com) is Rustici Software's free SCORM testing platform. It is the de facto industry standard for "does my package conform to the spec?" If your package passes SCORM Cloud, you can rule out the manifest itself as a cause of any later failures.

Sign up for a free account (you get a few hundred MB of free storage, plenty for testing). Upload your zip. SCORM Cloud will tell you immediately whether the manifest is valid.

Then launch the course inside SCORM Cloud's test interface. Click through it as a learner would. Then exit. SCORM Cloud will show you:

- Whether `LMSInitialize` was called successfully.
- Whether the course set a completion status, and what that status was.
- Whether the course set a success status and score.
- A full debug log of every SCORM API call the content made.

Three things to verify:

First, the course must reach `LMSFinish` cleanly. If it does not, the LMS may not save any of the data.

Second, the completion status must be what you expect (`completed` or `incomplete`). If your course is meant to mark complete on exit and SCORM Cloud shows `incomplete`, your completion logic is broken.

Third, if your course is supposed to send a score, that score must appear in the debug log. If it does not, the code that calls `LMSSetValue("cmi.core.score.raw", ...)` is not firing.

SCORM Cloud is strict. If something passes in SCORM Cloud, it does not guarantee it works in every LMS. If something fails in SCORM Cloud, it will definitely fail in production LMSs. So SCORM Cloud is necessary but not sufficient.

## Stage 3: Test in a real LMS (10 minutes)

The third stage is the one most people skip. SCORM Cloud is a player that follows the spec strictly. Real LMSs do not. Differences between SCORM Cloud and the client's actual LMS are where most production failures live.

Three options for getting a real LMS to test in:

**Option A: Use a free tier of a major LMS.** [TalentLMS](https://talentlms.com) has a free tier (5 users, 10 courses). [Moodle](https://moodle.org) has a free hosted instance via MoodleCloud, plus you can run it locally. [Adobe Learning Manager](https://learningmanager.adobe.com) has a 30-day trial. Each of these gives you a real-world implementation to test against.

**Option B: Use the demo tool.** [demo.dtttech.com](https://demo.dtttech.com) is a free demo viewer I built for showing courses to clients without LMS friction. It is not a full LMS, but it does verify that the package extracts correctly, the entry point loads, and the iframe-hosted SCORM API discovery works. Useful as a sanity check before going to a real LMS.

**Option C: Use the client's staging environment.** If the client has a staging or sandbox version of their LMS, ask for access. This is the gold standard because it tests against the exact same LMS, version, and configuration the production deploy will use. Many clients say no to this. Some say yes if you frame it as "this will reduce risk in production". Always worth asking.

What to test in each LMS:

Upload the package and verify it imports without error. Launch the course as a learner. Click through to the end. Exit. Then check the LMS's reporting view for that learner. Does it show the correct completion status? The correct score? The correct time?

If you have access to multiple LMSs, test in at least two. The most informative pairs are TalentLMS plus Moodle, because they have very different architectures. If your package works in both, it will work in most other LMSs.

## Stage 4: Edge case sweep (5 minutes)

The last stage is the one that catches the weird failures. Walk through these specific scenarios in whichever LMS you tested in:

**Re-entry.** Launch the course, partway through, exit. Then relaunch the course. Did the LMS resume you where you left off, or did it restart from the beginning? Both are valid behaviours, but you need to know which yours is so you can tell the client.

**Interrupted exit.** Launch the course, then close the browser tab without using the course's own exit button. Does the LMS still record the partial completion, or does it record nothing? This is where the `unload` event handler in your content really gets tested.

**Multiple browser sessions.** Some LMSs allow learners to have the course open in two tabs simultaneously. If that happens, do the SCORM API calls clash? Does one tab overwrite the other's progress? Usually not a problem for a single learner, but worth verifying.

**Browser console while running.** Launch the course, open DevTools, and watch the console as you click through. Any errors? Any warnings? Even if the course "works", silent errors are usually a sign of fragile code that will break on a different browser or LMS version.

**Mobile.** If the client's learners might launch on mobile, test on mobile. Tap targets, viewport scaling, audio playback, and orientation handling all behave differently from desktop.

## The handoff

Once the package has passed all four stages, you can hand it off with confidence. I include three things in the handoff:

A short test report. Just a few lines: "Tested in SCORM Cloud, TalentLMS, and the demo viewer. Completion tracking confirmed. No errors in browser console. Re-entry resumes from last screen." Clients appreciate this and it sets you up well if anything does go wrong.

The exact LMSs and browsers tested in. So that if a problem appears on an untested combination, there is a starting point for diagnosis.

A request: ask the client to test the package in their LMS as soon as it arrives, before publishing to their learners. This is the most important step because it catches LMS-specific issues while the project is still active rather than after launch.

## Where the packager fits

The [AI Learning Packager](https://packager.dtttech.com) generates packages that pass Stage 2 (SCORM Cloud validation) out of the box. The other three stages are still on you, because they test the content rather than the wrapping. But starting from a clean, valid package removes the biggest source of false positives, which means the failures you do find in Stages 1, 3, and 4 are almost always real content issues you can fix.

---

*Built by Michael at [Digital Technology Training](https://dtttech.com). [The packager](https://packager.dtttech.com) is in private beta. Request access below.*
