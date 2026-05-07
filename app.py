import streamlit as st
import pandas as pd
import random

# --- 1. ページ基本構成 ---
st.set_page_config(page_title="Ski Empire: Architect OS", layout="wide", initial_sidebar_state="expanded")

# --- 2. iPad最適化 & 3D・夜景描画スタイル ---
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    /* 3Dフィールドの土台 */
    .map-canvas {
        background: #ffffff;
        height: 650px;
        border: 5px solid #2c3e50;
        border-radius: 30px;
        position: relative;
        overflow: hidden;
        background-image: radial-gradient(#d1d1d1 1.5px, transparent 1.5px);
        background-size: 40px 40px; /* 配置用グリッド */
        box-shadow: inset 0 0 50px rgba(0,0,0,0.1);
    }
    /* 夜景モードへの切り替え */
    .night-mode {
        background: #0f172a !important;
        background-image: radial-gradient(#1e293b 1.5px, transparent 1.5px) !important;
        box-shadow: inset 0 0 100px rgba(0,0,0,0.5);
    }
    /* インフラ（道路） */
    .road-line {
        position: absolute;
        background: #475569;
        height: 12px;
        border-radius: 6px;
        z-index: 1;
        opacity: 0.8;
    }
    /* 建物・機材 */
    .building {
        position: absolute;
        z-index: 10;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .building-icon { font-size: 55px; cursor: pointer; }
    .building-label { font-size: 12px; font-weight: bold; color: #64748b; }
    .night-glow { text-shadow: 0 0 20px #fbbf24, 0 0 10px #f59e0b; }

    /* iPad用巨大ボタン */
    .stButton>button {
        width: 100%; height: 3.5em; border-radius: 15px; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. セッション状態（データ保持）の初期化 ---
if 'resort' not in st.session_state:
    st.session_state.resort = {
        "money": 30000, "fans": 100, "month": 12,
        "is_night": False, "selected_plan": "ニセコ・フリーズ",
        "buildings": [], # {'id': 0, 'icon': '🚠', 'name': 'リフト', 'x': 100, 'y': 200}
        "roads": [],     # {'x': 100, 'y': 200, 'w': 150, 'r': 45}
        "energy": 100, "security": 20
    }

r = st.session_state.resort

# --- 4. サイドバー：経営ダッシュボード ---
with st.sidebar:
    st.title("🦫 Boris Empire OS")
    st.metric("総資金", f"¥{r['money']}万", delta=f"知名度 {r['fans']}")
    st.write(f"📍 現在の拠点: **{r['selected_plan']}**")
    st.progress(r['energy'] / 100, text=f"⚡ 自給蓄電量: {r['energy']}%")
    
    st.divider()
    r['is_night'] = st.toggle("🌙 夜景・ライトアップモード", value=r['is_night'])
    
    if st.button("🗓️ 翌月へ進む（決算）"):
        r['month'] = r['month'] + 1 if r['month'] < 12 else 1
        # 収益ロジック（配置数やファン数に連動）
        r['money'] += (r['fans'] * 2) + (len(r['buildings']) * 100)
        st.rerun()

# --- 5. メインレイアウト ---
tab_build, tab_plan, tab_job, tab_eco = st.tabs(["🏗️ 3D配置・建設", "🗺️ 拠点プラン選択", "🕹️ 現場ダイブ", "🌱 農業・ECO"])

# TAB 1: 3D配置・建設
with tab_build:
    c_view, c_tool = st.columns([3, 1])
    
    with c_view:
        st.subheader("3Dフィールドプレビュー")
        night_class = "night-mode" if r['is_night'] else ""
        map_html = f'<div class="map-canvas {night_class}">'
        
        # 道路の描画
        for road in r['roads']:
            map_html += f'<div class="road-line" style="left:{road["x"]}px; top:{road["y"]}px; width:{road["w"]}px; transform:rotate({road["r"]}deg);"></div>'
        
        # 施設の描画
        for b in r['buildings']:
            glow = "night-glow" if r['is_night'] else ""
            map_html += f"""
            <div class="building" style="left:{b['x']}px; top:{b['y']}px;">
                <div class="building-icon {glow}">{b['icon']}</div>
                <div class="building-label">{b['name']}</div>
            </div>
            """
        map_html += '</div>'
        st.markdown(map_html, unsafe_allow_html=True)

    with c_tool:
        st.header("🧰 建設キット")
        item_type = st.selectbox("機材/施設", ["高速ゴンドラ", "ラグジュアリーホテル", "水力発電タービン", "AI監視カメラ塔", "専用バス停"])
        
        # iPadタッチ座標エミュレーション
        pos_x = st.slider("X（横方向）", 0, 800, 400)
        pos_y = st.slider("Y（縦方向）", 0, 600, 300)
        
        if st.button("🏗️ 配置を確定"):
            icons = {"高速ゴンドラ":"🚠", "ラグジュアリーホテル":"🏨", "水力発電タービン":"🌊", "AI監視カメラ塔":"📹", "専用バス停":"🚌"}
            costs = {"高速ゴンドラ":3000, "ラグジュアリーホテル":8000, "水力発電タービン":2000, "AI監視カメラ塔":1000, "専用バス停":500}
            
            if r['money'] >= costs[item_type]:
                r['money'] -= costs[item_type]
                r['buildings'].append({'icon': icons[item_type], 'name': item_type, 'x': pos_x, 'y': pos_y})
                st.success("配置完了！")
                st.rerun()
            else: st.error("資金不足です！")

        if st.button("🛣️ 道路を舗装（100万）"):
            r['roads'].append({'x': pos_x, 'y': pos_y, 'w': 150, 'r': random.randint(0, 360)})
            r['money'] -= 100
            st.rerun()

# TAB 2: 拠点プラン選択
with tab_plan:
    st.header("帝国拠点プラン選択（10選）")
    plans = {
        "ニセコ・フリーズ": "パウダー重視。インバウンド収益+50%",
        "軽井沢プリンス風": "平坦で配置しやすい。晴天率高。",
        "野沢温泉リゾート": "急斜面。温泉による宿泊単価UP。",
        "志賀高原メガマップ": "最大面積。インフラ整備が重要。",
        "苗場エンタメ": "イベント広場完備。テレビ中継率UP。",
        "白馬アルプス": "絶景。水力発電効率+30%。",
        "蔵王モンスター": "樹氷ライトアップボーナスあり。",
        "富良野ラベンダー": "春の農業収益+100%。",
        "八甲田バックカントリー": "未開の地。パトロール報酬+40%。",
        "琵琶湖バレイ": "湖畔アクセス。専用バス集客UP。"
    }
    selected = st.radio("プランを決定してください", list(plans.keys()))
    if st.button("この地で帝国を築く"):
        r['selected_plan'] = selected
        st.success(f"{selected} プランが適用されました！")

# TAB 3: 現場ダイブ（ジョブ体験）
with tab_job:
    st.header("🕹️ 配置施設へのダイブ・アクション")
    if r['buildings']:
        target = st.selectbox("入る施設を選択", [f"{b['name']} (X:{b['x']})" for b in r['buildings']])
        if st.button("一人称視点でアクション開始"):
            st.info("🚀 3Dビューへダイブ中... リフト操作/パトロール任務を開始します！")
            st.balloons()
    else: st.warning("施設を配置すると、そこへ入って仕事をすることができます。")

# TAB 4: 農業・ECO
with tab_eco:
    st.header("🌱 グリーンシーズン・エネルギー管理")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("農業収益")
        if 4 <= r['month'] <= 10:
            st.success("現在は春〜秋。農業が可能です！")
            if st.button("高原野菜を収穫"): r['money'] += 500; st.toast("500万獲得！")
        else: st.info("現在は冬期。雪室で貯蔵中。")
    with col2:
        st.subheader("自家発電ステータス")
        hydro_count = len([b for b in r['buildings'] if b['icon'] == '🌊'])
        st.write(f"稼働中の水力タービン: {hydro_count} 基")
        r['energy'] = min(100, r['energy'] + (hydro_count * 5))