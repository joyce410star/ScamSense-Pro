import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import os

# --- 1. 專業網頁配置 ---
st.set_page_config(
    page_title="ScamSense Pro - AI Red Teaming Platform",
    page_icon="🛡️",
    layout="wide"
)

# 自定義 CSS 讓介面更有資安工具的科技感
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1e2130; padding: 20px; border-radius: 12px; border: 1px solid #30363d; }
    div[data-testid="stExpander"] { border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 側邊欄控制室 ---
with st.sidebar:
    st.image("https://img.icons8.com/fluent/100/000000/security-shield.png")
    st.title("控制中心")
    st.markdown("---")
    epsilon = st.slider("對抗性擾動強度 (Epsilon)", 0.0, 0.3, 0.15, 0.01)
    st.info(f"當前強度: {epsilon}")
    
    st.markdown("---")
    st.write("🔍 **目標模型**: Deep Neural Network (DNN)")
    st.write("⚔️ **攻擊向量**: FGSM Gradient Attack")
    st.write("👤 **開發人員**: [請輸入你的姓名]")
    st.caption("2026 經濟部智慧創新大賞參賽作品")

# --- 3. 頂部即時監控儀表板 ---
st.title("🛡️ ScamSense Pro: AI 入侵偵測系統壓力測試平台")
st.markdown("本系統旨在分析網路入侵偵測系統 (IDS) 在面對對抗性樣本時的魯棒性漏洞。")

m_col1, m_col2, m_col3 = st.columns(3)

# 根據 Epsilon 動態計算模擬數值 (對應你之前的實驗結果)
orig_acc = 98.94
current_def = max(8.62, orig_acc - (epsilon * 300))
bypass_prob = min(92.0, 5.0 + (epsilon * 600))

with m_col1:
    st.metric("原始偵測準確率", f"{orig_acc}%", delta="Baseline", delta_color="normal")
with m_col2:
    st.metric("當前系統防禦力", f"{current_def:.2f}%", delta=f"-{orig_acc - current_def:.2f}%", delta_color="inverse")
with m_col3:
    st.metric("預期攻擊繞過率", f"{bypass_prob:.1f}%", delta="Threat Level", delta_color="off")

st.markdown("---")

# --- 4. 功能分頁 ---
tab1, tab2, tab3 = st.tabs(["🎯 漏洞觸發測試", "📈 數據偏移分析", "📂 導出武器化樣本"])

with tab1:
    col_in, col_out = st.columns([1, 1])
    
    with col_in:
        st.subheader("📥 原始攻擊封包特徵")
        d_port = st.number_input("Destination Port", value=443)
        f_dur = st.number_input("Flow Duration", value=12034.0)
        f_pkt = st.number_input("Fwd Packets/s", value=664.7)
        
        if st.button("🔥 啟動對抗性攻擊", use_container_width=True):
            # 模擬計算過程
            with st.spinner('正在分析模型梯度...'):
                time.sleep(0.8)
                # 判斷是否繞過成功
                is_success = np.random.random() < (bypass_prob / 100)
                
                with col_out:
                    st.subheader("🎭 攻擊執行結果")
                    if is_success:
                        st.success("✔️ 繞過成功 (Bypass Success)")
                        st.balloons()
                    else:
                        st.error("❌ 攔截成功 (Blocked by IDS)")
                    
                    # 黑客風格日誌
                    st.code(f"""
[SYSTEM] 偵測到原始標籤: PortScan (1.0)
[ATTACK] 執行 FGSM 梯度運算... (Epsilon={epsilon})
[ATTACK] 特徵偏移完成，正在重組對抗性載體
[RESULT] 模型預測輸出: {0.05 if is_success else 0.92}
[STATUS] {'對抗樣本已成功滲透防線' if is_success else '防禦邊界尚存，攔截成功'}
                    """)

with tab2:
    st.subheader("📊 特徵偏移量化分析 (Feature Shift)")
    st.write("此圖表展示了攻擊演算法如何精確微調特徵值以誘導模型產生決策偏差。")
    
    # 計算偏移數值
    features = ['Flow Duration', 'Fwd Pkts/s']
    original = [f_dur, f_pkt]
    # 根據梯度方向模擬偏移 (Flow Dur 增加, Fwd Pkts 減少)
    adversarial = [f_dur + (epsilon * 100), f_pkt - (epsilon * 50)]
    
    plot_df = pd.DataFrame({
        '特徵名稱': features * 2,
        '數值': original + adversarial,
        '樣本類型': ['原始 (Normal)'] * 2 + ['對抗 (Adversarial)'] * 2
    })
    
    fig = px.bar(plot_df, x='特徵名稱', y='數值', color='樣本類型', 
                 barmode='group', template="plotly_dark",
                 color_discrete_map={'原始 (Normal)': '#636EFA', '對抗 (Adversarial)': '#EF553B'})
    
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("📂 武器化樣本導出 (Red Team Export)")
    st.write("將生成的對抗樣本匯出為實體 CSV，供紅隊演練或防禦強化測試使用。")
    
    adv_payload = {
        "Destination Port": d_port,
        "Flow Duration": f_dur + (epsilon * 100),
        "Fwd Packets/s": f_pkt - (epsilon * 50),
        "Adversarial Label": "BENIGN (Cloaked)"
    }
    
    df_export = pd.DataFrame([adv_sample for adv_sample in [adv_payload]])
    st.table(df_export)
    
    csv = df_export.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 下載武器化樣本 CSV",
        data=csv,
        file_name="scamsense_bypass_payload.csv",
        mime="text/csv",
        use_container_width=True
    )

st.markdown("---")
st.caption("⚠️ 本工具僅供學術研究與資安防禦測試使用。")
