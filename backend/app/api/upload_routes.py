import os, tempfile, json
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Form
from ..database import get_conn
from ..services.pdf_loader import load_pdf
from ..services import store, audit_service, document_versioning_service
from ..services.tenant_service import normalize_tenant_id
from ..security.guardrails_service import evaluate_document_security
router = APIRouter()
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload(file: UploadFile = File(...), title: str = Form("Untitled"),
                 tenant_id: str = Form("demo"), access_groups: str = Form("[]")):
    tenant_id = normalize_tenant_id(tenant_id)
    groups = json.loads(access_groups) if access_groups else []
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        raw = await file.read(); tmp.write(raw); path = tmp.name
    pages = load_pdf(path)
    full_text = "\n".join(text for _, text in pages)
    document_security = evaluate_document_security(full_text)
    if document_security["decision"] == "REJECTED":
        with get_conn() as c, c.cursor() as cur:
            audit_service.log(cur, tenant_id, "system", "upload_rejected",
                              query=file.filename, guardrail="BLOCKED")
        return {
            "document_id": None,
            "chunks_inserted": 0,
            "embedded": False,
            "status": "rejected",
            "document_security": {k: v for k, v in document_security.items() if k != "safe_text"},
            "pipeline": ["loaded", "extracted", "security_scan", "rejected_before_storage"],
        }
    if document_security["decision"] == "ACCEPTED_WITH_REDACTIONS":
        pages = [(1, document_security["safe_text"])]
    doc_id = uuid4()
    with open(os.path.join(UPLOAD_DIR, str(doc_id) + '.pdf'), 'wb') as fh:
        fh.write(raw)
    with get_conn() as c, c.cursor() as cur:
        cur.execute("""INSERT INTO documents (id,tenant_id,title,filename,doc_type,access_groups,created_at)
                       VALUES (%s,%s,%s,%s,%s,%s, now())""",
                    (doc_id, tenant_id, title, file.filename, "RFP", groups))
        document_versioning_service.register_version(cur, doc_id, tenant_id, raw)
        inserted = store.ingest_pages(cur, doc_id, tenant_id, pages, groups)
        audit_service.log(cur, tenant_id, "system", "embed", query=file.filename,
                          guardrail=document_security["decision"])
    return {"document_id": str(doc_id), "chunks_inserted": inserted, "embedded": True,
            "status": "accepted",
            "document_security": {k: v for k, v in document_security.items() if k != "safe_text"},
            "pipeline": ["loaded", "extracted", "security_scan", "cleaned", "chunked", "embedded", "stored"]}
