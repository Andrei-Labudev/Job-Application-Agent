# Job-Application-Agent

This repository stores AI skills to help you set up a career profile and use AI agents to help you search and apply for jobs.

It's three Claude skills that turn Claude into a job-search assistant. It learns your background once, checks your target companies' own job systems for new openings, confirms every link is still live, and builds a tailored one-page resume and cover letter for any role you pick.

> **The easy way:** start a new chat with Claude, paste this repo's link, and say **"Help me set this up."** Claude reads this README and walks you through everything below, one step at a time.

| Skill | What it does | Say something like |
|---|---|---|
| `job-search-setup` | Interviews you and builds your `job-search/` folder: profile, criteria, target companies, tracker | "Set up my job search" |
| `job-search-sweep` | Checks your target companies (Greenhouse, Ashby, Lever, Workday, careers sites), confirms postings are live, ranks a shortlist, updates the tracker | "Run my job sweep" |
| `job-application` | Tailored ATS-friendly resume and cover letter PDFs, screening answers, optional form filling (never clicks Submit) | "Apply to #2" / "Tailor my resume to this posting: &lt;link&gt;" |

Your personal data lives in plain files you own (`job-search/`), not in the skills, so the skills stay shareable and you can edit your data any time.

At the end of setup, Claude also turns your finished profile into your own **`career-profile` skill**, so it knows your experience in any chat about resumes or applications. Keep that one to yourself: it has your contact details and history. **Never commit it, or your `job-search/` folder, to a public repo.**

## Before you start

Setup takes about 30–45 minutes, most of it Claude interviewing you about your experience. After that, finding jobs and building an application takes a few minutes each.

Have these ready:
- A Claude account. Skills work on Free, Pro, Max, Team and Enterprise plans.
- Your current resume, and your LinkedIn profile as a PDF (LinkedIn: your profile → More → Save to PDF).
- Optional: older resumes, performance reviews or promotion write-ups, and two or three job postings you'd love to land.
- Optional: a separate email address just for job applications.

Then follow **either** Option A (Claude app) **or** Option B (Claude Code), not both.

## Get the files

On this page, click **Code → Download ZIP** and unzip it. Or, if you use git:

```bash
git clone https://github.com/Andrei-Labudev/Job-Application-Agent.git
```

## Option A: Install in the Claude app (claude.ai or desktop)

Do the install on a computer; the phone app works for daily use afterwards.

1. **Turn on file creation.** Settings → Capabilities → switch on "Code execution and file creation" (it may be called "Create and edit files"). On a Team or Enterprise plan, your admin may need to allow skills first.
2. **Upload the three skills.** Customize → Skills → **+** → **Create skill → Upload a skill**, and pick one zip from the `claude-ai-uploads/` folder. Repeat for all three:
   - `job-search-setup.zip`
   - `job-search-sweep.zip`
   - `job-application.zip`
3. **Check they're on.** All three should appear in your skills list with the toggle switched on.
4. **Create a Project** called "Job Search" (Projects in the sidebar → New project). Your profile, criteria and tracker will live there.
5. **Desktop app only (recommended):** if your desktop app lets you connect a folder on your computer, connect an empty one such as `Documents/Job Search`. Claude can then save and update your files there by itself.

Without a connected folder, Claude can't edit Project files directly. It hands you each finished file; add it to the Project's files, and after each sweep paste in the tracker updates it gives you.

## Option B: Install in Claude Code (terminal or IDE)

From inside the downloaded folder:

```bash
# 1. Copy the skills so they work in every project
mkdir -p ~/.claude/skills
cp -R skills/* ~/.claude/skills/
#    (or copy into <some-project>/.claude/skills/ to keep them in one project)

# 2. Install the PDF libraries (needs Python 3)
pip install reportlab pypdf

# 3. Make a folder for your job search and start Claude Code there
mkdir -p ~/job-search-home && cd ~/job-search-home
claude
```

Type `/` and check that `job-search-setup`, `job-search-sweep` and `job-application` appear. If they don't, restart Claude Code.

## First run: set up your job search

Open a new chat in your Job Search Project (or Claude Code in your job-search folder) and say **"Set up my job search."** Answer in plain language; say "skip" or "not sure" whenever you need to.

1. **Hand over your material.** Attach your resume, LinkedIn PDF and anything else you gathered.
2. **Fill the gaps in your profile.** Claude drafts your work history and asks only about what's missing: exact dates, the numbers behind your achievements, which titles to lead with, and anything that must never appear (client names, confidential projects). It never invents an achievement; anything uncertain goes in a "Known gaps" list.
3. **Set your search criteria:** the kinds of roles you want (ranked), location and remote preference, minimum base pay, seniority, exclusions, the contact details for applications, and whether Claude may fill application forms for you.
4. **Build your company list.** Name companies you like; Claude suggests more and finds the job system each one uses, so it can check openings directly.
5. **Create your tracker,** an empty table of applications.
6. **Install your personal profile skill.** Claude turns your profile into `career-profile`.
   - Claude app: Claude gives you `career-profile.zip`; upload it under Customize → Skills like the others.
   - Claude Code: Claude asks permission, then copies it into `~/.claude/skills/`.

When setup finishes you'll have:

| File | What's in it | You edit it when… |
|---|---|---|
| `profile.md` | Your full career history and rules for presenting it | You get a new role, promotion or result |
| `criteria.md` | What you're looking for and your application rules | Your targets, pay floor or location change |
| `target_companies.md` | Companies to check and their job systems | You want to add or drop a company |
| `application_tracker.md` | Every role found, applied to, closed or rejected | Rarely; Claude keeps it current |

Read `profile.md` once yourself. Every resume is built from it, so a wrong date there ends up everywhere.

## Everyday use

| Say | What happens |
|---|---|
| "Run my job sweep" | Claude checks every company on your list, confirms each posting is open on the employer's own site, and gives you a numbered shortlist: link, pay, location, posting age, why you fit, and your real gaps. New roles go into your tracker. |
| "Apply to #2" | The employer's apply link, a tailored one-page resume PDF and a cover letter PDF, together. Look them over before using them. |
| "Fill in the application for #2" | Only if you allowed it in setup and Claude has a browser tool. Claude fills the form and stops before Submit; you check it, create any account or password yourself, and submit. |
| "I applied to #2" | The tracker row is marked Applied with today's date. |

Habits that help:
- **Apply to fresh postings fast.** Roles under a week old are marked Fresh; aim to apply within two or three days.
- **Tell Claude about replies** ("Acme rejected me", "I have an interview with Beta Co") so the tracker stays right.
- **When your experience changes,** say "Add this to my profile: …", then "Rebuild my profile skill", and reinstall `career-profile`.
- **Other writing works too:** screening questions, a LinkedIn summary, or a resume for a posting you found yourself.

## Optional extras

- **Daily automatic sweep:** ask "Schedule my job sweep every weekday at 7am", where your Claude plan supports scheduled tasks.
- **Workday companies** (many big employers use Workday) can only be searched in a browser. Connect Claude in Chrome or use the desktop app's browser and the sweep covers them; otherwise they're listed as "not checked".
- **Email:** connect your job-search inbox (for example the Gmail connector) and the sweep also picks up confirmations, rejections and interview requests.

## Troubleshooting

| Problem | Fix |
|---|---|
| Claude doesn't seem to use the skills | Check they're toggled on (Customize → Skills), or that the folders sit directly in `~/.claude/skills/`. Start a new chat. |
| Upload option missing in the app | Turn on code execution in Settings → Capabilities. On Team or Enterprise, ask your admin to allow skills. |
| The PDF doesn't build in Claude Code | Run `pip install reportlab pypdf`, then ask again. |
| A resume runs past one page | Claude trims the least relevant bullets automatically; ask for a shorter version if it still feels crowded. |
| A fact on the resume is wrong | Correct it in `profile.md` (or tell Claude to), then rebuild your profile skill. |
| The shortlist is empty | Nothing cleared your bar today. Widen `criteria.md` or add companies to `target_companies.md`. |

## What's inside

```
skills/
  job-search-setup/   SKILL.md, templates/ (profile, criteria, companies, tracker), scripts/ (profile-skill builder)
  job-search-sweep/   SKILL.md
  job-application/    SKILL.md, scripts/ (PDF builders), examples/ (sample JSON for a fictional person)
claude-ai-uploads/    one zip per skill, for uploading in the Claude app
```

## Instructions for Claude

If someone shared this repo with you and asked for help setting it up, guide them one step at a time:

1. **Find out where they are.** Ask whether they use the Claude app (claude.ai, desktop or phone) or Claude Code, unless your own tools already tell you.
2. **Claude app:** you can't change their settings or upload skills for them. Coach them through Option A one step at a time, waiting for them to confirm each step. If they're on a phone, suggest switching to a computer for the install. If they want to try before installing, read the SKILL.md files in `skills/` and follow `job-search-setup` in the chat, and tell them it lasts only for that conversation.
3. **Claude Code:** do Option B yourself. Ask before each step that writes outside the current folder, then ask them to restart Claude Code in their job-search folder.
4. **Start setup.** Once the skills are installed, start a fresh chat (the "Job Search" Project in the app, or the working folder in Claude Code) and run `job-search-setup`, including building their personal `career-profile` skill at the end.
5. **Wrap up** by showing them the "Everyday use" requests.

Keep each message short and give one step at a time. Never ask for passwords, and never put their personal files in a public repo.

## License

MIT. See [LICENSE](LICENSE).
