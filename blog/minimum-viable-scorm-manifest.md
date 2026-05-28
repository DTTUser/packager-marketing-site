---
title: The minimum viable SCORM manifest, explained line by line
description: A walk through the smallest valid SCORM 1.2 imsmanifest.xml, with every element explained.
og_description: The minimum SCORM 1.2 manifest, line by line. No fluff, no historical detours.
slug: minimum-viable-scorm-manifest
date: 23 June 2026
read_time: 9 minutes
lede: The smallest valid SCORM 1.2 imsmanifest, explained without the historical detours.
---

## Why bother reading this

If you use an authoring tool, the SCORM manifest is generated for you and you may never look at it. That works until it does not. The day a client LMS rejects your package with "manifest invalid" and no further detail, you are going to want to know what the manifest actually says.

This post walks through the smallest possible valid SCORM 1.2 imsmanifest.xml, line by line. It is the file the AI Learning Packager generates by default. Read this once and you can debug almost any SCORM 1.2 packaging problem.

## The full file

Here is the whole thing, minus content-specific values:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="com.example.course1"
          version="1.0"
          xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
          xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd
                              http://www.imsglobal.org/xsd/imsmd_rootv1p2p1 imsmd_rootv1p2p1.xsd
                              http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd">
  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>1.2</schemaversion>
  </metadata>
  <organizations default="ORG-1">
    <organization identifier="ORG-1">
      <title>Course Title Here</title>
      <item identifier="ITEM-1" identifierref="RES-1">
        <title>Course Title Here</title>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES-1"
              type="webcontent"
              adlcp:scormtype="sco"
              href="index.html">
      <file href="index.html"/>
    </resource>
  </resources>
</manifest>
```

That is the entire valid SCORM 1.2 manifest. About 25 lines. Now let us walk it.

## Line by line

### The XML declaration

```xml
<?xml version="1.0" encoding="UTF-8"?>
```

Standard XML preamble. The encoding must be `UTF-8`. Some LMSs choke on other encodings. The version must be 1.0 (this is the XML version, not the SCORM version).

### The manifest element

```xml
<manifest identifier="com.example.course1"
          version="1.0"
          xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
          xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="...">
```

The `manifest` element is the root of the document. A few things matter:

`identifier` is a globally unique identifier for this package. The convention is reverse-DNS (`com.dtttech.scorm-intro-101`) but any unique string works. The LMS uses this to recognise the package on re-upload.

`version` is the version of this package (your version, not the SCORM version). Increment it when you re-publish. Some LMSs will reject re-uploads with the same version, others will re-import without warning.

The four namespace declarations (`xmlns:...`) point to the XML schemas the manifest conforms to. Do not change these. They look ugly but they are what makes the file valid.

`xsi:schemaLocation` lists the same schemas plus their physical .xsd filenames. These .xsd files do not need to be in the package, the LMS will use its own copies, but their names must match the spec. Again, do not change.

### The metadata block

```xml
<metadata>
  <schema>ADL SCORM</schema>
  <schemaversion>1.2</schemaversion>
</metadata>
```

This is where you declare which SCORM version the package targets. `1.2` is what you want for SCORM 1.2. For SCORM 2004 you would write `2004 3rd Edition` or similar.

Note: the `schemaversion` element is what most LMSs actually read to decide which SCORM API to expose. If you say "1.2" here but your content calls SCORM 2004 APIs, you will get silent failures.

### Organizations

```xml
<organizations default="ORG-1">
  <organization identifier="ORG-1">
    <title>Course Title Here</title>
    <item identifier="ITEM-1" identifierref="RES-1">
      <title>Course Title Here</title>
    </item>
  </organization>
</organizations>
```

The `organizations` element describes the structure the LMS will show in its menu or table of contents. Even if your course is a single page, you still need this.

`default="ORG-1"` says which organization to use if there are multiple. There is almost never more than one. Just match this attribute to the identifier of your single organization.

Inside the `organization` element, the `title` is what shows in the LMS course catalogue. Make this descriptive and unique. "Course Title Here" is fine for development, useless in production.

The `item` element is a single launchable thing inside the organization. For a single-page SCORM, you have one item. For a multi-module SCORM, you would have nested items.

`identifierref="RES-1"` is the critical link. It connects this item to a resource (a file or set of files) defined further down. Get this wrong and the LMS will not know what to launch.

### Resources

```xml
<resources>
  <resource identifier="RES-1"
            type="webcontent"
            adlcp:scormtype="sco"
            href="index.html">
    <file href="index.html"/>
  </resource>
</resources>
```

This is where the actual files in the package are declared.

`identifier="RES-1"` must match the `identifierref` from the item above. The two link the menu structure to the actual content.

`type="webcontent"` tells the LMS this is HTML (rather than, say, a downloadable PDF or an external asset). Almost always `webcontent`.

`adlcp:scormtype="sco"` is the most important attribute on this element. `sco` means "Shareable Content Object", which means the content will talk back to the LMS via the SCORM API. The other option is `asset`, which means the content is dumb (just a file, no API calls). If you want completion tracking, you want `sco`. If you change this to `asset`, the LMS will not even try to listen for completion calls.

`href="index.html"` is the file the LMS launches when the learner clicks the course. This is your entry point.

The nested `file` element lists every file in the package. Strictly speaking, SCORM 1.2 only requires the entry point file to be listed. In practice, listing all of them is safer because some LMSs use this list to decide what to extract or serve. If your package has CSS, JS, images, video, list them all here.

## What you can leave out

The above is the minimum. SCORM 1.2 allows much more, but you do not need any of it for a working package:

You do not need sequencing rules. SCORM 1.2 has almost none, and what little exists is rarely useful for single-SCO packages.

You do not need detailed metadata (author, date, copyright). The LMS will not show most of it, and what it does show comes from its own course catalogue rather than the manifest.

You do not need multiple organizations. One is fine.

You do not need multiple resources unless you have multiple launchable items.

You do not need imsss namespaces (those are for SCORM 2004 sequencing).

The temptation when writing a manifest by hand is to add every possible attribute "just in case". Resist it. Extra attributes mean extra surface area for the LMS to misinterpret.

## What you cannot leave out

Five things, in order of how badly the package breaks if they are missing:

The `<resource>` with the correct `href` and `adlcp:scormtype="sco"`. Without this, the package will not launch.

The `<schemaversion>1.2</schemaversion>` (or equivalent for other SCORM versions). Without this, the LMS does not know which API to provide.

The matching `identifierref` linking item to resource. Without this, the LMS does not know what to launch.

The four XML namespaces on the `manifest` element. Without these, the manifest is not technically valid SCORM, and strict LMSs will reject it.

The `<title>` inside the organization. Without this, the course appears nameless in the LMS catalogue. Some LMSs will refuse to import a course with no title.

## Why the packager generates exactly this

The [AI Learning Packager](https://packager.dtttech.com) generates a manifest that matches the above almost line for line. The reasons:

It is the smallest valid SCORM 1.2 manifest. Smaller is better because there is less for an LMS to misinterpret.

It uses sensible defaults for the values it does include (UTF-8, version 1.0, lowercased identifiers based on the package name).

It lists every file in the resource so LMSs that use the file list for extraction get the full set.

It does not include sequencing, metadata, or anything optional. If your content needs more, you can edit the manifest after generation.

That last point is worth highlighting. The packager's output is not a black box. The manifest is a plain text file in the zip. Open it, edit it, regenerate the zip. The wrapper does not stop you from going deeper than the defaults if you need to.

---

*Built by Michael at [Digital Technology Training](https://dtttech.com). The [AI Learning Packager](https://packager.dtttech.com) is in private beta. Request access below.*
