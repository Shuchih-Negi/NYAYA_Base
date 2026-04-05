## You are building NYAYA — a hackathon pitch UI for a legal aid system that helps

## sexually harassed victims restructure their testimony using multimodal AI.

## 

## 

## Global rules:

##   \- Dark everywhere. No white backgrounds. No purple gradients.

##   \- Borders are always 1px solid var(--border), radius 2–4px max

##   \- Panels have subtle inner glow: box-shadow: inset 0 0 40px rgba(0,201,255,0.03)

##   \- Scanline texture on all panel backgrounds (CSS repeating-linear-gradient, 2px, 1% opacity)

##   \- All animated counters, probabilities, graphs must feel LIVE even when faked

## 

## ════════════════════════════════════════════════════════════════

## NAVIGATION — SIDEBAR

## ════════════════════════════════════════════════════════════════

## 

## Fixed left side. 48px wide invisible hover zone.

## When user hovers over the word "NYAYA" OR the left 48px edge:

##   sidebar slides in from left (translateX \-200px → 0), width 240px,

##   backdrop-filter blur(24px), background rgba(7,13,18,0.97)

## 

## Sidebar contents (top to bottom):

##   Brand: "NYA\<span accent\>YA\</span\>" in 22px Syne 800

##   Divider line

##   Nav items (each 12px Syne 600 uppercase, letter-spacing 0.16em):

##     ○  LANDING

##     ○  CONSENT  

##     ○  INTERVIEW ROOM

##     ○  NEURAL ANALYSIS

##     ○  INFERENCE ENGINE

##     ○  LEGAL MAPPING

##     ○  CASE OUTPUT

##   Active item has 2px left accent border \+ cyan color

##   Bottom of sidebar: pulsing green dot \+ "SESSION SECURE · AES-256"

## 

## Clicking any nav item navigates to that page (opacity 0→1 transition, 0.5s).

## Pages are position:fixed, stacked, only active page has opacity:1 pointer-events:all.

## ════════════════════════════════════════════════════════════════

## PAGE 1 — CONSENT

## ════════════════════════════════════════════════════════════════

## 

## Centered card layout. Max-width 560px. Serious, dignified tone.

## 

## Card style:

##   background var(--panel)

##   border 1px solid var(--border)

##   border-radius 4px

##   padding 52px

##   box-shadow: 0 0 80px rgba(0,0,0,0.6)

## 

## Card contents:

## 

##   Eyebrow: "INFORMED CONSENT — CASE INTAKE"

##   JetBrains Mono 10px, var(--accent), letter-spacing 0.2em, uppercase

## 

##   Title: "Before we begin"

##   Playfair Display italic 700, 36px

## 

##   Thin 40px cyan divider line (margin 24px 0\)

## 

##   Body text (13px, var(--dim), line-height 1.8):

##     "This session will use your camera and microphone to capture your testimony.

##      All processing happens on this device. Nothing is transmitted to any server

##      without your explicit action. You may stop at any time."

## 

##   Consent items list (4 items, each with small cyan circle icon \+ text):

##     ✦ Camera access — used for facial landmark analysis only. No video is stored.

##     ✦ Microphone access — speech is transcribed locally via Whisper-compatible API.

##     ✦ On-device processing — facial data exists for 15 seconds only, then discarded.

##     ✦ Right to erasure — all session data deleted within 7 days on request.

## 

##   Checkbox row:

##     Custom styled checkbox (18px, cyan border, fills cyan on check)

##     Label: "I understand and consent to the above. I am proceeding voluntarily."

##     When checked: enables the Begin Session button

## 

##   Button (full width, 16px tall):

##     "BEGIN SESSION — ACTIVATE CAMERA & MICROPHONE"

##     Disabled state: opacity 0.3, cursor not-allowed

##     Enabled state: bg var(--accent), color var(--black), Syne 700

##     onClick when enabled: request camera \+ mic permissions, then navigate to PAGE 2

## 

## ════════════════════════════════════════════════════════════════

## PAGE 2 — INTERVIEW ROOM

## ════════════════════════════════════════════════════════════════

## 

## Grid layout:

##   \- Top bar: 48px full width

##   \- Left column: \~60% width — camera \+ facemesh

##   \- Right column: \~40% width — STT transcript \+ stress panel

## 

## TOP BAR:

##   Left: "NYAYA" (brand, 13px Syne 800\) \+ "CASE-2024-0047" (JetBrains Mono 10px dim)

##   Right: "● LIVE" badge (red-pink bg, blinking dot) \+ "AES-256 SECURED" badge (teal)

##   Far right: session timer counting up from 00:00 (JetBrains Mono)

## 

## LEFT — VIDEO \+ FACEMESH:

##   Full height of remaining space.

##   \<video\> element hidden (used as source)

##   \<canvas\> on top, same dimensions, draws:

##     1\. The live video frame (drawImage)

##     2\. MediaPipe FaceMesh tessellation (468 triangle mesh)

##        — stroke color: rgba(0,201,255,0.35), lineWidth 0.5

##     3\. Key landmark dots (eyes, brow, nose tip, mouth corners)

##        — fill: rgba(0,201,255,0.8), radius 2px

##     4\. Floating data labels positioned over face landmarks:

##        Top of forehead: "AU6: 0.72" (JetBrains Mono 9px, cyan)

##        Left brow: "BROW: −4.2mm" (9px, amber)

##        Right eye: "EYE: 0.81" (9px, cyan)

##        Jaw: "JAW: 12.3°" (9px, dim)

##        These values animate slowly (±0.05 per frame, sin wave) to look live

## 

##   Bottom overlay strip (position absolute, bottom 0, full width):

##     Dark gradient strip. Left side:

##     "MEDIAPIPE FACEMESH · 478 LANDMARKS · 30FPS"

##     JetBrains Mono 9px, dim

##     Right side: frame counter "FRAME 01847" incrementing

## 

## RIGHT — STT \+ STRESS:

##   Top 60%: TRANSCRIPT PANEL

##     Header: "LIVE TRANSCRIPT" \+ recording dot

##     Scrolling text area, dark bg, no border radius

##     Words appear one by one (simulate with a predefined testimony array,

##     push one word every 400ms in demo mode)

##     Words color-coded by stress:

##       calm words: var(--calm)

##       moderate phrases: var(--gold)

##       high-stress words: var(--accent2)

##     Predefined testimony to stream (loop or use real STT if mic works):

##       "He... called me into his office... after everyone had left.

##        I had been working there since January. He said...

##        he said if I told anyone... he would make sure I lost my job.

##        I didn't know what to do. I just stood there.

##        This happened again in March. And then in April.

##        I finally told my sister. She said I should report it."

## 

##   Bottom 40%: STRESS MONITOR

##     Label: "BAYESIAN STRESS FUSION"

##     Big state badge (changes over time):

##       0–30s: "CALM" — teal color, teal glow

##       30–60s: "MODERATE DISTRESS" — amber

##       60s+: "HIGH DISTRESS" — red-pink, pulsing border

##     Three horizontal bars below:

##       VOICE (TRIBE v2):    animated fill bar, 0→87%

##       LEXICAL (NLP):       animated fill bar, 0→74%

##       FACIAL (FACEMESH):   animated fill bar, 0→61%

##     Formula below bars:

##       P \= 0.54·V \+ 0.32·W \+ 0.14·F

##       JetBrains Mono, 11px, dim. Highlight coefficients in cyan.

##     Computed score: "P \= 0.81" in large JetBrains Mono, accent color

## 

## ════════════════════════════════════════════════════════════════

## PAGE 3 — NEURAL ANALYSIS (THE SHOWSTOPPER)

## ════════════════════════════════════════════════════════════════

## 

## Full dark screen. This is the brain page. Make it cinematic.

## 

## Layout:

##   Left 65%: 3D brain visualization

##   Right 35%: neural data panel

## 

## LEFT — THREE.JS BRAIN:

##   Build a brain-like mesh using Three.js.

##   Since a real brain GLTF may not load from CDN, build it procedurally:

## 

##   Method — Layered sphere distortion to approximate brain shape:

##     Base: SphereGeometry(2.2, 128, 128\)

##     In the vertex shader / vertex manipulation:

##       For each vertex, apply sin/cos noise at multiple frequencies to create

##       folded gyri/sulci texture:

##         vertex.x \+= 0.15 \* sin(8\*vertex.y) \* cos(6\*vertex.z)

##         vertex.y \+= 0.1 \* sin(7\*vertex.x) \* cos(5\*vertex.z)

##         vertex.z \+= 0.12 \* sin(9\*vertex.x) \* cos(7\*vertex.y)

##     Material: MeshPhongMaterial

##       color: \#b0bec5 (cool grey)

##       specular: \#ffffff

##       shininess: 20

##       wireframe: false

## 

##   Three lights:

##     AmbientLight \#334455 intensity 0.6

##     DirectionalLight \#ffffff intensity 0.8 from top-right

##     PointLight \#00c9ff intensity 0.4 from left (cyan rim)

## 

##   Brain slowly rotates: y \+= 0.003 per frame

## 

##   STIMULUS GRADIENTS — the key effect:

##     Create 3 "hotspot" meshes (SphereGeometry 0.3, placed at approximate brain regions):

##       Amygdala: position (-0.8, \-0.6, 0.8)

##       ACC (anterior cingulate cortex): position (0, 0.9, 0.6)

##       Insula: position (1.1, 0.1, 0.5)

## 

##     Each hotspot has a PointLight child that pulses in intensity.

##     Each hotspot material color animates over time:

##       0–2s: \#1a3a5c (deep blue, low activation)

##       2–4s: \#7b61ff (violet, building)

##       4–6s: \#f0b429 (amber, moderate)

##       6s+:  \#ff4d6d (red-pink, high activation)

##     Use THREE.Color.lerp() to smoothly interpolate.

## 

##     Add particle spray from each hotspot:

##       Small points (3–5px) emitting outward in a slow sphere,

##       color matching the hotspot, fading to transparent at distance 1.5

## 

##   Label the 3 regions with floating HTML overlays (position:absolute, computed from

##   Three.js project() to screen coordinates):

##     "AMYGDALA · 0.87" — in red-pink

##     "ANT. CINGULATE · 0.74" — in violet

##     "INSULA · 0.61" — in amber

## 

##   Bottom of brain panel:

##     "TRIBE v2 NEURAL ENCODING · STIMULUS RESPONSE SIMULATION"

##     JetBrains Mono 9px, dim, letter-spacing 0.15em

## 

## RIGHT — NEURAL DATA PANEL:

##   Header: "NEURAL ACTIVATION SIGNATURE"

##   Syne 700, 13px, uppercase, letter-spacing 0.16em

## 

##   Three region cards (each with region name, score bar, activation class):

## 

##     Card 1: AMYGDALA

##       "Threat & fear processing"

##       Score bar: fills to 87%, color var(--accent2)

##       Tag: "HIGH ACTIVATION"

## 

##     Card 2: ANTERIOR CINGULATE

##       "Conflict monitoring · Pain response"

##       Score bar: fills to 74%, color var(--accent3)

##       Tag: "ELEVATED"

## 

##     Card 3: INSULA

##       "Interoception · Disgust · Social pain"

##       Score bar: fills to 61%, color var(--gold)

##       Tag: "MODERATE"

## 

##   Divider

## 

##   FUSION OUTPUT:

##     "STRESS CLASSIFICATION"

##     Big badge: "HIGH DISTRESS" — red-pink, pulsing

##     "Bayesian posterior: P(high | V,W,F) \= 0.81"

##     JetBrains Mono, dim

## 

##   Divider

## 

##   MODEL TAG:

##     "Foundation model: TRIBE v2 (Toneva et al.)"

##     "Facial proxy: MediaPipe FaceMesh AU extraction"

##     "Fusion: Bayesian · weights \[0.54, 0.32, 0.14\]"

##     JetBrains Mono 9px, dim

## 

##   Bottom button:

##     "PROCEED TO INFERENCE ENGINE →"

##     Goes to PAGE 4

## 

## ════════════════════════════════════════════════════════════════

## PAGE 4 — INFERENCE ENGINE

## ════════════════════════════════════════════════════════════════

## 

## Split layout:

##   Left 55%: D3 force-directed node graph

##   Right 45%: formula panel \+ reconstructed timeline

## 

## LEFT — D3 NODE GRAPH:

##   Title: "BAYESIAN TEMPORAL INFERENCE" (top left, Syne 700 12px)

##   Subtitle: "Event nodes · Certainty-weighted · Chronological reconstruction"

## 

##   Nodes (7 events from the predefined testimony):

##     E1: "Employment begins" — certainty 0.95 — size 28px

##     E2: "First incident: isolation" — certainty 0.89 — size 26px

##     E3: "Threat issued" — certainty 0.84 — size 24px

##     E4: "Second incident (March)" — certainty 0.91 — size 26px

##     E5: "Third incident (April)" — certainty 0.88 — size 25px

##     E6: "Disclosure to sister" — certainty 0.76 — size 22px

##     E7: "FIR consideration" — certainty 0.99 — size 30px

## 

##   Node color by certainty:

##     ≥ 0.85: var(--accent) (cyan)

##     0.70–0.84: var(--gold) (amber)

##     \< 0.70: var(--accent2) (red-pink)

## 

##   Node label: event text in JetBrains Mono 9px below node

##   Node sublabel: "89%" in JetBrains Mono 8px, dim, below event text

## 

##   Edges: directional arrows (temporal ordering)

##     stroke: rgba(255,255,255,0.15), strokeWidth 1.5

##     Animated dashes traveling along edges (stroke-dashoffset animation)

##     Edge label (small, dim): ordering probability "P=0.91"

## 

##   Nodes appear one by one with a 300ms stagger (scale 0→1, opacity 0→1)

##   Edges draw themselves after nodes appear (stroke-dasharray animation)

## 

##   Clicking a node shows a tooltip:

##     Event text, certainty %, temporal cue phrases used, BNS relevance tag

## 

##   Graph physics: d3.forceSimulation with:

##     forceLink (distance 120\)

##     forceManyBody (strength \-300)

##     forceCenter

## 

## RIGHT — FORMULA \+ TIMELINE:

##   Top section: CREDIBILITY FORMULA

##     Large display:

##       P  \=  0.54·V  \+  0.32·W  \+  0.14·F

##     Each coefficient lights up in sequence (cycle every 2s):

##       0.54 → cyan highlight

##       0.32 → violet highlight

##       0.14 → amber highlight

##     Below formula:

##       Three live bar charts (horizontal):

##         V (VOICE)   \[████████░░\] 0.87  — bar color cyan

##         W (WORDS)   \[██████░░░░\] 0.74  — bar color violet

##         F (FACIAL)  \[█████░░░░░\] 0.61  — bar color amber

##       Each bar animates to its value over 1.5s

##     Result line:

##       "P \= 0.81" — JetBrains Mono 28px, var(--accent), centered

##       "HIGH CREDIBILITY SIGNAL" — Syne 700 10px, uppercase, dim

## 

##   Divider

## 

##   Bottom section: RECONSTRUCTED TIMELINE

##     Title: "CHRONOLOGICAL RECONSTRUCTION"

##     Horizontal scrolling timeline bar:

##       Each event is a vertical mark on the bar

##       The bar draws itself left to right over 2s

##       Events appear as markers with labels below:

##         ├── Jan 2024 · "Employment" · ●95%

##         ├── Feb 2024 · "First incident" · ●89%

##         ├── Mar 2024 · "Second incident" · ●91%

##         ├── Mar 2024 · "Threat issued" · ●84%

##         ├── Apr 2024 · "Third incident" · ●88%

##         ├── May 2024 · "Disclosed to sister" · ●76%

##         └── Jun 2024 · "FIR" · ●99%

##       Markers colored by certainty (same scheme as nodes)

##     Below timeline:

##       "Non-linear disclosure → chronological reconstruction complete"

##       JetBrains Mono 10px, var(--calm)

## 

## ════════════════════════════════════════════════════════════════

## PAGE 5 — LEGAL MAPPING

## ════════════════════════════════════════════════════════════════

## 

## Three-column layout.

## 

## LEFT COLUMN (30%): ENTITY KNOWLEDGE GRAPH

##   Title: "ENTITY MAP"

##   Small D3 force graph:

##     Nodes:

##       "Priya" (survivor) — circle, teal

##       "Accused Person A" — circle, red-pink

##       "Sector 17 Office" — square, amber

##       "Police Station" — square, dim

##       "Sister" — circle, violet

##     Edges with labels:

##       Priya → Accused: "employed under"

##       Accused → Sector 17: "controls"

##       Priya → Sector 17: "confined at"

##       Priya → Sister: "disclosed to"

##       Sister → Police: "reported"

##   Node labels: Syne 600, 10px

##   Edge labels: JetBrains Mono 8px, dim

## 

## CENTER COLUMN (40%): BNS SECTIONS

##   Title: "BNS 2023 LEGAL MAPPING"

##   Subtitle: "FAISS semantic search · 358 sections indexed"

##   

##   5 BNS cards (each):

##     Section number (JetBrains Mono, accent)

##     Section title (Syne 600, white, 12px)

##     Description (dim, 11px, 1 line)

##     Confidence bar (fills with color)

##     Confidence label RIGHT-ALIGNED

##     

##     BNS 63  — Rape                     ████████████ HIGH   (accent2)

##     BNS 74  — Assault on woman         █████████░░░ HIGH   (accent2)

##     BNS 85  — Cruelty                  ███████░░░░░ MED    (gold)

##     BNS 143 — Trafficking              █████░░░░░░░ MED    (gold)

##     BNS 351 — Criminal intimidation    ███░░░░░░░░░ LOW    (dim)

## 

##   Each card has a checkbox (custom styled, cyan)

##   Checking it increments a counter: "3 / 5 SECTIONS VERIFIED"

## 

## RIGHT COLUMN (30%): COUNSELOR PANEL \+ GENERATE

##   Title: "COUNSELOR VERIFICATION"

##   Subtitle: "Human confirmation required to proceed"

## 

##   Counselor name field (pre-filled): "Adv. Sunita Sharma"

##   Case ID field (pre-filled): "CASE-2024-0047"

##   Verification checkboxes:

##     ☑ Timeline reviewed and confirmed

##     ☑ BNS sections approved

##     ☑ Survivor consent documented

##     ☐ Signature obtained

## 

##   Divider

## 

##   STATS BOX (dark inset):

##     "Session Duration  18 min 42s"

##     "Events Extracted  7"

##     "Avg Certainty     86.0%"

##     "BNS Mapped        3 sections"

##     "Time Saved        \~110 minutes"

##     All in JetBrains Mono, 10px

## 

##   Big button at bottom:

##     "GENERATE LEGAL AID PDF"

##     Full width, bg var(--accent), color var(--black)

##     Syne 800, 12px, letter-spacing 0.18em, uppercase

##     On click: show loading animation (typewriter: "Structuring testimony…

##     Mapping BNS sections… Generating SHA-256 hash… Compiling PDF…")

##     Each line appears over 600ms, then navigate to PAGE 6

## 

## ════════════════════════════════════════════════════════════════

## PAGE 6 — CASE OUTPUT

## ════════════════════════════════════════════════════════════════

## 

## Layout:

##   Left 50%: PDF preview mockup

##   Right 50%: case stats \+ closing statement

## 

## LEFT — PDF PREVIEW:

##   A styled div that looks like a white paper document (but with dark theme):

##   White background, dark text (this is the ONE place with light bg)

##   Box shadow: 0 20px 80px rgba(0,0,0,0.8)

##   Slides in from bottom on page load (translateY 60px → 0, 0.6s ease-out)

## 

##   PDF header:

##     "NYAYA LEGAL AID DOCUMENT"

##     "Prepared under BNS 2023 | Case: 2024-0047"

##     "Date: \[current date\]"

## 

##   Section: STRUCTURED TESTIMONY (excerpt)

##     "The survivor, referred to as Complainant A, states:

##     Employment commenced January 2024 at \[LOCATION REDACTED\].

##     First incident occurred February 2024\.

##     The accused issued verbal threats of termination.

##     Second and third incidents March–April 2024\.

##     Disclosure to family member May 2024."

## 

##   Section: BAYESIAN TIMELINE

##     Small horizontal bar with the 7 events listed chronologically

## 

##   Section: APPLICABLE BNS SECTIONS

##     "BNS 63 — Rape (High relevance)"

##     "BNS 74 — Assault on woman (High relevance)"

##     "BNS 85 — Cruelty (Moderate relevance)"

## 

##   Footer of PDF:

##     "SHA-256: a3f9c2d1e8b7...4f2a"

##     "AI-reconstructed timeline — subject to legal review"

##     "Generated by NYAYA · Human-verified by Adv. Sunita Sharma"

## 

## RIGHT — STATS \+ CLOSING:

##   Top: large stats in a grid (2x3):

##     "18:42" / "SESSION DURATION"

##     "7" / "EVENTS EXTRACTED"

##     "86%" / "AVG CERTAINTY"

##     "3" / "BNS SECTIONS"

##     "\~110 min" / "TIME SAVED"

##     "SHA-256" / "TAMPER PROOF"

##   All labels: JetBrains Mono 9px, dim, uppercase

##   All values: Syne 800, 32px (large), var(--accent)

## 

##   Divider

## 

##   Closing statement (centered, with generous whitespace above and below):

##     "Human-led."    — Playfair Display italic, 28px, var(--white)

##     "AI-assisted."  — Playfair Display italic, 28px, var(--dim)

##     "Trauma-aware." — Playfair Display italic, 28px, var(--accent)

##     Each line fades in with 0.4s stagger

## 

##   Below:

##     "She spoke once." — Syne 700, 13px, letter-spacing 0.2em, var(--dim)

##     "This is what her lawyer receives." — same style, var(--white)

## 

##   Bottom: Download button (outline style, full width):

##     "↓ DOWNLOAD PDF" — border var(--accent), color var(--accent)

## 

## ════════════════════════════════════════════════════════════════

## GLOBAL EFFECTS TO IMPLEMENT

## ════════════════════════════════════════════════════════════════

## 

## 1\. SCANLINE TEXTURE (all panel backgrounds):

##    background-image: repeating-linear-gradient(

##      0deg,

##      transparent,

##      transparent 1px,

##      rgba(255,255,255,0.008) 1px,

##      rgba(255,255,255,0.008) 2px

##    );

## 

## 2\. ANIMATED NUMBER COUNTERS:

##    All percentage values and scores must count up from 0 when their page activates.

##    Duration: 1.2s, easing: cubic-bezier(0.16, 1, 0.3, 1\)

##    Implement with requestAnimationFrame \+ lerp.

## 

## 3\. BAR ANIMATIONS:

##    All bar fills animate from 0% to target width when page activates.

##    Duration: 1.5s, staggered 150ms between bars.

## 

## 4\. PAGE TRANSITIONS:

##    Active page: opacity 1, transform translateY(0)

##    Inactive page: opacity 0, transform translateY(8px)

##    Transition: 0.5s cubic-bezier(0.16, 1, 0.3, 1\)

##    When navigating, run exit animation on current page simultaneously.

## 

## 5\. STRESS STATE COLOR TRANSITIONS (page 2):

##    Stress badge and its border-color smoothly interpolate via CSS transition 1s.

##    The STT transcript background also subtly tints (rgba of stress color at 3%).

## 

## 6\. D3 GRAPH PHYSICS (pages 4 and 5):

##    Must be interactive — nodes can be dragged.

##    Tooltip on hover shows full event details.

##    Graph must settle within 2s (alpha decay 0.028).

## 

## 7\. KEYBOARD SHORTCUTS:

##    Arrow keys / 1-6 number keys navigate between pages.

##    This is for the demo presenter — speeds up pitch.

## 

## 8\. NO REAL BACKEND NEEDED:

##    All data is hardcoded in JS constants at the top of the file.

##    STT in page 2 can optionally use Web Speech API if browser supports it,

##    with a fallback to the predefined testimony auto-typing demo.

##    Camera/facemesh is real if MediaPipe loads, falls back to a static

##    placeholder with animated fake landmark positions if not.

## 

## ════════════════════════════════════════════════════════════════

## THINGS TO NEVER DO

## ════════════════════════════════════════════════════════════════

## 

## \- No lorem ipsum anywhere

## \- No placeholder "coming soon" panels

## \- No purple gradients on white

## \- No Inter or system fonts

## \- No rounded corners \> 4px (this is a serious legal tool, not a SaaS app)

## \- No emoji in the UI

## \- No loading spinners (use typewriter text instead)

## \- No generic dashboard chrome (no hamburger menus, no breadcrumbs)

## \- No mobile layout (this is a desktop pitch demo only)

## \- Never show an error state — if camera fails, show a graceful static placeholder

##   that still has animated facemesh dots to look live

## 

## ════════════════════════════════════════════════════════════════

## DEFINITION OF DONE

## ════════════════════════════════════════════════════════════════

## 

## The file opens in Chrome with no build step.

## All 7 pages render correctly and navigation works.

## The brain (Page 3\) rotates and has glowing hotspots.

## The node graph (Page 4\) is interactive and animates in.

## The STT window (Page 2\) shows text streaming in live.

## The PDF page (Page 6\) has the closing statement fade in.

## Keyboard shortcuts 1–6 work for the presenter.

## The sidebar slides in on hover of the left edge.

## All numbers count up. All bars animate. All transitions are smooth.

## 

## A judge watching this demo should believe this is a working product.

##   