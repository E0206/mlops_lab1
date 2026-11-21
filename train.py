
import mlflow
import mlflow.sklearn
import joblib

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. 載入 Iris 資料集
iris = load_iris()
X, y = iris.data, iris.target

# 2. 分割訓練集與測試集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. 設定 MLflow 實驗名稱
mlflow.set_experiment("iris-classification")

# 4. 開始記錄一次 MLflow Run
with mlflow.start_run():

    # 建立並訓練模型
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
    model.fit(X_train, y_train)

    # 評估模型
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    # 記錄超參數與準確率
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", accuracy)

    # 記錄模型
    mlflow.sklearn.log_model(
    	sk_model=model,
    	name="iris-model",
    	serialization_format="skops",
    	skops_trusted_types=["sklearn.tree._tree.Tree"]
	)

    # 儲存模型，讓後續 FastAPI 使用
    joblib.dump(model, "model.joblib")

    print(f"Model accuracy: {accuracy:.4f}")
    print("Model saved as model.joblib")
