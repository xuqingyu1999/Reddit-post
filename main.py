###############################################################################
# 0️⃣  ADD OR REPLACE the code below in your existing reddit_like_experiment.py
###############################################################################
import streamlit as st
from datetime import datetime
import uuid, csv, os

# --------------------------------------------------------------------------- #
# 1. PALETTE & HELPER FOR DYNAMIC CSS                                          #
# --------------------------------------------------------------------------- #
PALETTE = {
    "neutral_bg":  "#ECEFF1",
    "neutral_fg":  "#000000",
    "up_bg":       "#FF4500",   # Reddit orange‑red
    "down_bg":     "#6E4AFF",   # Indigo‑purple
    "active_fg":   "#FFFFFF",
}

def _inject_vote_css(user_vote: int):
    """Inject dynamic CSS that colours the buttons and brings ▲ N ▼ closer."""
    # --- decide colours for this render pass ---------------------------------
    up_bg   = PALETTE["up_bg"]   if user_vote ==  1 else PALETTE["neutral_bg"]
    down_bg = PALETTE["down_bg"] if user_vote == -1 else PALETTE["neutral_bg"]
    up_fg   = PALETTE["active_fg"] if user_vote ==  1 else PALETTE["neutral_fg"]
    down_fg = PALETTE["active_fg"] if user_vote == -1 else PALETTE["neutral_fg"]
    score_c = (
        up_bg if user_vote == 1 else
        down_bg if user_vote == -1 else
        PALETTE["neutral_fg"]
    )

    st.markdown(
        f"""
        <style>
        /* ───── BUTTONS & SCORE COLOURS ───── */
        div[data-testid="column"]:nth-of-type(1) button{{
            border-radius:9999px !important;
            padding:4px 10px !important;
            background:{up_bg} !important;
            color:{up_fg} !important;
            border:none !important;
            min-width:auto !important;
        }}
        div[data-testid="column"]:nth-of-type(2) button{{
            border-radius:9999px !important;
            padding:4px 10px !important;
            background:{down_bg} !important;
            color:{down_fg} !important;
            border:none !important;
            min-width:auto !important;
        }}
        span.vote-score{{
            font-weight:600;
            color:{score_c};
            padding:0 2px;                    /* virtually no gap */
        }}

        /* ───── COLLAPSE THE 3‑COLUMN ROW ───── */
        /* The vote widget is the first st.columns() row in the page.          */
        div[data-testid="stHorizontalBlock"]:nth-of-type(1){{
            display:inline-flex !important;   /* shrink to contents           */
            gap:0 !important;                 /* NO extra space               */
            align-items:center !important;
        }}
        div[data-testid="stHorizontalBlock"]:nth-of-type(1) > div[data-testid="column"]{{
            flex:0 0 auto !important;         /* prevent stretching           */
            width:auto !important;
            padding:0 !important;
            margin:0 !important;
        }}
        button:focus{{outline:none;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------- #
# 2. (UNCHANGED) SESSION‑STATE INITIALISATION & LOGGING                       #
# --------------------------------------------------------------------------- #
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

DEFAULT_SCORE = 5
st.session_state.setdefault("vote_count", DEFAULT_SCORE)
st.session_state.setdefault("user_vote", 0)          # -1 / 0 / +1
st.session_state.setdefault("comments",  [])

LOGFILE = "interaction_log.csv"
if not os.path.exists(LOGFILE):
    with open(LOGFILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["timestamp", "session_id", "event", "payload"])

def log(ev: str, payload: str = ""):
    with open(LOGFILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([datetime.utcnow().isoformat(),
                                st.session_state.session_id, ev, payload])

# --------------------------------------------------------------------------- #
# 3.  VOTE WIDGET WITH THE NEW LOOK                                           #
# --------------------------------------------------------------------------- #
from pathlib import Path
from datetime import datetime
import base64, mimetypes

BANNER_PNG = Path(__file__).parent / "reddit_logo.png"   # 200×200 px works fine
mime = mimetypes.guess_type(BANNER_PNG)[0] or "image/png"
banner_b64 = base64.b64encode(BANNER_PNG.read_bytes()).decode()

st.markdown(
    f"""
    <style>
    /* Streamlit 1.32+ sets its main h1 (st.title) to 2rem / 32 px.            */
    /* If that ever changes you can bump this one number below.               */
    :root {{
        --banner-font-size: 2rem;
    }}
    </style>

    <div style="
         display:flex;align-items:center;gap:10px;
         width:100%;
         /* ↑ container grows full‑width, but we add generous padding */
         padding:16px 0 24px 0;      /* top / sides / bottom */
    ">
        <!-- logo -->
        <img src="data:{mime};base64,{banner_b64}"
             style="width:36px;height:36px;">
        <!-- word‑mark -->
        <span style="
              font-family:Roboto,Arial,sans-serif;
              font-size:var(--banner-font-size);
              line-height:1.1;
              font-weight:700;
              color:#FF4500;">
            reddit
        </span>
    </div>
    <!-- horizontal rule with extra margin to push body down a bit -->
    <hr style="margin:0 0 20px 0;">
    """,
    unsafe_allow_html=True,
)

# ---------- AUTHOR HEADER (Reddit‑style) ----------
SUBREDDIT      = "r/business"
AUTHOR_NAME    = "Fit_Bet_1261"
PUBLISHED_AT   = datetime(2025, 5, 11, 10, 30)          # ↩ your real post time
DAYS_AGO       = (datetime.utcnow() - PUBLISHED_AT).days
AVATAR_LOCAL   = Path(__file__).parent / "avatar.jpg"    # ↩ 40×40px preferred

import base64, mimetypes
mime_type = mimetypes.guess_type(AVATAR_LOCAL)[0] or "image/png"
avatar_b64 = base64.b64encode(AVATAR_LOCAL.read_bytes()).decode()

st.markdown(
    f"""
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
        <img src="data:{mime_type};base64,{avatar_b64}"
             style="width:40px;height:40px;border-radius:50%;object-fit:cover;">
        <div style="line-height:1;">
            <div style="font-weight:700;">
                {SUBREDDIT}&nbsp;&bull;&nbsp;{DAYS_AGO}&nbsp;days&nbsp;ago
            </div>
            <div style="color:#6e6e6e;font-size:0.85rem;">
                {AUTHOR_NAME}
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.title("Rate My Business Idea")

st.markdown(
    """
    Hey, I've been in the app/website/startup development space for a good portion of my life (don't take this too far, as I'm still fairly young), and my mind wandered upon an idea that I think could have potential.

As someone who runs many side-hustles and SaaS businesses, I always had trouble with marketing my business and finding Social Media content creators that were willing and capable of doing so was hard.

I just felt like, if I could just put in some money, and advertisements would make themselves, then I'd had a much easier time growing my businesses. Then I came across the idea, what if I made a platform similar to Whop, Posted, and Fiverr, but for businesses and content creators.

I know it seems vague, but let me dive into it a bit more. Essentially, businesses would be able to create listings/posts that would have a set CPM (Cost Per Mille), Max Budget, Max Payout, required hashtags, and allowed Social Media Platforms. In these listings, there would be information on the business to get an idea of what they're about. On the content creators side, they could search through listings that align with things their interested in (for example, a content creator creates content centered around Computers[like CarterPCs], so they'll most likely find a business that builds computers for you [like Build Redux]).

After the content creator finds a business they like, they can gather some info on it, and they can create a Social Media video about it. After the social media creator creates their video, they can publish it to the listing, and depending on how well it performs by the time the business' listing ends, they get payed based on the set CPM. (So if CarterPCs gets 500k views on a video, and the Build Redux's CPM is \$0.50, then CarterPCs gets \$250).

It's an idea that I haven't put much thought into, but I thought it would be best to hear what you guys think.

PS, the creation of this isn't a problem for me as I have the skills to do so, I'm just scared how I'll get the first load of Businesses and Content Creators onto it in the first place. Also, so that I get enough money to maintain the business and myself, I'll just take a small cut from both the business and the content creator's side.  
    """
)
cols = st.columns([1, 1, 1])    # 3 equal columns → ▲  number  ▼

# ---------- VOTE PILL --------------------------------------------------------
# Four columns: ▲ | number | ▼ | (big empty spacer)
cols = st.columns([0.8, 0.2, 1, 8.2], gap="small")

with cols[0]:
    if st.button("▲", key="up_btn"):
        if st.session_state.user_vote == 1:
            st.session_state.vote_count -= 1
            st.session_state.user_vote = 0
            log("undo_upvote")
        else:
            if st.session_state.user_vote == -1:
                st.session_state.vote_count += 1
            st.session_state.vote_count += 1
            st.session_state.user_vote = 1
            log("upvote")

with cols[2]:
    if st.button("▼", key="down_btn"):
        if st.session_state.user_vote == -1:
            st.session_state.vote_count += 1
            st.session_state.user_vote = 0
            log("undo_downvote")
        else:
            if st.session_state.user_vote == 1:
                st.session_state.vote_count -= 1
            st.session_state.vote_count -= 1
            st.session_state.user_vote = -1
            log("downvote")

with cols[1]:
    st.markdown(
        f"<div style='display:flex;justify-content:center;"
        f"align-items:center;height:100%;'>"
        f"<span class='vote-score'>{st.session_state.vote_count}</span></div>",
        unsafe_allow_html=True,
    )

# --- Strip the default column padding so the three visible columns touch ---
st.markdown(
    """
    <style>
    /* First st.columns() block after the banner = vote row */
    div[data-testid="stHorizontalBlock"]:nth-of-type(2){
        column-gap:0 !important;
    }
    div[data-testid="stHorizontalBlock"]:nth-of-type(2)
        > div[data-testid="column"]{
        padding:0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Inject the CSS **after** the vote logic so colours reflect the new state
_inject_vote_css(st.session_state.user_vote)

# --------------------------------------------------------------------------- #
# 4.  (UNCHANGED) COMMENT FORM & LIST                                         #
# --------------------------------------------------------------------------- #
st.divider()
st.subheader("Add your comment")
with st.form("comment_form", clear_on_submit=True):
    txt = st.text_area("", placeholder="Write something…", height=120)
    if st.form_submit_button("Post"):
        if txt.strip():
            st.session_state.comments.append((datetime.utcnow(), txt.strip()))
            log("comment", txt.strip())
            st.success("Comment posted!")

if st.session_state.comments:
    st.subheader("Your comments")
    for ts, txt in reversed(st.session_state.comments):
        with st.expander(f"🗨️ {ts.strftime('%Y-%m-%d %H:%M:%S')} UTC", expanded=False):
            st.markdown(txt)

st.caption("Clicks & comments are logged locally to interaction_log.csv")

###############################################################################
# END OF PATCH
###############################################################################
