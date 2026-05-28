---
title: Why your SCORM package works in SCORM Cloud but not in your client's LMS
description: The five most common reasons a SCORM package validates in SCORM Cloud but fails in a production LMS, and how to fix each one.
og_description: The SCORM Cloud passes, the client LMS does not. Here are the five usual suspects.
slug: scorm-cloud-versus-client-lms
date: 16 June 2026
read_time: 7 minutes
lede: A practical debugging guide for the most universal frustration in instructional design.
---

## The pattern

You build a SCORM package. You upload it to SCORM Cloud, the industry's de facto SCORM tester. It passes. Green ticks across the board. You send it to the client. The client uploads it to their LMS. Something is wrong. The course will not launch, or it launches but does not track, or it tracks the wrong thing, or it tracks correctly for some learners but not others.

This is one of the most universal frustrations in instructional design. SCORM Cloud is a strict, well-implemented SCORM player. Real-world LMSs are a patchwork of partial implementations, custom behaviours, and quirks accumulated over 25 years. Passing in SCORM Cloud is necessary but not sufficient.

What follows is the five most common causes I have seen, in rough order of frequency, with the fix for each.

## 1. Manifest format and version mismatches

The most common cause. The client's LMS expects SCORM 1.2, you sent SCORM 2004, or vice versa. SCORM Cloud accepts both happily. Many LMSs accept only one, and the error message when they do not is usually unhelpful (often "package invalid" with no detail).

**How to confirm:** open the imsmanifest.xml inside your package. Look for the `schemaversion` element. SCORM 1.2 says "1.2". SCORM 2004 has a 3rd, 4th, or 5th Edition variant. The client's LMS documentation will tell you which they support, if you can find it.

**How to fix:** rebuild the package in the version the LMS expects. Most authoring tools have a publish setting for SCORM version. If your content is hand-rolled HTML, the manifest version is what you control.

## 2. Content type headers and character encoding

The LMS expects certain MIME types on the files inside the zip. If your HTML files are served as `text/plain` instead of `text/html`, the LMS may refuse to render them. If the LMS extracts the zip to a server with strict character encoding rules and your HTML uses a different encoding, the result is mojibake or a failed launch.

**How to confirm:** open the LMS's content viewer in Chrome with DevTools. The Network tab shows the actual `Content-Type` headers being served for each file. If `index.html` is coming back as `text/plain` or `application/octet-stream`, that is your problem.

**How to fix:** ensure the HTML files have a proper `<meta charset="utf-8">` tag in the head. Add a `.htaccess` or equivalent file to the package if the LMS supports it, forcing the right MIME types. If the LMS strips these on upload, you may need to escalate to LMS support.

## 3. Case-sensitive file paths

The killer one. SCORM Cloud and most local testing tools run on case-insensitive file systems (Windows defaults, macOS in default mode). Many production LMSs run on Linux, which is case-sensitive. A reference to `Images/banner.png` works in testing and fails in production because the actual file is `images/banner.png`.

**How to confirm:** open the LMS's browser console in DevTools. Look for 404 errors. The URLs in the errors will tell you exactly which files are not loading.

**How to fix:** rename all files and folders to lowercase. Update all references in the HTML, CSS, and JavaScript. Use a tool like `git mv` to ensure the case change actually propagates to all platforms. Test the package on a Linux file system before sending, even if it is just `unzip` and serving via Python's built-in HTTP server on a Linux box.

## 4. Sequencing rules and launch behaviour

SCORM 2004 has sequencing rules that determine what learners can navigate to and when. Many LMSs implement these inconsistently. SCORM Cloud follows the spec strictly. The client's LMS may not. Result: the course launches but the learner cannot get past the first screen, or the LMS marks the course incomplete even after the learner reaches the end.

**How to confirm:** if your SCO has any sequencing in the manifest (look for `imsss:sequencing` elements), and the symptom is navigation-related, sequencing is the prime suspect.

**How to fix:** simplify or remove sequencing rules. For most courses, you do not need them. Mark the SCO as a single launchable unit with no internal sequencing constraints, and let the content itself handle navigation. This is one area where SCORM 1.2 is genuinely easier than SCORM 2004 because SCORM 1.2 has almost no sequencing concept.

## 5. JavaScript timing and the SCORM API

The course launches, content renders, but the LMS shows the learner as incomplete even after they reach the end. The cause is almost always the SCORM API call timing.

The SCORM API is exposed by the LMS via a parent window or opener relationship. Your content has to find it before it can send any data. SCORM Cloud makes the API available immediately on load. Some LMSs delay it by a few hundred milliseconds while the launch frame initialises. If your content tries to call the API too early, it fails silently, and nothing gets sent.

**How to confirm:** open the LMS browser console. Look for errors like "API not found" or "LMSInitialize returned false". If you see these, the timing is the issue.

**How to fix:** wrap the SCORM API discovery in a retry loop with a short delay (50ms, up to 10 retries). Most well-built SCORM API wrappers do this by default. If your content is using a hand-rolled wrapper, replace it with a tested one.

## Two bonus causes that are less common but worth knowing

**Iframe sandboxing.** Some LMSs run SCORM content in a sandboxed iframe with restrictive permissions. If your content uses APIs that are blocked in sandboxes (clipboard, camera, fullscreen on certain browsers), it will fail. Workaround: detect the sandbox and provide a non-sandboxed fallback.

**Single sign-on issues.** Some LMSs hand off content launches via SSO redirects that strip query parameters. If your content reads the learner's ID or session token from the URL, it may be missing. Workaround: read these values from the SCORM API (`cmi.core.student_name`, `cmi.core.student_id`) rather than from the URL.

## The general debugging approach

When a package fails in the client's LMS, work through this checklist before you escalate:

First, open the LMS browser console while launching the course. Watch for errors. Most causes show themselves there.

Second, compare the SCORM Cloud launch and the LMS launch side by side. What is different? URL structure, parent window setup, query parameters, file path resolution. The difference is usually the cause.

Third, if you have access to the LMS server logs (rare, but ask), look at the file requests. 404s tell you the file path issue. 500s tell you a server-side processing issue.

Fourth, isolate. Make the smallest possible SCORM package that exhibits the problem. A single HTML file calling `LMSInitialize` and `LMSFinish`. If even that fails, the problem is at the LMS level, not in your content.

Fifth, only escalate to the client or LMS support after you have done the above. Vague "the package does not work" tickets get vague responses. Specific tickets with browser console output get useful responses.

## Where the packager fits

The [AI Learning Packager](https://packager.dtttech.com) was built with most of these gotchas already addressed. The manifest is SCORM 1.2 (sidestepping the version mismatch issue). All file names are lowercased. The included SCORM API wrapper handles the discovery timing. The manifest contains no sequencing rules to misfire.

If you are still hitting LMS-specific issues with a packager-built zip, the cause is almost certainly in the HTML content itself rather than in the packaging, and the debugging steps above will find it.

---

*Built by Michael at [Digital Technology Training](https://dtttech.com). If you have wrestled with a SCORM upload that worked in SCORM Cloud but not in production, [the packager](https://packager.dtttech.com) is in private beta. Request access below.*
