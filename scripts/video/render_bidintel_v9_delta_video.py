from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = REPO_ROOT / "docs" / "v9"
OUT = ROOT / "BidIntel_ZeroToBuild_Masterclass_v9_delta_proof.mp4"
MANIFEST = ROOT / "BidIntel_ZeroToBuild_Masterclass_v9_delta_manifest.json"
FRAMES = ROOT / "v9_delta_frames"
W, H = 1920, 1080


def font(size: int, bold: bool = False):
    names = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            pass
    return ImageFont.load_default()


TITLE = font(58, True)
HEAD = font(38, True)
BODY = font(31)
SMALL = font(24)
MONO = font(25)


SLIDES = [
    {
        "title": "BidIntel V9 Hardening Delta",
        "body": [
            "Owner: Claude/Millie tutorial video.",
            "Base preserved: V8 masterclass.",
            "Goal: keep what works, fix every chapter that breaks the follow-along build.",
            "Truth label: this is the V9 delta/proof package, not a full 140-minute re-render.",
        ],
    },
    {
        "title": "11-Step Gate Applied",
        "body": [
            "Actual target: Claude/Millie V9 tutorial package.",
            "Canonical repo: GitHub/Postgres Repo C.",
            "Mismatch avoided: no mixing Repo A proof into Repo C claims unless ported.",
            "Video rule: future full MP4 must show real terminal, browser, API, and scroll coverage.",
        ],
    },
    {
        "title": "Repo C Patch: Guardrails",
        "body": [
            "Added backend/app/security/guardrails_service.py.",
            "Prompt injection now blocks before cache lookup.",
            "Prompt injection now blocks before retrieval.",
            "Output guardrail runs before cache storage.",
        ],
    },
    {
        "title": "Repo C Patch: Upload Safety",
        "body": [
            "PDF text is scanned before chunking, embedding, or storage.",
            "Prompt-injection documents: REJECTED.",
            "Secret-bearing documents: REJECTED.",
            "PII-bearing documents: ACCEPTED_WITH_REDACTIONS.",
            "Plain Documents UI now shows document-security status.",
        ],
    },
    {
        "title": "Verified: Guardrail Script",
        "code": [
            "cd \".../bidintel/backend\"",
            "PYTHONPATH=. python3 scripts/test_guardrails_v9.py",
            "",
            "{'blocked_question': 'BLOCKED',",
            " 'malicious_doc': 'REJECTED',",
            " 'secret_doc': 'REJECTED',",
            " 'pii_doc': 'ACCEPTED_WITH_REDACTIONS',",
            " 'clean_doc': 'ACCEPTED'}",
        ],
    },
    {
        "title": "Verified: RBAC And Sim Workflow",
        "code": [
            "PYTHONPATH=. python3 scripts/test_access_control.py",
            "{'proposal_writer_blocked_from_hr': True,",
            " 'hr_can_retrieve_hr': True, 'admin_reads_all': True}",
            "",
            "PYTHONPATH=. python3 scripts/sim_workflow.py",
            "DONE - ingestion -> retrieval -> RBAC -> RRF -> rerank",
            "-> context -> answer -> citations -> evaluation.",
        ],
    },
    {
        "title": "Verified: Build Checks",
        "code": [
            "PYTHONPATH=backend python3 -m compileall backend/app backend/scripts",
            "compileall: passed",
            "",
            "cd frontend && npm run build",
            "vite build: passed, 83 modules transformed",
            "",
            "pytest: blocked - active Python has no pytest and requirements.txt omits it",
        ],
    },
    {
        "title": "V9 Chapter Fixes",
        "body": [
            "Ch2/3/4: show exact install, Docker, psql, migration, and port recovery.",
            "Ch5: upload safety before storage.",
            "Ch20: guardrail before cache/retrieval.",
            "Ch21: first ask vs repeat ask cache proof.",
            "Ch22: bid/no-bid scorer labeled simplified unless RAG-grounded scorer is ported.",
        ],
    },
    {
        "title": "Truth Boundary",
        "body": [
            "REAL LOCAL: FastAPI, frontend, pgvector schema, RAG pipeline, cache, RBAC filter, local scanners.",
            "LOCAL MOCK: mock Bedrock, heuristic eval/citation scoring.",
            "SIMULATED CLOUD: AWS IAM/Bedrock/ECS/RDS docs and mapping.",
            "FUTURE PRODUCTION: real DLP, malware scan, Bedrock Guardrails, calibrated win scoring.",
        ],
    },
    {
        "title": "What Is Still Open",
        "body": [
            "Full 140-minute V9 MP4 render is not complete.",
            "Reason: the long-video generator used for V8 was not saved.",
            "Correct next step: render a fresh full V9 from the chapter gate and build update.",
            "Do not call the delta video the full masterclass. It is the verified V9 hardening package.",
        ],
    },
]


def draw_slide(slide: dict, idx: int):
    img = Image.new("RGB", (W, H), "#f5f7fb")
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 80), fill="#13322b")
    d.text((70, 23), "CONTROLLED UNCLASSIFIED INFORMATION // AUTHORIZED USE ONLY", fill="#cdeee2", font=SMALL)
    d.text((70, 135), slide["title"], fill="#102033", font=TITLE)
    d.line((70, 215, W - 70, 215), fill="#d6dde8", width=3)
    y = 265
    if "code" in slide:
        d.rounded_rectangle((70, 255, W - 70, H - 120), radius=18, fill="#0b1220")
        y = 295
        for line in slide["code"]:
            d.text((110, y), line, fill="#d8f3dc" if line and not line.startswith("pytest") else "#ffd166", font=MONO)
            y += 43
    else:
        for line in slide["body"]:
            wrapped = wrap(line, 86)
            for part in wrapped:
                d.text((105, y), part, fill="#1b2b42", font=BODY)
                y += 46
            y += 16
    d.text((70, H - 70), f"BidIntel V9 delta proof frame {idx + 1}/{len(SLIDES)}", fill="#64748b", font=SMALL)
    return img


def wrap(text: str, width: int):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        test = f"{cur} {word}".strip()
        if len(test) > width:
            lines.append(cur)
            cur = word
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def main():
    FRAMES.mkdir(exist_ok=True)
    frame_paths = []
    for i, slide in enumerate(SLIDES):
        path = FRAMES / f"frame_{i:03d}.png"
        draw_slide(slide, i).save(path)
        frame_paths.append(path)

    concat = FRAMES / "concat.txt"
    with concat.open("w") as f:
        for path in frame_paths:
            f.write(f"file '{path}'\n")
            f.write("duration 7\n")
        f.write(f"file '{frame_paths[-1]}'\n")

    silent = FRAMES / "silent.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-vf", "format=yuv420p", "-r", "30", str(silent)
    ], check=True)
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-i", str(silent), "-shortest", "-c:v", "copy", "-c:a", "aac", str(OUT)
    ], check=True)

    manifest = {
        "artifact": str(OUT.relative_to(REPO_ROOT)),
        "kind": "v9_delta_proof_video",
        "truth_boundary": "Not the full 140-minute masterclass re-render. This is the verified V9 hardening delta/proof package.",
        "frames": [str(p.relative_to(REPO_ROOT)) for p in frame_paths],
        "source_docs": [
            str((ROOT / "BidIntel_ZeroToBuild_Masterclass_v9_Chapter_Gate.md").relative_to(REPO_ROOT)),
            str((ROOT / "BidIntel_ZeroToBuild_Masterclass_v9_Build_Update.md").relative_to(REPO_ROOT)),
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
