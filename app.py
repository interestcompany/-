import streamlit as st
import pandas as pd
import random
import time

# --- ページ基本設定 ---
st.set_page_config(page_title="Ski Resort Empire: Ultimate", layout="wide")

# --- セッション状態の初期化（全ステータス管理） ---
if 'data' not in st.session_state:
    st.session_state.data = {
        "money": 50000, "fans": 50, "year": 1, "month": 11,
        "energy": 100, "security": 10, "stock_price": 100,
        "assets": {"リフト": 1, "人工降雪機": 1, "ホテル": 0, "農園": 0, "蓄電池": 0},
        "courses": {"ボリス・スロープ": 15},
        "logs": ["リゾート経営を開始しました！"]
    }

d = st.session_state.data

# --- サイドバー：経営ダッシュボード ---
with st.sidebar:
    st.title("🦫 帝国指令室")
    st.metric("総資金", f"{d['money']} 万円", delta=f"株価: ¥{d['stock_price']}")
    st.progress(d['energy'] / 100, text=f"蓄電量: {d['energy']}%")
    st.write(f"🛡️ 防犯レベル: {d['security']}")
    
    st.divider()
    st.subheader("🚀 現場ジョブに出動")
    job = st.selectbox("体験する職種", ["リフト運転士", "パトロール", "雪職人", "電力マネージャー"])
    if st.button("ジョブ開始"):
        # ジョブロジック
        if job == "リフト運転士":
            st.info("🎡 吹雪発生！速度を50%に落として安全を確保しました。")
            d['fans'] += 5
        elif job == "パトロール":
            if random.random() > 0.5:
                st.success("👮 板の泥棒を確保！報酬100万。")
                d['money'] += 100
            else:
                st.error("⚠️ 犯人に逃げられました...知名度低下。")
                d['fans'] -= 10

# --- メイン画面構成 ---
tab1, tab2, tab3, tab4 = st.tabs(["🏗️ 建設・投資", "🎿 滑走プレビュー", "🌱 農業・エコ", "📈 経済・メディア"])

# TAB 1: 建設と投資
with tab1:
    st.header("設備投資・インフラ整備")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚠 最新高速ゴンドラ建設 (5000万)"):
            if d['money'] >= 5000: d['money'] -= 5000; d['assets']['リフト'] += 1; st.rerun()
        if st.button("🏨 ラグジュアリーホテル建設 (15000万)"):
            if d['money'] >= 15000: d['money'] -= 15000; d['assets']['ホテル'] += 1; st.rerun()
    with col2:
        if st.button("🚌 専用シャトルバス運行 (1000万)"):
            if d['money'] >= 1000: d['money'] -= 1000; d['fans'] += 30; st.rerun()
        if st.button("🛡️ AI監視ドローン導入 (500万)"):
            if d['money'] >= 500: d['money'] -= 500; d['security'] += 20; st.rerun()

# TAB 2: 滑走プレビュー
with tab2:
    st.header("コース・プレビュー")
    c_name = st.text_input("新コース名入力", "デビル・フォール")
    if st.button(f"{c_name} をテスト滑走"):
        with st.status("滑走中...", expanded=True):
            st.write("⛷️ パウダーを切り裂いています...")
            time.sleep(1)
            st.write("🌟 360ジャンプ成功！")
            time.sleep(1)
            st.success("🏁 ゴール！最高の雪質です。")

# TAB 3: 農業・エコ
with tab3:
    st.header("グリーンシーズン農業 & 自家発電")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("春の農業")
        if 4 <= d['month'] <= 10:
            st.write("🌱 現在、高原レタスが成長中...")
            if st.button("収穫して出荷"):
                d['money'] += 500; st.toast("500万円の売上！")
        else:
            st.write("❄️ 現在は冬期につき農園は休止中（雪下貯蔵中）")
    with col_b:
        st.subheader("エネルギー管理")
        st.write("🌊 水力発電：稼働中")
        if st.button("蓄電池を増設 (3000万)"):
            if d['money'] >= 3000: d['money'] -= 3000; d['assets']['蓄電池'] += 1; st.rerun()

# TAB 4: 経済・メディア
with tab4:
    st.header("メディア戦略・株式")
    if d['fans'] > 100:
        st.write("📺 **テレビ中継のオファーが来ています！**")
        if st.button("生中継を許可"):
            reward = d['fans'] * 10
            d['money'] += reward
            st.balloons()
            st.success(f"全国放送されました！報酬 {reward} 万円獲得！")
    
    if st.button("他プレイヤーのリゾートを視察"):
        st.info("✈️ ニセコ・オンライン・リゾートへ移動中...（マルチプレイ接続中）")

# --- ターン経過処理 ---
st.divider()
if st.button("🗓️ 翌月へ進む"):
    d['month'] = d['month'] + 1 if d['month'] < 12 else 1
    if d['month'] == 1: d['year'] += 1
    
    # 自動収益・維持費計算
    profit = (d['fans'] * 10) + (d['assets']['ホテル'] * 500)
    cost = (d['assets']['リフト'] * 100) - (d['assets']['蓄電池'] * 50)
    d['money'] += (profit - cost)
    
    # 犯罪イベント
    if random.randint(1, 100) > d['security']:
        crime_loss = random.randint(50, 200)
        d['money'] -= crime_loss
        d['fans'] -= 10
        st.error(f"🚨 事件発生！盗難により {crime_loss} 万の損害。知名度が低下しました。")
    
    st.rerun()