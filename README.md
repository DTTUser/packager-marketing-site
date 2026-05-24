# packager.dtttech.com

The marketing site for the AI Learning Packager. One static HTML page plus a thank-you page, deployed on Netlify, with email capture via Netlify Forms.

## What is here

```
Marketing_Site/
  index.html      The landing page
  thanks.html     Where the form redirects after a successful signup
  README.md       This file
```

That is the whole site. No build step, no dependencies, no framework.

## How to deploy it

The plan is to host this on Netlify at the custom domain `packager.dtttech.com`. The steps below assume you have a Netlify account and access to the DNS for `dtttech.com`.

### 1. Create a GitHub repo

```bash
cd /Users/michaelosullivan/Desktop/Cowork/SCORM\ wrapper\ for\ Vibe\ Code/Marketing_Site
git init
git add .
git commit -m "Initial landing page for AI Learning Packager"
gh repo create DTTUser/packager-marketing-site --public --source=. --push
```

If you do not have `gh` installed, create the repo on github.com first, then:

```bash
git remote add origin https://github.com/DTTUser/packager-marketing-site.git
git branch -M main
git push -u origin main
```

### 2. Connect it to Netlify

1. Sign in to Netlify.
2. Click "Add new site" then "Import an existing project".
3. Choose GitHub, then pick `packager-marketing-site`.
4. Leave build command blank, set publish directory to `.` (the root), and click Deploy.
5. Netlify will give the site a temporary URL like `random-name-12345.netlify.app`. Open it and confirm the page loads and the form is visible.

### 3. Point packager.dtttech.com at the site

In Netlify, on the new site:

1. Go to "Site configuration" then "Domain management".
2. Click "Add a domain", enter `packager.dtttech.com`, and follow the prompts.

In your DNS provider (the one that controls `dtttech.com`):

1. Add a CNAME record:
   - Name: `packager`
   - Value: the `*.netlify.app` URL Netlify gave you, without the leading `https://`
   - TTL: 3600 (or whatever the default is)

DNS usually propagates within an hour. Netlify will issue a free Let's Encrypt SSL certificate automatically once it sees the domain pointed correctly.

### 4. Verify Netlify Forms is collecting signups

1. Open the live site, fill in the email form, click "Request access".
2. You should land on `thanks.html`.
3. In Netlify, go to "Forms" in the left sidebar. You should see the `early-access` form listed, with one submission.
4. Click into the form to see the email address.

If the form does not appear in Netlify, the most common cause is that the hidden `<input type="hidden" name="form-name" value="early-access">` field was removed from the HTML. That hidden field is what tells Netlify which form was submitted.

## How to make edits later

The site is plain HTML and CSS in `index.html`. To change copy, open the file, edit the text inside the tags, save, and push to GitHub. Netlify auto-deploys on push.

To add a new section, copy one of the existing `<section>` blocks and adapt the contents. The CSS uses utility-style variables for colours; the palette is at the top of the `<style>` block in `index.html`.

## Notes on Netlify Forms

- The free tier allows 100 submissions per month per site, which is plenty for a private beta.
- Submissions are stored in Netlify's dashboard. You can also forward them to an email address via "Form notifications".
- The honeypot field (`bot-field`) catches naive spam bots. If real spam becomes a problem, add reCAPTCHA by replacing `data-netlify-honeypot="bot-field"` with `data-netlify-recaptcha="true"` and following Netlify's instructions.

## When to consider an upgrade

This setup is deliberately minimal. Reconsider when any of these are true:

- You want to send a real newsletter to signups. Move the list to ConvertKit, Mailchimp, or Buttondown and replace the Netlify form with their embed code.
- You have more than one blog post and editing them by hand is annoying. Migrate to a static site generator like Astro or Eleventy.
- The site grows beyond five or six pages. Same recommendation as above.

Until then, this is the right amount of tool.
