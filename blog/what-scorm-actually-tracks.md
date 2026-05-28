---
title: What SCORM actually tracks
description: A short, practical guide to what SCORM 1.2 records, what it does not, and why the difference matters for course design.
og_description: A short, practical guide for anyone who has ever sworn at an LMS upload screen.
slug: what-scorm-actually-tracks
date: 28 May 2026
read_time: 6 minutes
lede: A short, practical guide for anyone who has ever sworn at an LMS upload screen.
---

Most people who deal with SCORM have a vague sense of what it does. The LMS asks for a SCORM file, you give it a SCORM file, the LMS goes "thanks", and at some point a tick appears next to the learner's name. Job done.

That sketch is enough to get through the day. It is not enough to design good courses, debug a failing upload, or have a useful conversation with an LMS administrator. So here is what SCORM actually tracks, what it does not, and why the difference matters.

## The short version

SCORM 1.2, which is what most LMSs still run on in 2026, tracks five things.

First, completion status. Did the learner finish or not? This is a yes or no flag, not a percentage. There is a separate "incomplete" state for someone halfway through, and a "not attempted" state for someone who has not started yet, but the headline question is binary.

Second, success status. Did the learner pass or fail? Again binary. A course can be "completed" but "failed", which trips up a lot of people. The learner can finish all the screens and still bomb the quiz.

Third, score. A number between 0 and 100, plus optional minimum and maximum bounds. The LMS will display this on the learner's transcript if you tell it to. Many courses never bother to send one, which is fine if the course is informational.

Fourth, time. How long the learner had the course open. Note: open, not engaged. The course has no way to know whether they were reading, eating a sandwich, or asleep.

Fifth, interactions. If your course is set up to send them, SCORM will record individual question results: which question, what they answered, whether it was right, how long they took. This is the most useful data, and it is also the most commonly missing because most authoring tools either do not send it or hide it behind a setting nobody finds.

That is the whole list. Anything else you have ever seen in an LMS dashboard is built on top of those five primitives.

## What SCORM does not track

This is where people get caught out.

It does not track which screen the learner is on. You can rebuild this from the interactions log if your content sends one per screen, but the base spec has no concept of "page 4 of 12".

It does not track video plays, clicks, hovers, drag-and-drop attempts, or any of the rich interaction data that modern web analytics tools take for granted. If you want that, you need xAPI, which is the spiritual successor to SCORM and is a whole separate conversation.

It does not track learner behaviour across multiple courses. Each SCORM session is self-contained. The LMS may roll up data across courses for reporting, but the course itself only knows about itself.

It does not track engagement quality. There is no "did this resonate" field. The closest you get is time on screen, which as already noted, is a lousy proxy.

It does not enforce sequencing in any sophisticated way. SCORM 2004 added more sequencing logic, but almost nobody uses it because it is fiddly and most LMSs implement it inconsistently.

## Why this matters for course design

A few practical consequences.

If your course is informational and there is no quiz, you only need to send "completed". The simplest possible SCORM call. Most authoring tools do this automatically.

If you want a pass or fail flag, you need a quiz somewhere, and your code has to send a score and a success status. Worth checking what your authoring tool sends by default, because some send pass or fail based on quiz score and others ignore the quiz entirely.

If you want per-question reporting in the LMS, your quiz code has to send an interaction record per question. Storyline does this, iSpring does this, Captivate does this. Hand-coded HTML quizzes usually do not unless someone went to the trouble of wiring up the SCORM API.

If your LMS is showing weird results (a 100% score but "failed", or "completed" with no score), the issue is almost always that the course code is sending an inconsistent mix of values. The LMS is just displaying what it was told.

## Why the wrapper matters

This is why the AI Learning Packager exists. Most modern HTML learning content does not call the SCORM API at all. It is just web content. Drop it into an LMS as a zip and the LMS has no idea what to do with it.

The wrapper adds the bare minimum: an imsmanifest file so the LMS knows what it is looking at, a SCORM API wrapper script so the content can call out to the LMS, and a simple "mark complete on exit" call so the LMS gets at least one signal back. The original HTML is untouched.

If you want more than completion tracking, your HTML has to do the work. The wrapper exposes the SCORM API to the page. From there, your code can send a score, a pass or fail, interactions, anything the spec supports. Most courses will not need this. The ones that do, can.

## When SCORM is the wrong tool

SCORM is a 2001 specification. It was designed when learning content was a CD-ROM. It has the strengths and the limits you would expect from that era.

If you are building something that needs detailed behaviour analytics, multi-session memory, mobile-native interaction, or anything resembling modern web app data flows, SCORM is the wrong tool. Look at xAPI (also called Tin Can), or at custom backend integration.

If you are building a course that needs to drop into an existing LMS, get marked complete, optionally show a score, and not require IT involvement, SCORM is the right tool, and probably will be for another decade. There is too much infrastructure built on it for the industry to move on.

## In summary

SCORM tracks completion, success, score, time, and optional interactions. That is the whole feature set. Anything fancier than that, you either build on top of it or use a different standard.

If that sounds like a smaller surface area than the LMS dashboards suggest, that is because most of the dashboards are doing the dressing up. The underlying data is simpler than it looks.

---

*Built by Michael at [Digital Technology Training](https://dtttech.com). If you are wrestling with SCORM and want to try wrapping HTML content without touching an authoring tool, the [AI Learning Packager](https://packager.dtttech.com) is in private beta. Email for access.*
