"""
Turn job-search/profile.md into a personal `career-profile` skill that loads
automatically whenever the user drafts a resume, cover letter or application.

  python3 make_profile_skill.py <profile.md> <output_dir> "<Full Name>"

Creates:
  <output_dir>/career-profile/SKILL.md   (copy this folder into ~/.claude/skills/ for Claude Code)
  <output_dir>/career-profile.zip        (upload in the Claude app: Customize > Skills > Upload a skill)

Re-run it whenever profile.md changes, then reinstall / re-upload.
"""

import os
import re
import sys
import zipfile

HOW_TO_USE = """\
## How to use this skill

- This is {name}'s career source of truth. Use only facts written here; never invent metrics, titles, dates, certifications or responsibilities.
- When tailoring to a job posting, pick the 3–5 most relevant bullets per role and reword them toward the posting's keywords while keeping the underlying fact the same.
- Follow every presentation rule and "never name" rule below.
- Check "Known gaps" before finalizing anything and ask {first} rather than guessing.
- If {first} gives new facts in chat, use them, and remind them to add them to `job-search/profile.md` and rebuild this skill so they aren't lost.
- For building the PDFs and the application workflow, use the `job-application` skill.

---

"""


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    src, out_dir, name = sys.argv[1], sys.argv[2], sys.argv[3].strip()
    with open(src, encoding="utf-8") as f:
        profile = f.read().strip()

    if re.search(r"<[A-Z][^>]*>", profile) and "<Your Name>" in profile:
        print("profile.md still looks like the blank template — fill it in first.")
        return 1

    first = name.split()[0]
    safe = name.replace('"', "'")
    description = (
        f"{safe}'s career history, quantified achievements, skills and presentation rules. "
        f"Use whenever drafting or tailoring a resume, cover letter, LinkedIn summary, "
        f"interview answer or job application answer for {first}."
    )
    skill_md = (
        "---\n"
        "name: career-profile\n"
        f'description: "{description}"\n'
        "---\n\n"
        + HOW_TO_USE.format(name=name, first=first)
        + profile
        + "\n"
    )

    skill_dir = os.path.join(out_dir, "career-profile")
    os.makedirs(skill_dir, exist_ok=True)
    skill_path = os.path.join(skill_dir, "SKILL.md")
    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(skill_md)

    zip_path = os.path.join(out_dir, "career-profile.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(skill_path, "career-profile/SKILL.md")

    print(f"Wrote {skill_path}")
    print(f"Wrote {zip_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
