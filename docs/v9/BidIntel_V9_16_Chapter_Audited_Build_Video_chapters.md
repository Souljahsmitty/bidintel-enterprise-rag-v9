# BidIntel V9 16-Chapter Audited Build Video Chapters

## 1. 1. Product Map And Truth Boundary

- Start: 00:00
- Goal: Define BidIntel, RAG, response scoring, bid/no-bid scoring, and real-vs-simulated lanes.
- Proof: Learner can point to REAL LOCAL, LOCAL MOCK, SIMULATED CLOUD, FUTURE PRODUCTION.

## 2. 2. Install And Verify Tools

- Start: 00:18
- Goal: Prove Git, Python, Node, npm, Docker, and Compose are available before cloning.
- Proof: Every command prints a version; Docker Desktop is running before Docker commands.

## 3. 3. Clone V9 And Read The Repo

- Start: 00:36
- Goal: Start from the same standalone V9 repo a reviewer can clone.
- Proof: Repo contains backend, frontend, docker-compose.yml, README.md, docs/v9.

## 4. 4. Local Security Proof Before Docker

- Start: 00:54
- Goal: Run cheap proof scripts before the full stack.
- Proof: BLOCKED, REJECTED, ACCEPTED_WITH_REDACTIONS, and RBAC True outputs appear.

## 5. 5. Compile Backend And Build Frontend

- Start: 01:12
- Goal: Catch syntax/build failures before runtime.
- Proof: compileall exits 0; Vite build says modules transformed.

## 6. 6. Docker, Postgres, And Migrations

- Start: 01:30
- Goal: Run the local full stack and apply schema/migrations.
- Proof: Frontend, Swagger, and health URLs are printed; health returns db connected.

## 7. 7. Upload Documents Safely

- Start: 01:48
- Goal: Teach file upload as hostile input before chunk/embed/store.
- Proof: Frontend shows document_security decision; malicious uploads reject before chunks.

## 8. 8. Ask RAG Question And Show Evidence

- Start: 02:06
- Goal: Follow one question from frontend click to backend answer/citations.
- Proof: Response contains answer, citations, evidence, eval, and answer_source.

## 9. 9. Hybrid Retrieval Internals

- Start: 02:24
- Goal: Show BM25, vector search, RRF, rerank, context, citations, evaluation.
- Proof: Sim workflow reaches DONE and prints retrieval stages.

## 10. 10. Cache Proof

- Start: 02:42
- Goal: Show first ask vs repeated ask, and why guardrails run before cache.
- Proof: Repeated ask shows cache metadata or none-cache-hit when stack is warm.

## 11. 11. Prompt Injection Defense

- Start: 03:00
- Goal: Prove hostile prompt blocks before cache/retrieval.
- Proof: answer_source=blocked_by_guardrail, model=none-guardrail-block, cache=skipped.

## 12. 12. Bid / No-Bid Scorecard

- Start: 03:18
- Goal: Separate opportunity scoring from answer-quality scoring.
- Proof: Frontend shows score, recommendation, factors; scorer is labeled simplified.

## 13. 13. Dashboard, Audit Logs, And Admin Surfaces

- Start: 03:36
- Goal: Show operations pages and route wiring.
- Proof: Dashboard, audit table, and Swagger route list load.

## 14. 14. AWS IAM And Bedrock Guardrails Simulation

- Start: 03:54
- Goal: Teach local simulation now and live AWS path later.
- Proof: Local sim passes; paid/live AWS remains future until Adam logs in and approves.

## 15. 15. AWS Hosting Path

- Start: 04:12
- Goal: Map local Docker to ECR/ECS/Fargate/RDS/S3/CloudFront/Secrets.
- Proof: Learner can map local containers to AWS services; no live AWS claim until tested.

## 16. 16. Final Proof And Handoff

- Start: 04:30
- Goal: Run final proof commands and label what is complete vs handoff.
- Proof: All lightweight checks pass; Docker/AWS live proof is handoff if not run now.

