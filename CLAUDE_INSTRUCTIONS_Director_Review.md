# CLAUDE SELF-INSTRUCTIONS — JV PULSE REPORT DIRECTOR REVIEW WORKBOOK
# Version: Poland 2026 reference build
# Upload this file at the start of every new country chat.
# Read it completely before doing anything else.

═══════════════════════════════════════════════════════════════════════════════
WHAT THIS IS
═══════════════════════════════════════════════════════════════════════════════

You are building the JV People & Culture Pulse Report Director Review workbook
for a new country. This is an Excel file with one tab per department plus a
Summary tab. It is used by country directors to review survey data and select
content for the final PDF report.

The workbook format is 100% controlled by build_country_pulse_report.py.
DO NOT write any openpyxl formatting code. DO NOT build the workbook any other
way. Your only job is to feed the script correct data.

═══════════════════════════════════════════════════════════════════════════════
FILES YOU HAVE BEEN GIVEN — VERIFY ALL ARE PRESENT BEFORE STARTING
═══════════════════════════════════════════════════════════════════════════════

  build_country_pulse_report.py          <- THE BUILD SCRIPT. Do not rewrite it.
  Survey_Basics__What___Why.xlsx         <- Interpretation text source
  Survey_Basics_Corrections.json         <- Manual lookup fixes from Poland
  [COUNTRY]_Raw_Data_[DATE].xlsx         <- Raw survey data for this country
  Poland_All_Departments_Director_Review.xlsx  <- Reference (target format)

If any file is missing, stop and ask before proceeding.

═══════════════════════════════════════════════════════════════════════════════
THE THREE THINGS YOU CHANGE IN THE SCRIPT
═══════════════════════════════════════════════════════════════════════════════

Open build_country_pulse_report.py and change ONLY these:

LINE 6:   COUNTRY = 'POLAND 2026'
          -> Change to e.g. COUNTRY = 'ROMANIA 2026'

LINE 4:   SB_PATH = '/mnt/user-data/uploads/Survey_Basics__What___Why.xlsx'
          -> Verify path matches where file was uploaded (usually correct as-is)

LINE 15:  CORRECTIONS_PATH = '/home/claude/Survey_Basics_Corrections.json'
          -> Change to '/mnt/user-data/uploads/Survey_Basics_Corrections.json'

NEAR BOTTOM (the combined.save line):
          path = os.path.join(OUT, 'Poland_All_Departments_Director_Review.xlsx')
          -> Change Poland to the new country name

That is all. Everything else in the script stays exactly as it is.

═══════════════════════════════════════════════════════════════════════════════
THE DEPTS LIST — WHAT YOU REPLACE
═══════════════════════════════════════════════════════════════════════════════

The DEPTS list (starting around line 563) contains all Poland data. Replace the
entire list with new country data. Keep the exact same Python dict structure.

Each department is one dict with this EXACT structure:

  {
    "name": "Human Resources",

    "avg": 3.24,
    # Mean of all FINAL scores (after burden inversion). Compute before writing.

    "status": "Watch",
    # Status from avg only: Healthy>=3.50 | Watch 2.50-3.49 | Concern<2.50
    # The script re-applies concern-count override automatically.

    "groups": [
      ("Human Resources", [
        (
          "HR",
          # Survey Basics sheet name. Must be exactly one of:
          # HR | L&D | L&C | MPD | Counseling | Women | Singles | Marriages | JVK

          "I believe that HR policies and decisions are applied fairly across the organization.",
          # LOOKUP text: drives the Survey Basics lookup.
          # Match the exact wording in Survey_Basics__What___Why.xlsx.
          # If SB uses a contraction ("I'm") use that here even if survey says "I am".

          "I believe that HR policies and decisions are applied fairly across the organization.",
          # DISPLAY text: shown in the workbook Column B.
          # For burden questions append " [Burden -- inverted]" at the end.

          2.52,
          # RAW mean score BEFORE burden inversion.
          # Compute: sum(SD*1 + D*2 + U*3 + A*4 + SA*5) / n

          False,
          # True = Burden question (negatively worded, higher agreement = worse).
          # Script applies final = 6 - raw for burden questions.

          [4, 5, 9, 3, 0],
          # Response counts [SD, D, U, A, SA] as integers.
          # Count directly from raw data. Must sum to n.
          # CRITICAL: wrong counts = wrong heatmap AND wrong DIST scoring.

          21,
          # n = number of respondents for this question.
        ),
        # ... more question tuples in same format
      ]),
    ],

    "strengths": [
      "Statement 1.",
      "Statement 2.",
    ],

    "growth": [
      "Statement 1.",
      "Statement 2.",
    ],

    "leadership": [
      "Question 1?",
      "Question 2?",
      "Question 3?",
      "Question 4?",
    ],
    # Always 4 questions. Directors choose 2.

    "quotes": [
      ("Growth Area", "Quote text verbatim.", "", None),
      # Format: (tag, quote_text, culture_label, translation_or_None)
      # tag: "Growth Area" or "Strength"
      # culture_label: "" for standard depts
      #                "1st Culture" or "2nd Culture" for JVK and L&C only
      # 4th element: English translation string if quote is in local language, else None
    ],

    "open_q": "What would make HR support more helpful to you?",
    # Exact survey question that generated the staff voice quotes.

    "lead_question": "Clarity and accessibility of HR processes, roles, and support.",
    # One sentence shown on Summary tab "Area to explore further" column.
  }

═══════════════════════════════════════════════════════════════════════════════
CULTURE GROUPS -- JVK AND L&C ONLY
═══════════════════════════════════════════════════════════════════════════════

JVK and L&C use MULTIPLE groups. All other depts use ONE group.

JVK (three groups -- include actual n in label string):
  "groups": [
    ("Second Culture Parents (n=6)", [ ...question tuples... ]),
    ("First Culture Parents (n=4)",  [ ...question tuples... ]),
    ("All Parents -- Shared Questions (n=10)", [ ...question tuples... ]),
  ],

L&C (two groups):
  "groups": [
    ("Second Culture Staff (n=5)",  [ ...question tuples... ]),
    ("First Culture Staff (n=12)", [ ...question tuples... ]),
  ],

JVK and L&C quotes MUST include culture_label (3rd element):
  ("Growth Area", "Quote text.", "2nd Culture", None)
  ("Growth Area", "Romanian text.", "1st Culture", "English translation.")

═══════════════════════════════════════════════════════════════════════════════
DEPARTMENT ORDER
═══════════════════════════════════════════════════════════════════════════════

Sort WORST to BEST -- lowest avg score first. Rank 1 = worst. Script assigns
rank in list order.

═══════════════════════════════════════════════════════════════════════════════
SCORING -- COMPUTE BEFORE WRITING DEPTS LIST
═══════════════════════════════════════════════════════════════════════════════

STEP 1 -- RAW MEAN
  raw = sum(SD*1 + D*2 + U*3 + A*4 + SA*5) / n
  Skip missing responses. Adjust n if respondents skipped a question.

STEP 2 -- BURDEN INVERSION
  If burden=True:  final_score = 6 - raw_mean
  If burden=False: final_score = raw_mean
  Put the RAW value in the tuple. Script inverts.

STEP 3 -- SCALE (check SCALE_MAP in the script, lines ~70-160)
  'mean' = personal/relational/emotional/formation questions
  'dist' = structural/process/access/awareness questions
  If n <= 5: always 'mean' regardless.
  If not in SCALE_MAP: default 'mean'.

  MEAN questions (how I feel, what I experience):
    emotional depletion, feeling connected, feeling valued, personal growth,
    professional growth, confidence, learning, thriving, isolation,
    carrying weight, navigating challenges

  DIST questions (is this available/accessible/clear):
    awareness of resources, clarity of process, knowing who to contact,
    access to tools, HR systems, MPD tools, counseling pathway,
    position focus clarity, financial reporting, uplink rhythms (L&D only)

STEP 4 -- STATUS PER QUESTION

  MEAN scale (applied to final_score after inversion):
    Healthy >= 3.50 | Watch 2.50-3.49 | Concern < 2.50

  DIST scale (applied to response counts):
    For non-burden: pos = (A+SA)/n * 100    neg = (SD+D)/n * 100
    For burden:     pos = (SD+D)/n * 100    neg = (A+SA)/n * 100

    Healthy = pos >= 75% AND neg <= 15%
    Watch   = pos >= 50% AND neg <= 30% AND neg does not outnumber pos
    Concern = pos < 50% OR neg > 30% OR neg outnumbers pos

STEP 5 -- DEPARTMENT STATUS
  avg = mean of all final_scores (all groups combined)
  Set "status" from avg using mean thresholds.
  Script auto-applies CONCERN-COUNT OVERRIDE:
    If 3+ questions score Concern -> dept status = Concern regardless of avg.

═══════════════════════════════════════════════════════════════════════════════
SURVEY BASICS LOOKUP -- HOW TO FIX "NOT FOUND"
═══════════════════════════════════════════════════════════════════════════════

The script normalises both strings and matches on 80 chars. The lookup text
(1st tuple element) drives this. Fix ALL "not found" before delivering.

FIX 1 -- Adjust the lookup text to match the SB spreadsheet exactly.
  Common mismatches: contractions, word order, extra/missing words.
  Open Survey_Basics__What___Why.xlsx and find the exact wording.

FIX 2 -- Survey_Basics_Corrections.json is loaded automatically. Check it first.

FIX 3 -- If question truly not in SB, add to MANUAL_INTERP in script (~line 57):
  "first 60 chars of lookup text (lowercase, no punctuation)": {
      'low':  'Concern-level interpretation.',
      'med':  'Watch-level interpretation.',
      'high': 'Healthy-level interpretation.',
  }

KNOWN CORRECTIONS ALREADY IN Survey_Basics_Corrections.json (from Poland):
  * Singles "I'm learning to navigate" -- SB uses "I'm" not "I am"
  * Women "Often I feel isolated" -- SB word order differs
  * Women "Our organization provides opportunities for women to encourage" -- NOT in SB, use MANUAL_INTERP
  * L&C "I know who to turn to for help with cultural or language learning" -- SB includes "cultural or"
  * JVK "I feel my children are cared for and supported by JV" -- SB text must be POSITIVE (Healthy)
  * HR "I believe that HR policies and decisions are applied fairly" -- must be Concern-level text

═══════════════════════════════════════════════════════════════════════════════
WRITING RULES -- STRENGTHS
═══════════════════════════════════════════════════════════════════════════════

Observational. Describe what staff report. Not verdicts. 3-5 per department.

GOOD: "The majority of staff report feeling noticed and cared for by the team."
BAD:  "Staff are cared for."  <- verdict

GOOD: "Staff report a working knowledge of JV policies and procedures."
BAD:  "HR is doing well."  <- too vague

═══════════════════════════════════════════════════════════════════════════════
WRITING RULES -- GROWTH AREAS
═══════════════════════════════════════════════════════════════════════════════

Inquiry framing. Signal what needs attention. Never render a verdict. 3-5 per dept.

ALWAYS USE:
  "warrants direct exploration"                  NOT "is broken"
  "not being experienced consistently"           NOT "does not exist"
  "reflects patterns that need closer attention" NOT "is failing"
  "at risk of being overlooked"                  NOT "is being overlooked"
  "could be strengthened"                        NOT "is weak"

GOOD: "HR processes are not consistently experienced as clear or easy to navigate."
BAD:  "HR processes are broken."

═══════════════════════════════════════════════════════════════════════════════
WRITING RULES -- LEADERSHIP QUESTIONS  <- MOST CRITICAL
═══════════════════════════════════════════════════════════════════════════════

QUESTIONS MUST NEVER ASSUME THE STAFF PERCEPTION IS CONFIRMED REALITY.
Write as genuine inquiry. Test every question: "Does this assume the perception
is accurate?" If yes -- rewrite it.

WRONG: "What concrete steps does your team take to share the load with singles?"
       Assumes load is NOT being shared. Positions leader as guilty.

RIGHT: "How does your team engage with single staff to understand what they carry
        and whether they need more support?"
       Opens inquiry without assuming the answer.

WRONG: "Why is the counseling process not clear to staff?"
RIGHT: "Could you explain JV's counseling process clearly to a staff member who
        asks today? If not, that is the starting point."

Write 4 questions per department. Directors choose 2.

═══════════════════════════════════════════════════════════════════════════════
QUOTES
═══════════════════════════════════════════════════════════════════════════════

* Include 5-8 per department. Directors reduce to their preferred set.
* Keep verbatim. Do not paraphrase, correct grammar, or clean up.
* Local language quotes: include English translation as 4th tuple element.
* Tag each "Growth Area" or "Strength" based on content.
* JVK and L&C: always include culture label ("1st Culture" or "2nd Culture").
* All other depts: culture_label = "" and translation = None.

Tuple format:
  Standard:     ("Growth Area", "English quote.", "", None)
  With trans:   ("Growth Area", "Romanian text.", "", "English translation.")
  Culture tag:  ("Growth Area", "Quote text.", "2nd Culture", None)
  Both:         ("Growth Area", "Romanian text.", "2nd Culture", "English translation.")

═══════════════════════════════════════════════════════════════════════════════
RUNNING THE SCRIPT
═══════════════════════════════════════════════════════════════════════════════

  python3 build_country_pulse_report.py

Output: /mnt/user-data/outputs/[COUNTRY]_All_Departments_Director_Review.xlsx

If any error occurs, read the error and fix the data -- do not rewrite the script.

═══════════════════════════════════════════════════════════════════════════════
QA CHECKLIST -- CHECK EVERY ITEM BEFORE DELIVERING
═══════════════════════════════════════════════════════════════════════════════

Open the output file and verify against Poland reference workbook:

[ ] Summary tab is first. All departments listed worst to best.
[ ] Every department has a tab.
[ ] Tab colours: green=Healthy, yellow=Watch, red=Concern.
[ ] Row 1: navy bar with country name and department name in CAPS.
[ ] Row 2: navy bar with score, status, n, rank.
[ ] Freeze panes at C3 on every department tab.
[ ] Grid lines hidden on every tab.
[ ] Section 1 questions sorted worst to best within each group.
[ ] NO cell shows "[Survey Basics text not found]". Fix all.
[ ] Burden questions: Col A = "Burden [inv.]" in amber. Display text has "[Burden -- inverted]".
[ ] Heatmap columns J-P: percentage and count shown, blue gradient by intensity.
[ ] Section 2 Strengths: green fill rows. Col F and G are yellow input cells.
[ ] Section 3 Growth Areas: amber fill rows. Col F and G are yellow input cells.
[ ] Section 4 Leadership Questions: 4 drafted + 2 blank write-in rows at bottom.
[ ] Section 5 Quotes: open_q prompt shown above quotes. One quote per row.
[ ] JVK and L&C: culture group label rows between groups.
[ ] JVK/L&C quotes: Col D shows "1st Culture" or "2nd Culture" colour-coded.
[ ] Translated quotes: both languages in one cell with "Translation:" label.
[ ] Summary tab "Area to explore further" matches lead_question for each dept.
[ ] Status on Summary tab reflects concern-count override if triggered.
[ ] Structure and layout identical to Poland reference. Only data differs.

═══════════════════════════════════════════════════════════════════════════════
WHAT THE SCRIPT BUILDS AUTOMATICALLY -- DO NOT ADD CODE FOR THESE
═══════════════════════════════════════════════════════════════════════════════

Column widths | Row heights | Freeze panes | Section header bars
Score colour coding | Heatmap (from SD/D/U/A/SA counts) | Burden amber styling
Input cell yellow fill | Culture tag colours | Write-in rows in Section 4
Summary tab structure | Tab colour coding | Concern-count override
Question sort order (worst to best) | Survey Basics lookup and text population

═══════════════════════════════════════════════════════════════════════════════
END OF INSTRUCTIONS
═══════════════════════════════════════════════════════════════════════════════
