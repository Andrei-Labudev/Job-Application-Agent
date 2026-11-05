---
name: job-search-setup
description: First-time setup for the job-search kit. Interviews the user and creates their job-search folder (profile, search criteria, target companies, tracker). Use when the user says set up my job search, start the job search kit, or when another job-search skill finds the job-search folder missing or empty.
---

# Job Search Setup

This kit keeps everything personal in one folder of plain files, and keeps the method in the skills. Setup creates that folder and fills it with the user, conversationally.

## The data folder

Default location: `job-search/` in the user's working folder (Claude Code repo, a connected desktop folder, or a claude.ai Project). If the user already keeps these files somewhere else, use that location and tell them once where you found it.

```
job-search/
  profile.md            # career history, achievements, rules for presenting them (source of truth)
  criteria.md           # target roles, lanes, location, pay floor, level, exclusions, contact details
  target_companies.md   # curated companies + their job system (Greenhouse / Ashby / Lever / Workday / custom)
  application_tracker.md
  materials/            # tailored resume + cover-letter data and PDFs, one set per application
```

Blank templates for each file are in this skill's `templates/` folder. Copy them in, then fill them with the user.

**If you can't write files** (for example a claude.ai chat where the files live as Project knowledge), produce each finished file in full in the reply and ask the user to save it into the Project. Do the same after every later change.

## Steps

1. **Check what exists.** If `job-search/` already has filled files, don't overwrite them. Offer to update a specific file instead.
2. **Collect source material first.** Ask the user to attach or paste any of: current resume, LinkedIn profile export (PDF), past resumes, performance reviews or promotion write-ups, job descriptions they liked. Read everything before asking questions so you don't ask for what you already have.
3. **Build `profile.md`** from the material, then ask only about gaps:
   - exact titles and dates for each role (which source is canonical when they disagree)
   - 3–6 quantified results per role; never invent a number, ask
   - which roles or titles they want to lead with, and any titles they held informally
   - anything that must never appear (client names, confidential projects, internal codenames, people's names)
   - defaults: include Education? Certifications? How many years back?
   Put open questions in the **Known gaps** section rather than guessing.
4. **Build `criteria.md`** by asking, at most 4 questions at a time:
   - target role families, ranked into 2–4 "lanes" (top priority → selective backups) and what to deprioritize
   - location (city, remote, hybrid, onsite, relocation), travel tolerance
   - minimum base pay; what to answer in salary fields
   - level / years of experience; what counts as a stretch
   - hard exclusions (industries, platforms, role types)
   - contact details to use on applications (name, city, phone, email, LinkedIn); a dedicated job-search email is a good idea
   - working rules: apply only on the employer's own site? cover letter always? may Claude fill application forms (it never clicks Submit and never enters passwords)?
5. **Build `target_companies.md`**: ask for companies they already want, then suggest 20–40 more that fit the lanes and location. For each, find the job system:
   - Greenhouse: board token from `job-boards.greenhouse.io/<token>` or `boards.greenhouse.io/<token>`; confirm `https://boards-api.greenhouse.io/v1/boards/<token>/jobs` returns JSON.
   - Ashby: `jobs.ashbyhq.com/<board>`; confirm `https://api.ashbyhq.com/posting-api/job-board/<board>`.
   - Lever: `jobs.lever.co/<board>`; confirm `https://api.lever.co/v0/postings/<board>?mode=json`.
   - Workday: `<tenant>.wd<N>.myworkdayjobs.com/<site>`; record `tenant.wdN / site`.
   - Anything else: record the careers URL as "custom (search-based)".
   Put companies you couldn't confirm in the "Couldn't confirm" section.
6. **Create `application_tracker.md`** from the template (empty table).
7. **Make the personal profile skill** (offer it; do it unless the user declines). This turns `profile.md` into a `career-profile` skill that Claude loads automatically in any chat about resumes, cover letters or applications, even outside this folder or Project.
   - Run `python3 <this skill>/scripts/make_profile_skill.py job-search/profile.md job-search/profile-skill "<Full Name>"`.
   - Claude Code: copy `job-search/profile-skill/career-profile/` into `~/.claude/skills/` (ask before writing outside the working folder).
   - Claude app: send the user `career-profile.zip` and tell them to upload it under Customize → Skills → "+" → Upload a skill, and make sure it's toggled on.
   - `profile.md` stays the editable source. Whenever it changes (new role, promotion, corrected fact), re-run the script and reinstall / re-upload, replacing the old version. Remind the user of this whenever you update the profile.
   - The skill contains personal contact details and history: tell the user it's for them only, not for sharing.
8. **Finish** with a short summary of what's set up, the known gaps, and how to run things next: "run my job sweep", "apply to #2", "tailor my resume to this posting".

## Optional: daily sweep

If the user wants the sweep to run on its own (for example every weekday at 7am), set up a scheduled task with whatever scheduling the current Claude surface offers, with the prompt: "Run my job-search sweep using the job-search-sweep skill and send me the shortlist." Workday career sites usually need a real browser to search, so a cloud-only schedule will cover Greenhouse, Ashby and Lever reliably and Workday only partially; say so.
