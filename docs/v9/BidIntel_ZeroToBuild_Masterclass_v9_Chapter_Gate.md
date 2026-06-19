# BidIntel Zero-To-Build Masterclass V9 Chapter Gate

Target video owner: Claude/Millie tutorial video.

Canonical repo for V9: `/Users/adamsmith/Documents/Claude/Projects/BidIntel Bid Contract AI  Automation/bidintel`

Public GitHub repo taught by V9: `https://github.com/Souljahsmitty/bidintel-enterprise-rag`

Reference base kept: `BidIntel_ZeroToBuild_Masterclass_v8.mp4`

V9 rule: keep the strong V8 structure, but no chapter stays unless it passes the
beginner gate and educator/AI-engineer gate.

Important correction: the finished V9 is not a sidecar delta or patch recap. It
must look and behave like V8's full masterclass, only better: same useful course
spine, audited chapter-by-chapter, with replacement scenes and missing proof
integrated into the right chapters. A delta package is only render input.

## Result Gate

| Area | Beginner Gate | Educator Gate | V9 Action |
|---|---|---|---|
| Project framing | Pass | Pass | Keep. Add AWS/local truth boundary before code. |
| Prerequisites | Fix needed | Fix needed | Add install sources, Docker Desktop check, `python3` vs `python`, PATH recovery, port conflict recovery. |
| Create project | Fix needed | Partial | Show Vite non-empty-dir prompt, exact working directory, and one pasteable install block. |
| Postgres/pgvector | Fix needed | Fix needed | Use Docker DB commands. Run `create_tables.sql` and `003_enterprise_tables.sql`. Show table/column proof. |
| Ingestion/upload | Fixed in Repo C V9 patch | Pass with local truth label | Uploaded text is scanned before storage. Prompt injection/secrets reject; PII redacts. |
| Hybrid retrieval | Needs visible proof | Pass | Show BM25, vector, RRF, rerank, evidence chunks, and RBAC filter. |
| Context/generation/citations | Pass with proof | Pass | Keep. Add live `/ask` response and citation/evidence proof. |
| Response quality/retry | Partial | Partial | Response-quality scoring exists. Retry loop remains optional unless ported and proven. |
| Backend API | Fix needed | Partial | Add missing-file scene or clone-reference-repo scene so imports do not surprise beginners. |
| Frontend | Partial | Partial | Teach plain UI as beginner path. Label React as optional enhanced path. |
| Local run proof | Fix needed | Partial | Add live Docker/backend/frontend/API proof segment. |
| Guardrails | Fixed in Repo C V9 patch | Pass for local stand-in | `/ask` input guardrail now runs before cache/retrieval. Output guardrail runs before cache store. |
| Cache | Needs video proof | Pass | Existing cache is wired. V9 must show first ask, repeated ask, cache metadata/hit count. |
| Bid/no-bid scorecard | Partial | Partial | Current Repo C scorer is placeholder/illustrative. Label as local simplified scorer unless RAG-grounded scorer is ported. |
| IAM/RBAC/control plane | Partial | Partial | RBAC retrieval filter exists. AWS IAM/RBAC dashboard remains simulated unless control-plane sims are ported. |
| AWS | Partial | Pass with labels | Keep as simulated/local-to-production mapping. Do not imply deployed AWS. |
| Final packaging | Not finished | Open | V9 delta docs/video generated as render input only. Finished V9 requires a full improved masterclass that preserves V8 bones and integrates all fixes in sequence. |

## Top V9 Blockers That Are Now Fixed

- Repo C now has `backend/app/security/guardrails_service.py`.
- `/ask` now blocks prompt-injection input before cache lookup, retrieval, or model call.
- `/ask` now checks the final answer before storing it in cache.
- `/upload` now scans extracted document text before chunking, embedding, or storage.
- The plain Documents UI now shows document-security status after upload.
- `scripts/demo.sh` now proves cache repeat call and prompt-injection block.
- `backend/scripts/test_guardrails_v9.py` proves BLOCKED, REJECTED, REDACTED, and ACCEPTED cases.

## Still Not Safe To Claim As Full Production

- Bedrock Guardrails are simulated locally by deterministic scanners.
- AWS IAM, Cognito, ECS, RDS, CloudFront, and Bedrock hosting are documented/simulated, not deployed.
- `proposal_scoring_service.py` is still an illustrative bid/no-bid scorer in Repo C.
- `pytest` is not installed in the active local Python and is not listed in `backend/requirements.txt`.
- The final 140-minute V9 MP4 has not been fully re-rendered because the previous long-video generator was not saved.

## Verified Commands

Run from canonical Repo C:

```bash
cd "/Users/adamsmith/Documents/Claude/Projects/BidIntel Bid Contract AI  Automation/bidintel/backend"
PYTHONPATH=. python3 scripts/test_guardrails_v9.py
PYTHONPATH=. python3 scripts/test_access_control.py
PYTHONPATH=. python3 scripts/sim_workflow.py
```

Run from the frontend:

```bash
cd "/Users/adamsmith/Documents/Claude/Projects/BidIntel Bid Contract AI  Automation/bidintel/frontend"
npm run build
```

Run from the repo root:

```bash
cd "/Users/adamsmith/Documents/Claude/Projects/BidIntel Bid Contract AI  Automation/bidintel"
PYTHONPATH=backend python3 -m compileall backend/app backend/scripts
```

## Correct V9 Claim

The V9 hardening package is built as verified render input over V8: repo patch,
chapter gate, guide update, proof commands, and delta proof video. The finished
V9 masterclass remains open. It should not be called built until a full improved
version exists that looks like V8's masterclass, but with the audited fixes
integrated chapter-by-chapter and verified with `ffprobe`, manifest, scroll
audit, transcript/SRT, and visual spot-checks.
