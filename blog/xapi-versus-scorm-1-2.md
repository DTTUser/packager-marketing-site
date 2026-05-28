---
title: xAPI versus SCORM 1.2 in 2026, an honest comparison
description: A practical comparison of xAPI and SCORM 1.2, the trade-offs that actually matter, and how to decide which one your project needs.
og_description: xAPI was supposed to replace SCORM by now. The honest version of what actually happened.
slug: xapi-versus-scorm-1-2
date: 9 June 2026
read_time: 8 minutes
lede: xAPI was supposed to replace SCORM years ago. SCORM 1.2 is still what every LMS actually runs on. Here is the honest version of why.
---

## The awkward truth, said out loud

xAPI has been "the future of e-learning" for over a decade. It was launched in 2013. It is now 2026. SCORM 1.2 is still what every commercial LMS actually accepts without configuration. If you have read this far, you already suspect this is the case, and you may even feel slightly disloyal for suspecting it. Do not.

This post is the comparison written by someone who builds for both and is tired of the marketing version of the answer. It is structured around five questions that actually matter when you are choosing between them for a real project, and it ends with a one-page decision matrix.

## What each one is, in plain language

SCORM 1.2 is a 2001 specification. The content sits inside the LMS. While the learner is taking the course, the content reports a small set of values back to the LMS (completed yes or no, passed yes or no, a score, a time, optional question results). The LMS stores these and shows them on its dashboard. The whole thing is self-contained.

xAPI, also called Tin Can, is a 2013 specification. Content sends "statements" of the form "actor verb object" to a Learning Record Store, which is a database designed for this. The LRS may or may not live inside the LMS. The vocabulary is open-ended. You can record "Michael completed Module 4" but also "Michael watched a video for 12 seconds" or "Michael clicked the help button three times" or anything else you can describe.

There is also cmi5, which is the bridge. cmi5 uses xAPI underneath but adds the bits SCORM had and xAPI lacked: a launch mechanism, sequencing, a course structure. If you want the data flexibility of xAPI and the LMS integration of SCORM, cmi5 is what you want, in theory. In practice, LMS support for cmi5 is patchy.

## The five questions that actually matter

### 1. What does the LMS accept?

SCORM 1.2 wins by a mile. Almost every LMS in 2026 accepts SCORM 1.2 natively, without configuration, without procurement involvement, without an IT review. Drop the zip in, the LMS knows what to do.

xAPI requires a Learning Record Store. Some LMSs include one (Cornerstone, Docebo, some flavours of Moodle with the right plugin). Most do not. If the LRS is missing, your xAPI content has nowhere to send statements, and you are stuck.

cmi5 is in the worst position of the three on this question. It needs both xAPI support and a cmi5-compliant launch mechanism. Adoption is growing but a long way from universal.

If your project ends with "upload to the client's LMS and walk away", SCORM 1.2 is almost always the right answer for this reason alone.

### 2. What data can you capture?

xAPI wins by a mile. The vocabulary is genuinely open-ended. If you can describe what a learner did in three words (actor, verb, object), xAPI can record it.

SCORM 1.2 is limited to the five primitives covered in the previous post: completion, success, score, time, and optional interactions. That is the whole list. You can be clever inside the interactions log to encode richer data, but it is a hack, and the LMS does not understand it as anything other than question results.

If you genuinely need to record behaviour at the granularity of clicks, hovers, video plays, off-platform activity, cross-system journeys, simulator runs, or anything outside the "did they finish the course" frame, xAPI is the right tool and SCORM 1.2 is the wrong tool. Full stop.

### 3. What data can you act on?

This is where the conversation usually gets uncomfortable for xAPI advocates. Capturing data is not the same as doing anything useful with it.

SCORM 1.2 captures less, but the LMS reporting is built around it. Out of the box, you can see who passed, who failed, who scored what, how long they took. Your client's training manager can run those reports on day one with no consultancy.

xAPI captures more, but most LRSs make it hard to actually act on the captured data. Querying xAPI statements requires either a custom dashboard, a BI tool with an LRS connector, or someone willing to write JSON queries by hand. Most ID teams do not have any of these. The result, in real client environments, is "we are capturing a vast amount of xAPI data and looking at almost none of it".

So the honest question is not "what can I capture", it is "what will the client actually look at six months after launch". For 90% of clients, the answer is the SCORM 1.2 dashboard.

### 4. Implementation effort

SCORM 1.2 is well-understood, well-documented, has 25 years of community knowledge behind it, and works the same in every LMS. The boring stable choice.

xAPI is well-documented at the spec level, but the LRS landscape is fragmented. Different LRSs handle the same statements slightly differently. Most ID teams have never touched an LRS directly and would have to either learn or hire that capacity.

cmi5 requires understanding both xAPI and the cmi5 launch envelope, plus an LMS that supports it. The upside is that when it works, you get the best of both. The downside is more moving parts.

Rough effort multiplier for a typical project of comparable scope: SCORM 1.2 is the baseline at 1x. xAPI is 2x to 4x. cmi5 is 3x to 5x.

### 5. Future-proofing

This is where xAPI advocates lean, and they are mostly right, but the trend has been slow.

The argument for xAPI being the future: it can describe modern learning experiences (mobile, simulator, on-the-job, microlearning, social) that SCORM cannot. The argument against: it has been the future for 13 years and SCORM 1.2 is still the present.

SCORM 1.2 will not be replaced by an industry-wide alternative in the next five years. There is simply too much infrastructure built on it. It will eventually be replaced by something, but probably not by xAPI in its current form, and probably not within the working horizon of most current projects.

So "future-proofing" is a real consideration, but a 5-to-10-year consideration, not a "this project we are starting next month" consideration.

## The decision matrix

If you want a one-page version, here it is.

Use **SCORM 1.2** when:

- The client's LMS is the only consumer of the data.
- You want the training manager to be able to pull reports without consultancy.
- The course is self-contained (one set of HTML or web content, one outcome to track).
- You do not know what kind of LRS the client has, which usually means they do not have one.
- You want the project to be finished on time.

Use **xAPI** when:

- The client genuinely has an LRS in production and someone who knows how to query it.
- You need to track behaviour across multiple systems (LMS, mobile, simulator, on-the-job tools).
- The data capture is the point, and you have buyers for that data who will use it.
- The client is willing to pay for the additional setup and consultancy.

Use **cmi5** when:

- You want xAPI flexibility plus SCORM-style LMS launch.
- You have confirmed the LMS supports cmi5 (do not assume).
- You are willing to be on the early end of the adoption curve.

Use **a custom backend integration** (not SCORM, not xAPI) when:

- The data flow is unique enough that no standard fits.
- The LMS is not actually involved in the workflow.
- The team has the engineering capacity to build and maintain it.

## Where the packager fits

The [AI Learning Packager](https://packager.dtttech.com) currently emits SCORM 1.2 only, because that covers the 90% case. A future build could add cmi5 output, which would let the same wrapped HTML send xAPI statements while still launching from a SCORM-style manifest. Jeff Batt's open source [scorm-drivers](https://github.com/jeffbatt01/scorm-drivers) project is the obvious template for that, layering an xAPI driver on top of a SCORM-conformant base.

That feature lands when (and if) the SCORM 1.2 use case is validated. Right now, that validation is still in progress.

## Closing thought

The argument against SCORM 1.2 is that it is 25 years old. The argument for it is that every LMS in the wild speaks it fluently. In 2026, both are still true. Either one being true is enough to keep it as the default for another decade.

xAPI is not really the question. The question is whether your client's setup can actually use what xAPI captures. Most cannot. Some can. Know which one you are dealing with before you make the call.

---

*Built by Michael at [Digital Technology Training](https://dtttech.com). The AI Learning Packager is in private beta. If you want to try wrapping HTML content as SCORM 1.2 packages without touching an authoring tool, request access below.*
