"""Baseline ML: Logistic Regression dự báo dự án trễ hạn (chia train/test theo thời gian)."""
import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, average_precision_score, confusion_matrix,
                             f1_score, recall_score, roc_auc_score)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CAT = ["loai_san_pham", "the_loai"]
NUM = ["bpm", "so_track", "so_vst", "do_phuc_tap_brief", "khach_hang_moi",
       "co_bai_tham_khao", "so_ngay_deadline"]
FEATURES = CAT + NUM  # KHÔNG gồm so_vong_chinh_sua / so_ngay_tre (chỉ biết sau khi xong -> rò rỉ)
TARGET = "tre_han"
SEED = 42
TEST_RATIO = 0.2


def build_pipeline() -> Pipeline:
    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT),
        ("num", StandardScaler(), NUM),
    ])
    clf = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=SEED)
    return Pipeline([("pre", pre), ("clf", clf)])


def time_split(df: pd.DataFrame):
    df = df.sort_values("ngay_nhan_brief").reset_index(drop=True)
    n_train = int(len(df) * (1 - TEST_RATIO))
    return df.iloc[:n_train], df.iloc[n_train:]


@st.cache_resource
def train(df: pd.DataFrame) -> dict:
    train_df, test_df = time_split(df)
    model = build_pipeline().fit(train_df[FEATURES], train_df[TARGET])
    proba = model.predict_proba(test_df[FEATURES])[:, 1]
    pred = (proba >= 0.5).astype(int)
    y = test_df[TARGET]
    majority = int(train_df[TARGET].mode()[0])
    metrics = {
        "Accuracy": accuracy_score(y, pred),
        "F1": f1_score(y, pred, zero_division=0),
        "Recall (bắt được dự án trễ)": recall_score(y, pred, zero_division=0),
        "AUC": roc_auc_score(y, proba),
        "PR-AUC": average_precision_score(y, proba),
    }
    names = model.named_steps["pre"].get_feature_names_out()
    coefs = pd.DataFrame({"đặc trưng": names, "hệ số": model.named_steps["clf"].coef_[0]})
    coefs = coefs.reindex(coefs["hệ số"].abs().sort_values(ascending=False).index)
    return {
        "model": model,
        "metrics": metrics,
        "confusion": confusion_matrix(y, pred),
        "baseline_accuracy": float((y == majority).mean()),  # luôn đoán lớp đa số
        "n_train": len(train_df),
        "n_test": len(test_df),
        "test_from": str(test_df["ngay_nhan_brief"].min().date()),
        "coefs": coefs,
    }


def predict_proba(model: Pipeline, row: dict) -> float:
    return float(model.predict_proba(pd.DataFrame([row])[FEATURES])[0, 1])
