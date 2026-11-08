import os
import shutil
import tempfile

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles

from shadowsaas.catalog.loader import load_catalog
from shadowsaas.detection.shadow_ai import find_ai_usage
from shadowsaas.engine.risk_engine import assess
from shadowsaas.ingestion.csv_loader import load_events
from shadowsaas.ingestion.hennge_adapter import load_hennge_events
from shadowsaas.detection.iam_streaming import analyze_iam_csv
from shadowsaas.reporting.report_generator import format_report

app = FastAPI(
    title="ShadowSaaS Radar API",
    description="Identity-based Shadow AI and IAM behavioral analysis",
    version="1.0.0",
)


MAX_UPLOAD_BYTES = 10 * 1024 * 1024

def save_upload(upload):
    filename = upload.filename or "data.csv"
    if not filename.lower().endswith(".csv"):
        raise HTTPException(415, "Only CSV files are accepted")

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    path = temp.name

    try:
        total = 0
        while True:
            chunk = upload.file.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_UPLOAD_BYTES:
                raise HTTPException(413, "CSV file exceeds 10 MB limit")
            temp.write(chunk)

        if total == 0:
            raise HTTPException(400, "CSV file is empty")

        return path
    except Exception:
        if os.path.exists(path):
            os.unlink(path)
        raise
    finally:
        temp.close()


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "application": "ShadowSaaS Radar",
        "version": "1.0.0",
    }


@app.post("/api/analyze/shadow-ai")
async def analyze_shadow_ai(
    file: UploadFile = File(...),
    source: str = Form("generic"),
    approved: str = Form(""),
):
    if source not in ("generic", "hennge"):
        raise HTTPException(400, "Source must be generic or hennge")

    path = save_upload(file)
    try:
        events = (
            load_hennge_events(path)
            if source == "hennge"
            else load_events(path)
        )

        apps = load_catalog()
        usages = find_ai_usage(events, apps)
        approved_apps = frozenset(
            item.strip().lower()
            for item in approved.split(",")
            if item.strip()
        )
        results = assess(usages, approved_apps)

        return jsonable_encoder({
            "source": source,
            "events_loaded": len(events),
            "ai_usages_detected": len(usages),
            "results_count": len(results),
            "results": results,
            "report": format_report(results),
            "limitation": (
                "Authentication events do not prove file uploads, "
                "data transfers, or data leakage."
            ),
        })
    except Exception as exc:
        raise HTTPException(400, str(exc))
    finally:
        os.unlink(path)


@app.post("/api/analyze/iam")
async def analyze_iam(file: UploadFile = File(...)):
    path = save_upload(file)
    try:
        result = analyze_iam_csv(path)
        return jsonable_encoder({
            "analysis": result,
            "dataset_note": (
                "IAM behavioral data; this dataset does not establish "
                "AI application usage."
            ),
        })
    except Exception as exc:
        raise HTTPException(400, str(exc))
    finally:
        os.unlink(path)


# Serve the React production build from the same FastAPI port.
FRONTEND_DIST = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "frontend",
    "dist",
)

if os.path.isdir(FRONTEND_DIST):
    app.mount(
        "/",
        StaticFiles(directory=FRONTEND_DIST, html=True),
        name="frontend",
    )
