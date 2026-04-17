import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import os

# --- 1. 專業介面設定 ---
st.set_page_config(page_title="ScamSense Pro - AI Red Teaming Tool", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ScamSense Pro: AI 入侵偵測系統壓力測試平台")
st.sidebar.image("https://img.icons8.com/fluent/100/000000/security-shield.png")
st.sidebar.header("🕹️ 攻擊引擎控制室")
epsilon = st.sidebar.slider("擾動強度 (Perturbation Epsilon)", 0.0, 0.3, 0.15, 0.01)
st.sidebar.markdown("---")
st.sidebar.write("🎯 **目標系統**: DNN-based IDS")
st.sidebar.write("⚔️ **攻擊演算法**: FGSM (Fast Gradient Sign Method)")

# --- 2. 模擬核心邏輯 ---
def run_attack(eps):
    # 計算成功率 (根據你之前的實驗數據 0.15 為 80% 繞過)
    success_rate = min(92, 5 + (eps * 600)) 
    is_success = np.random.random() < (success_rate / 100)
    return is_success, success_rate

# --- 3. 頂部儀表板 ---
st.subheader("🚀 攻防即時監控")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric("原始偵測準確率", "98.94%", delta="Baseline", delta_color="normal")
with col_m2:
    current_acc = max(8.6, 98.9 - (epsilon * 300))
    st.metric("當前防禦能力", f"{current_acc:.2f}%", delta=f"-{98.9-current_acc:.1f}%", delta_color="inverse")
with col_m3:
    st.metric("攻擊繞過成功率", f"{min(92, 5 + (epsilon * 600)):.1f}%", delta="High Threat", delta_color="off")

# --- 4. 主操作區 ---
tabs = st.tabs(["🎯 漏洞觸發測試", "📈 數據偏移分析", "📄 導出武器化樣本"])

with tabs[0]:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.write("### 📥 輸入原始特徵")
        dst_port = st.number_input("Dest Port", value=443)
        flow_dur = st.number_input("Flow Duration", value=12034.0)
        fwd_s = st.number_input("Fwd Packets/s", value=664.7)
        if st.button("🔥 啟動對抗性攻擊", use_container_width=True):
            with st.spinner('正在計算梯度方向並注入擾動...'):
                time.sleep(1)
                is_success, _ = run_attack(epsilon)
                
                with c2:
                    st.write("### 🎭 攻擊執行結果")
                    if is_success:
                        st.success("✔️ 繞過成功 (Bypass Success)")
                        st.balloons()
                    else:
                        st.error("❌ 攔截成功 (Blocked by IDS)")
                    
                    # 模擬展示偏移
                    noise = epsilon * 10
                    st.code(f"""
[LOG] 正在對特徵向量進行 FGSM 運算...
[LOG] 方向: Positive Gradient Sign
[LOG] 原始標籤: PortScan (1.0)
[LOG] 擾動後預測值: {'0.02 (Normal)' if is_success else '0.94 (Attack)'}
[LOG] 狀態: {'攻擊載體偽裝完成' if is_success else '防禦邊界未突破'}
                    """)

with tabs[1]:
    st.subheader("📊 特徵偏移程度分析 (Feature Shift)")
    # 展示原始 vs 擾動後的長條圖
    features = ['Flow Dur', 'Fwd Pkts/s', 'Pkt Len Var']
    orig_vals = [12034, 664.7, 120]
    adv_vals = [12034 + epsilon*100, 664.7 - epsilon*50, 120 + epsilon*20]
    
    df_plot = pd.DataFrame({
        'Feature': features * 2,
        'Value': orig_vals + adv_vals,
        'Type': ['Original'] * 3 + ['Adversarial'] * 3
    })
    fig = px.bar(df_plot, x='Feature', y='Value', color='Type', barmode='group', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    st.write("此圖表展示了 FGSM 演算法如何微調每個特徵值以誘導模型產生判斷偏差。")

with tabs[2]:
    st.subheader("📄 下載專用於滲透測試的 CSV 樣本")
    st.write("你可以將此樣本餵給其他 Intrusion Detection 系統，測試其防禦極限。")
    sample_df = pd.DataFrame([{
        "Dest Port": dst_port,
        "Flow Duration": flow_dur + (epsilon*100),
        "Fwd Pkts/s": fwd_s - (epsilon*50),
        "Label": "PortScan (Adversarial)"
    }])
    st.dataframe(sample_df)
    csv = sample_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 匯出惡意 Payload CSV", data=csv, file_name="attack_payload.csv", mime="text/csv")
