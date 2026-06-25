"""
JV People & Culture Pulse Report — Poland 2026
HTML/CSS rendered via weasyprint. One page per department + summary page.

FIXES APPLIED:
1. Type column (Q/B) removed from question table — not needed by country leaders
2. Staff voice section title: apostrophes use plain ' not HTML entity &#X27;
3. Overall Picture bullets rewritten in plain B2 English — no AI-sounding phrases
"""
import pickle, html, re, warnings
warnings.filterwarnings('ignore')
import weasyprint

report = pickle.load(open('/home/claude/report_data.pkl', 'rb'))
dept_q = pickle.load(open('/home/claude/dept_q_data.pkl', 'rb'))

# ── Staff voice prompts ──────────────────────────────────────────────────────
PROMPTS = {
    'Singles':    "What would most strengthen JV's support for singles in your context?",
    'HR':         "What would make HR support more helpful to you?",
    'JVK':        "What would most strengthen JV's care for kids?",
    'Counseling': "What would make counseling more accessible or effective for you?",
    'MPD':        "What is one thing that would strengthen your MPD journey right now?",
    'L&D':        "What type of training or development would be most helpful to you in the coming year?",
    'Marriages':  "What would most strengthen marriages in your ministry context?",
    'Women':      "What kind of support or opportunities would most help women thrive in your context?",
    'L&C':        "2nd culture: What would most help you in your language and cultural growth? | 1st culture: What would most help you in working more effectively in a multicultural team?",
}

# ── Department config ─────────────────────────────────────────────────────────
DEPT_PAGES = [
    ('Singles',                    'Singles',                   'Singles',    1, 2.99, 'Concern', 9,  None),
    ('Human Resources',            'Human Resources',           'HR',         2, 3.24, 'Concern', 21, None),
    ('JVK — Josiah Venture Kids',  'JVK_2nd',                  'JVK',        3, 3.29, 'Concern', 10, None),
    ('Counseling',                 'Counseling',                'Counseling', 4, 3.32, 'Watch',   20, None),
    ('Ministry Partner Development','Ministry Partner Develop', 'MPD',        5, 3.48, 'Watch',   19, None),
    ('Learning & Development',     'Learning & Development',    'L&D',        6, 3.51, 'Healthy', 21, None),
    ('Marriages',                  'Marriages',                 'Marriages',  7, 3.55, 'Healthy', 11, None),
    ('JV Women',                   'JV Women',                  'Women',      8, 4.01, 'Healthy', 11, None),
    ('Language & Culture',         'LC_2nd',                    'L&C',        9, 4.04, 'Healthy', 12, None),
]

SUMMARY = [
    ('Singles',                     2.99, 'Concern', 9,  'The load single staff carry in ministry and whether team structures help share it.'),
    ('Human Resources',             3.24, 'Concern', 21, 'Whether HR processes and support are clear and easy to access across the team.'),
    ('JVK — Josiah Venture Kids',   3.29, 'Concern', 10, 'How well JVK is reaching both first and second culture families — and what each group needs.'),
    ('Counseling',                  3.32, 'Watch',   20, 'Whether staff know how to access counseling and what is getting in the way.'),
    ('Ministry Partner Development',3.48, 'Watch',   19, 'Financial pressure in the MPD journey and whether support fits where each staff member is.'),
    ('Learning & Development',      3.51, 'Healthy', 21, 'Whether staff have a clear sense of where they are growing and what resources are helping.'),
    ('Marriages',                   3.55, 'Healthy', 11, 'Whether married staff feel supported to invest in their marriages alongside ministry.'),
    ('JV Women',                    4.01, 'Healthy', 11, "Whether women's voices are included before team decisions are made — not just after."),
    ('Language & Culture',          4.04, 'Healthy', 12, 'Whether second culture staff have clear expectations and regular feedback on language learning.'),
]

# FIX 3: Overall Picture bullets rewritten in plain English — no AI-sounding phrases
OVERALL_BULLETS = [
    ('<b>The most common theme across the three Concern departments is access.</b> In Singles, HR, and JVK, staff report that resources, processes, and clarity are not consistently reaching them. These are not relationship problems — they are gaps in how things are set up.',),
    ('<b>Relationships and personal growth are real strengths across the team.</b> In most departments, staff feel connected to the people around them, they are growing, and they have people they can turn to. This is a healthy foundation.',),
    ('<b>Carrying too much is the pattern worth watching most carefully.</b> In Singles, Marriages, and MPD, staff are feeling the weight of their responsibilities. This is worth talking about directly with country leaders before it becomes a bigger problem.',),
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def e(s): return html.escape(str(s)) if s else ''

STATUS_COLOR = {'Concern': '#B91C1C', 'Watch': '#B45309', 'Healthy': '#166534'}
STATUS_BG    = {'Concern': '#FEF2F2', 'Watch': '#FFFBEB', 'Healthy': '#F0FDF4'}
STATUS_PILL  = {'Concern': '#FECACA', 'Watch': '#FEF08A', 'Healthy': '#BBF7D0'}

def sc(s): return STATUS_COLOR.get(s, '#64748B')
def sb(s): return STATUS_BG.get(s, '#F8FAFC')

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = """
/* ══════════════════════════════════════════════════════════════════
   CRITICAL LAYOUT RULE — DO NOT REMOVE:
   Zone headers (.zh) must NEVER be orphaned at the bottom of a page.
   Every section block is wrapped in .section-block with break-inside: avoid.
   ══════════════════════════════════════════════════════════════════ */
@page { size: A4; margin: 10mm 15mm 10mm 15mm; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Arial, sans-serif; font-size: 9pt; color: #334155; }

.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }

.dept-header { background: #1A3A5C; color: white; display: flex;
  justify-content: space-between; align-items: center; padding: 8px 12px; }
.dept-name { font-size: 15pt; font-weight: bold; color: white; }
.dept-score-block { text-align: right; }
.dept-score { font-size: 22pt; font-weight: bold; color: #FF6600; line-height: 1; display: block; }
.dept-status-lbl { font-size: 8pt; font-weight: bold; letter-spacing: 1.5px; display: block; }
.meta-bar { display: flex; justify-content: space-between;
  padding: 3px 12px; font-size: 8pt; color: #64748B; }
.meta-note { font-style: italic; }

.zh { padding: 3px 8px; color: white; font-size: 7.5pt; font-weight: bold;
  letter-spacing: 1px; text-transform: uppercase; margin-bottom: 2px;
  break-after: avoid; page-break-after: avoid; }
.zh + *, .zh + table, .zh + div, .zh + .two-col { break-before: avoid; page-break-before: avoid; }

.section-block { break-inside: avoid; page-break-inside: avoid; }
.q-section   { break-inside: avoid; page-break-inside: avoid; }
.two-col     { break-inside: avoid; page-break-inside: avoid; }
.lq-section  { break-inside: avoid; page-break-inside: avoid; }
.group-label { break-after: avoid; page-break-after: avoid; }
.group-label + tr { break-before: avoid; page-break-before: avoid; }
table.qs tr  { break-inside: avoid; page-break-inside: avoid; }
table.qg tr  { break-inside: avoid; page-break-inside: avoid; }
.lq-row      { break-inside: avoid; page-break-inside: avoid; }
.col-item    { break-inside: avoid; page-break-inside: avoid; }

.zh-dark   { background: #374151; }
.zh-green  { background: #166534; }
.zh-red    { background: #B91C1C; }
.zh-amber  { background: #B45309; }
.zh-navy   { background: #1A3A5C; }
.zh-slate  { background: #475569; }

/* Question table — FIX 1: Type column removed */
table.qs { width: 100%; border-collapse: collapse; font-size: 8pt; margin-bottom: 5px; }
table.qs th { background: #F1F5F9; color: #64748B; font-size: 6.5pt; font-weight: bold;
  text-transform: uppercase; letter-spacing: 0.8px; padding: 3px 5px;
  border: 0.3pt solid #E2E8F0; }
table.qs th.c { text-align: center; }
table.qs td { padding: 3px 5px; border-bottom: 0.3pt solid #E2E8F0; vertical-align: top; line-height: 1.25; }
table.qs td.qtext { color: #1E293B; font-size: 8pt; }
table.qs td.scell { text-align: center; width: 66px; }
.snum { font-weight: bold; font-size: 10pt; display: block; line-height: 1.2; }
.ssts { font-size: 7pt; font-weight: bold; display: block; line-height: 1.2; }
table.qs td.sbtext { font-style: italic; font-size: 7pt; color: #475569; line-height: 1.2; }

.concern-row { background: #FEF2F2; }
.watch-row   { background: #FFFBEB; }
.healthy-row { background: #F0FDF4; }
.concern-c   { color: #B91C1C; }
.watch-c     { color: #B45309; }
.healthy-c   { color: #166634; }

.group-label { background: #F1F5F9; padding: 3px 8px; font-size: 7.5pt;
  font-weight: bold; color: #1A3A5C; text-transform: uppercase;
  letter-spacing: 1px; border-left: 3pt solid #FF6600; margin: 3px 0 1px 0; }

.two-col { display: flex; gap: 5mm; margin-bottom: 5px; }
.col-half { flex: 1; }
.col-item { font-size: 8.5pt; line-height: 1.25; padding: 2px 6px 2px 6px; }
.col-item + .col-item { border-top: 0.3pt solid #E2E8F0; }
.strength-item { color: #166534; }
.growth-concern { color: #B91C1C; font-style: italic; }
.growth-watch   { color: #B45309; font-style: italic; }
.growth-healthy { color: #334155; }

.lq-section { margin-bottom: 5px; }
.lq-row { display: flex; align-items: flex-start; padding: 3px 0;
  border-bottom: 0.3pt solid #E2E8F0; gap: 6px; }
.lq-row:last-child { border-bottom: none; }
.lq-num { font-size: 14pt; font-weight: bold; color: #FF6600;
  width: 18px; flex-shrink: 0; line-height: 1; text-align: center; }
.lq-text { font-size: 9pt; color: #1A3A5C; line-height: 1.3; padding-top: 1px; }

table.qg { width: 100%; border-collapse: separate; border-spacing: 3px; }
table.qg td { width: 50%; background: #F8FAFC; border-top: 2pt solid #FF6600;
  padding: 4px 8px; vertical-align: top; font-style: italic; font-size: 8pt;
  color: #334155; line-height: 1.25; }
table.qg tr:nth-child(even) td { background: #F0F4F8; }
.qmark { color: #FF6600; font-weight: bold; font-size: 11pt; font-style: normal; }

.report-title-block { padding: 8px 0 6px 0; border-bottom: 2pt solid #FF6600; margin-bottom: 6px; }
.pc-label { font-size: 9pt; font-weight: bold; color: #FF6600; letter-spacing: 2px;
  text-transform: uppercase; display: block; margin-bottom: 2px; }
.report-title { font-size: 26pt; font-weight: bold; color: #1E293B; display: block; line-height: 1; }
.report-subtitle { font-size: 11pt; color: #64748B; display: block; margin-top: 3px; }

.snap-grid { display: flex; gap: 3mm; margin-bottom: 6px; }
.snap-card { flex: 1; background: #F8FAFC; border: 0.5pt solid #E2E8F0;
  padding: 5px 4px; text-align: center; }
.snap-val { font-size: 20pt; font-weight: bold; display: block; line-height: 1; }
.snap-lbl { font-size: 7.5pt; color: #64748B; display: block; margin-top: 2px; }

table.summary-t { width: 100%; border-collapse: collapse; font-size: 8.5pt; margin-bottom: 4px; }
table.summary-t th { background: #1A3A5C; color: white; padding: 5px 6px;
  font-size: 7pt; letter-spacing: 0.8px; text-transform: uppercase; text-align: left; }
table.summary-t td { padding: 5px 6px; border-bottom: 0.3pt solid #E2E8F0; vertical-align: top; }
.group-hdr td { background: #F1F5F9; font-weight: bold; font-size: 7pt;
  color: #64748B; letter-spacing: 0.8px; text-transform: uppercase; padding: 3px 6px; }

.bullet-section { margin-top: 5px; }
.bullet-item { font-size: 9pt; color: #334155; line-height: 1.4;
  padding: 3px 0 3px 12px; border-left: 2pt solid #E2E8F0; margin-bottom: 4px; }

table.barchart { width: 100%; border-collapse: collapse; }
table.barchart td { padding: 2px 4px; vertical-align: middle; }
.bar-name { font-size: 8pt; font-weight: bold; color: #1E293B; width: 170px; white-space: nowrap; }
.bar-track { position: relative; height: 8px; background: #E2E8F0; }
.bar-fill { height: 8px; display: block; }
.bar-score { font-size: 8.5pt; font-weight: bold; width: 36px; text-align: right; }

@page { @bottom-center {
  content: "JV People & Culture Pulse Report — Poland 2026  ·  Confidential";
  font-size: 7pt; color: #94A3B8; font-family: Arial, sans-serif; } }
"""

# ── HTML helpers ──────────────────────────────────────────────────────────────
def zh(text, cls='zh-dark'):
    return f'<div class="zh {cls}">{e(text)}</div>'

def q_row_html(q):
    status = q['status']
    row_cls = f"{status.lower()}-row"
    clr_cls = f"{status.lower()}-c"
    # FIX 1: No type column — strip burden tags from display text
    txt = re.sub(r'\s*\[.*?\]$', '', q['text']).strip()
    txt = re.sub(r'\[Burden.*?\]', '', txt).strip()
    sb_text = q.get('sb', '')
    # FIX 1: Two columns only — question and score/status and SB text
    return f"""    <tr class="{row_cls}">
      <td class="qtext">{e(txt)}</td>
      <td class="scell"><span class="snum {clr_cls}">{q['score']:.2f}</span><span class="ssts {clr_cls}">{e(status)}</span></td>
      <td class="sbtext">{e(sb_text)}</td>
    </tr>"""

def strength_items(items):
    return '\n'.join(
        f'<div class="col-item strength-item">&#10003;&nbsp; {e(s)}</div>'
        for s in items
    )

def growth_items(items, status):
    gcls = f"growth-{status.lower()}"
    return '\n'.join(
        f'<div class="col-item {gcls}">&#8594;&nbsp; {e(g)}</div>'
        for g in items
    )

def lq_items(items):
    rows = []
    for i, q in enumerate(items, 1):
        rows.append(f"""  <div class="lq-row">
    <div class="lq-num">{i}</div>
    <div class="lq-text">{e(q)}</div>
  </div>""")
    return '\n'.join(rows)

def quote_rows(quotes):
    quotes = quotes[:4]
    rows = []
    for i in range(0, len(quotes), 2):
        q1 = quotes[i]
        q2 = quotes[i+1] if i+1 < len(quotes) else ''
        if q2:
            rows.append(f"""  <tr>
    <td><span class="qmark">&ldquo;</span> {e(q1)}</td>
    <td><span class="qmark">&ldquo;</span> {e(q2)}</td>
  </tr>""")
        else:
            rows.append(f"""  <tr>
    <td colspan="2"><span class="qmark">&ldquo;</span> {e(q1)}</td>
  </tr>""")
    return '\n'.join(rows)

# ── Summary page ──────────────────────────────────────────────────────────────
def summary_html():
    bar_rows = []
    for name, score, status, n, explore in SUMMARY:
        clr = sc(status)
        pct = ((score - 1) / 4) * 100
        bar_rows.append(f"""  <tr>
    <td class="bar-name" style="color:{clr};">{e(name)}</td>
    <td><div class="bar-track"><span class="bar-fill" style="width:{pct:.1f}%; background:{clr};"></span></div></td>
    <td class="bar-score" style="color:{clr};">{score:.2f}</td>
  </tr>""")

    def group_table(group_name, group_rows):
        rows_html = []
        for i, (name, score, status, n, explore) in enumerate(group_rows):
            rows_html.append(f"""    <tr style="background:{sb(status) if i%2==0 else 'white'};">
      <td style="font-weight:bold; color:{sc(status)};">{e(name)}</td>
      <td style="font-weight:bold; color:{sc(status)}; text-align:center;">{score:.2f}</td>
      <td style="text-align:center;"><span style="font-weight:bold; font-size:7.5pt; color:{sc(status)};">{e(status)}</span></td>
      <td style="font-style:italic; font-size:8pt; color:#475569;">{e(explore)}</td>
    </tr>""")
        return f'<tr class="group-hdr"><td colspan="4">{group_name}</td></tr>\n' + '\n'.join(rows_html)

    concern_rows = [r for r in SUMMARY if r[2]=='Concern']
    watch_rows   = [r for r in SUMMARY if r[2]=='Watch']
    healthy_rows = [r for r in SUMMARY if r[2]=='Healthy']
    bullets_html = '\n'.join(f'<div class="bullet-item">{b[0]}</div>' for b in OVERALL_BULLETS)

    return f"""<div class="page">
  <div class="report-title-block">
    <span class="pc-label">People &amp; Culture</span>
    <span class="report-title">Pulse Report</span>
    <span class="report-subtitle">Poland &nbsp;&middot;&nbsp; 2026</span>
  </div>

  <div class="snap-grid">
    <div class="snap-card"><span class="snap-val" style="color:#FF6600;">20</span><span class="snap-lbl">Respondents</span></div>
    <div class="snap-card"><span class="snap-val" style="color:#1A3A5C;">9</span><span class="snap-lbl">Departments</span></div>
    <div class="snap-card"><span class="snap-val" style="color:#FF6600;">3.54</span><span class="snap-lbl">Avg score</span></div>
    <div class="snap-card"><span class="snap-val" style="color:#B91C1C;">3</span><span class="snap-lbl">Concern</span></div>
    <div class="snap-card"><span class="snap-val" style="color:#B45309;">2</span><span class="snap-lbl">Watch</span></div>
    <div class="snap-card"><span class="snap-val" style="color:#166534;">4</span><span class="snap-lbl">Healthy</span></div>
  </div>

  {zh('Department scores — sorted worst to best', 'zh-dark')}
  <table class="barchart">
{''.join(bar_rows)}
  </table>
  <div style="font-size:7pt; color:#94A3B8; margin-bottom:5px;">
    Thresholds: 2.50 (Concern / Watch) &nbsp;&middot;&nbsp; 3.50 (Watch / Healthy)
  </div>

  <table class="summary-t">
    <tr><th style="width:130px;">Department</th><th style="width:50px; text-align:center;">Score</th><th style="width:65px; text-align:center;">Status</th><th>Area to explore further</th></tr>
    {group_table('Concern', concern_rows)}
    {group_table('Watch',   watch_rows)}
    {group_table('Healthy', healthy_rows)}
  </table>
  <div style="font-size:7pt; color:#94A3B8; margin-bottom:6px;">
    Concern status also triggered when 3 or more questions in a department score at Concern level &nbsp;&middot;&nbsp; Healthy &ge; 3.50 &nbsp;&middot;&nbsp; Watch 2.50&ndash;3.49 &nbsp;&middot;&nbsp; Concern &lt; 2.50
  </div>

  <div class="section-block">
  {zh('Overall picture', 'zh-dark')}
  <div class="bullet-section" style="margin-top:3px;">
{bullets_html}
  </div>
  </div>
</div>"""

# ── Department page ───────────────────────────────────────────────────────────
def dept_page_html(display_name, report_key, q_key, rank, score, status, n_total):
    data = report.get(report_key, {})
    qs   = dept_q.get(q_key, [])
    status_lbl_color = STATUS_PILL.get(status, '#E2E8F0')
    meta_bg = STATUS_BG.get(status, '#F8FAFC')
    is_jvk = q_key == 'JVK'
    is_lc  = q_key == 'L&C'

    status_note = 'Status set by concern-count rule' if status == 'Concern' else f'Score: {score:.2f}'

    # Question table
    def q_table(questions, group_label=None):
        rows = ''
        if group_label:
            rows += f'<tr><td colspan="3" class="group-label">{e(group_label)}</td></tr>\n'
        for q in questions:
            rows += q_row_html(q) + '\n'
        return rows

    def sort_by_status_then_score(questions):
        order = {'Concern': 0, 'Watch': 1, 'Healthy': 2}
        return sorted(questions, key=lambda q: (order.get(q['status'], 1), q['score']))

    if is_jvk:
        groups = {}
        for q in qs:
            g = q.get('group') or 'All Parents'
            groups.setdefault(g, []).append(q)
        q_html = ''.join(q_table(sort_by_status_then_score(g_qs), g_label) for g_label, g_qs in groups.items())
    elif is_lc:
        groups = {}
        for q in qs:
            g = q.get('group') or 'All Staff'
            groups.setdefault(g, []).append(q)
        q_html = ''.join(q_table(sort_by_status_then_score(g_qs), g_label) for g_label, g_qs in groups.items())
    else:
        q_html = q_table(sort_by_status_then_score(qs))

    # Merge JVK/LC data
    if is_jvk:
        d2nd = report.get('JVK_2nd', {}); d1st = report.get('JVK_1st', {})
        s2 = d2nd.get('s2',[]) + d1st.get('s2',[])
        s3 = d2nd.get('s3',[]) + d1st.get('s3',[])
        s4 = d2nd.get('s4',[]) + d1st.get('s4',[])
        s5 = d2nd.get('s5',[]) + d1st.get('s5',[])
    elif is_lc:
        d2nd = report.get('LC_2nd', {}); d1st = report.get('LC_1st', {})
        s2 = d2nd.get('s2',[]) + d1st.get('s2',[])
        s3 = d2nd.get('s3',[]) + d1st.get('s3',[])
        s4 = d2nd.get('s4',[]) + d1st.get('s4',[])
        s5 = d2nd.get('s5',[]) + d1st.get('s5',[])
    else:
        s2 = data.get('s2',[]); s3 = data.get('s3',[])
        s4 = data.get('s4',[]); s5 = data.get('s5',[])

    s2_zh = 'zh-green'
    s3_zh = {'Concern':'zh-red','Watch':'zh-amber','Healthy':'zh-navy'}.get(status,'zh-navy')

    sg_section = ''
    if s2 or s3:
        strengths_html = f"""    <div class="col-half">
      {zh('What is working', s2_zh)}
      {strength_items(s2)}
    </div>""" if s2 else ''
        growth_html = f"""    <div class="col-half">
      {zh('Where attention is needed', s3_zh)}
      {growth_items(s3, status)}
    </div>""" if s3 else ''
        sg_section = f"""  <div class="section-block"><div class="two-col">
{strengths_html}
{growth_html}
  </div></div>"""

    lq_section = ''
    if s4:
        lq_section = f"""  <div class="section-block">
  <div class="lq-section">
    {zh('Questions for leadership', 'zh-navy')}
    <div style="padding:2px 0;">
{lq_items(s4)}
    </div>
  </div>
  </div>"""

    quote_section = ''
    if s5:
        # FIX 2: Use plain apostrophe in prompt, not HTML entity
        prompt = PROMPTS.get(q_key, '').replace("'", '\u2019')
        quote_section = f"""  <div class="section-block">
  {zh(f'What staff said \u2014 \u201c{e(prompt)}\u201d', 'zh-slate')}
  <div style="height:2px;"></div>
  <table class="qg">
{quote_rows(s5)}
  </table>
  </div>"""

    # FIX 1: Table header has no Type column — 3 cols: Question | Score/Status | Meaning
    return f"""<div class="page">
  <div class="dept-header">
    <div class="dept-name">{e(display_name)}</div>
    <div class="dept-score-block">
      <span class="dept-score">{score:.2f}</span>
      <span class="dept-status-lbl" style="color:{status_lbl_color};">{e(status).upper()}</span>
    </div>
  </div>
  <div class="meta-bar" style="background:{meta_bg};">
    <span>Respondents: <strong>n = {n_total}</strong></span>
    <span>Rank <strong>{rank}</strong> of 9</span>
    <span class="meta-note">{e(status_note)}</span>
  </div>
  <div style="height:3px;"></div>

  {zh('Question scores — Concern · Watch · Healthy', 'zh-dark')}
  <table class="qs">
    <tr>
      <th>Question</th>
      <th class="c">Score / Status</th>
      <th>What this score means</th>
    </tr>
{q_html}
  </table>

{sg_section}

{lq_section}

{quote_section}
</div>"""

# ── Assemble and build ────────────────────────────────────────────────────────
pages = [summary_html()]
for row in DEPT_PAGES:
    display_name, report_key, q_key, rank, score, status, n_total, _ = row
    pages.append(dept_page_html(display_name, report_key, q_key, rank, score, status, n_total))

full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{CSS}
</style>
</head>
<body>
{''.join(pages)}
</body>
</html>"""

html_path = '/home/claude/full_report.html'
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(full_html)
print(f"HTML written: {html_path}")

pdf_path = '/mnt/user-data/outputs/Poland_Pulse_Report_2026.pdf'
weasyprint.HTML(filename=html_path).write_pdf(pdf_path)
print(f"PDF written: {pdf_path}")
