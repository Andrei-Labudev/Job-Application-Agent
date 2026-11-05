---
name: job-search-sweep
description: Find, verify and rank new job openings that match the user's criteria by checking target companies' own job systems, dedupe against the application tracker, and present a shortlist with live apply links. Use when the user asks to run a job sweep, find new jobs, or check what's new.
---

# Job Search Sweep

Reads the user's `job-search/` folder (see `job-search-setup`). If `criteria.md` or `target_companies.md` is missing or still a blank template, stop and run `job-search-setup` first.

Inputs, read fresh every run:
- `job-search/criteria.md` — lanes, filters, application rules
- `job-search/target_companies.md` — where to look
- `job-search/application_tracker.md` — what's already been seen or applied to
- `job-search/profile.md` — for honest fit scoring

## Standing rules

- **Never send a dead link.** A role goes on the numbered shortlist only if it passed the live check below during this run.
- **Employer links only.** Aggregators (LinkedIn, Indeed, Built In, etc.) are fine for discovery, but always trace back to the employer's own posting and use the apply URL the employer's job system returns. Never build, guess or edit a job URL by hand.
- **Honest fit.** Score against `profile.md` only. Name real gaps; never paper over a hard requirement.
- Respect every exclusion and filter in `criteria.md`.

## 1. Read the tracker

Never re-surface a role marked Applied, Rejected, Dropped or Posting closed. Re-run the live check on rows marked Candidate or In progress: mark closed ones "Posting closed YYYY-MM-DD", and flag any Candidate unapplied for 7+ days as "apply now or drop".

If an email connector is available and the user uses a job-search inbox, search it for recruiter replies, confirmations, rejections and interview requests since the last sweep, and update statuses.

## 2. Sweep the target companies

For each row in `target_companies.md` (top lanes first, lower lanes selectively):

- **Greenhouse:** GET `https://boards-api.greenhouse.io/v1/boards/<board>/jobs?content=true`
- **Ashby:** GET `https://api.ashbyhq.com/posting-api/job-board/<board>?includeCompensation=true`
- **Lever:** GET `https://api.lever.co/v0/postings/<board>?mode=json`
- **Workday** (`tenant.wdN / site`): search needs a POST of `{"appliedFacets":{},"limit":20,"offset":0,"searchText":"<query>"}` to `https://<tenant>.<wdN>.myworkdayjobs.com/wday/cxs/<tenant>/<site>/jobs`. Plain fetch tools usually can't POST, so do this from a browser tab on that careers site when a browser tool is available; otherwise list Workday companies under "not checked this run". A single job can be confirmed with a GET on `https://<tenant>.<wdN>.myworkdayjobs.com/wday/cxs/<tenant>/<site>/job/<externalPath>`.
- **Custom sites:** targeted web searches for the lane titles at that company; keep a role only after confirming it on the company's own careers site.

Filter by title family, location, level and pay from `criteria.md`, then read the description to judge fit. Don't narrow by too many keywords; well-paid roles often have unexpected titles.

## 3. Discovery (secondary)

Run the discovery searches listed in `criteria.md` (and a few of your own for lane-1 titles + location). Anything good must still pass the live check on the employer's own system. When one does, suggest adding that company to `target_companies.md`.

## 4. Live check (required for every shortlisted role)

Use the job system's data API, not the HTML page and not an aggregator — cached pages have shown closed jobs as open.
- Greenhouse: `https://boards-api.greenhouse.io/v1/boards/<board>/jobs/<id>` returns the job, and the id appears in the board list. 404 or any error = not live.
- Ashby / Lever: the job id appears in the board API listing above.
- Workday: the per-job data URL returns the job, or the req appears in a browser search.
- Custom: the posting page loads, shows the job and an Apply button.

Unverified roles never get a number. List them in one line at the bottom ("Couldn't verify — check yourself": company + title only) and don't add them to the tracker.

Note: in some sandboxes shell `curl` to job sites is blocked; use the web-fetch tool instead.

## 5. Freshness

Find the posting date from the employer's data: Greenhouse `first_published` (not `updated_at`), Ashby `publishedAt`, Lever `createdAt` (epoch ms), Workday `postedOn`. If none, say "unknown" — never guess.

- **Fresh (0–7 days):** top priority; apply within 48–72 hours
- **Active (8–21):** normal priority
- **Aging (22–45):** only if fit is strong; suggest pairing with recruiter / hiring-manager outreach
- **Stale (45+):** near-miss line unless fit is exceptional, hard-to-fill senior role, or clearly re-posted

Rank by lane and fit first, then freshness.

## 6. Present the shortlist

0–8 verified roles, numbered, grouped or labeled by lane. For each:
- title, company, **apply link from the job system**
- location / work arrangement, pay (base vs OTE)
- posted date + age bucket, lane
- why it fits (2–3 strongest matches from the profile), real gaps
- "verified live <time>"

Then: one short line per near-miss (stale, deprioritized, just below the bar), the "Couldn't verify" line, Workday or other companies not checked this run, and suggested additions to the company list. If nothing clears the bar, say so — don't pad.

## 7. Update the tracker

Add each shortlisted role as a row with Status "Candidate (posted YYYY-MM-DD)" and date applied "—". If you can't write files, give the user the new rows to paste.

When the user picks a role ("apply to #3"), hand off to the `job-application` skill.
