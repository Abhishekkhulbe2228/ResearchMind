import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,300;0,400;0,600;0,700;0,800;1,700;1,800&family=Barlow:wght@300;400;500&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg:         #0f0d0b;
    --bg2:        #181410;
    --surface:    #1c1814;
    --surface2:   #231e19;
    --border:     #2e2820;
    --orange:     #f26419;
    --orange2:    #ff8c42;
    --orange-dim: rgba(242,100,25,.12);
    --green:      #39d353;
    --green-dim:  rgba(57,211,83,.10);
    --red:        #f05454;
    --text:       #e8e0d5;
    --muted:      #7a6e63;
    --display:    'Barlow Condensed', sans-serif;
    --body:       'Barlow', sans-serif;
    --mono:       'Space Mono', monospace;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text);
    font-family: var(--body);
}
[data-testid="stHeader"]              { background: transparent !important; }
[data-testid="stSidebar"]             { background: var(--bg2) !important; }
[data-testid="stMainBlockContainer"]  { padding-top: 0 !important; }
#MainMenu, footer                     { visibility: hidden; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3.2rem 1rem 1.6rem;
}
.hero-eyebrow {
    font-family: var(--mono);
    font-size: .65rem;
    letter-spacing: .22em;
    color: var(--orange);
    text-transform: uppercase;
    margin-bottom: .9rem;
}
.hero h1 {
    font-family: var(--display);
    font-size: clamp(3.5rem, 9vw, 7.5rem);
    font-weight: 800;
    font-style: italic;
    line-height: .95;
    color: var(--orange);
    margin: 0 0 1.1rem;
    text-transform: uppercase;
    letter-spacing: -.01em;
}
.hero p {
    color: var(--muted);
    font-size: .97rem;
    font-weight: 300;
    max-width: 440px;
    margin: 0 auto;
    line-height: 1.7;
}

/* ── Divider ── */
hr { border: none; border-top: 1px solid var(--border) !important; margin: 1rem 0 !important; }

/* ── Section label ── */
.section-label {
    font-family: var(--mono);
    font-size: .63rem;
    letter-spacing: .18em;
    color: var(--orange);
    text-transform: uppercase;
    display: block;
    margin-bottom: .45rem;
}

/* ── Text input ── */
.stTextInput > label { display: none !important; }
.stTextInput > div > div > input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: var(--body) !important;
    font-size: .97rem !important;
    padding: .78rem 1.05rem !important;
    caret-color: var(--orange);
    transition: border-color .2s, box-shadow .2s;
}
.stTextInput > div > div > input:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px rgba(242,100,25,.14) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }

/* ── Button ── */
.stButton > button {
    background: var(--orange) !important;
    border: none !important;
    border-radius: 8px !important;
    color: #0f0d0b !important;
    font-family: var(--display) !important;
    font-weight: 800 !important;
    font-style: italic !important;
    font-size: 1.1rem !important;
    letter-spacing: .05em !important;
    text-transform: uppercase !important;
    padding: .7rem 1.5rem !important;
    width: 100% !important;
    transition: background .15s, transform .12s;
}
.stButton > button:hover    { background: var(--orange2) !important; transform: translateY(-1px); }
.stButton > button:active   { transform: translateY(0); }
.stButton > button:disabled { background: var(--border) !important; color: var(--muted) !important; }

/* ── Pipeline card ── */
.pipe-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--border);
    border-radius: 8px;
    padding: .85rem 1rem;
    margin-bottom: .55rem;
    display: flex;
    align-items: center;
    gap: .85rem;
    transition: border-color .25s, background .25s;
}
.pipe-card.active { border-left-color: var(--orange); background: rgba(242,100,25,.07); }
.pipe-card.done   { border-left-color: var(--green);  background: var(--green-dim); }
.pipe-card.error  { border-left-color: var(--red);    background: rgba(240,84,84,.07); }

.pipe-num   { font-family: var(--mono); font-size: .6rem; color: var(--muted); min-width: 1.3rem; }
.pipe-body  { flex: 1; }
.pipe-title { font-weight: 500; font-size: .88rem; color: var(--text); }
.pipe-desc  { font-size: .73rem; color: var(--muted); margin-top: .08rem; }

.badge {
    font-family: var(--mono);
    font-size: .58rem;
    letter-spacing: .1em;
    text-transform: uppercase;
    padding: .18rem .5rem;
    border-radius: 4px;
    font-weight: 700;
    white-space: nowrap;
}
.badge-idle   { color: var(--muted); border: 1px solid var(--border); }
.badge-active { color: var(--orange); border: 1px solid var(--orange); background: var(--orange-dim); }
.badge-done   { color: var(--green);  border: 1px solid var(--green);  background: var(--green-dim); }
.badge-error  { color: var(--red);    border: 1px solid var(--red);    background: rgba(240,84,84,.1); }

/* ── Pipeline title ── */
.pipeline-title {
    font-family: var(--display);
    font-size: 1.55rem;
    font-weight: 800;
    font-style: italic;
    text-transform: uppercase;
    color: var(--text);
    margin-bottom: .75rem;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: .8rem 1rem !important;
}
[data-testid="stMetric"] label   { color: var(--muted) !important; font-size: .62rem !important; font-family: var(--mono) !important; letter-spacing: .1em !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"]     { color: var(--orange) !important; font-family: var(--display) !important; font-size: 1.7rem !important; font-weight: 700 !important; }

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: .2rem !important;
    gap: 0 !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 6px !important;
    font-family: var(--mono) !important;
    font-size: .68rem !important;
    letter-spacing: .07em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    padding: .38rem .85rem !important;
    transition: background .15s, color .15s;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: var(--orange) !important;
    color: #0f0d0b !important;
    font-weight: 700 !important;
}
[data-testid="stTabContent"] { padding-top: 1rem !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
[data-testid="stExpander"] summary { color: var(--text) !important; }

/* ── Result panel ── */
.result-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.3rem 1.4rem;
}
.rp-header {
    display: flex;
    align-items: center;
    margin-bottom: .9rem;
    padding-bottom: .75rem;
    border-bottom: 1px solid var(--border);
}
.rp-title {
    font-family: var(--display);
    font-size: 1.25rem;
    font-weight: 800;
    font-style: italic;
    color: var(--text);
    text-transform: uppercase;
    letter-spacing: .02em;
}
.rp-body {
    white-space: pre-wrap;
    line-height: 1.8;
    color: #9e8e7e;
    font-size: .88rem;
    font-weight: 300;
}

/* ── Text area ── */
.stTextArea textarea {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    font-family: var(--mono) !important;
    font-size: .74rem !important;
    border-radius: 8px !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    border: 1px solid var(--orange) !important;
    border-radius: 6px !important;
    color: var(--orange) !important;
    font-family: var(--mono) !important;
    font-size: .68rem !important;
    letter-spacing: .1em !important;
    text-transform: uppercase !important;
    padding: .42rem .95rem !important;
    width: auto !important;
    margin-top: 1rem !important;
}
[data-testid="stDownloadButton"] > button:hover { background: var(--orange-dim) !important; }

/* ── Warning ── */
[data-testid="stAlert"] {
    background: rgba(240,84,84,.08) !important;
    border: 1px solid rgba(240,84,84,.3) !important;
    border-radius: 8px !important;
    color: #f09090 !important;
}

/* ── Progress bar custom ── */
.prog-wrap {
    background: var(--border);
    border-radius: 4px;
    height: 4px;
    overflow: hidden;
    margin-top: .6rem;
}
.prog-fill {
    background: var(--orange);
    height: 100%;
    border-radius: 4px;
    transition: width .4s ease;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
def _init():
    for k, v in {
        "pipeline_run":  False,
        "running":       False,
        "state":         {},
        "error":         None,
        "elapsed":       0,
        "topic_ran":     "",
        "step_statuses": {"search":"idle","reader":"idle","writer":"idle","critic":"idle"},
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()


# ── Runner ────────────────────────────────────────────────────────────────────
def run_pipeline(topic: str):
    st.session_state.update(
        running=True, pipeline_run=False, error=None,
        state={}, topic_ran=topic,
        step_statuses={"search":"idle","reader":"idle","writer":"idle","critic":"idle"},
    )
    t0 = time.time()
    try:
        res = {}

        st.session_state.step_statuses["search"] = "active"
        sa = build_search_agent()
        sr = sa.invoke({"messages":[("user", f"Find recent, reliable and detailed information about: {topic}")]})
        for m in sr["messages"]:
            if hasattr(m,"name") and m.name=="web_search":
                res["search_results"] = m.content
        if "search_results" not in res:
            res["search_results"] = sr["messages"][-1].content
        st.session_state.step_statuses["search"] = "done"

        st.session_state.step_statuses["reader"] = "active"
        ra = build_reader_agent()
        rr = ra.invoke({"messages":[("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{res['search_results'][:800]}")]})
        for m in rr["messages"]:
            if hasattr(m,"name") and m.name=="scrape_url":
                res["scraped_content"] = m.content
        if "scraped_content" not in res:
            res["scraped_content"] = rr["messages"][-1].content
        st.session_state.step_statuses["reader"] = "done"

        st.session_state.step_statuses["writer"] = "active"
        res["report"] = writer_chain.invoke({
            "topic": topic,
            "research": f"SEARCH RESULTS:\n{res['search_results']}\n\nDETAILED SCRAPED CONTENT:\n{res['scraped_content']}"
        })
        st.session_state.step_statuses["writer"] = "done"

        st.session_state.step_statuses["critic"] = "active"
        res["feedback"] = critic_chain.invoke({"report": res["report"]})
        st.session_state.step_statuses["critic"] = "done"

        st.session_state.state   = res
        st.session_state.elapsed = round(time.time()-t0, 1)
        st.session_state.pipeline_run = True

    except Exception as e:
        st.session_state.error = str(e)
        for k, v in st.session_state.step_statuses.items():
            if v == "active":
                st.session_state.step_statuses[k] = "error"
    finally:
        st.session_state.running = False


# ── Step metadata ─────────────────────────────────────────────────────────────
STEPS = [
    ("search", "01", "Search Agent",  "Gathers recent web information"),
    ("reader", "02", "Reader Agent",  "Scrapes top relevant sources"),
    ("writer", "03", "Writer Chain",  "Drafts the structured report"),
    ("critic", "04", "Critic Chain",  "Reviews and scores the output"),
]
BADGE = {"idle":"Waiting","active":"Running","done":"✓ Done","error":"! Error"}


def pipe_card(key, num, title, desc):
    s   = st.session_state.step_statuses[key]
    css = s if s != "idle" else ""
    st.markdown(f"""
    <div class="pipe-card {css}">
        <span class="pipe-num">{num}</span>
        <div class="pipe-body">
            <div class="pipe-title">{title}</div>
            <div class="pipe-desc">{desc}</div>
        </div>
        <span class="badge badge-{s}">{BADGE[s]}</span>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════ RENDER ════════════════════════════════════

st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>ResearchMind</h1>
    <p>Four specialized AI agents collaborate — searching, scraping, writing, and
    critiquing — to deliver a polished research report on any topic.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)

left, right = st.columns([1, 1.65], gap="large")

# ── LEFT ──────────────────────────────────────────────────────────────────────
with left:
    st.markdown('<span class="section-label">Research Topic</span>', unsafe_allow_html=True)
    topic = st.text_input("t", placeholder="e.g. Quantum computing in 2025",
                          label_visibility="collapsed")
    st.markdown("<div style='height:.35rem'></div>", unsafe_allow_html=True)
    run_btn = st.button("Run Research →", disabled=st.session_state.running)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="pipeline-title">Pipeline</div>', unsafe_allow_html=True)

    for args in STEPS:
        pipe_card(*args)

    if st.session_state.pipeline_run:
        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        report_txt = str(st.session_state.state.get("report",""))
        with c1: st.metric("Time", f"{st.session_state.elapsed}s")
        with c2: st.metric("Words", f"{len(report_txt.split()):,}")

    if st.session_state.running:
        active_name = next(
            (t for k,_,t,_ in STEPS if st.session_state.step_statuses[k]=="active"), ""
        )
        st.markdown(
            f"<p style='font-family:Space Mono,monospace;font-size:.65rem;"
            f"letter-spacing:.12em;text-transform:uppercase;color:#7a6e63;"
            f"margin-top:.5rem'>⟳ &nbsp;{active_name}</p>",
            unsafe_allow_html=True)

# ── RIGHT ─────────────────────────────────────────────────────────────────────
with right:
    if run_btn:
        if topic.strip():
            run_pipeline(topic.strip())
            st.rerun()
        else:
            st.warning("Please enter a research topic first.")

    # Error
    if st.session_state.error:
        st.error(f"Pipeline error: {st.session_state.error}")

    # Results
    elif st.session_state.pipeline_run:
        st.markdown(
            f'<span class="section-label">Results — {st.session_state.topic_ran[:70]}</span>',
            unsafe_allow_html=True)

        t1, t2, t3 = st.tabs(["Report", "Critic Review", "Raw Data"])

        with t1:
            report = st.session_state.state.get("report","")
            if hasattr(report,"content"): report = report.content
            report = str(report)
            st.markdown(f"""
            <div class="result-panel">
                <div class="rp-header"><span class="rp-title">Research Report</span></div>
                <div class="rp-body">{report}</div>
            </div>""", unsafe_allow_html=True)
            st.download_button(
                "↓ Download Report (.txt)", data=report,
                file_name=f"report_{st.session_state.topic_ran[:30].replace(' ','_')}.txt",
                mime="text/plain")

        with t2:
            fb = st.session_state.state.get("feedback","")
            if hasattr(fb,"content"): fb = fb.content
            fb = str(fb)
            st.markdown(f"""
            <div class="result-panel">
                <div class="rp-header"><span class="rp-title">Critic Feedback</span></div>
                <div class="rp-body">{fb}</div>
            </div>""", unsafe_allow_html=True)

        with t3:
            with st.expander("Search Results"):
                st.text_area("s", value=str(st.session_state.state.get("search_results","")),
                             height=200, label_visibility="collapsed")
            with st.expander("Scraped Content"):
                st.text_area("c", value=str(st.session_state.state.get("scraped_content","")),
                             height=200, label_visibility="collapsed")

    # Running — progress card
    elif st.session_state.running:
        done = sum(1 for v in st.session_state.step_statuses.values() if v=="done")
        pct  = int(done/4*100)
        active_name = next(
            (t for k,_,t,_ in STEPS if st.session_state.step_statuses[k]=="active"), "Processing")
        st.markdown(f"""
        <div class="result-panel" style="text-align:center;padding:3.5rem 2rem">
            <div style="font-family:'Barlow Condensed',sans-serif;font-size:5rem;
                        font-weight:800;font-style:italic;color:#f26419;
                        text-transform:uppercase;line-height:1">{pct}%</div>
            <p style="font-family:'Space Mono',monospace;font-size:.68rem;
                      letter-spacing:.14em;text-transform:uppercase;
                      color:#7a6e63;margin:.6rem 0 1.2rem">{active_name}</p>
            <div class="prog-wrap">
                <div class="prog-fill" style="width:{pct}%"></div>
            </div>
            <p style="color:#4a3f35;font-size:.78rem;margin-top:.8rem">
                Step {done} of 4 complete
            </p>
        </div>""", unsafe_allow_html=True)
        time.sleep(1.5)
        st.rerun()

    # Idle
    else:
        st.markdown("""
        <div class="result-panel" style="text-align:center;padding:4rem 2rem;border-style:dashed">
            <div style="font-family:'Barlow Condensed',sans-serif;font-size:5rem;
                        font-weight:800;font-style:italic;text-transform:uppercase;
                        color:#2e2820;line-height:1">Ready</div>
            <p style="color:#4a3f35;font-size:.88rem;margin-top:.9rem;font-weight:300">
                Enter a topic and click
                <strong style="color:#f26419;font-style:italic">Run Research →</strong>
                <br>to start the four-agent pipeline.
            </p>
            <div style="display:flex;gap:.45rem;justify-content:center;
                        flex-wrap:wrap;margin-top:1.4rem">
                <span class="badge badge-idle">Search Agent</span>
                <span class="badge badge-idle">Reader Agent</span>
                <span class="badge badge-idle">Writer Chain</span>
                <span class="badge badge-idle">Critic Chain</span>
            </div>
        </div>""", unsafe_allow_html=True)