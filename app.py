import streamlit as st
import pandas as pd
import random
import time

# --- ページ基本設定 ---
st.set_page_config(page_title="Ski Empire OS", layout="wide", initial_sidebar_state="expanded")

# --- iPad最適化・3DビジュアルCSS ---
st.markdown("""
<style>
    /* 全体フォントと背景 */
    .main { background-color: #f0f4f8; }
    
    /* 3D滑走ビューのシミュレーション */
    .ski-view {
        background: linear-gradient(180deg, #87CEEB 0%, #E0F7FA 50%, #FFFFFF 100%);
        height: 400px;
        border-radius: 30px;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        border: 5px solid #2c3e50;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    
    /* スピード感のエフェクト */
    .speed-line {
        position: absolute;
        background: rgba(255, 255, 255, 0.6);
        width: 2px;
        height: 100px;
        animation: speed-flow 0.2s linear infinite;
    }
    @keyframes speed-flow {
        from { transform: translateY(-400px); }
        to { transform: translateY(400px); }
    }

    /* スキー板のアニメーション */
    .ski-tips {
        width: 180px;
        margin-bottom: -20px;
        animation: shake 0.15s infinite;
    }
    @keyframes shake {
        0% { transform: rotate(0deg) translateY(0); }
        50% { transform: rotate(1deg) translateY(-5px); }
        100% { transform: rotate(-1deg) translateY(0); }
    }

    /* iPad用巨大ボタン */
    .stButton>button {
        width: 100%;
        height: 3.5em;
        border-radius: 15px;
        font-weight: bold;
        font-size: 18px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- セッション状態の初期化 ---
if 'resort' not in st.session_state:
    st.session_state.resort = {
        "money": 10000, "fans": 60, "month": 12, "day": 1,
        "energy": 80, "security": 15, "stock": 100,
        "assets": {"hotel": 0, "farm": 1, "battery": 1, "bus": 1, "lift": 2},
        "log": ["帝国が始動しました。"],
        "view_mode": "Normal" # Normal, Action, Drone
    }

r = st.session_state.resort

# --- サイドバー：経営スタッツ ---
with st.sidebar:
    st.title("🦫 Boris Command")
    st.image("https://img.icons8.com/color/144/beaver.png", width=100)
    st.metric("資産", f"¥{r['money']}万", delta=f"株価 {r['stock']}")
    st.write(f"📅 **{r['month']}月 {r['day']}日**")
    st.progress(r['energy'] / 100, text=f"⚡ 自給蓄電量: {r['energy']}%")
    
    st.divider()
    st.subheader("🛠️ 現場へ直行")
    job = st.selectbox("職種を選択", ["リフト運転士", "パトロール", "リフト技術員", "ホテルマネージャー"])
    if st.button("業務開始"):
        if job == "リフト運転士":
            st.success("安全に稼働中。顧客満足度アップ！")
            r['fans'] += 3
        elif job == "パトロール":
            if random.random() > 0.6:
                st.warning("🚨 泥棒を検挙しました！")
                r['money'] += 50
            else: st.write("異常なし！")

# --- メインコンテンツ ---

tab1, tab2, tab3, tab4, tab5 = st.tabs(["⛷️ 3D滑走", "🏨 建設/投資", "🌱 農業/ECO", "📺 メディア", "🚌 アクセス"])

# TAB 1: 3D ACTION VIEW
with tab1:
    st.subheader("LIVE ACTION PREVIEW")
    # 滑走画面の描画
    action_html = f"""
    <div class="ski-view">
        <div class="speed-line" style="left: 20%;"></div>
        <div class="speed-line" style="left: 50%; animation-delay: 0.1s;"></div>
        <div class="speed-line" style="left: 80%; animation-delay: 0.05s;"></div>
        <div style="position: absolute; top: 30px; font-size: 24px; color: #2c3e50; font-weight: bold;">
            {r['month']}月の雪質: パウダースノー ❄️
        </div>
        <img src="https://img.icons8.com/color/240/ski.png" class="ski-tips">
    </div>
    """
    st.markdown(action_html, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⬅️ Sharp Turn"): st.toast("エッジが効いています！")
    with c2:
        if st.button("🚀 Trick Jump"): 
            st.balloons()
            st.info("ボリス・スピン成功！知名度+10")
            r['fans'] += 10
    with c3:
        if st.button("➡️ Sharp Turn"): st.toast("雪飛沫が舞う！")

# TAB 2: HOTEL & CONSTRUCTION
with tab2:
    st.header("リゾート開発")
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        if st.button("🏨 ホテル建設 (¥5000万)"):
            if r['money'] >= 5000:
                r['money'] -= 5000; r['assets']['hotel'] += 1; st.rerun()
    with col_h2:
        if st.button("🚠 新型ゴンドラ (¥3000万)"):
            if r['money'] >= 3000:
                r['money'] -= 3000; r['assets']['lift'] += 1; st.rerun()

# TAB 3: AGRICULTURE & ENERGY
with tab3:
    st.header("サステナブル経営")
    is_spring = 4 <= r['month'] <= 10
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.subheader("春の農業部門")
        if is_spring:
            st.write("🥬 高原野菜が収穫時期です！")
            if st.button("野菜を出荷して利益確定"):
                r['money'] += 300; st.toast("300万の売上獲得！")
        else: st.info("現在は冬期。野菜は雪室で熟成中...")
    with col_e2:
        st.subheader("水力発電 & 蓄電池")
        st.write(f"現在の蓄電池数: {r['assets']['battery']}基")
        if st.button("メガ蓄電池を追加 (¥1000万)"):
            if r['money'] >= 1000:
                r['money'] -= 1000; r['assets']['battery'] += 1; st.rerun()

# TAB 4: MEDIA & STOCK
with tab4:
    st.header("テレビ局 & 株式")
    if r['fans'] > 100:
        st.success("📺 テレビ番組『絶景リゾート！』から中継が来ています！")
        if st.button("独占生中継を許可"):
            r['money'] += 1000; r['fans'] += 50
            st.balloons()
    else: st.write("知名度が上がるとメディアがやってきます。")
    
    if st.button("📈 株式市場にIPO（上場）する"):
        r['stock'] += 50; st.success("上場完了！巨額の資金調達が可能になりました。")

# TAB 5: BUS & PARKING
with tab5:
    st.header("アクセス・駐車場")
    st.write(f"運行中のシャトルバス: {r['assets']['bus']}台")
    if st.button("駅から直行バスを増便 (¥500万)"):
        if r['money'] >= 500:
            r['money'] -= 500; r['assets']['bus'] += 1; r['fans'] += 20; st.rerun()
    if st.button("駐車場ロードヒーティング導入 (¥300万)"):
        r['security'] += 5; st.write("冬のマイカー客が増加！")

# --- ターン進展システム ---
st.divider()
if st.button("⏭️ 翌月に進む（決算）"):
    r['month'] = r['month'] + 1 if r['month'] < 12 else 1
    
    # 収益ロジック
    income = (r['fans'] * 5) + (r['assets']['hotel'] * 200)
    # エネルギー節約ロジック
    electricity_cost = 500 - (r['assets']['battery'] * 50)
    r['money'] += (income - max(0, electricity_cost))
    
    # 治安イベント
    if random.randint(1, 100) > r['security']:
        st.error("🚨 犯罪発生！機材泥棒により損害が出ました。")
        r['money'] -= 100; r['fans'] -= 10
    
    st.rerun()