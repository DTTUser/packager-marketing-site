---
title: Why authoring tools hide the SCORM API from you, and what you can do about it
description: An honest look at why Articulate, iSpring, and Captivate make the SCORM API hard to reach, and how to work around it.
og_description: An honest look at why authoring tools obscure the SCORM API, and how to work around it.
slug: why-authoring-tools-hide-scorm-api
date: 7 July 2026
read_time: 8 minutes
lede: An honest look at the gap between what SCORM 1.2 actually offers and what authoring tools let you reach.
---

## A small disclaimer before we begin

This is the most opinionated post in the current run. It argues that the big authoring tools (Articulate Storyline, iSpring Suite, Adobe Captivate, Lectora) intentionally limit access to the underlying SCORM API in ways that benefit the tool vendor more than the user. If that frames you as the user, the rest of the post will read true. If you make a living from Articulate certifications, you may want to skim past the next section.

I do not think any of the tool vendors are villains. They are responding to incentives. The incentives just happen to leave instructional designers with less control than they realise.

## What is actually possible with the SCORM 1.2 API

SCORM 1.2 exposes a small but useful set of methods:

- `LMSInitialize`: tell the LMS the course has started.
- `LMSGetValue`: read a value from the LMS (the learner's name, their previous progress, their preferences, etc.).
- `LMSSetValue`: write a value to the LMS (completion status, score, time, lesson location, individual interaction results).
- `LMSCommit`: force any pending writes to be saved.
- `LMSFinish`: tell the LMS the course has ended.
- `LMSGetLastError` and friends: error handling.

That is the whole API. About a dozen methods. From them, your content can read anything the LMS knows about the learner and write almost any kind of progress data, including custom suspend data of up to about 4KB per session that you can use to store anything you want.

So in theory, an instructional designer should be able to:

- Resume a learner exactly where they left off, on any screen, with any state.
- Show different content based on the learner's previous answers in this or a previous course.
- Record fine-grained question-by-question data the LMS can then report on.
- Store and retrieve arbitrary state (preferences, choices, history) across sessions.

In practice, very few authoring-tool-built courses do any of this. The reason is not technical. The API supports it. The authoring tools have chosen not to expose it.

## What authoring tools actually expose

Each of the major tools has its own model for SCORM, and each of them stops short of the full API surface.

**Articulate Storyline.** Trigger-based interface. You can set a quiz score to be sent to the LMS, you can mark complete on a slide, you can use a small JavaScript trigger to call `SCORM_CallLMSGetValue` and similar. The JavaScript trigger is the escape hatch, but it requires you to know the internal helper function names, which Articulate does not document. You learn them from community forums or by decompiling the published output.

**iSpring Suite.** PowerPoint plugin. Exposes completion criteria, score, and a small set of completion behaviours. Direct SCORM API access is not officially supported, though you can drop raw JavaScript into a slide with some difficulty.

**Adobe Captivate.** Advanced actions and JavaScript windows. You can call `window.cp.GetCmiValue` and similar, which proxies to the SCORM API. Documentation is partial.

**Lectora.** Variables and actions. Direct SCORM API access via JavaScript is possible but undocumented.

The pattern: in every case, the SCORM API is technically reachable, but the tool's UI does not expose it. To get to it, you need either undocumented vendor-specific helpers or raw JavaScript inserted into a slide. Both are fragile, both break on tool updates, both make your course harder to maintain.

## Why this might be

Three reasons, in roughly increasing order of how cynical I am about them.

**First, complexity hiding.** The simplest reading is that the tool vendors want the tool to be approachable to non-developers. Exposing the full SCORM API would mean exposing a dozen methods with idiosyncratic semantics. The tool vendor reasonably decides to surface only the most common operations (mark complete, set score) and hide the rest. This is a defensible product decision.

**Second, content lock-in.** Courses built in Articulate Storyline are reasonably portable as long as you stay within Articulate's model. The moment you start using raw SCORM API calls, your content becomes harder to migrate, harder to support, harder for the next developer to understand. The tool vendor benefits from this because it makes switching tools more painful. This is not malicious, but it is real.

**Third, feature differentiation.** The tools compete on features that are inside the authoring environment, not on what the underlying SCORM API can do. If "full SCORM API access" became a marketing checkbox, every tool would have to add it. By all silently restricting it to the same subset, none of them have to compete on it. This is the kind of unspoken alignment that happens in mature markets. Whether it counts as collusion depends on your reading.

Any one of these three is enough to explain the current state. I suspect all three are at play.

## What you can do about it

Five practical options, in roughly increasing order of effort and capability.

### 1. Use the authoring tool's escape hatch

Every major tool has a way to drop raw JavaScript into a course. Use it. Find the SCORM API the tool's published output exposes (usually via `window.parent.API` or a vendor-specific helper). Call it directly. Document what you did and where, so the next person who opens the source file can find it.

This is the lowest-effort option. You stay inside the authoring tool, you get authoring-tool support for everything else, and you only break out to the API for the specific things the tool does not surface.

### 2. Build the content in HTML directly

Skip the authoring tool entirely. Write the course in HTML, CSS, and JavaScript. You have full control of every aspect of the experience. The downside is no built-in interactions library, no SCORM packaging, no quiz engine. You build these yourself or wire in libraries.

This used to be a huge amount of work. With modern AI coding tools (Lovable, v0, Cursor, Claude), it is increasingly viable. You generate the HTML content in the AI tool. You add a SCORM API wrapper script. You package the result. This is, not coincidentally, the workflow the AI Learning Packager exists to support.

### 3. Use a lightweight SCORM API wrapper

Several open source SCORM API wrappers exist. They sit between your HTML content and the LMS, exposing the full SCORM API in a clean JavaScript interface. Examples include [pipwerks SCORM Wrapper](https://github.com/pipwerks/scorm-api-wrapper) and Jeff Batt's [scorm-drivers](https://github.com/jeffbatt01/scorm-drivers) which adds xAPI on top.

You include the wrapper in your HTML content, then make calls like `scorm.set("cmi.core.score.raw", 85)` rather than the raw SCORM API. The wrapper handles error checking, retry, and the slightly different syntaxes between SCORM 1.2 and SCORM 2004.

### 4. Build your own wrapper

For most cases, an off-the-shelf wrapper is fine. If your project has unusual needs (specific reporting requirements, integration with another system, custom state storage), writing your own wrapper is a few hundred lines of JavaScript. It is not glamorous work, but it is well-understood.

### 5. Switch to a more open standard

If you find yourself fighting authoring tool limitations repeatedly, the underlying issue may be that SCORM 1.2 itself is not the right standard for what you are trying to build. xAPI was covered in a previous post. cmi5 is the bridge. Custom integrations may be appropriate when the data flow is unique enough.

This is the largest-effort option but sometimes the right one.

## A small honest admission

The AI Learning Packager exists because of this exact frustration. After watching multiple projects get blocked by authoring tools that would not let me reach the SCORM API, I built a tool that does only the packaging step and gets out of the way. The HTML content is yours. The SCORM API is exposed to your code with no abstraction. Anything the spec supports, your content can do.

That is also a marketing argument, of course. So treat it accordingly. But the underlying observation about authoring tools is true whether or not the packager is the right answer for you specifically.

## Closing thought

Authoring tools are not bad. They are excellent at what they do, which is letting non-developers build attractive courses quickly. They become a problem when the project's requirements outgrow what the tool exposes, and you find yourself fighting the tool rather than building the course.

The way to know whether you have reached that point is simple. If you have ever said "the tool will not let me do that", and "that" is something the SCORM API actually supports, you have hit the limit. From there, you have the five options above. Pick whichever fits the project.

---

*Built by Michael at [Digital Technology Training](https://dtttech.com). [The packager](https://packager.dtttech.com) is in private beta. Request access below.*
