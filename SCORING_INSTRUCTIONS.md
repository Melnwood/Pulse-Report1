# JV PULSE REPORT — COMPLETE SCORING INSTRUCTIONS
# Add this to your Romania chat immediately.

═══════════════════════════════════════════════════════════════════════════════
THE SCORING SYSTEM — READ THIS BEFORE SCORING ANY QUESTION
═══════════════════════════════════════════════════════════════════════════════

Every question uses ONE of two scales: MEAN or DIST.
You must apply the correct scale to every question. Using the wrong scale
produces wrong statuses and wrong heatmap colours.

───────────────────────────────────────────────────────────────────────────────
STEP 1 — COMPUTE THE RAW MEAN
───────────────────────────────────────────────────────────────────────────────

raw_mean = (SD×1 + D×2 + U×3 + A×4 + SA×5) / n

SD = Strongly Disagree, D = Disagree, U = Unsure/Neutral,
A = Agree, SA = Strongly Agree
n = number of respondents who answered this question (skip blanks)

───────────────────────────────────────────────────────────────────────────────
STEP 2 — APPLY BURDEN INVERSION (if burden=True)
───────────────────────────────────────────────────────────────────────────────

Burden questions are negatively worded. High agreement = bad.
Examples: "I often feel depleted", "I feel alone in MPD", "I feel confused by HR"

If burden=True:   final_score = 6 - raw_mean
If burden=False:  final_score = raw_mean

Put the RAW mean in the DEPTS tuple. The script inverts it automatically.
The [SD, D, U, A, SA] counts go in AS-IS — do not flip them for burden questions.

───────────────────────────────────────────────────────────────────────────────
STEP 3 — DETERMINE THE SCALE (MEAN or DIST)
───────────────────────────────────────────────────────────────────────────────

OVERRIDE: If n <= 5, ALWAYS use MEAN regardless of question type.

Otherwise, look up the question in the SCALE_MAP below.
If not found, default to MEAN.

MEAN questions = how I feel, what I experience personally
DIST questions = whether something exists/is accessible/is clear

QUICK GUIDE:
  MEAN: feeling connected, feeling valued, feeling depleted, growing personally,
        confidence, thriving, navigating challenges, feeling isolated, feeling alone

  DIST: access to resources, clarity of process, knowing who to contact,
        awareness of what is available, tools and systems, structural/process questions

FULL SCALE_MAP (match by substring — first 40+ characters of question):

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

  JVK
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

───────────────────────────────────────────────────────────────────────────────
STEP 4A — STATUS FOR MEAN QUESTIONS
───────────────────────────────────────────────────────────────────────────────

Apply to final_score (after inversion):

  Healthy  >= 3.50
  Watch    2.50 to 3.49
  Concern  < 2.50

───────────────────────────────────────────────────────────────────────────────
STEP 4B — STATUS FOR DIST QUESTIONS (the three-factor weighted scoring)
───────────────────────────────────────────────────────────────────────────────

This is the weighted three-factor distribution scale.
Do NOT use the mean score for DIST questions. Use the response counts.

FIRST — define pos and neg from the [SD, D, U, A, SA] counts:

  For NON-BURDEN questions:
    pos = (A + SA) / n × 100
    neg = (SD + D) / n × 100

  For BURDEN questions (inverted):
    pos = (SD + D) / n × 100     <- agreement with burden = bad, so disagreement = positive
    neg = (A + SA) / n × 100

SECOND — apply all three factors:

  HEALTHY  = pos >= 75%  AND  neg <= 15%
             (strong positive response, very few negative)

  WATCH    = pos >= 50%  AND  neg <= 30%  AND  neg does NOT outnumber pos
             (majority positive, but not strong enough for Healthy)

  CONCERN  = pos < 50%   OR   neg > 30%   OR   neg outnumbers pos
             (any one of these three triggers Concern)

WORKED EXAMPLE:
  Question: "I understand JV's process for getting counseling help" (DIST, not burden)
  Counts: [SD=5, D=10, U=4, A=1, SA=0], n=20
  pos = (1+0)/20 × 100 = 5%
  neg = (5+10)/20 × 100 = 75%
  -> pos < 50% -> CONCERN   (and neg > 30%, and neg outnumbers pos — all three triggered)

WORKED EXAMPLE 2:
  Question: "I am able to utilize HR information, tools, and support" (DIST, not burden)
  Counts: [SD=1, D=2, U=6, A=12, SA=0], n=21
  pos = (12+0)/21 × 100 = 57.1%
  neg = (1+2)/21 × 100 = 14.3%
  -> pos >= 50%, neg <= 30%, neg does not outnumber pos -> WATCH

WORKED EXAMPLE 3 (BURDEN question):
  Question: "Financial pressure sometimes distracts me" (DIST, burden=True)
  Counts: [SD=0, D=5, U=2, A=4, SA=8], n=19
  pos = (SD+D)/19 × 100 = (0+5)/19 × 100 = 26.3%  <- disagreement = positive for burden
  neg = (A+SA)/19 × 100 = (4+8)/19 × 100 = 63.2%
  -> pos < 50% -> CONCERN

───────────────────────────────────────────────────────────────────────────────
STEP 5 — DEPARTMENT STATUS
───────────────────────────────────────────────────────────────────────────────

1. Compute the mean of all final_scores for the department.
2. Apply MEAN thresholds to get initial status.
3. Apply CONCERN-COUNT OVERRIDE:
   Count how many questions in the department scored Concern.
   If 3 or more -> department status = Concern regardless of the average.

Set "status" in the DEPTS dict from step 2 (the avg threshold, before override).
The script re-applies the concern-count override automatically when it runs.

───────────────────────────────────────────────────────────────────────────────
SURVEY BASICS LOOKUP LEVEL
───────────────────────────────────────────────────────────────────────────────

After computing status, use it to pick the Survey Basics interpretation level:
  Concern -> use 'low' column (col 6) from Survey Basics sheet
  Watch   -> use 'med' column (col 9)
  Healthy -> use 'high' column (col 12)

This means the same question will show different interpretation text depending
on how this country's staff scored it. That is correct and intended.

───────────────────────────────────────────────────────────────────────────────
QUICK REFERENCE — THE WHOLE SYSTEM IN ONE TABLE
───────────────────────────────────────────────────────────────────────────────

  raw_mean = sum(SD×1 + D×2 + U×3 + A×4 + SA×5) / n
  final    = 6 - raw_mean  if burden  else  raw_mean
  n <= 5?  -> always MEAN scale

  MEAN scale (on final_score):
    >= 3.50 -> Healthy
    2.50-3.49 -> Watch
    < 2.50 -> Concern

  DIST scale (on response counts):
    non-burden: pos=(A+SA)/n×100, neg=(SD+D)/n×100
    burden:     pos=(SD+D)/n×100, neg=(A+SA)/n×100

    pos>=75 AND neg<=15           -> Healthy
    pos>=50 AND neg<=30 AND neg<pos -> Watch
    anything else                 -> Concern

  Dept override: 3+ Concern questions -> dept = Concern

