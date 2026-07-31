from fastapi import APIRouter, Depends, status
from app.services.model_trainer import load_active_model, train_and_benchmark_models

router = APIRouter(prefix="/model", tags=["ML Model Management"])

@router.get("/status")
def get_model_status():
    """Get active ML model metadata, benchmark metrics, and features."""
    model, meta = load_active_model()
    return {
        "status": "online",
        "active_model": meta.get("active_model", "Random Forest"),
        "f1_score": meta.get("f1_score", 0.0),
        "feature_count": len(meta.get("feature_names", [])),
        "feature_names": meta.get("feature_names", []),
        "benchmark_results": meta.get("benchmark_results", {})
    }

@router.post("/retrain", status_code=status.HTTP_200_OK)
def retrain_model_endpoint():
    """Trigger automated model training, evaluation, and selection pipeline."""
    result = train_and_benchmark_models()
    return {
        "message": "Model retraining completed successfully",
        "details": result
    }
