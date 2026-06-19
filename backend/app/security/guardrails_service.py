"""Local security guardrails for reviewer-runnable BidIntel.

This is a deterministic local stand-in for production Bedrock Guardrails,
enterprise DLP, malware scanning, and policy services. It runs before cache,
retrieval, chunking, embedding, or storage when wired into request/document
paths, so untrusted text cannot silently become model instructions.
"""
from __future__ import annotations

import re


INJECTION_PATTERNS = [
    r"ignore (all|any|previous|prior).{0,30}(instructions|prompt|rules)",
    r"disregard.{0,30}(instructions|above|previous|rules)",
    r"(reveal|show|print|repeat).{0,30}(system prompt|your prompt|instructions)",
    r"you are now|act as (a|an)?\s*(dan|developer mode|unrestricted)",
    r"jailbreak|do anything now",
    r"(drop|delete|truncate)\s+(table|database)|dump\s+(db|database|all)",
    r"override.{0,20}(rules|policy|guardrail)",
]

PII_PATTERNS = {
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "email": r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
    "phone": r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
    "credit_card": r"\b(?:\d[ -]?){13,16}\b",
}

SECRET_PATTERNS = {
    "aws_access_key": r"\bAKIA[0-9A-Z]{16}\b",
    "private_key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "bearer_token": r"\b[Bb]earer\s+[A-Za-z0-9._\-]{20,}",
}


def detect_injection(text: str) -> dict:
    matched = [p for p in INJECTION_PATTERNS if re.search(p, text or "", re.I)]
    return {"risk": "high" if matched else "low", "matched": matched}


def scan_pii(text: str) -> dict:
    findings = []
    redacted = text or ""
    for kind, pattern in PII_PATTERNS.items():
        for match in re.findall(pattern, text or ""):
            findings.append({"type": kind, "sample": str(match)[:40]})
        redacted = re.sub(pattern, f"[REDACTED-{kind.upper()}]", redacted)
    return {"findings": findings, "redacted": redacted}


def scan_secrets(text: str) -> dict:
    findings = []
    for kind, pattern in SECRET_PATTERNS.items():
        if re.search(pattern, text or ""):
            findings.append(kind)
    return {"findings": findings}


def evaluate_guardrails(question: str = "", answer: str = "") -> dict:
    """Return OK, REVIEW, or BLOCKED for /ask input and output."""
    reasons = []
    if detect_injection(question)["risk"] == "high":
        reasons.append("prompt_injection")
    if scan_secrets(question)["findings"] or scan_secrets(answer)["findings"]:
        reasons.append("secret_detected")

    answer_pii = scan_pii(answer)
    question_pii = scan_pii(question)
    if answer_pii["findings"]:
        reasons.append("pii_in_answer")

    decision = "OK"
    if "prompt_injection" in reasons or "secret_detected" in reasons:
        decision = "BLOCKED"
    elif "pii_in_answer" in reasons:
        decision = "REVIEW"

    return {
        "decision": decision,
        "reasons": reasons,
        "redacted_answer": answer_pii["redacted"],
        "pii_in_question": bool(question_pii["findings"]),
    }


def evaluate_document_security(text: str) -> dict:
    """Gate uploaded document text before chunking, embedding, or storage."""
    injection = detect_injection(text)
    pii = scan_pii(text)
    secrets = scan_secrets(text)
    reasons = []
    decision = "ACCEPTED"
    safe_text = text or ""

    if injection["risk"] == "high":
        reasons.append("prompt_injection")
    if secrets["findings"]:
        reasons.append("secret_detected")
    if reasons:
        decision = "REJECTED"
        safe_text = ""
    elif pii["findings"]:
        decision = "ACCEPTED_WITH_REDACTIONS"
        reasons.append("pii_redacted")
        safe_text = pii["redacted"]

    return {
        "decision": decision,
        "reasons": reasons,
        "prompt_injection": "failed" if injection["risk"] == "high" else "passed",
        "pii": "redacted" if pii["findings"] and decision != "REJECTED" else "passed",
        "secrets": "failed" if secrets["findings"] else "passed",
        "counts": {
            "prompt_injection_patterns": len(injection["matched"]),
            "pii_findings": len(pii["findings"]),
            "secret_findings": len(secrets["findings"]),
        },
        "safe_text": safe_text,
    }

