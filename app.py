
from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib

# 建立 FastAPI 應用程式
app = FastAPI(title="Iris Prediction API")

# 載入 Step 2 訓練好的模型
model = joblib.load("model.joblib")


# 定義 API 接收的資料格式
class Req(BaseModel):
    instances: list[list[float]] = Field(min_length=1)


# 模型預測 API
@app.post("/predict")
def predict(req: Req):
    # Iris 每筆資料有四個特徵
    if any(len(instance) != 4 for instance in req.instances):
        from fastapi import HTTPException
        raise HTTPException(
            status_code=422,
            detail="Each instance must contain exactly 4 features."
        )

    predictions = model.predict(req.instances)

    return {
        "predictions": predictions.tolist()
    }


# Kubernetes 健康檢查 API
@app.get("/healthz")
def healthz():
    return {"ok": True}
