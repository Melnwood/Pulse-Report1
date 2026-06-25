# JV PULSE REPORT — MASTER BUILD INSTRUCTIONS
# For Claude. Upload this file at the start of every new country chat.
# This covers everything needed to build the Director Review workbook AND
# the PDF Pulse Report identically to Poland, with zero questions.
#
# Last updated: Poland 2026 reference build
# Covers: Director Review (Excel) + PDF Report + Scoring + Writing + QA

════════════════════════════════════════════════════════════════════════════════
PART 0 — WHAT YOU ARE BUILDING AND HOW
════════════════════════════════════════════════════════════════════════════════

You are building two outputs for a new JV country:

OUTPUT 1: Director Review workbook (.xlsx)
  One Excel tab per department + a Summary tab.
  Sent to country directors to review and select content.
  Built by running build_country_pulse_report.py with updated data.

OUTPUT 2: PDF Pulse Report (.pdf)
  One page per department + summary page.
  Built by writing and running a Python script that generates HTML
  rendered to PDF via weasyprint.

THE RULE THAT OVERRIDES EVERYTHING:
  Do not rewrite the formatting engine in build_country_pulse_report.py.
  Do not build the Excel workbook manually with openpyxl formatting commands.
  Do not build the PDF by hand.
  Your job is to extract data from the raw survey file, compute scores
  correctly, populate the DEPTS list in the script, and run it.
  The script produces the workbook. The formatting is already correct.

════════════════════════════════════════════════════════════════════════════════
PART 1 — FILES NEEDED. VERIFY ALL ARE PRESENT BEFORE STARTING.
════════════════════════════════════════════════════════════════════════════════

For the Director Review workbook:
  build_country_pulse_report.py          <- THE build script. Do not rewrite.
  Survey_Basics__What___Why.xlsx         <- Source of interpretation text
  Survey_Basics_Corrections.json         <- Manual lookup fixes from Poland
  [COUNTRY]_Raw_Data_[DATE].xlsx         <- Raw survey export for this country
  Poland_All_Departments_Director_Review.xlsx  <- Visual reference only

For the PDF Report (after director review is returned):
  [COUNTRY]_All_Departments_Director_Review.xlsx  <- Completed director review
  Poland_Pulse_Report_2026.pdf                    <- Visual reference only

If any file is missing, stop and ask before proceeding.

════════════════════════════════════════════════════════════════════════════════
PART 2 — READING THE RAW SURVEY DATA
════════════════════════════════════════════════════════════════════════════════

Open [COUNTRY]_Raw_Data_[DATE].xlsx and identify:

1. The column that contains department assignment for each respondent.
2. The list of departments present in this country's data.
3. For each department, the list of survey questions.
4. For each question, for each respondent: their response (1-5 or SD/D/U/A/SA).
5. Which questions are Burden questions (negatively worded).
   Clue: burden questions contain words like "feel alone", "feel depleted",
   "feel confused", "feel isolated", "feel unsure", "feel overwhelmed",
   "distracts me", "too depleted", "needs are overlooked", "feel disconnected".
6. The open-ended staff voice responses for each department.
7. n per department (count of respondents with complete responses).

RESPONSE VALUE MAPPING:
  Strongly Disagree = 1
  Disagree = 2
  Unsure / Neutral = 3
  Agree = 4
  Strongly Agree = 5

If the export uses text labels instead of numbers, map them as above.
If a respondent skipped a question, exclude them from n for that question.

════════════════════════════════════════════════════════════════════════════════
PART 3 — COMPLETE SCORING SYSTEM
════════════════════════════════════════════════════════════════════════════════

STEP 3.1 — COMPUTE RAW MEAN

  raw_mean = (SD×1 + D×2 + U×3 + A×4 + SA×5) / n

  where n = number of respondents who answered this specific question.
  Record [SD, D, U, A, SA] as integer counts. They must sum to n.
  These counts go in the DEPTS tuple exactly as-is regardless of burden.

STEP 3.2 — BURDEN INVERSION

  Burden questions are negatively worded. High agreement = worse experience.
  The script inverts them automatically using: final = 6 - raw_mean
  You record the RAW mean in the tuple. The script does the inversion.

  If burden=True:  final_score = 6 - raw_mean   (script applies this)
  If burden=False: final_score = raw_mean

  Append " [Burden — inverted]" to the display text for burden questions.
  Example: "I often feel depleted... [Burden — inverted]"

STEP 3.3 — DETERMINE SCALE: MEAN or DIST

  SMALL N OVERRIDE: If n <= 5, ALWAYS use MEAN. No exceptions.

  Otherwise look up the question in the SCALE_MAP below.
  If not found, default to MEAN.

  MEAN = personal/relational/emotional questions (how I feel, what I experience)
  DIST = structural/access/process questions (is this available, do I have access)

  COMPLETE SCALE_MAP — match by substring (first 40+ chars of question text):

  SINGLES
    "I have access to resources that address the unique needs"            -> DIST
    "I have a clear understanding of what is expected of me in ministry" -> DIST
    "My practical needs as a single (housing, financial, social)"        -> DIST
    "I feel my singleness is respected and valued"                       -> MEAN
    "I am learning to navigate my singleness"                            -> MEAN
    "I feel relationally connected to my team and community as a single" -> MEAN
    "I see my gifts and opportunities as a single person"                -> MEAN
    "I have safe people I can turn to for support"                       -> MEAN
    "I sometimes feel the weight of carrying ministry responsibilities"  -> MEAN
    "I sometimes feel emotionally or spiritually depleted"               -> MEAN

  HUMAN RESOURCES
    "I believe that HR policies and decisions are applied fairly"        -> DIST
    "HR processes and systems are clear and efficient"                   -> DIST
    "I often feel unsure about my place within the organization"         -> DIST
    "I often feel confused or overwhelmed by complicated HR"             -> DIST
    "The compensation and benefits I receive are appropriate"            -> DIST
    "I am able to utilize HR information, tools, and the support"        -> DIST
    "I have a clear and up-to-date Position Focus"                       -> DIST
    "I have a working knowledge of JV policies and procedures"           -> MEAN
    "I feel noticed and cared for by my team when I have needs"          -> MEAN

  JVK — JOSIAH VENTURE KIDS
    "My children are growing in resilience"                              -> MEAN
    "JV provides opportunities for my kids to connect"                   -> DIST
    "I see my children thriving in at least some areas"                  -> MEAN
    "I regularly feel my children's needs are overlooked"                -> MEAN
    "My children often feel isolated or disconnected"                    -> MEAN
    "I am aware of available resources to support my children"           -> DIST
    "I have someone to turn to for help when my kids"                    -> DIST
    "I clearly understand JV's approach to caring for kids"              -> DIST
    "I feel my children are cared for and supported by JV"               -> MEAN
    "My children have 1-2 adults outside our family"                     -> MEAN

  COUNSELING
    "I understand JV's process for getting counseling help"              -> DIST
    "I feel encouraged to pursue counseling when needed"                 -> MEAN
    "I feel more equipped to navigate challenges because of counseling"  -> MEAN
    "I know who to contact for personal or family care"                  -> DIST
    "Counseling is viewed in our organization as a healthy"              -> MEAN
    "I have safe and trusted people I can talk to about seeking help"    -> MEAN
    "I see counseling as a proactive tool for growth"                    -> MEAN
    "Practical barriers (time, cost, access) keep me from seeking"       -> DIST
    "I know someone on staff who has benefitted from counseling"         -> DIST

  MINISTRY PARTNER DEVELOPMENT
    "Financial pressure sometimes distracts me from focusing"            -> DIST
    "I often feel alone in carrying the responsibility of MPD"           -> MEAN
    "I know who to turn to for encouragement or accountability in MPD"   -> DIST
    "I have the practical MPD tools and guidance I need"                 -> DIST
    "I receive valid and regular financial reports about my support"     -> DIST
    "I feel supported by my uplink or ministry team in building"         -> MEAN
    "I am confident when sharing my ministry vision"                     -> MEAN
    "I am effective when sharing my ministry vision"                     -> MEAN
    "I regularly communicate with my partners to let them know"          -> MEAN

  LEARNING & DEVELOPMENT
    "I often struggle to apply Christ's strategy to daily ministry"      -> MEAN
    "I frequently feel unsure about how to move forward in my dev"       -> DIST
    "The equipping resources available enable me to be developed"        -> DIST
    "I am experiencing professional growth in this season"               -> MEAN
    "I receive helpful feedback and encouragement that supports"         -> MEAN
    "I am growing in healthy rhythms that help me serve others"          -> MEAN
    "My uplink rhythms (meetings, guidance, support) help me thrive"     -> DIST
    "I am continually learning how Christ's strategy shapes"             -> MEAN
    "I am experiencing personal growth in this season"                   -> MEAN

  MARRIAGES
    "I feel supported and encouraged by JV and my team culture"          -> MEAN
    "I often feel that ministry demands leave me too depleted"           -> MEAN
    "I know where to go for help if our marriage faces challenges"       -> DIST
    "We are learning to navigate ministry pressures together"            -> MEAN
    "I have couples or mentors I can turn to for support"                -> MEAN
    "My team culture values and respects the importance of nurturing"    -> MEAN

  JV WOMEN
    "I struggle to understand how my gifts and role fit"                 -> MEAN
    "I often feel isolated in ministry and lack women"                   -> MEAN
    "I often feel disconnected from my team and uninformed"              -> DIST
    "I feel my voice is valued in team and organizational settings"      -> MEAN
    "I feel that my organization provides clear guidance on women"       -> DIST
    "Our organization provides opportunities for women to encourage"     -> DIST
    "JV gatherings (such as conferences or retreats) provide a safe"     -> MEAN

  LANGUAGE & CULTURE
    "I receive regular accountability and helpful feedback on my progress in language" -> DIST
    "I regularly feel discouraged about my pace of language learning"    -> MEAN
    "I often struggle to balance ministry demands with language"         -> MEAN
    "I feel increasingly capable in ministry because of my language"     -> MEAN
    "I know who to turn to for help with language learning challenges"   -> DIST
    "I clearly understand the expectations for my progress in language"  -> DIST
    "My team helps me with my language and cultural adaptation needs"    -> MEAN
    "I am growing in my ability to live and function daily"              -> MEAN
    "I am aware of cultural differences on my team"                      -> MEAN
    "It is important for me to grow in my English skills"                -> MEAN
    "I am able to switch into English and still communicate"             -> MEAN
    "I regularly offer grace and encouragement to teammates"             -> MEAN

STEP 3.4 — COMPUTE STATUS PER QUESTION

  CRITICAL WARNING: Do NOT read question status from the workbook Column D.
  Column D may contain rounded or incorrect values from an earlier pass.
  ALWAYS compute status from scratch using the raw survey response counts
  and the rules below. This is the only way to get DIST scoring right.

  FOR MEAN QUESTIONS (applied to final_score after inversion):
    Healthy  >= 3.50
    Watch    2.50 to 3.49
    Concern  < 2.50

  FOR DIST QUESTIONS (the three-factor weighted distribution scale):

    Do NOT use the mean score. Use the response counts [SD, D, U, A, SA].

    For NON-BURDEN questions:
      pos = (A + SA) / n × 100
      neg = (SD + D) / n × 100

    For BURDEN questions:
      pos = (SD + D) / n × 100   <- disagreement with a burden = positive
      neg = (A + SA) / n × 100

    Apply all three factors:
      HEALTHY = pos >= 75% AND neg <= 15%
      WATCH   = pos >= 50% AND neg <= 30% AND neg does NOT outnumber pos
      CONCERN = pos < 50% OR neg > 30% OR neg outnumbers pos

    Any single Concern condition triggers Concern. All three Healthy
    conditions must be true for Healthy. Watch is everything in between.

  WORKED EXAMPLE — DIST, non-burden:
    "I understand JV's process for getting counseling" [DIST, n=20]
    Counts: [SD=5, D=10, U=4, A=1, SA=0]
    pos = (1+0)/20 × 100 = 5%
    neg = (5+10)/20 × 100 = 75%
    pos < 50% -> CONCERN

  WORKED EXAMPLE — DIST, burden:
    "Financial pressure distracts me from ministry" [DIST, burden, n=19]
    Counts: [SD=0, D=5, U=2, A=4, SA=8]  (raw, not flipped)
    pos = (SD+D)/n = (0+5)/19 × 100 = 26.3%
    neg = (A+SA)/n = (4+8)/19 × 100 = 63.2%
    pos < 50% -> CONCERN

  WORKED EXAMPLE — MEAN, burden:
    "I sometimes feel the weight of carrying responsibilities" [MEAN, burden, n=9]
    Counts: [SD=0, D=0, U=1, A=1, SA=7]
    raw_mean = (0+0+3+4+35)/9 = 4.67
    final = 6 - 4.67 = 1.33 -> CONCERN

STEP 3.5 — DEPARTMENT STATUS

  1. Compute final_score for every question (after inversion).
  2. Compute dept_avg = mean of all final_scores across all groups.
  3. Apply MEAN thresholds to get initial status from dept_avg.
  4. CONCERN-COUNT OVERRIDE: count how many questions scored Concern.
     If 3 or more -> department status = Concern, regardless of avg.

  In the DEPTS dict, set "status" from step 3 (the avg threshold only).
  The script re-applies the concern-count override automatically when it runs.
  So set "status": "Watch" even if you expect the override to make it Concern.
  The script will correct it.

STEP 3.6 — SURVEY BASICS LOOKUP LEVEL

  After computing the final status for each question, select the SB column:
    Concern -> 'low'  (column 6 in Survey Basics sheet)
    Watch   -> 'med'  (column 9)
    Healthy -> 'high' (column 12)

  The same question will show different interpretation text for different
  countries depending on how staff scored it. This is correct.

════════════════════════════════════════════════════════════════════════════════
PART 4 — THE DEPTS LIST: EXACT FORMAT AND EVERY FIELD
════════════════════════════════════════════════════════════════════════════════

The DEPTS list starts at line 563 of build_country_pulse_report.py.
Replace the entire list with new country data. Keep the exact Python structure.

COMPLETE DEPT DICT FORMAT:

  {
    "name": "Human Resources",
    # Department display name. Must match how it appears in the workbook tabs.

    "avg": 3.24,
    # Mean of all final_scores across all questions in all groups.
    # Compute this yourself before writing the dict.

    "status": "Watch",
    # Department status from avg threshold ONLY (before concern-count override).
    # Healthy>=3.50 | Watch 2.50-3.49 | Concern<2.50
    # The script re-applies concern-count override automatically.

    "groups": [
      ("Human Resources", [
      # Group label (string) + list of question tuples.
      # Standard departments have exactly ONE group with the department name.
      # JVK has THREE groups. L&C has TWO groups. (See Part 5 below.)

        (
          "HR",
          # Survey Basics SHEET NAME. Must be exactly one of:
          # HR | L&D | L&C | MPD | Counseling | Women | Singles | Marriages | JVK

          "I believe that HR policies and decisions are applied fairly across the organization.",
          # LOOKUP TEXT: used to find the question in Survey_Basics__What___Why.xlsx.
          # Must match the wording in the SB spreadsheet as closely as possible.
          # If SB uses a contraction ("I'm") use that here even if survey says "I am".
          # This is what drives the Survey Basics text lookup.

          "I believe that HR policies and decisions are applied fairly across the organization.",
          # DISPLAY TEXT: shown in Column B of the workbook.
          # Usually identical to lookup text.
          # For burden questions, append " [Burden — inverted]" at the end.
          # Example: "I often feel confused by HR requirements. [Burden — inverted]"

          2.52,
          # RAW MEAN SCORE — before burden inversion.
          # Compute: (SD×1 + D×2 + U×3 + A×4 + SA×5) / n
          # The script applies final = 6 - raw for burden questions.

          False,
          # True = this is a Burden question (negatively worded).
          # False = standard question.
          # The script inverts the score and handles heatmap display.

          [4, 5, 9, 3, 0],
          # Response counts [SD, D, U, A, SA] as integers.
          # Count directly from the raw data file.
          # Must sum to n for this question.
          # Do NOT flip these for burden questions — record as-is.
          # CRITICAL: wrong counts = wrong heatmap AND wrong DIST scoring.

          21,
          # n = number of respondents who answered this specific question.
          # May differ from dept n if some respondents skipped it.
        ),
        # ... more question tuples
      ]),
    ],

    "strengths": [
      "Statement 1.",
      "Statement 2.",
    ],
    # 3-5 items. See Part 6 for writing rules.

    "growth": [
      "Statement 1.",
      "Statement 2.",
    ],
    # 3-5 items. See Part 6 for writing rules.

    "leadership": [
      "Question 1?",
      "Question 2?",
      "Question 3?",
      "Question 4?",
    ],
    # Always 4 questions. Directors choose 2. See Part 6 for writing rules.

    "quotes": [
      ("Growth Area", "Quote text verbatim.", "", None),
      # FORMAT: (tag, quote_text, culture_label, translation_or_None)
      #
      # tag: "Growth Area" or "Strength"
      # quote_text: verbatim from the survey. Never paraphrase.
      # culture_label: "" for standard departments.
      #                "1st Culture" or "2nd Culture" for JVK and L&C only.
      # 4th element: if quote is in local language, English translation as string.
      #              If English or no translation needed, use None.
      #
      # EXAMPLES:
      # Standard:          ("Growth Area", "English quote.", "", None)
      # With translation:  ("Growth Area", "Hungarian text.", "", "English translation.")
      # JVK/L&C culture:   ("Growth Area", "Quote.", "2nd Culture", None)
      # Both:              ("Growth Area", "Hungarian.", "1st Culture", "English.")
    ],
    # Include 5-8 quotes. Directors reduce to their preferred set in review.

    "open_q": "What would make HR support more helpful to you?",
    # The exact open-ended survey question that generated the staff voice quotes.
    # Shown as a header above the quotes section in the workbook.

    "lead_question": "Clarity and accessibility of HR processes, roles, and support.",
    # One sentence shown on Summary tab in "Area to explore further" column.
    # Describes what the country leader should dig into for this department.
  }

════════════════════════════════════════════════════════════════════════════════
PART 5 — JVK AND L&C: CULTURE GROUP STRUCTURE
════════════════════════════════════════════════════════════════════════════════

JVK and L&C have questions split by culture group. All other departments have
one group. Do not add culture groups to other departments.

JVK — THREE groups (include actual n in each label):
  "groups": [
    ("Second Culture Parents (n=6)", [
      # questions asked only to 2nd culture parents
      # questions asked to all parents (shared questions)
    ]),
    ("First Culture Parents (n=4)", [
      # questions asked only to 1st culture parents
    ]),
    ("All Parents — Shared Questions (n=10)", [
      # questions asked to all parents regardless of culture
    ]),
  ],

L&C — TWO groups (include actual n in each label):
  "groups": [
    ("Second Culture Staff (n=5)", [
      # questions for 2nd culture staff only
    ]),
    ("First Culture Staff (n=12)", [
      # questions for 1st culture staff only
    ]),
  ],

JVK and L&C QUOTES must include the culture label (3rd element):
  ("Growth Area", "Quote text.", "2nd Culture", None)
  ("Growth Area", "Quote text.", "1st Culture", None)

JVK and L&C SB sheet name is "JVK" and "L&C" respectively for all groups.

════════════════════════════════════════════════════════════════════════════════
PART 6 — WRITING RULES (STRENGTHS, GROWTH AREAS, LEADERSHIP QUESTIONS)
════════════════════════════════════════════════════════════════════════════════

STRENGTHS — what to write:
  Observational. Describe what staff report experiencing. Not verdicts.
  Ground each statement in what the data actually shows.
  3-5 per department.

  GOOD: "The majority of staff report feeling noticed and cared for by the team."
  BAD:  "Staff are cared for."  <- verdict, not observation

  GOOD: "Staff report a working knowledge of JV policies and procedures."
  BAD:  "HR is doing well."  <- too vague, not grounded in data

GROWTH AREAS — what to write:
  Inquiry framing. Signal what needs attention. Never render a verdict.
  Never say something is broken, failing, or absent.
  3-5 per department.

  ALWAYS USE:
    "warrants direct exploration"                  NOT "is broken"
    "not being experienced consistently"           NOT "does not exist"
    "reflects patterns that need closer attention" NOT "is failing"
    "at risk of being overlooked"                  NOT "is being overlooked"
    "could be strengthened"                        NOT "is weak"
    "would benefit from"                           NOT "needs to be fixed"

  GOOD: "HR processes are not consistently experienced as clear or easy to navigate."
  BAD:  "HR processes are broken and staff can't access them."

  GOOD: "Awareness of what HR offers is not consistently reaching staff."
  BAD:  "Staff don't know what HR does."

LEADERSHIP QUESTIONS — CRITICAL RULE:
  QUESTIONS MUST NEVER ASSUME THE STAFF PERCEPTION IS CONFIRMED REALITY.
  They must be written as genuine inquiry that opens a conversation.

  TEST EVERY QUESTION: Does this question assume the staff perception is accurate?
  If yes -> rewrite it as an open question.

  WRONG: "What concrete steps does your team take to share the load with singles?"
         This assumes the load is not being shared. It puts the leader on trial.

  RIGHT: "How does your team engage with single staff to understand what they
          carry and whether they need more support?"
         This opens inquiry without assuming the answer.

  WRONG: "Why is the counseling process not clear to your team?"
  RIGHT: "Could you clearly explain JV's counseling process to a staff member
          who asks today? If not, that is the starting point."

  Write 4 questions per department. Directors choose 2 for the final report.
  The 2 write-in rows in the workbook are for the director to add custom questions.

QUOTES — rules:
  Keep verbatim. Never paraphrase, correct grammar, or clean up phrasing.
  Include 5-8 per department. Directors reduce to their preferred set.
  If quote is in local language (Hungarian, Romanian, etc.):
    - Put the local language text as the quote
    - Put the English translation as the 4th tuple element
  Tag each quote "Growth Area" or "Strength" based on its content.
  For JVK and L&C only: always include culture label (3rd element).
  For all other depts: culture_label = "" and 4th element = None.

════════════════════════════════════════════════════════════════════════════════
PART 7 — SURVEY BASICS LOOKUP: HOW IT WORKS AND HOW TO FIX FAILURES
════════════════════════════════════════════════════════════════════════════════

The script looks up interpretation text from Survey_Basics__What___Why.xlsx.
It normalises both strings (lowercase, strip punctuation) and matches on 80 chars.
The LOOKUP TEXT (first element of each question tuple) drives this.

If a question is NOT FOUND, the workbook cell shows: [Survey Basics text not found]
Fix ALL not-found cells before delivering the workbook to directors.

HOW TO FIX NOT-FOUND:

Fix 1 — Check Survey_Basics_Corrections.json first.
  It is loaded automatically by the script. It already contains Poland fixes.

Fix 2 — Adjust the lookup text to match the SB spreadsheet exactly.
  Open Survey_Basics__What___Why.xlsx and find the exact wording used there.
  Common mismatches: contractions ("I'm" vs "I am"), word order, extra words.

Fix 3 — If the question is genuinely not in Survey Basics, add it to MANUAL_INTERP
  in the script (around line 57). Format:
    "first 60 chars of lookup text (normalised: lowercase, no punctuation)": {
        'low':  'Concern-level interpretation.',
        'med':  'Watch-level interpretation.',
        'high': 'Healthy-level interpretation.',
    }

KNOWN POLAND CORRECTIONS (already in Survey_Basics_Corrections.json):
  1. Singles "I'm learning to navigate" — SB uses "I'm" not "I am"
  2. Women "Often I feel isolated" — SB word order differs from display text
  3. Women "Our organization provides opportunities for women to encourage"
     -> NOT in SB at all. Use MANUAL_INTERP with this text:
     'low':  'Staff report limited or inconsistent opportunities for women to connect.'
     'med':  'Some opportunities exist but are not consistently accessible or used.'
     'high': 'Staff report the organization provides meaningful guidance on roles,
              leadership opportunities, and representation of women's voices in
              leadership conversations.'
  4. L&C "I know who to turn to for help with language learning challenges"
     -> SB includes "cultural or" before "language learning" in its wording.
        Use: "I know who to turn to for help with cultural or language learning challenges"
  5. JVK "I feel my children are cared for and supported by JV" at Healthy score
     -> Must use POSITIVE text. Manually set:
        'high': 'Parents report their children are cared for and supported by JV.'
  6. HR "I believe that HR policies and decisions are applied fairly" at Concern
     -> Must use: 'Staff report perceiving unfairness or favoritism.'

════════════════════════════════════════════════════════════════════════════════
PART 8 — RUNNING THE DIRECTOR REVIEW BUILD SCRIPT
════════════════════════════════════════════════════════════════════════════════

STEP 1 — Change exactly these things in build_country_pulse_report.py:

  Line 6:   COUNTRY = 'POLAND 2026'
            -> Change to: COUNTRY = 'HUNGARY 2026'  (or whatever country/year)

  Line 4:   SB_PATH = '/mnt/user-data/uploads/Survey_Basics__What___Why.xlsx'
            -> Verify this path matches where the file was uploaded. Usually correct.

  Line 15:  CORRECTIONS_PATH = '/home/claude/Survey_Basics_Corrections.json'
            -> Change to: '/mnt/user-data/uploads/Survey_Basics_Corrections.json'

  Near bottom, the combined.save line:
            path = os.path.join(OUT, 'Poland_All_Departments_Director_Review.xlsx')
            -> Change Poland to new country name.

STEP 2 — Replace the DEPTS list (starting at line 563) with new country data.
  Sort departments WORST to BEST by avg score. Rank 1 = worst, n = best.
  Do not change anything else in the script.

STEP 3 — Run it:
  python3 build_country_pulse_report.py

Output: /mnt/user-data/outputs/[COUNTRY]_All_Departments_Director_Review.xlsx

If weasyprint is needed for the PDF later:
  pip install weasyprint --break-system-packages

════════════════════════════════════════════════════════════════════════════════
PART 9 — DIRECTOR REVIEW WORKBOOK: QA CHECKLIST
════════════════════════════════════════════════════════════════════════════════

Open the output file. Compare against Poland_All_Departments_Director_Review.xlsx.
Check every item:

TABS AND NAVIGATION
  [ ] Summary tab is first (leftmost).
  [ ] One tab per department, named "[Country] [Department Name]".
  [ ] Tab colours: green=Healthy (#C6EFCE), yellow=Watch (#FFEB9C), red=Concern (#FFC7CE).
  [ ] Freeze panes set at C3 on every department tab.
  [ ] Grid lines hidden on every department tab.

ROW 1 AND 2 (every dept tab)
  [ ] Row 1: navy bar with "PEOPLE AND CULTURE DIRECTORS REVIEW — [COUNTRY] | [DEPT]"
  [ ] Row 2: navy bar with score, status, n, rank.

SECTION 1 — QUESTION SCORES
  [ ] Column A: "Q" for standard, "Burden [inv.]" in amber for burden questions.
  [ ] Column B: question display text. Burden questions end with "[Burden — inverted]".
  [ ] Column C: final score (after inversion), 2 decimal places, colour-coded.
  [ ] Column D: status (Concern/Watch/Healthy), colour-coded.
  [ ] Column E: Survey Basics interpretation text. NO cell shows "[Survey Basics text not found]".
  [ ] Column F: yellow input cell (blank — for director input).
  [ ] Column G: yellow input cell with hint text.
  [ ] Column H: yellow input cell with hint text.
  [ ] Column I: narrow grey spacer column.
  [ ] Columns J-P: heatmap. J=type label, K=score, L-P=SD/D/U/A/SA as "X.X% (n)".
  [ ] Heatmap cells colour-coded blue gradient (deeper blue = higher %).
  [ ] Questions sorted worst to best (lowest final_score first) within each group.
  [ ] JVK and L&C: group label rows between culture groups.

SECTION 2 — STRENGTHS
  [ ] Green fill rows with draft strength statements.
  [ ] Column F: yellow input cell (directors type Yes to keep).
  [ ] Column G: yellow input cell (directors type rewrite).

SECTION 3 — GROWTH AREAS
  [ ] Amber fill rows with draft growth area statements.
  [ ] Column F and G: yellow input cells.

SECTION 4 — LEADERSHIP QUESTIONS
  [ ] Light blue fill rows with 4 drafted questions.
  [ ] 2 blank write-in rows at the bottom.
  [ ] Column F: yellow input cells (directors type Yes, max 2).

SECTION 5 — STAFF VOICE QUOTES
  [ ] "Responding to: [open_q]" header row showing the survey prompt.
  [ ] One row per quote with verbatim text.
  [ ] Column D: culture tag for JVK and L&C (colour-coded navy/green).
  [ ] Column E: tag badge (Growth Area/Strength, colour-coded amber/green).
  [ ] Column F: yellow input cells.
  [ ] Quotes with translations: both languages in one cell with "Translation:" label.

SECTION 6 — HEATMAP REFERENCE
  [ ] Full response distribution for reference only. No director input.

SUMMARY TAB
  [ ] All departments listed, ranked worst to best.
  [ ] Scores and statuses colour-coded.
  [ ] "Area to explore further" column populated from lead_question.

════════════════════════════════════════════════════════════════════════════════
PART 10 — BUILDING THE PDF PULSE REPORT
════════════════════════════════════════════════════════════════════════════════

After directors return their selections, build the PDF report.

STEP 10.1 — EXTRACT DIRECTOR SELECTIONS FROM THE RETURNED WORKBOOK

Read the completed workbook using openpyxl. For each department sheet:

Find the LAST occurrence of each section header (the workbook has how-to rows
at the top that contain section names — skip these and find the real section).

Section 2 (Strengths): rows where Col A = "Strength"
  - Include if Col F = "Yes" OR Col F is blank (blank means keep)
  - If Col G has a rewrite (not placeholder text), use Col G instead of Col B

Section 3 (Growth Areas): rows where Col A = "Growth Area"
  - Same rules as strengths

Section 4 (Leadership Questions): rows where Col A = "Leader Q" or "Write-in"
  - Include ONLY if Col F = "Yes" (directors must explicitly select)
  - Skip write-in rows where Col B contains "Add your own"
  - If write-in row has real text and Col F = "Yes", include it

Section 5 (Quotes): rows where Col A = "Quote"
  - Include if Col F = "Yes" (directors must explicitly select)
  - Use Col B text. Strip leading/trailing quote marks.

Open-ended question prompt: find row containing "Responding to:" in Col A or B.

STEP 10.2 — EXTRACT QUESTION DATA FROM SECTION 1

For each question row (Col A = "Q" or "Burden [inv.]"):
  type: "Q" or "B"
  text: Col B (display text)
  score: Col C (float)
  status: Col D
  sb: Col G if G has real content (>15 chars, not placeholder), else Col E
  group: from the most recent group label row (rows starting with "▸")

STEP 10.3 — BUILD THE REPORT DATA STRUCTURES

Save two pickle files:

report_data dict — keyed by department name string:
  {
    'score': float,
    'status': str,
    'n': int,
    'rank': int,
    's2': [strength strings],     <- approved strengths
    's3': [growth area strings],  <- approved growth areas
    's4': [leadership questions], <- selected leadership questions (2-3)
    's5': [quote strings],        <- selected quotes (up to 8, PDF caps at 4)
  }

  For JVK: also add keys 'JVK_2nd' and 'JVK_1st' with their sub-group data.
  For L&C: also add keys 'LC_2nd' and 'LC_1st' with their sub-group data.

dept_q_data dict — keyed by q_key (HR, JVK, L&C, etc.):
  List of question dicts:
  {
    'type': 'Q' or 'B',
    'text': display text string,
    'score': float (final score after inversion),
    'status': str,
    'sb': Survey Basics interpretation string,
    'group': culture group label string or None,
  }

STEP 10.4 — WRITE THE PDF BUILD SCRIPT

Write a Python script that:
  1. Loads the two pickle files
  2. Sets DEPT_PAGES, SUMMARY, OVERALL_BULLETS, PROMPTS for this country
  3. Generates HTML with the CSS and helper functions below
  4. Renders to PDF via weasyprint

DEPT_PAGES list — one tuple per department, sorted worst to best:
  (display_name, report_key, q_key, rank, score, status, n_total, None)

  display_name: shown in the PDF header
  report_key:   key into report_data dict
                For JVK use 'JVK_2nd' (script merges both groups)
                For L&C use 'LC_2nd' (script merges both groups)
  q_key:        key into dept_q_data dict (HR, JVK, L&C, etc.)
  rank:         1=worst
  score:        float
  status:       Concern/Watch/Healthy
  n_total:      total respondents for this department
  None:         always None

SUMMARY list — one tuple per department:
  (dept_name, score, status, n, area_to_explore)
  area_to_explore: one sentence from the lead_question field

OVERALL_BULLETS list — three tuples, each containing one HTML string:
  Write three bullets covering:
  1. The most common pattern across Concern departments (access/structural gaps)
  2. The genuine strength pattern across the team (relationships, growth)
  3. The pattern that needs most careful watching (depletion, load, sustainability)

  Use plain language. Not academic. Not AI-sounding.
  Bold the opening phrase of each bullet with <b>...</b>.
  Do NOT reference 2030 Vision, OKRs, or JV strategy.

PROMPTS dict — maps q_key to open-ended survey question text:
  Read from the workbook "Responding to:" rows.

STEP 10.5 — CSS RULES (copy exactly, change footer country/year only)

Critical rules that MUST be present:

  @page { size: A4; margin: 10mm 15mm 10mm 15mm; }
  .page { page-break-after: always; }
  .page:last-child { page-break-after: auto; }

  /* PAGE BREAK RULE — NEVER REMOVE */
  .section-block { break-inside: avoid; page-break-inside: avoid; }
  .zh { break-after: avoid; page-break-after: avoid; }
  .zh + *, .zh + table, .zh + div { break-before: avoid; page-break-before: avoid; }
  .q-section, .two-col, .lq-section { break-inside: avoid; page-break-inside: avoid; }
  .group-label { break-after: avoid; page-break-after: avoid; }
  table.qs tr, table.qg tr, .lq-row, .col-item { break-inside: avoid; page-break-inside: avoid; }

  /* BAR CHART — department names must never wrap */
  .bar-name { width: 170px; white-space: nowrap; }

  /* STATUS COLOURS — do not change */
  Concern text: #B91C1C  background: #FEF2F2  pill: #FECACA
  Watch text:   #B45309  background: #FFFBEB  pill: #FEF08A
  Healthy text: #166534  background: #F0FDF4  pill: #BBF7D0
  Orange:       #FF6600  (scores, LQ numbers, quote marks, bar fills)
  Navy:         #1A3A5C  (dept header background, LQ text)

  Zone header colours:
  .zh-dark   { background: #374151; }  question scores, overall picture
  .zh-green  { background: #166534; }  what is working
  .zh-red    { background: #B91C1C; }  where attention needed (Concern depts)
  .zh-amber  { background: #B45309; }  where attention needed (Watch depts)
  .zh-navy   { background: #1A3A5C; }  questions for leadership, where attention (Healthy depts)
  .zh-slate  { background: #475569; }  what staff said

  Summary table group headers read: "Concern" / "Watch" / "Healthy"
  NEVER "Concern departments" — directors know their departments.

STEP 10.6 — PDF PAGE STRUCTURE PER DEPARTMENT

Each department page has exactly these sections in order:

1. HEADER: navy bar, dept name left, score + status right (orange score, pill colour)
2. META BAR: respondents n, rank "X of [total]", status note (italic)
   Status note: "Status set by concern-count rule" for Concern, else "Score: X.XX"
3. QUESTION SCORES TABLE: 3 columns — Question | Score/Status | What this score means
   No Type column (Q/B removed from PDF — directors don't need it)
   Rows sorted worst to best. Group labels for JVK and L&C.
4. TWO-COLUMN SECTION: "What is working" (left, green) | "Where attention is needed" (right)
   Wrap in section-block div.
5. LEADERSHIP QUESTIONS: numbered 1, 2, 3 in large orange. Wrap in section-block.
6. WHAT STAFF SAID: slate header with exact survey question in quotes.
   Quote grid: 2 per row, max 4 total. Alternating light backgrounds.
   Orange top border on each quote card. Orange quotation mark.
   Wrap in section-block.

SECTION-BLOCK RULE (CRITICAL):
  Every zone header (.zh) and its content must be inside <div class="section-block">.
  This prevents headers from being stranded at the bottom of a page without content.
  If you see an orphaned header in the output, find it in the HTML and wrap it.

STEP 10.7 — RUN THE PDF BUILD SCRIPT

  python3 build_report_[country].py 2>/dev/null

  Output: /mnt/user-data/outputs/[COUNTRY]_Pulse_Report_[YEAR].pdf

════════════════════════════════════════════════════════════════════════════════
PART 11 — PDF REPORT: QA CHECKLIST
════════════════════════════════════════════════════════════════════════════════

Compare against Poland_Pulse_Report_2026.pdf page by page.

SUMMARY PAGE
  [ ] Title: "Pulse Report" with "People & Culture" label above and country/year below
  [ ] Six snapshot cards: respondents, departments, avg score, Concern, Watch, Healthy
  [ ] Bar chart: all department names on ONE LINE — no wrapping
  [ ] Bar chart: sorted worst to best, coloured by status
  [ ] Summary table: three group headers "Concern" / "Watch" / "Healthy" (no "departments")
  [ ] Summary table: scores and statuses colour-coded correctly
  [ ] Overall picture: three bullet points, first phrase bolded in each
  [ ] Everything on one page

DEPARTMENT PAGES (check every one)
  [ ] Navy header with department name and large orange score
  [ ] Status in light-coloured caps next to score (pink/yellow/green)
  [ ] Meta bar below with n, rank, status note
  [ ] Question table: all questions listed, sorted worst to best
  [ ] Question rows colour-coded by status
  [ ] No "Type" column (Q/B column is NOT in the PDF)
  [ ] Score shown as large bold number with status label below
  [ ] Survey Basics text in italic — all cells populated (none blank or "not found")
  [ ] JVK and L&C: culture group label rows visible between groups
  [ ] "What is working" left column: green header, green checkmarks
  [ ] "Where attention is needed" right column: correct colour by dept status, arrows
  [ ] Leadership questions: numbered 1, 2, 3 in large orange
  [ ] Staff said: dark slate header with exact survey question in quotes
  [ ] Staff said: no garbled characters (no &#X27; or &amp; in visible text)
  [ ] Quotes: max 4, 2 per row, orange top border, orange quotation mark
  [ ] No zone header stranded alone at bottom of page
  [ ] Footer: "JV People & Culture Pulse Report — [COUNTRY] [YEAR]  ·  Confidential"

════════════════════════════════════════════════════════════════════════════════
PART 12 — DEPARTMENT ORDER AND RANKING
════════════════════════════════════════════════════════════════════════════════

Sort departments in the DEPTS list WORST to BEST (lowest avg score first).
Rank 1 = worst. Rank n = best.

In the workbook Row 2 shows: "Rank X of [total] (worst → best)"
In the PDF meta bar shows: "Rank X of [total]"

The summary page bar chart and table also show departments in this order.

════════════════════════════════════════════════════════════════════════════════
PART 13 — WHAT THE BUILD SCRIPT HANDLES AUTOMATICALLY
════════════════════════════════════════════════════════════════════════════════

Do not add code or content for any of these — the script already does them:

  Column widths (A=14.71, B=44.71, C=11.71, D=10, E=46, F=12, G=34, H=44,
                 I=2 spacer, J-P=10 each)
  Row heights (auto-calculated from text length)
  Freeze panes at C3 on every department tab
  Section header bars (SECTION 1 through SECTION 6)
  Score and status colour coding (green/amber/red by computed status)
  Heatmap (built from [SD,D,U,A,SA] counts — blue gradient by response %)
  Burden question amber styling in Col A and J
  Input cell yellow fill (Col F and G in sections 2-5)
  Culture tag colour coding in Section 5 for JVK and L&C
  Section 4 write-in rows (2 blank rows added automatically)
  Summary tab structure and ranking
  Tab colour coding
  Concern-count override applied to effective department status
  Sort order of questions within each group (worst to best by final_score)
  Survey Basics lookup and interpretation text population
  "Responding to:" prompt row in Section 5

════════════════════════════════════════════════════════════════════════════════
PART 14 — TROUBLESHOOTING
════════════════════════════════════════════════════════════════════════════════

"[Survey Basics text not found]" in cells:
  -> Check Part 7. Adjust lookup text or add to Survey_Basics_Corrections.json.
  -> Fix ALL before delivering.

Department names wrap in PDF bar chart:
  -> Verify .bar-name has white-space: nowrap in CSS.

Orphaned zone header at page bottom in PDF:
  -> Find section in full_report.html.
  -> Ensure zh() and its content are inside <div class="section-block">.

Concern-count override not working:
  -> The script applies it automatically. Check that [SD,D,U,A,SA] counts
     are correct — wrong counts produce wrong DIST statuses.

DIST scoring not matching expected result:
  -> Re-read Part 3. DIST uses response counts, not the mean.
  -> For burden questions, pos and neg definitions are flipped.
  -> Show your work: compute pos%, neg%, and state which condition triggered.

JVK or L&C data not appearing in PDF:
  -> Check that report_data has both 'JVK_2nd' and 'JVK_1st' keys (or LC).
  -> The PDF script merges s2/s3/s4/s5 from both sub-groups.

Weasyprint not installed:
  -> pip install weasyprint --break-system-packages

Output file not appearing:
  -> Check the combined.save path at the bottom of the script.
  -> Ensure OUT directory exists (the script creates it with os.makedirs).

════════════════════════════════════════════════════════════════════════════════
END OF INSTRUCTIONS
════════════════════════════════════════════════════════════════════════════════
