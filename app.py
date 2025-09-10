
###############################################################################
#  MEGA-MERGED  :  AI Automation Hub  +  Desktop Assistant  +  File Manager
#               +  SSH Assistant  +  Live AI Camera  +  Saundarya Lite
#               +  Motivation Buddy  -  All features preserved
###############################################################################
import datetime
import os
import streamlit as st
from collections import defaultdict
import pandas as pd
import cv2
from PIL import Image
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------------
# 1.  Import helper modules
# ------------------------------------------------------------------
import utility_manager      # AI Automation Hub utilities
import pc_task              # Desktop Assistant (voice / hot-key tasks)
import file_manager         # Advanced File-Manager
import ssh_gemini_manager   # AI + SSH helper
import cv_manager           # AI Camera backend
import saundarya_manager    # Fashion assistant
import motivation_manager   # Motivation buddy
import vehicle_manager      # AI Vehicle Recommender Hub
import regression_manager   # Study Hours vs Marks Predictor
import ml_manager           # Interactive Classification Lab

# ------------------------------------------------------------------
# 2.  Load secrets – independent try-blocks so any can fail
# ------------------------------------------------------------------
# --- 2-A  Secrets for AI Automation Hub ---
try:
    from my_secrets import (
        EMAIL, EMAIL_PASSWORD, WHATSAPP_TEST_NUMBER,
        TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE, TWILIO_WHATSAPP,
        INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD,
        TWITTER_API_KEY, TWITTER_API_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )
    HUB_SECRETS_OK = True
except ImportError:
    HUB_SECRETS_OK = False

# --- 2-B  Secrets for Desktop / File-Manager / SSH ---
try:
    from my_secrets import GEMINI_API_KEY, SSH_IP, SSH_USER, SSH_PASS
    gemini_model = ssh_gemini_manager.configure_gemini(GEMINI_API_KEY)
    if isinstance(gemini_model, str):
        st.error(gemini_model)
        st.stop()
    SSH_SECRETS_OK = True
except ImportError:
    SSH_SECRETS_OK = False
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDlFTIqP6j8DO97JJXGDXPs4jRU4UNaMmo")

###############################################################################
# 3.  Sidebar Router – lets user choose which world to enter
###############################################################################
st.set_page_config(page_title="Unified AI Hub", layout="wide")
st.sidebar.title("🧭 Navigation")
main_choice = st.sidebar.radio(
    "Choose environment:",
    ("Home",
     "AI Automation Hub (9 Tools)", 
     "Desktop Assistant", 
     "File Manager", 
     "SSH Assistant", 
     "Live AI Camera", 
     "Saundarya Lite", 
     "Motivation Buddy",
     "AI Vehicle Recommender Hub",
     "Study Hours vs Marks Predictor",
     "Interactive Classification Lab")
)

###############################################################################
# 4.  COMMAND_MENU for SSH Assistant (full original list)
###############################################################################
COMMAND_MENU = {
    "System Information": {
        "Show date and time": "date",
        "Show system uptime": "uptime",
        "Show system info (kernel, etc.)": "uname -a",
        "Display CPU information": "lscpu",
        "Display memory information": "free -h",
        "List block devices (disks)": "lsblk",
        "Show OS architecture (32/64 bit)": "getconf LONG_BIT",
        "Show kernel version": "uname -r",
        "Show hostname": "hostname",
        "Show BIOS information": "sudo dmidecode -t bios",
        "List PCI devices": "lspci",
        "List USB devices": "lsusb",
    },
    "User & Process Management": {
        "Show current user": "whoami",
        "List logged-in users and their activity": "w",
        "Show last 10 logins": "last -n 10",
        "Top 10 memory-consuming processes": "ps aux --sort=-%mem | head -11",
        "Top 10 CPU-consuming processes": "ps aux --sort=-%cpu | head -11",
        "List running services": "systemctl list-units --type=service --state=running",
        "Show process tree": "pstree",
        "List scheduled cron jobs": "crontab -l",
        "List all users": "cut -d: -f1 /etc/passwd",
    },
    "File & Directory Management": {
        "List files (long format)": "ls -lah",
        "Show current directory path": "pwd",
        "Show disk usage": "df -h",
        "Show folder sizes in current directory": "du -sh * | sort -rh",
        "List 10 newest files/folders": "ls -lt | head -n 11",
        "Show mounted filesystems": "mount | column -t",
        "Find top 10 largest files": "find . -type f -print0 | xargs -0 du -h | sort -rh | head -n 10",
    },
    "Networking": {
        "Show IP configuration": "ip a",
        "Display routing table": "ip route",
        "Show active connections": "ss -tuln",
        "Test internet connectivity (ping Google)": "ping -c 4 8.8.8.8",
        "Show open ports and services": "sudo netstat -tulpn",
        "Show local IP addresses": "hostname -I",
        "Perform DNS lookup for google.com": "dig google.com",
        "Show network statistics": "ss -s",
        "Show ARP table": "arp -a",
    },
    "Security & Logs": {
        "Show last 10 failed logins": "sudo lastb -n 10",
        "Show firewall rules (iptables)": "sudo iptables -L -n -v",
        "Check SELinux status": "sestatus",
        "Show last 20 authentication logs (Debian/Ubuntu)": "sudo cat /var/log/auth.log | tail -n 20",
        "Show last 20 secure logs (CentOS/RHEL)": "sudo cat /var/log/secure | tail -n 20",
        "Show last 50 system journal logs": "journalctl -n 50 --no-pager",
        "List processes using port 80": "sudo lsof -i :80",
        "Show systemd failed units": "systemctl --failed",
    }
}

###############################################################################
# 5.  Main rendering functions
###############################################################################
# ------------------ 5-A  AI Automation Hub ------------------
def render_ai_automation_hub():
    st.title("🤖 AI Automation Hub")
    st.info("Your central dashboard for communication, social-media & web-automation tasks.")
    if not HUB_SECRETS_OK:
        st.error("Missing secrets for AI Automation Hub")
        return

    tabs = st.tabs([
        "WhatsApp (Browser)", "Email (Gmail)", "WhatsApp (API)", "SMS (API)",
        "Call (API)", "Google Search", "Instagram Post", "Twitter/X Post",
        "Web Scraper"
    ])

    # ---------- Tab 0 : WhatsApp (pywhatkit) ----------
    with tabs[0]:
        st.subheader("Schedule WhatsApp via Browser")
        st.warning("WhatsApp Web will open – stay logged in.")
        number = st.text_input("Recipient (+91...)", value=WHATSAPP_TEST_NUMBER, key="py_num")
        message = st.text_area("Message", key="py_msg")
        c1, c2 = st.columns(2)
        now = datetime.datetime.now()
        hour = c1.number_input("Hour (24h)", 0, 23, now.hour, key="py_h")
        minute = c2.number_input("Minute", 0, 59, (now.minute + 2) % 60, key="py_m")
        if st.button("Schedule", key="py_btn"):
            if number and message:
                try:
                    utility_manager.send_whatsapp_pywhatkit(number, message, hour, minute)
                    st.success("Scheduled! Browser will open at the set time.")
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("Fill both number and message.")

    # ---------- Tab 1 : Email ----------
    with tabs[1]:
        st.subheader("Send Email via Gmail")
        st.info("Use Google 'App Password'.")
        to = st.text_input("To", key="mail_to")
        subj = st.text_input("Subject", key="mail_sub")
        body = st.text_area("Body", key="mail_body")
        if st.button("Send", key="mail_btn"):
            if to and subj and body:
                try:
                    utility_manager.send_email_gmail(subj, body, to, EMAIL, EMAIL_PASSWORD)
                    st.success("Email sent!")
                except Exception as e:
                    st.error(str(e))

    # ---------- Tab 2 : WhatsApp (Twilio) ----------
    with tabs[2]:
        st.subheader("WhatsApp via Twilio API")
        to_wa = st.text_input("WhatsApp Number", value=WHATSAPP_TEST_NUMBER, key="tw_wa_num")
        msg_wa = st.text_area("Message", key="tw_wa_msg")
        if st.button("Send", key="tw_wa_btn"):
            if to_wa and msg_wa:
                try:
                    utility_manager.send_whatsapp_twilio(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN,
                                                         TWILIO_WHATSAPP, to_wa, msg_wa)
                    st.success("WhatsApp sent via Twilio!")
                except Exception as e:
                    st.error(str(e))

    # ---------- Tab 3 : SMS ----------
    with tabs[3]:
        st.subheader("Send SMS via Twilio")
        to_sms = st.text_input("Mobile Number", value=WHATSAPP_TEST_NUMBER, key="tw_sms_num")
        sms_msg = st.text_area("SMS Text", key="tw_sms_msg")
        if st.button("Send SMS", key="tw_sms_btn"):
            if to_sms and sms_msg:
                try:
                    utility_manager.send_sms_twilio(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN,
                                                    TWILIO_PHONE, to_sms, sms_msg)
                    st.success("SMS sent!")
                except Exception as e:
                    st.error(str(e))

    # ---------- Tab 4 : Phone Call ----------
    with tabs[4]:
        st.subheader("Initiate Phone Call")
        st.info("Twilio will call and play TwiML audio.")
        to_call = st.text_input("Number to Call", value=WHATSAPP_TEST_NUMBER, key="tw_call_num")
        twiml_url = st.text_input("TwiML URL", value="http://demo.twilio.com/docs/voice.xml", key="tw_call_url")
        if st.button("Make Call", key="tw_call_btn"):
            if to_call and twiml_url:
                try:
                    utility_manager.make_call_twilio(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN,
                                                     TWILIO_PHONE, to_call, twiml_url)
                    st.success("Call initiated!")
                except Exception as e:
                    st.error(str(e))

    # ---------- Tab 5 : Google Search ----------
    with tabs[5]:
        st.subheader("Google Search")
        q = st.text_input("Query", key="g_q")
        if st.button("Search", key="g_btn"):
            if q:
                try:
                    title = utility_manager.search_google(q)
                    st.success(f"Top result: **{title}**")
                    st.markdown(f"[Open Google](https://www.google.com/search?q={q.replace(' ', '+')})")
                except Exception as e:
                    st.error(str(e))

    # ---------- Tab 6 : Instagram ----------
    with tabs[6]:
        st.subheader("Post to Instagram")
        img = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], key="ig_up")
        caption = st.text_area("Caption", key="ig_cap")
        if st.button("Post", key="ig_btn"):
            if img and caption:
                tmp = f"temp_{img.name}"
                with open(tmp, "wb") as f:
                    f.write(img.getbuffer())
                try:
                    utility_manager.post_to_instagram(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, tmp, caption)
                    st.success("Posted!")
                except Exception as e:
                    st.error(str(e))
                finally:
                    if os.path.exists(tmp):
                        os.remove(tmp)
            else:
                st.warning("Need image + caption.")

    # ---------- Tab 7 : Twitter ----------
    with tabs[7]:
        st.subheader("Post Tweet to X")
        tweet = st.text_area("Tweet (≤280 chars)", max_chars=280, key="twt")
        if st.button("Tweet", key="twt_btn"):
            if tweet:
                try:
                    utility_manager.post_to_twitter(TWITTER_API_KEY, TWITTER_API_SECRET,
                                                    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET,
                                                    tweet)
                    st.success("Tweet posted!")
                except Exception as e:
                    st.error(str(e))

    # ---------- Tab 8 : Web Scraper ----------
    with tabs[8]:
        st.subheader("Basic Web Scraper")
        url = st.text_input("URL", placeholder="https://example.com", key="sc_url")
        if st.button("Scrape HTML", key="sc_btn"):
            if url:
                try:
                    html = utility_manager.scrape_website_html(url)
                    st.code(html, language="html")
                except Exception as e:
                    st.error(str(e))

# ------------------ 5-B  Desktop Assistant ------------------
def render_desktop_assistant():
    st.title("🤖 Desktop Assistant")
    st.write("Click a button below, or use voice/text.")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🗣️ Speak")
        if st.button("Start Listening"):
            with st.spinner("Listening…"):
                cmd = pc_task.take_command_from_mic()
            if cmd and cmd.lower() != "none":
                with st.spinner("Executing…"):
                    result = pc_task.execute_command(cmd)
                    st.success(f"**Result:** {result}")

    with col2:
        st.subheader("⌨️ Type")
        typed = st.text_input("Enter command", key="da_type")
        if st.button("Run"):
            if typed:
                with st.spinner("Executing…"):
                    result = pc_task.execute_command(typed)
                    st.success(f"**Result:** {result}")

    st.markdown("---")
    st.header("Interactive Command Menu")
    tasks = defaultdict(list)
    for t in pc_task.TASK_REGISTRY.values():
        tasks[t['cat']].append(t)

    for cat, items in sorted(tasks.items()):
        with st.expander(f"**{cat} Commands**"):
            for it in items:
                if st.button(it['desc'], key=f"da_{it['desc']}"):
                    with st.spinner(f"Running '{it['desc']}'…"):
                        out = it['func']()
                        pc_task.speak(out)
                        st.success(f"**Result:** {out}")

# ------------------ 5-C  File Manager ------------------
def render_file_manager():
    st.title("📂 Advanced File Manager")

    if 'fm_dir' not in st.session_state:
        st.session_state.fm_dir = os.getcwd()

    st.sidebar.header("File Manager")
    d = st.sidebar.text_input("Current path", st.session_state.fm_dir)
    if os.path.isdir(d):
        st.session_state.fm_dir = d
    else:
        st.sidebar.error("Invalid path")
    if st.sidebar.button("↑ Parent"):
        st.session_state.fm_dir = os.path.dirname(st.session_state.fm_dir)
        st.rerun()

    cur = st.session_state.fm_dir
    st.info(f"**Location:** `{cur}`")

    df = file_manager.list_files_as_dataframe(cur)
    if isinstance(df, str):
        st.error(df)
        return

    q = st.text_input("Search files/folders")
    if q:
        df = df[df['Name'].str.contains(q, case=False)]

    st.dataframe(df, use_container_width=True)

    with st.expander("Actions", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Create / Rename / Delete")
            newf = st.text_input("New Folder")
            if newf:
                st.success(file_manager.create_directory(cur, newf))

            old = st.text_input("Rename – current name")
            new = st.text_input("Rename – new name")
            if old and new:
                st.success(file_manager.rename_item(cur, old, new))

            del_name = st.text_input("Delete name")
            if del_name:
                st.info(file_manager.delete_item(cur, del_name))

        with col2:
            st.subheader("Upload / Download / Preview")
            up = st.file_uploader("Upload file")
            if up:
                with open(os.path.join(cur, up.name), "wb") as f:
                    f.write(up.getbuffer())
                st.success("Uploaded!")

            files = df[df['Type'] == '📄 File']['Name'].tolist()
            if files:
                dl = st.selectbox("Download file", files)
                try:
                    with open(os.path.join(cur, dl), "rb") as f:
                        st.download_button("Download", data=f, file_name=dl)
                except Exception as e:
                    st.error(str(e))

                pv = st.selectbox("Preview file", [""] + files)
                if pv:
                    path = os.path.join(cur, pv)
                    if path.lower().endswith(('.png', '.jpg', '.jpeg')):
                        st.image(path)
                    else:
                        st.code(file_manager.get_file_content_for_preview(path))

# ------------------ 5-D  SSH Assistant ------------------
def render_ssh_assistant():
    if not SSH_SECRETS_OK:
        st.error("Missing `my_secrets.py` credentials for SSH Assistant. Cannot proceed.")
        return

    st.title("🧠 AI-Powered SSH Assistant")
    st.info(f"Target Server: **{SSH_USER}@{SSH_IP}**.  All commands require confirmation.")
    st.markdown("---")

    tab1, tab2 = st.tabs(["🤖 AI Assistant", "📋 Command Menu"])

    with tab1:
        st.subheader("Describe Your Task")
        prompt = st.text_area("Describe what you want to do:", key="ssh_prompt")
        if st.button("Generate Command", key="ssh_generate"):
            if prompt:
                with st.spinner("Generating…"):
                    st.session_state.cmd = ssh_gemini_manager.get_linux_command_from_gemini(gemini_model, prompt)
            else:
                st.warning("Please enter a task description.")

    with tab2:
        st.subheader("Select a Pre-defined Command")
        for category, commands in COMMAND_MENU.items():
            with st.expander(f"**{category}**"):
                for desc, cmd in commands.items():
                    if st.button(desc, key=cmd, use_container_width=True):
                        st.session_state.cmd = cmd

    if st.session_state.get("cmd"):
        st.markdown("---")
        st.header("Confirm Command Execution")
        st.warning("⚠️  Review carefully before executing!")
        st.code(st.session_state.cmd, language="bash")
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("✅ Yes, Execute", type="primary", use_container_width=True):
                command = st.session_state.cmd
                with st.spinner(f"Running `{command}`…"):
                    output = ssh_gemini_manager.execute_remote_command(SSH_IP, 22, SSH_USER, SSH_PASS, command)
                    st.session_state.output = output
                    st.session_state.last_command = command
                    st.session_state.cmd = None
                st.rerun()
        with col2:
            if st.button("❌ No, Cancel", use_container_width=True):
                st.session_state.cmd = None
                st.rerun()

    if st.session_state.get("output"):
        st.markdown("---")
        st.header(f"Output for: `{st.session_state.last_command}`")
        st.code(st.session_state.output, language="bash")
        st.session_state.output = None

# ------------------ 5-E  Live AI Camera ------------------
def render_camera():
    st.title("📸 Live AI Camera")
    st.markdown("---")

    # Session-state for lifecycle
    if "camera_active" not in st.session_state:
        st.session_state.camera_active = False
    if "is_recording" not in st.session_state:
        st.session_state.is_recording = False
    if "recorded_frames" not in st.session_state:
        st.session_state.recorded_frames = []
    if "captured_photo" not in st.session_state:
        st.session_state.captured_photo = None
    if "video_path" not in st.session_state:
        st.session_state.video_path = None
    if "cap" not in st.session_state:
        st.session_state.cap = None

    processor = cv_manager.MediaPipeProcessor()

    with st.sidebar:
        st.header("Camera Controls")

        def start_camera_cb():
            if st.session_state.cap is None or not st.session_state.cap.isOpened():
                st.session_state.cap = cv2.VideoCapture(0)
            st.session_state.camera_active = True

        def stop_camera_cb():
            st.session_state.camera_active = False
            st.session_state.is_recording = False

        def toggle_recording_cb():
            st.session_state.is_recording = not st.session_state.is_recording

        def capture_photo_cb():
            st.session_state.capture_flag = True

        st.button("Start Camera", on_click=start_camera_cb, use_container_width=True)
        st.button("Stop Camera", on_click=stop_camera_cb, use_container_width=True)
        st.button("📸 Capture", on_click=capture_photo_cb, use_container_width=True,
                  disabled=not st.session_state.camera_active)
        if st.session_state.is_recording:
            st.button("🛑 Stop Recording", on_click=toggle_recording_cb, use_container_width=True)
        else:
            st.button("⏺️ Start Recording", on_click=toggle_recording_cb, use_container_width=True,
                      disabled=not st.session_state.camera_active)

        st.markdown("---")
        st.header("Captured Media")
        if st.session_state.captured_photo is not None:
            st.image(st.session_state.captured_photo, channels="BGR", use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Photo", use_container_width=True):
                    res = processor.save_photo(st.session_state.captured_photo)
                    st.success(res)
                    st.session_state.captured_photo = None
            with col2:
                if st.button("Discard", use_container_width=True):
                    st.session_state.captured_photo = None

        if st.session_state.video_path:
            st.write("Video ready:")
            with open(st.session_state.video_path, "rb") as f:
                st.download_button(label="Download Video", data=f,
                                   file_name=os.path.basename(st.session_state.video_path),
                                   mime="video/mp4")
            if st.button("Clear Link", use_container_width=True):
                st.session_state.video_path = None

    frame_placeholder = st.empty()
    info_placeholder = st.empty()

    if st.session_state.camera_active:
        cap = st.session_state.cap
        if cap is None or not cap.isOpened():
            st.error("Cannot access camera")
            st.session_state.camera_active = False
            st.rerun()
        else:
            while st.session_state.camera_active:
                ret, frame = cap.read()
                if not ret:
                    st.warning("Failed to grab frame")
                    stop_camera_cb()
                    st.rerun()
                    break
                frame = cv2.flip(frame, 1)
                processed = processor.process_frame(frame)
                frame_placeholder.image(processed, channels="BGR", use_container_width=True)

                if st.session_state.get("capture_flag", False):
                    st.session_state.captured_photo = frame.copy()
                    st.session_state.capture_flag = False

                if st.session_state.is_recording:
                    info_placeholder.info("🔴 Recording…")
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    st.session_state.recorded_frames.append(rgb)
                else:
                    info_placeholder.empty()

            # When loop exits
            if st.session_state.cap is not None and st.session_state.cap.isOpened():
                st.session_state.cap.release()
                st.session_state.cap = None
                cv2.destroyAllWindows()

            if st.session_state.recorded_frames:
                res_path = processor.save_video(st.session_state.recorded_frames)
                st.session_state.video_path = res_path.split(": ")[-1]
                st.session_state.recorded_frames = []
                st.rerun()
    else:
        if st.session_state.cap is not None and st.session_state.cap.isOpened():
            st.session_state.cap.release()
            st.session_state.cap = None
            cv2.destroyAllWindows()
        st.info("Click **Start Camera** in the sidebar to begin.")

# ------------------ 5-F  Saundarya Lite ------------------
def render_saundarya_lite():
    # Apply custom CSS styling for Saundarya Lite
    st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    .stButton > button {
        background: linear-gradient(45deg, #FF6B9D, #C44CAE);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
        font-weight: bold;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(196, 76, 174, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.sidebar.title("🌸 Saundarya Lite")
    st.sidebar.markdown("*Your Personal Fashion Assistant*")
    
    menu_options = [
        "📸 Analyse Outfit",
        "🗂️ My Closet", 
        "📈 Trend Dashboard",
        "💡 Daily Style Tip",
        "⚙️ Settings"
    ]
    selected_menu = st.sidebar.radio("Navigate", menu_options)
    
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        st.sidebar.warning("⚠️ Demo Mode (Set API key for full features)")
    else:
        st.sidebar.success("✅ Gemini API Connected")
    
    # ------------------------------------------------------------------
    # UI: ANALYSE OUTFIT TAB
    # ------------------------------------------------------------------
    if selected_menu == "📸 Analyse Outfit":
        st.title("📸 Outfit Analysis")
        st.markdown("Upload your outfit photo and get AI-powered fashion insights!")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Upload Details")
            occasion = st.selectbox(
                "Select Occasion",
                ["Casual", "Work/Professional", "Party/Event", "Date Night", "Travel", "Workout", "Formal"]
            )
            uploaded_file = st.file_uploader(
                "Upload Outfit Photo",
                type=["jpg", "jpeg", "png"]
            )
            with st.expander("Advanced Options"):
                focus_areas = st.multiselect(
                    "Focus Analysis On:",
                    ["Color Coordination", "Style Matching", "Occasion Appropriateness", "Accessories", "Fit Assessment"],
                    default=["Color Coordination", "Style Matching"]
                )
        
        with col2:
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.subheader("Your Outfit")
                st.image(image, caption="Uploaded Image", use_container_width=True)
                
                # The button is placed here but the results will show below the columns
                analyze_button = st.button("✨ Analyse My Outfit", type="primary", use_container_width=True)
            else:
                analyze_button = False
    
        # FIXED: Results are displayed below the columns to prevent layout issues
        if uploaded_file is not None and analyze_button:
            st.markdown("---")
            st.header("AI Analysis Results")
            with st.spinner("🤖 AI is analyzing your outfit..."):
                focus_text = ", ".join(focus_areas) if focus_areas else "overall style"
                
                prompt = f"""
                You are an expert fashion stylist. Analyze this outfit image for a '{occasion}' occasion.
                Focus particularly on: {focus_text}
                
                Please provide your analysis in the following structured format:
                
                **Gender**: [Detected gender presentation]
                **Mood**: [What mood/energy does this outfit convey?]
                **Skin Tone**: [Observed skin tone - e.g., Warm, Cool, Neutral, Medium]
                **Upper Wear Color**: [Primary color of top/shirt/jacket]
                **Lower Wear Color**: [Primary color of bottom wear]
                **Outfit Style**: [e.g., Minimalist, Bohemian, Chic, Sporty]
                **Fit Assessment**: [e.g., Well-fitted, Oversized, Tailored, A bit loose]
                **Pattern**: [e.g., Solid, Striped, Floral, Plaid]
                **Fabric Suggestion**: [Suggest suitable fabrics like Cotton, Silk, Denim]
                **Overall Vibe**: [Describe the overall aesthetic and style in a few words]
                **Accessory Recommendations**:
                • [Specific accessory recommendation 1]
                • [Specific accessory recommendation 2]
                **Fashion Tips**: 
                • [Specific, actionable styling tip 1]
                • [Specific, actionable styling tip 2]
                **Confidence Score**: [Rate from 1-10 how confident this outfit looks]
                """
                
                ai_response = saundarya_manager.call_gemini(GEMINI_API_KEY, prompt, image)
                analysis_features = saundarya_manager.parse_gemini_response(ai_response)
                
                st.success("✅ Analysis Complete!")
                with st.expander("📝 Detailed Analysis", expanded=True):
                    st.markdown(ai_response)
                
                st.subheader("Key Metrics")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Confidence Score", analysis_features.get("Confidence Score", "N/A"))
                with col_b:
                    st.metric("Overall Vibe", analysis_features.get("Overall Vibe", "N/A"))
                with col_c:
                    st.metric("Outfit Style", analysis_features.get("Outfit Style", "N/A"))
                
                saved_image_path = saundarya_manager.save_image(image)
                if saved_image_path and saundarya_manager.save_analysis_result(analysis_features, saved_image_path, occasion):
                    st.success("💾 Analysis saved to your closet!")
                else:
                    st.warning("⚠️ Could not save analysis")
    
    # ------------------------------------------------------------------
    # UI: MY CLOSET TAB
    # ------------------------------------------------------------------
    elif selected_menu == "🗂️ My Closet":
        st.title("🗂️ My Virtual Closet")
        st.markdown("Browse your fashion history and past analyses")
        
        df = saundarya_manager.load_fashion_history()
        
        if df.empty:
            st.info("👗 Your closet is empty! Upload your first outfit in the 'Analyse Outfit' section.")
        else:
            # Filtering and Sorting
            filtered_df = df.copy()
            # ... (rest of the filtering/sorting logic remains the same) ...
            
            # Display items
            for idx, row in filtered_df.iterrows():
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if os.path.exists(row['image_path']):
                            st.image(row['image_path'], width=150, caption=f"{row['occasion']}")
                        else:
                            st.write("🖼️ Image not found")
                    
                    with col2:
                        st.markdown(f"**{row['occasion']}** • {row['timestamp'].strftime('%Y-%m-%d %H:%M') if pd.notna(row['timestamp']) else 'N/A'}")
                        with st.expander("View Full Analysis"):
                            # UPDATED to show all new details
                            st.write(f"**Overall Vibe:** {row.get('Overall Vibe', 'N/A')}")
                            st.write(f"**Outfit Style:** {row.get('Outfit Style', 'N/A')}")
                            st.write(f"**Confidence Score:** {row.get('Confidence Score', 'N/A')}")
                            st.markdown("**Colors:**")
                            st.write(f"&nbsp;&nbsp;&nbsp;**Upper Wear:** {row.get('Upper Wear Color', 'N/A')}")
                            st.write(f"&nbsp;&nbsp;&nbsp;**Lower Wear:** {row.get('Lower Wear Color', 'N/A')}")
                            st.markdown("**Details:**")
                            st.write(f"&nbsp;&nbsp;&nbsp;**Fit:** {row.get('Fit Assessment', 'N/A')}")
                            st.write(f"&nbsp;&nbsp;&nbsp;**Pattern:** {row.get('Pattern', 'N/A')}")
                            st.markdown("**Recommendations:**")
                            st.markdown(f"**Accessory Recs:**\n{row.get('Accessory Recommendations', 'N/A')}")
                            st.markdown(f"**Fashion Tips:**\n{row.get('Fashion Tips', 'N/A')}")
    
                    st.divider()
    
    # ------------------------------------------------------------------
    # UI: TREND DASHBOARD TAB
    # ------------------------------------------------------------------
    elif selected_menu == "📈 Trend Dashboard":
        st.title("📈 Fashion Trend Dashboard")
        st.markdown("Discover your style patterns and fashion insights")
        
        df = saundarya_manager.load_fashion_history()
        
        if df.empty:
            st.info("📊 No data available yet. Start by analyzing some outfits!")
        else:
            # ... (Metrics calculation remains the same) ...
            avg_confidence = pd.to_numeric(df['Confidence Score'].astype(str).str.extract(r'(\d+)').iloc[:, 0], errors='coerce').mean()
            
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Total Outfits", len(df))
            with col2: st.metric("Avg Confidence", f"{avg_confidence:.1f}/10" if pd.notna(avg_confidence) else "N/A")
            with col3: st.metric("Top Occasion", df['occasion'].mode().iloc[0] if not df['occasion'].mode().empty else "N/A")
            
            st.divider()
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.subheader("📅 Occasion Distribution")
                occasion_counts = df['occasion'].value_counts()
                fig = px.pie(values=occasion_counts.values, names=occasion_counts.index, title="Outfits by Occasion")
                st.plotly_chart(fig, use_container_width=True)
                
                # NEW CHART: Outfit Style
                st.subheader("✨ Your Dominant Styles")
                if 'Outfit Style' in df.columns:
                    style_counts = df['Outfit Style'].value_counts()
                    fig_style = px.bar(x=style_counts.index, y=style_counts.values, labels={'x': 'Style', 'y': 'Count'})
                    st.plotly_chart(fig_style, use_container_width=True)
    
            with chart_col2:
                st.subheader("🎨 Color Preferences")
                upper_colors = df['Upper Wear Color'].value_counts().head(8)
                fig = px.bar(x=upper_colors.values, y=upper_colors.index, orientation='h', title="Most Worn Upper Wear Colors")
                st.plotly_chart(fig, use_container_width=True)
    
    # ------------------------------------------------------------------
    # UI: DAILY STYLE TIP TAB
    # ------------------------------------------------------------------
    elif selected_menu == "💡 Daily Style Tip":
        st.title("💡 Daily Style Tip")
        st.markdown("Get a fresh, AI-powered fashion tip to inspire your day!")
        
        if st.button("✨ Get My Daily Tip", type="primary", use_container_width=True):
            with st.spinner("Getting your personalized tip..."):
                # A dummy image is needed for the API call structure, but content doesn't matter
                dummy_image = Image.new('RGB', (100, 100), color='white')
                tip_prompt = "Give me one fresh, actionable fashion tip for today. Make it specific, practical, and inspiring. Keep it to 1-2 sentences maximum."
                
                daily_tip = saundarya_manager.call_gemini(GEMINI_API_KEY, tip_prompt, dummy_image)
                clean_tip = daily_tip.replace("**", "").strip()
                
                st.success(f"💎 {clean_tip}")
                st.balloons()
    
    # ------------------------------------------------------------------
    # UI: SETTINGS TAB
    # ------------------------------------------------------------------
    elif selected_menu == "⚙️ Settings":
        st.title("⚙️ Settings & Information")
    
        # Initialize session state for confirmation
        if 'confirm_delete' not in st.session_state:
            st.session_state.confirm_delete = False
    
        st.subheader("API Configuration")
        status = "Set" if GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE" else "Not Set"
        st.write(f"**Gemini API Key Status:** {status}")
        if status == "Not Set":
            st.warning("Running in demo mode. Set your Gemini API key for full functionality.")
            st.markdown("1. Get a key from [Google AI Studio](https://makersuite.google.com/)\n2. Set it as an environment variable `GEMINI_API_KEY` or replace the placeholder in the code.")
    
        st.markdown("---")
        st.subheader("Data Management")
        df = saundarya_manager.load_fashion_history()
        st.write(f"**Total Outfits Logged:** {len(df)}")
        st.write(f"**Storage Location:** `{saundarya_manager.CSV_FILE}`")
        st.write(f"**Images Directory:** `{saundarya_manager.UPLOAD_DIR}`")
        
        if st.button("🗑️ Clear All Data", type="secondary"):
            st.session_state.confirm_delete = True
        
        # Confirmation workflow for deleting data
        if st.session_state.confirm_delete:
            st.warning("**This will permanently delete all your fashion data, including the CSV log and all uploaded images. This action cannot be undone.**")
            if st.button("Yes, I'm sure. Delete Everything.", type="primary"):
                try:
                    if os.path.exists(saundarya_manager.CSV_FILE):
                        os.remove(saundarya_manager.CSV_FILE)
                    
                    # Clear images directory
                    for img_file in saundarya_manager.UPLOAD_DIR.glob("*.jpg"):
                        img_file.unlink()
                    
                    st.success("✅ All data cleared successfully!")
                    st.session_state.confirm_delete = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error clearing data: {e}")

# ------------------ 5-G  Motivation Buddy ------------------
def render_motivation_buddy():
    # Custom CSS for Motivation Buddy
    st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .st-emotion-cache-1y4p8pa { /* Main content area */
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 2rem;
        }
        h1, h3 {
            color: white !important;
        }
        .st-emotion-cache-16txtl3 { /* Sidebar */
            background-color: rgba(0, 0, 0, 0.2);
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize Session State
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar for Personalization and Actions
    with st.sidebar:
        st.title("🎯 Personalization")
        
        user_name = st.text_input("👤 Your Name", placeholder="Enter name for personalized streaks!")
        mood = st.radio(
            "🎭 How are you feeling?",
            ["Happy", "Sad", "Stressed", "Motivated", "Neutral", "Anxious", "Tired"],
            index=4 # Default to Neutral
        )

        st.markdown("---")
        st.title("🏆 Quick Actions")
        if st.button("🌟 Quick Motivation", use_container_width=True):
            st.session_state.quick_action = "Give me some motivation to get through today!"
        if st.button("⚡ Productivity Tip", use_container_width=True):
            st.session_state.quick_action = "Share a practical productivity tip I can use right now!"
        if st.button("🎯 Goal Setting Help", use_container_width=True):
            st.session_state.quick_action = "Help me set and achieve my goals effectively!"
        
        st.markdown("---")
        st.title("📊 My Stats")
        stats_placeholder = st.empty()
        stats_placeholder.markdown(motivation_manager.get_user_stats(user_name))

    # Main Chat Interface
    st.title("🚀 Ultimate Productivity & Motivation Buddy")
    st.write("Your personal coach for productivity, motivation, and a positive mindset!")

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Process quick action if triggered
    if st.session_state.get("quick_action"):
        prompt = st.session_state.quick_action
        st.session_state.quick_action = None # Reset after use
        
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = motivation_manager.get_ai_response(GEMINI_API_KEY, prompt, mood, user_name)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    # Accept user input
    if prompt := st.chat_input("Share your thoughts or ask for help..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = motivation_manager.get_ai_response(GEMINI_API_KEY, prompt, mood, user_name)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Update stats in the sidebar after an interaction
        stats_placeholder.markdown(motivation_manager.get_user_stats(user_name))

###############################################################################
# 5.  Render functions for new programs
###############################################################################

def render_home():
    # Create a visually appealing header
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; background-color: #f0f2f6; padding: 30px; border-radius: 10px;'>
            <h1 style='color: #0066cc;'>🏠 Welcome to Unified AI Hub</h1>
            <h3>Your All-in-One AI Toolkit</h3>
            <p>Explore our comprehensive suite of AI-powered tools designed to enhance productivity, creativity, and decision-making.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Introduction section
    st.markdown("""    
    ## 🌟 About Unified AI Hub
    
    Unified AI Hub brings together multiple AI-powered tools in one convenient interface. Whether you need to automate communications, 
    manage files, control your desktop, analyze images, get fashion advice, or build machine learning models, we've got you covered.
    
    Simply select a tool from the sidebar or click one of the buttons below to get started!
    """)
    
    # Create a container with a light background
    with st.container():
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
            <h2 style='text-align: center;'>🛠️ Available Tools</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for categorized tools
        tabs = st.tabs(["All Tools", "Automation & Productivity", "AI Assistants", "Machine Learning"])
        
        with tabs[0]:
            st.markdown("### All Tools in One Place")
            st.markdown("Browse all available tools in the Unified AI Hub.")
            st.markdown("---")
        
        # Function to create a tool card with description and button
        def tool_card(title, emoji, description, key):
            st.markdown(f"""
            <div style='background-color: #ffffff; padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #e6e6e6;'>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {emoji} {title}")
                st.markdown(f"<div style='color: #666666;'>{description}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
                button_style = """<style>
                div[data-testid="stButton"] button {
                    background-color: #0066cc;
                    color: white;
                    border-radius: 5px;
                    padding: 10px 15px;
                    font-weight: bold;
                }
                div[data-testid="stButton"] button:hover {
                    background-color: #004d99;
                    border-color: #004d99;
                }
                </style>"""
                st.markdown(button_style, unsafe_allow_html=True)
                if st.button(f"Open {title}", key=key, use_container_width=True):
                    # Set the session state to navigate to this tool
                    st.session_state.navigate_to = title
                    st.rerun()
        
        # Tab 1: All Tools
        with tabs[0]:
            # AI Automation Hub
            tool_card(
                "AI Automation Hub", 
                "🤖", 
                "Your central dashboard for communication, social-media & web-automation tasks. Features include WhatsApp messaging, email sending, SMS, calls, Google search, Instagram posting, Twitter/X posting, and web scraping.",
                "btn_hub_all"
            )
            
            # Desktop Assistant
            tool_card(
                "Desktop Assistant", 
                "💻", 
                "Control your computer with voice commands or hotkeys. Perform tasks like taking screenshots, recording screen activity, and executing system commands hands-free.",
                "btn_desktop_all"
            )
            
            # File Manager
            tool_card(
                "File Manager", 
                "📁", 
                "Advanced file management system with AI capabilities. Organize, search, and manipulate files with intelligent features and automation.",
                "btn_file_all"
            )
            
            # SSH Assistant
            tool_card(
                "SSH Assistant", 
                "🔐", 
                "AI-powered SSH terminal that helps you manage remote servers. Execute commands, get explanations, and troubleshoot issues with intelligent assistance.",
                "btn_ssh_all"
            )
            
            # Live AI Camera
            tool_card(
                "Live AI Camera", 
                "📷", 
                "Real-time computer vision with AI analysis. Capture photos and videos with intelligent object detection, face recognition, and scene analysis.",
                "btn_camera_all"
            )
            
            # Saundarya Lite
            tool_card(
                "Saundarya Lite", 
                "👗", 
                "AI fashion assistant that provides style recommendations and outfit analysis. Upload your fashion items and get personalized advice.",
                "btn_saundarya_all"
            )
            
            # Motivation Buddy
            tool_card(
                "Motivation Buddy", 
                "🚀", 
                "Your personal coach for productivity, motivation, and positive mindset. Get customized motivation, track your progress, and maintain a positive outlook.",
                "btn_motivation_all"
            )
            
            # AI Vehicle Recommender Hub
            tool_card(
                "AI Vehicle Recommender Hub", 
                "🚗", 
                "Get personalized vehicle recommendations based on your preferences. Find the perfect 2-wheeler or 4-wheeler that matches your needs and budget.",
                "btn_vehicle_all"
            )
            
            # Study Hours vs Marks Predictor
            tool_card(
                "Study Hours vs Marks Predictor", 
                "📊", 
                "Predict academic performance based on study hours using machine learning. Upload your data or use the default dataset to visualize the relationship between study time and marks.",
                "btn_marks_all"
            )
            
            # Interactive Classification Lab
            tool_card(
                "Interactive Classification Lab", 
                "🧪", 
                "Build and evaluate machine learning classification models interactively. Upload your dataset, preprocess data, train models, and make predictions with a user-friendly interface.",
                "btn_ml_all"
            )
        
        # Tab 2: Automation & Productivity
        with tabs[1]:
            st.markdown("### Automation & Productivity Tools")
            st.markdown("Tools to automate tasks and boost your productivity.")
            st.markdown("---")
            
            # AI Automation Hub
            tool_card(
                "AI Automation Hub", 
                "🤖", 
                "Your central dashboard for communication, social-media & web-automation tasks. Features include WhatsApp messaging, email sending, SMS, calls, Google search, Instagram posting, Twitter/X posting, and web scraping.",
                "btn_hub"
            )
            
            # Desktop Assistant
            tool_card(
                "Desktop Assistant", 
                "💻", 
                "Control your computer with voice commands or hotkeys. Perform tasks like taking screenshots, recording screen activity, and executing system commands hands-free.",
                "btn_desktop"
            )
            
            # File Manager
            tool_card(
                "File Manager", 
                "📁", 
                "Advanced file management system with AI capabilities. Organize, search, and manipulate files with intelligent features and automation.",
                "btn_file"
            )
            
            # SSH Assistant
            tool_card(
                "SSH Assistant", 
                "🔐", 
                "AI-powered SSH terminal that helps you manage remote servers. Execute commands, get explanations, and troubleshoot issues with intelligent assistance.",
                "btn_ssh"
            )
        
        # Tab 3: AI Assistants
        with tabs[2]:
            st.markdown("### AI Assistant Tools")
            st.markdown("Intelligent assistants to help with specific tasks.")
            st.markdown("---")
            
            # Live AI Camera
            tool_card(
                "Live AI Camera", 
                "📷", 
                "Real-time computer vision with AI analysis. Capture photos and videos with intelligent object detection, face recognition, and scene analysis.",
                "btn_camera"
            )
            
            # Saundarya Lite
            tool_card(
                "Saundarya Lite", 
                "👗", 
                "AI fashion assistant that provides style recommendations and outfit analysis. Upload your fashion items and get personalized advice.",
                "btn_saundarya"
            )
            
            # Motivation Buddy
            tool_card(
                "Motivation Buddy", 
                "🚀", 
                "Your personal coach for productivity, motivation, and positive mindset. Get customized motivation, track your progress, and maintain a positive outlook.",
                "btn_motivation"
            )
            
            # AI Vehicle Recommender Hub
            tool_card(
                "AI Vehicle Recommender Hub", 
                "🚗", 
                "Get personalized vehicle recommendations based on your preferences. Find the perfect 2-wheeler or 4-wheeler that matches your needs and budget.",
                "btn_vehicle"
            )
        
        # Tab 4: Machine Learning
        with tabs[3]:
            st.markdown("### Machine Learning Tools")
            st.markdown("Tools for data analysis and machine learning.")
            st.markdown("---")
            
            # Study Hours vs Marks Predictor
            tool_card(
                "Study Hours vs Marks Predictor", 
                "📊", 
                "Predict academic performance based on study hours using machine learning. Upload your data or use the default dataset to visualize the relationship between study time and marks.",
                "btn_marks"
            )
            
            # Interactive Classification Lab
            tool_card(
                "Interactive Classification Lab", 
                "🧪", 
                "Build and evaluate machine learning classification models interactively. Upload your dataset, preprocess data, train models, and make predictions with a user-friendly interface.",
                "btn_ml"
            )

def render_vehicle_recommender():
    st.title("🚗 AI Vehicle Recommender Hub")
    st.write("Get personalized vehicle recommendations based on your preferences.")
    
    # Create tabs for different recommendation types
    tabs = st.tabs(["2-Wheeler", "4-Wheeler", "Ask Anything"])
    
    # --- Tab 1: 2-Wheeler Recommendations ---
    with tabs[0]:
        st.header("🏍️ 2-Wheeler Recommendations")
        st.write("Tell us your preferences, and we'll suggest the best 2-wheelers for you.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fuel_2w = st.selectbox(
                "Fuel Type",
                ["Petrol", "Electric", "Any"],
                key="fuel_2w"
            )
            
            budget_2w = st.slider(
                "Budget (₹)",
                50000, 500000, 100000, 10000,
                key="budget_2w"
            )
            
            brand_2w = st.selectbox(
                "Preferred Brand",
                ["Any", "Hero", "Honda", "Bajaj", "TVS", "Royal Enfield", "Yamaha", "Suzuki", "KTM", "Jawa", "Ola Electric", "Ather"],
                key="brand_2w"
            )
        
        with col2:
            usage_2w = st.selectbox(
                "Primary Usage",
                ["Daily Commute", "Long Rides", "Off-Road", "City Riding", "Any"],
                key="usage_2w"
            )
            
            look_2w = st.selectbox(
                "Style Preference",
                ["Any", "Sporty", "Classic", "Modern", "Retro", "Cruiser", "Adventure"],
                key="look_2w"
            )
            
            extra_2w = st.text_area(
                "Any other requirements?",
                key="extra_2w",
                height=100
            )
        
        if st.button("Get 2-Wheeler Recommendations", key="btn_2w"):
            with st.spinner("AI is finding the perfect 2-wheelers for you..."):
                recommendations = vehicle_manager.recommend_2wheeler(
                    GEMINI_API_KEY, fuel_2w, budget_2w, brand_2w, usage_2w, look_2w, extra_2w
                )
                
                if isinstance(recommendations, str):
                    st.error(recommendations)
                else:
                    st.success(f"Found {len(recommendations)} recommendations for you!")
                    
                    for i, rec in enumerate(recommendations):
                        with st.expander(f"**{rec['data']['brand']} {rec['data']['model_name']}**", expanded=True):
                            col_img, col_details = st.columns([1, 2])
                            
                            with col_img:
                                st.image(rec['image_url'], width=250)
                            
                            with col_details:
                                st.write(f"**Price:** ₹{rec['data']['price_inr']}")
                                st.write(f"**Fuel Type:** {rec['data']['fuel_type']}")
                                st.write(f"**Why this vehicle:** {rec['data']['reason']}")
    
    # --- Tab 2: 4-Wheeler Recommendations ---
    with tabs[1]:
        st.header("🚙 4-Wheeler Recommendations")
        st.write("Tell us your preferences, and we'll suggest the best cars for you.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fuel_4w = st.selectbox(
                "Fuel Type",
                ["Petrol", "Diesel", "Electric", "Hybrid", "CNG", "Any"],
                key="fuel_4w"
            )
            
            budget_4w = st.slider(
                "Budget (₹)",
                300000, 5000000, 1000000, 100000,
                key="budget_4w"
            )
            
            brand_4w = st.selectbox(
                "Preferred Brand",
                ["Any", "Maruti Suzuki", "Hyundai", "Tata", "Mahindra", "Toyota", "Honda", "Kia", "MG", "Volkswagen", "Skoda", "Ford", "Renault", "Nissan"],
                key="brand_4w"
            )
            
            seating_4w = st.selectbox(
                "Seating Capacity",
                ["Any", "2", "4", "5", "6", "7+"],
                key="seating_4w"
            )
        
        with col2:
            usage_4w = st.selectbox(
                "Primary Usage",
                ["City Driving", "Highway Cruising", "Off-Road", "Family Use", "Any"],
                key="usage_4w"
            )
            
            transmission_4w = st.selectbox(
                "Transmission Type",
                ["Any", "Manual", "Automatic", "AMT", "CVT", "DCT"],
                key="transmission_4w"
            )
            
            look_4w = st.selectbox(
                "Vehicle Type",
                ["Any", "Hatchback", "Sedan", "SUV", "MUV/MPV", "Luxury", "Sports"],
                key="look_4w"
            )
            
            extra_4w = st.text_area(
                "Any other requirements?",
                key="extra_4w",
                height=100
            )
        
        if st.button("Get 4-Wheeler Recommendations", key="btn_4w"):
            with st.spinner("AI is finding the perfect cars for you..."):
                recommendations = vehicle_manager.recommend_4wheeler(
                    GEMINI_API_KEY, fuel_4w, budget_4w, brand_4w, seating_4w, usage_4w, transmission_4w, look_4w, extra_4w
                )
                
                if isinstance(recommendations, str):
                    st.error(recommendations)
                else:
                    st.success(f"Found {len(recommendations)} recommendations for you!")
                    
                    for i, rec in enumerate(recommendations):
                        with st.expander(f"**{rec['data']['brand']} {rec['data']['model_name']}**", expanded=True):
                            col_img, col_details = st.columns([1, 2])
                            
                            with col_img:
                                st.image(rec['image_url'], width=250)
                            
                            with col_details:
                                st.write(f"**Price:** ₹{rec['data']['price_inr']}")
                                st.write(f"**Fuel Type:** {rec['data']['fuel_type']}")
                                st.write(f"**Transmission:** {rec['data']['transmission']}")
                                st.write(f"**Seating Capacity:** {rec['data']['seating']}")
                                st.write(f"**Why this vehicle:** {rec['data']['reason']}")
    
    # --- Tab 3: Ask Anything ---
    with tabs[2]:
        st.header("❓ Ask Anything About Vehicles")
        st.write("Have a specific question about vehicles? Ask our AI assistant!")
        
        custom_prompt = st.text_area(
            "Your Question",
            placeholder="E.g., What are the best SUVs under 15 lakhs in India? Or, Compare Honda City vs Hyundai Verna.",
            height=100,
            key="custom_prompt"
        )
        
        if st.button("Get Answer", key="btn_custom"):
            if not custom_prompt:
                st.warning("Please enter a question first.")
            else:
                with st.spinner("AI is thinking..."):
                    response = vehicle_manager.ask_anything(GEMINI_API_KEY, custom_prompt)
                    
                    if isinstance(response, str):
                        st.info(response)
                    else:
                        st.success(f"Found {len(response)} recommendations for you!")
                        
                        for i, rec in enumerate(response):
                            with st.expander(f"**{rec['data']['brand']} {rec['data']['model_name']}**", expanded=True):
                                col_img, col_details = st.columns([1, 2])
                                
                                with col_img:
                                    st.image(rec['image_url'], width=250)
                                
                                with col_details:
                                    st.write(f"**Price:** ₹{rec['data']['price_inr']}")
                                    st.write(f"**Fuel Type:** {rec['data']['fuel_type']}")
                                    if rec['data']['transmission'] != "N/A":
                                        st.write(f"**Transmission:** {rec['data']['transmission']}")
                                    if rec['data']['seating'] != "N/A":
                                        st.write(f"**Seating Capacity:** {rec['data']['seating']}")
                                    st.write(f"**Why this vehicle:** {rec['data']['reason']}")

def render_marks_predictor():
    # The code for Study Hours vs Marks Predictor is already in app.py
    # This section uses regression_manager for predictions
    
    # --- Main App UI ---
    st.title("📚 Study Hours vs Marks Predictor")
    st.write("An interactive web app to visualize and predict student marks based on study hours using Linear Regression.")
    
    # --- Sidebar for Data Input ---
    st.sidebar.header("Data Configuration")
    uploaded_file = st.sidebar.file_uploader("Upload your own CSV file", type=["csv"])
    
    # Load data based on user choice
    if uploaded_file is not None:
        data = regression_manager.load_and_clean_data(uploaded_file)
        if isinstance(data, str): # Check if the load function returned an error message
            st.error(data)
            st.stop()
        st.sidebar.success("CSV file uploaded and processed successfully!")
    else:
        data = regression_manager.get_default_data()
        st.sidebar.info("Using the default sample dataset. Upload a CSV to use your own data.")
    
    # --- Main Panel for Displaying Results ---
    
    # Train the model with the selected data
    model, X, y = regression_manager.train_regression_model(data)
    
    if model is None:
        st.warning("The dataset is empty or invalid. Please upload a valid CSV file.")
    else:
        # Display the dataset
        st.subheader("📊 Dataset Used for Training")
        st.dataframe(data)
    
        st.markdown("---")
        
        # Display Model Performance
        st.subheader("⚙️ Model Performance")
        r2, equation = regression_manager.get_model_performance(model, X, y)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="R-squared Score", value=f"{r2:.2f}")
            st.info(
                "**R-squared** (from 0 to 1) shows how well the model explains the data. "
                "A score of 0.90 means 90% of the variation in marks can be explained by study hours."
            )
        with col2:
            st.write("**Regression Equation:**")
            st.latex(equation.replace(" ", "\ ").replace("×", "\\times"))
            st.info(
                "This is the mathematical formula the model uses to make predictions."
            )
    
        st.markdown("---")
    
        # --- Prediction and Visualization Section ---
        st.subheader("🔮 Make a Prediction")
        
        col3, col4 = st.columns([1, 2])
        
        with col3:
            # User input for prediction
            user_hours = st.number_input("Enter Study Hours to Predict Marks:", min_value=0.0, max_value=24.0, value=5.0, step=0.5)
            
            # Get prediction
            predicted_marks = regression_manager.predict_marks(model, user_hours)
            
            st.success(f"Predicted Marks: **{predicted_marks:.2f}**")
        
        with col4:
            # Plotting
            st.write("**Visual Representation:**")
            fig, ax = plt.subplots()
            ax.scatter(X, y, color='blue', label='Actual Data')
            ax.plot(X, model.predict(X), color='red', linewidth=2, label='Regression Line')
            ax.scatter([user_hours], [predicted_marks], color='green', s=150, zorder=5, label='Your Prediction')
            
            ax.set_xlabel("Study Hours")
            ax.set_ylabel("Marks Obtained")
            ax.set_title("Study Hours vs. Marks")
            ax.legend()
            st.pyplot(fig)
    
    # --- Footer ---
    st.markdown("---")
    st.caption("Made with ❤️ using Streamlit and Scikit-learn")

def render_classification_lab():
    st.title("🧪 Interactive Classification Lab")
    st.write("Train and evaluate machine learning classification models with your own data.")
    
    # Initialize session state variables
    if 'model' not in st.session_state:
        st.session_state.model = None
    if 'features' not in st.session_state:
        st.session_state.features = None
    if 'label_encoders' not in st.session_state:
        st.session_state.label_encoders = {}
    if 'target_column' not in st.session_state:
        st.session_state.target_column = None
    
    # Create tabs for different steps
    tabs = st.tabs(["1. Upload & Prepare Data", "2. Train & Evaluate Model", "3. Make Predictions", "4. View History"])
    
    # =================================================================
    # TAB 1: UPLOAD & PREPARE DATA
    # =================================================================
    with tabs[0]:
        st.header("1. Upload & Prepare Data")
        st.write("Upload your dataset and prepare it for training.")
        
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        
        if uploaded_file is not None:
            # Load the data
            df = ml_manager.load_data(uploaded_file)
            
            if isinstance(df, str):  # Error message
                st.error(df)
            else:
                st.success("Data loaded successfully!")
                
                # Display basic info
                st.subheader("Dataset Preview")
                st.dataframe(df.head())
                
                # Display data info
                info = ml_manager.get_data_info(df)
                st.subheader("Dataset Information")
                st.write(f"**Shape:** {info['shape'][0]} rows, {info['shape'][1]} columns")
                st.write(f"**Numerical columns:** {', '.join(info['numerical_cols'])}")
                st.write(f"**Categorical columns:** {', '.join(info['categorical_cols'])}")
                
                # Data cleaning options
                st.subheader("Data Cleaning Options")
                
                # Columns to drop
                columns_to_drop = st.multiselect(
                    "Select columns to drop:",
                    df.columns.tolist()
                )
                
                # Missing value strategies
                st.write("**Handle Missing Values:**")
                missing_value_strategies = {}
                for col in df.columns:
                    if df[col].isnull().sum() > 0:
                        strategy = st.selectbox(
                            f"Strategy for '{col}' ({df[col].isnull().sum()} missing values):",
                            ["Drop Rows", "Fill with Mean", "Fill with Median", "Fill with Mode"],
                            key=f"missing_{col}"
                        )
                        missing_value_strategies[col] = strategy
                
                # Target column selection
                target_column = st.selectbox(
                    "Select target column (what you want to predict):",
                    df.columns.tolist()
                )
                
                # Clean data button
                if st.button("Clean Data"):
                    cleaned_df, label_encoders = ml_manager.clean_data(
                        df, columns_to_drop, missing_value_strategies
                    )
                    
                    st.session_state.cleaned_df = cleaned_df
                    st.session_state.original_df = df
                    st.session_state.label_encoders = label_encoders
                    st.session_state.target_column = target_column
                    
                    st.success("Data cleaned successfully!")
                    st.subheader("Cleaned Dataset Preview")
                    st.dataframe(cleaned_df.head())
                    
                    # Show encoding information
                    if label_encoders:
                        st.subheader("Categorical Encoding Information")
                        for col, encoder in label_encoders.items():
                            st.write(f"**{col}:** {dict(zip(encoder.classes_, encoder.transform(encoder.classes_)))}")
    
    # =================================================================
    # TAB 2: TRAIN & EVALUATE MODEL
    # =================================================================
    with tabs[1]:
        st.header("2. Train & Evaluate Model")
        
        if hasattr(st.session_state, 'cleaned_df') and st.session_state.cleaned_df is not None:
            st.write("Select model parameters and train your classification model.")
            
            # Model selection
            model_name = st.selectbox(
                "Select classification algorithm:",
                ["Logistic Regression", "Random Forest", "Support Vector Machine (SVM)"]
            )
            
            # Test size selection
            test_size = st.slider("Test set size (%)", 10, 50, 20) / 100
            
            # Train model button
            if st.button("Train Model"):
                with st.spinner("Training model..."):
                    model, metrics, features = ml_manager.train_classification_model(
                        st.session_state.cleaned_df,
                        st.session_state.target_column,
                        model_name,
                        test_size
                    )
                    
                    if model is None:
                        st.error(metrics)  # In this case, metrics contains the error message
                    else:
                        st.session_state.model = model
                        st.session_state.metrics = metrics
                        st.session_state.features = features
                        
                        st.success("Model trained successfully!")
                        
                        # Display metrics
                        st.subheader("Model Performance")
                        st.write(f"**Accuracy:** {metrics['accuracy']:.4f}")
                        
                        # Display confusion matrix
                        st.subheader("Confusion Matrix")
                        fig, ax = plt.subplots(figsize=(10, 8))
                        sns.heatmap(metrics['conf_matrix'], annot=True, fmt='d', cmap='Blues',
                                   xticklabels=metrics['labels'], yticklabels=metrics['labels'])
                        plt.ylabel('True Label')
                        plt.xlabel('Predicted Label')
                        st.pyplot(fig)
                        
                        # Display classification report
                        st.subheader("Classification Report")
                        report_df = pd.DataFrame(metrics['class_report']).transpose()
                        st.dataframe(report_df.style.format({
                            'precision': '{:.2f}',
                            'recall': '{:.2f}',
                            'f1-score': '{:.2f}',
                            'support': '{:.0f}'
                        }))
        else:
            st.warning("Please upload and clean your data in the 'Upload & Prepare Data' tab first.")
    
    # =================================================================
    # TAB 3: MAKE PREDICTIONS
    # =================================================================
    with tabs[2]:
        st.header("3. Make Predictions")
        
        if st.session_state.model is not None:
            st.write("Enter values for each feature to get a prediction from your trained model.")
            
            # Create input fields for each feature
            input_data = {}
            original_df = st.session_state.original_df
            
            for feature in st.session_state.features:
                if feature == st.session_state.target_column:
                    continue
                    
                # Check if the feature is categorical
                if feature in st.session_state.label_encoders:
                    unique_values = st.session_state.label_encoders[feature].classes_
                    input_data[feature] = st.selectbox(f"Select value for '{feature}':", unique_values)
                else:
                    # For numerical features
                    min_val = float(original_df[feature].min())
                    max_val = float(original_df[feature].max())
                    mean_val = float(original_df[feature].mean())
                    
                    input_data[feature] = st.slider(
                        f"Value for '{feature}':", 
                        min_val, max_val, mean_val
                    )
            
            if st.button("Predict", type="primary"):
                prediction, prediction_proba = ml_manager.make_prediction(
                    st.session_state.model, st.session_state.features, input_data,
                    st.session_state.label_encoders, original_df, st.session_state.target_column
                )
                
                st.success(f"**Predicted Outcome:** `{prediction}`")
                st.write("**Prediction Probabilities:**")
                
                class_labels = st.session_state.model.classes_
                if st.session_state.label_encoders.get(st.session_state.target_column):
                    class_labels = st.session_state.label_encoders[st.session_state.target_column].inverse_transform(class_labels)
                    
                st.write(dict(zip(class_labels, prediction_proba)))
                
        else:
            st.warning("Please train a model on the 'Train & Evaluate Model' tab first.")
    
    # =================================================================
    # TAB 4: VIEW HISTORY
    # =================================================================
    with tabs[3]:
        st.header("4. Training History")
        st.write("Here is a log of all the models you have trained.")
        
        history = ml_manager.load_training_history()
        
        if not history:
            st.info("No training history found. Train a model to see it here.")
        else:
            history_df = pd.DataFrame(history)
            st.dataframe(history_df)

###############################################################################
# 6.  Initialize session state for navigation
###############################################################################
# Initialize the navigation session state if it doesn't exist
if 'navigate_to' not in st.session_state:
    st.session_state.navigate_to = None
    
# Set default page to Home if this is the first run
if 'first_run' not in st.session_state:
    st.session_state.first_run = True
    main_choice = "Home"

# Check if we need to navigate based on button clicks from home page
if st.session_state.navigate_to is not None:
    # Map the button titles to the main_choice options
    navigation_map = {
        "AI Automation Hub": "AI Automation Hub (9 Tools)",
        "Desktop Assistant": "Desktop Assistant",
        "File Manager": "File Manager",
        "SSH Assistant": "SSH Assistant",
        "Live AI Camera": "Live AI Camera",
        "Saundarya Lite": "Saundarya Lite",
        "Motivation Buddy": "Motivation Buddy",
        "AI Vehicle Recommender Hub": "AI Vehicle Recommender Hub",
        "Study Hours vs Marks Predictor": "Study Hours vs Marks Predictor",
        "Interactive Classification Lab": "Interactive Classification Lab"
    }
    
    # Set the main_choice based on the navigation
    if st.session_state.navigate_to in navigation_map:
        main_choice = navigation_map[st.session_state.navigate_to]
    
    # Reset the navigation state
    st.session_state.navigate_to = None

###############################################################################
# 7.  Router based on sidebar choice
###############################################################################
if main_choice == "Home":
    render_home()
elif main_choice == "AI Automation Hub (9 Tools)":
    render_ai_automation_hub()
elif main_choice == "Desktop Assistant":
    render_desktop_assistant()
elif main_choice == "File Manager":
    render_file_manager()
elif main_choice == "SSH Assistant":
    render_ssh_assistant()
elif main_choice == "Live AI Camera":
    render_camera()
elif main_choice == "Saundarya Lite":
    render_saundarya_lite()
elif main_choice == "Motivation Buddy":
    render_motivation_buddy()
elif main_choice == "AI Vehicle Recommender Hub":
    render_vehicle_recommender()
elif main_choice == "Study Hours vs Marks Predictor":
    render_marks_predictor()
elif main_choice == "Interactive Classification Lab":
    render_classification_lab()
