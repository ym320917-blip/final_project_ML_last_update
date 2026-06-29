import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Olist E-Commerce Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*, *::before, *::after { box-sizing: border-box; font-family: 'Inter', sans-serif; }

/* ── HEADER ── */
.olist-header {
    background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 55%, #43A047 100%);
    padding: 1.6rem 2rem; border-radius: 14px; margin-bottom: 1.2rem; color: white;
}
.olist-header h1 { margin:0; font-size:1.75rem; font-weight:800; letter-spacing:-.02em; }
.olist-header p  { margin:0.3rem 0 0; font-size:0.85rem; opacity:0.85; }

/* ── KPI ── */
.kpi { background:white; border:1px solid #E8F5E9; border-radius:10px;
       padding:.9rem 1rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,.06); }
.kpi .v { font-size:1.55rem; font-weight:800; color:#1B5E20; }
.kpi .l { font-size:0.68rem; color:#999; margin-top:2px; text-transform:uppercase; letter-spacing:.06em; }

/* ── RESULT BOXES ── */
.rbox { border-radius:12px; padding:1.8rem 1rem; text-align:center; margin-top:.5rem; }
.rbox-good { background:#E8F5E9; border:2px solid #43A047; }
.rbox-bad  { background:#FFEBEE; border:2px solid #E53935; }
.rbox .big { font-size:3.2rem; font-weight:800; line-height:1; }
.rbox .lbl { font-size:1.2rem; font-weight:700; margin-top:.5rem; }
.rbox .sub { font-size:.82rem; margin-top:.3rem; opacity:.75; }
.c-good { color:#2E7D32; } .c-bad { color:#C62828; }

/* ── PROB BARS ── */
.prob-row { display:flex; align-items:center; gap:10px; margin:5px 0; font-size:.83rem; }
.prob-label { min-width:105px; font-weight:500; }
.prob-bar-bg { flex:1; background:#F5F5F5; border-radius:20px; height:18px; overflow:hidden; }
.prob-bar-good { height:100%; border-radius:20px; background:#43A047; }
.prob-bar-bad  { height:100%; border-radius:20px; background:#E53935; }
.prob-pct { min-width:40px; text-align:right; font-weight:700; color:#333; }

.sec { font-size:.68rem; font-weight:600; text-transform:uppercase; letter-spacing:.07em;
       color:#aaa; border-bottom:1px solid #eee; padding-bottom:4px; margin:1rem 0 .6rem; }

.tip     { background:#F1F8E9; border-left:4px solid #43A047; border-radius:0 8px 8px 0;
           padding:.65rem 1rem; font-size:.8rem; color:#1B5E20; margin-top:.8rem; }
.tip-bad { background:#FFF3E0; border-left:4px solid #E53935; border-radius:0 8px 8px 0;
           padding:.65rem 1rem; font-size:.8rem; color:#B71C1C; margin-top:.8rem; }

div[data-testid="stButton"] > button {
    background:#2E7D32 !important; color:white !important; border:none !important;
    border-radius:8px !important; padding:.6rem 0 !important;
    font-size:.9rem !important; font-weight:600 !important; width:100% !important;
}
div[data-testid="stButton"] > button:hover { background:#1B5E20 !important; }

.empty-state { background:#F9FBF9; border:2px dashed #A5D6A7; border-radius:12px;
               padding:2.5rem 1rem; text-align:center; color:#999; }
.arch-card { background:white; border:1px solid #E8F5E9; border-radius:10px; padding:1rem 1.2rem; }
.arch-card h4 { margin:0 0 .7rem; color:#2E7D32; font-size:.85rem; font-weight:700; }
.arch-card li { font-size:.79rem; color:#444; margin:.22rem 0; }

/* ── ANALYSIS TAB ── */
.section-banner {
    background: linear-gradient(90deg, #E8F5E9, #F1F8E9);
    border-left: 4px solid #2E7D32;
    border-radius: 0 8px 8px 0;
    padding: 10px 16px;
    margin: 1.4rem 0 1rem;
}
.section-banner-title { font-size:.8rem; font-weight:700; text-transform:uppercase;
                         letter-spacing:.07em; color:#1B5E20; }

.plot-card {
    background: white; border: 1px solid #E8F5E9; border-radius: 12px;
    padding: 1.1rem 1.3rem; margin-bottom: 1rem;
    box-shadow: 0 1px 6px rgba(0,0,0,.05);
}
.plot-header { display:flex; align-items:center; gap:10px; margin-bottom:.7rem;
               padding-bottom:.7rem; border-bottom:1px solid #F5F5F5; }
.plot-num { background:#1B5E20; color:white; font-size:.75rem; font-weight:800;
            width:26px; height:26px; border-radius:6px;
            display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.plot-title { font-size:.92rem; font-weight:700; color:#111; flex:1; }
.plot-badge { background:#E8F5E9; color:#1B5E20; font-size:.65rem; font-weight:700;
              padding:2px 8px; border-radius:4px; white-space:nowrap; }
.badge-must { background:#FFEBEE; color:#C62828; }
.badge-high { background:#FFF8E1; color:#E65100; }
.badge-new  { background:#E3F2FD; color:#1565C0; }

.meta-grid { display:grid; grid-template-columns:1fr 1fr; gap:7px; margin-bottom:.7rem; }
.meta-box { background:#FAFAFA; border-radius:7px; padding:7px 9px; }
.meta-lbl { font-size:.62rem; font-weight:700; text-transform:uppercase;
             letter-spacing:.06em; color:#bbb; margin-bottom:2px; }
.meta-txt { font-size:.76rem; color:#444; line-height:1.55; }

.insight-box { background:#F1F8E9; border-left:3px solid #2E7D32;
               border-radius:0 7px 7px 0; padding:8px 11px; margin-bottom:.6rem; }
.insight-lbl { font-size:.62rem; font-weight:700; text-transform:uppercase;
               letter-spacing:.06em; color:#2E7D32; margin-bottom:3px; }
.insight-txt { font-size:.78rem; color:#1a1a1a; line-height:1.6; }

.rec-lbl { font-size:.65rem; font-weight:700; text-transform:uppercase;
           letter-spacing:.06em; color:#2E7D32; margin-bottom:3px; }
</style>
""", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    path = "best olist model"
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

model = load_model()

# ── Load data (optional – needed for live plots) ──────────────────────────────
@st.cache_data
def load_data():
    for p in ["olist_analytical_dataset.csv", "df.csv", "data.csv", "dataset.csv"]:
        if os.path.exists(p):
            return pd.read_csv(p)
    return None

df = load_data()

# ── Constants ─────────────────────────────────────────────────────────────────
ORDER_STATUS    = ['delivered', 'shipped', 'processing', 'canceled']
PAYMENT_TYPES   = ['credit_card', 'boleto', 'voucher', 'debit_card']
CATEGORIES      = sorted([
    'housewares','perfumery','auto','pet_shop','stationery','furniture_decor',
    'office_furniture','garden_tools','computers_accessories','bed_bath_table',
    'toys','telephony','health_beauty','electronics','baby','cool_stuff',
    'watches_gifts','air_conditioning','sports_leisure','books_general_interest',
    'construction_tools_construction','small_appliances','food',
    'luggage_accessories','fashion_underwear_beach','christmas_supplies',
    'fashion_bags_accessories','musical_instruments','construction_tools_lights',
    'books_technical','costruction_tools_garden','home_appliances','market_place',
    'agro_industry_and_commerce','party_supplies','home_confort',
    'cds_dvds_musicals','industry_commerce_and_business','consoles_games',
    'furniture_bedroom','construction_tools_safety','fixed_telephony','drinks',
    'kitchen_dining_laundry_garden_furniture','fashion_shoes','home_construction',
    'audio','home_appliances_2','fashion_male_clothing','cine_photo',
    'furniture_living_room','art','food_drink','tablets_printing_image',
    'fashion_sport','la_cuisine','flowers','computers','home_comfort_2',
    'small_appliances_home_oven_and_coffee','dvds_blu_ray','costruction_tools_tools',
    'fashio_female_clothing','furniture_mattress_and_upholstery',
    'signaling_and_security','diapers_and_hygiene','books_imported',
    'fashion_childrens_clothes','music','arts_and_craftmanship','security_and_services'
])
CUSTOMER_TYPES   = ['loyal', 'new', 'regular']
SHIPPING_SPEEDS  = ['fast shipping', 'regular shipping', 'bad shipping', 'soo bad shipping']
OPERATION_SPEEDS = ['perfect operation', 'regular operation', 'bad operation', 'soo bad operation']
EXPECTATIONS     = ['perfect expectation', 'bad expectation']
SELLER_LEVELS    = ['good seller', 'bad seller']
MONTHS           = ['January','February','March','April','May','June',
                    'July','August','September','October','November','December']

color_map = {'good review':'#2ECC71','bad review':'#E74C3C','regular':'#F39C12'}

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="olist-header">
  <h1>🛒 Olist E-Commerce Intelligence Dashboard</h1>
  <p>Brazilian E-Commerce · XGBoost + SMOTE · Review Predictor + Business Analysis · 115K Orders</p>
</div>
""", unsafe_allow_html=True)

if model is None:
    st.warning("⚠️ Model file **`best olist model`** not found. Place it next to `app5.py` and restart.")

# ── KPIs ─────────────────────────────────────────────────────────────────────
c1,c2,c3,c4,c5,c6 = st.columns(6)
kpis = [("87.4%","Test Accuracy"),("91.9%","Train Accuracy"),("XGBoost","Algorithm"),
        ("2 Classes","Good / Bad"),("115K","Training Rows"),("20","Features")]
for col,(v,l) in zip([c1,c2,c3,c4,c5,c6],kpis):
    col.markdown(f'<div class="kpi"><div class="v">{v}</div><div class="l">{l}</div></div>',
                 unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🔮  Review Predictor", "📊  Business Analysis & Plots", "💡  Insights & Recommendations", "📖  Project Overview"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ML PREDICTOR
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("#### Order Details")

    r1c1,r1c2,r1c3,r1c4 = st.columns(4)
    with r1c1:
        st.markdown('<p class="sec">📦 Order</p>', unsafe_allow_html=True)
        order_status         = st.selectbox("Order status", ORDER_STATUS)
        order_item_id        = st.number_input("Number of items", 1, 21, 1)
        order_purchase_month = st.selectbox("Purchase month", MONTHS)
        order_purchase_year  = st.selectbox("Purchase year", [2016,2017,2018])

    with r1c2:
        st.markdown('<p class="sec">💳 Price & Payment</p>', unsafe_allow_html=True)
        price                = st.number_input("Item price (R$)", 0.01, 7000.0, 120.0, 10.0)
        freight_value        = st.number_input("Freight (R$)", 0.0, 400.0, 18.0, 1.0)
        payment_type         = st.selectbox("Payment type", PAYMENT_TYPES)
        payment_installments = st.slider("Installments", 0, 24, 1)
        payment_sequential   = st.number_input("Payment sequential", 1, 29, 1)
        payment_value        = st.number_input("Payment value (R$)", 0.0, 14000.0,
                                               round(120.0+18.0,2), 5.0)

    with r1c3:
        st.markdown('<p class="sec">📦 Product</p>', unsafe_allow_html=True)
        product_category  = st.selectbox("Category", CATEGORIES)
        product_weight_g  = st.number_input("Weight (g)", 0.0, 40000.0, 500.0, 50.0)
        product_height_cm = st.number_input("Height (cm)", 0.0, 105.0, 15.0, 1.0)
        product_width_cm  = st.number_input("Width (cm)", 0.0, 105.0, 15.0, 1.0)

    with r1c4:
        st.markdown('<p class="sec">🚚 Delivery & Seller</p>', unsafe_allow_html=True)
        customer_type      = st.selectbox("Customer type", CUSTOMER_TYPES)
        shipping_speed     = st.selectbox("Shipping speed", SHIPPING_SPEEDS)
        operation_speed    = st.selectbox("Operation speed", OPERATION_SPEEDS)
        actual_expectation = st.selectbox("Actual vs expectation", EXPECTATIONS)
        seller_level       = st.selectbox("Seller level", SELLER_LEVELS)
        distance           = st.slider("Distance (km)", 0.0, 4500.0, 300.0, 10.0)

    st.markdown("<br>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([3,2,3])
    with btn_col:
        predict_btn = st.button("🔮 Predict Review Outcome")

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([1,1], gap="large")

    with left:
        st.markdown("##### 📋 Input Summary")
        summary = pd.DataFrame({
            "Field": ["Order Status","Items","Purchase","Price","Freight",
                      "Payment Type","Installments","Payment Value","Category",
                      "Weight","Dimensions","Customer Type","Shipping Speed",
                      "Operation Speed","Expectation","Seller Level","Distance"],
            "Value": [order_status, order_item_id,
                      f"{order_purchase_month} {order_purchase_year}",
                      f"R$ {price:,.2f}", f"R$ {freight_value:,.2f}",
                      payment_type, payment_installments, f"R$ {payment_value:,.2f}",
                      product_category, f"{product_weight_g:,.0f} g",
                      f"{product_height_cm:.0f} × {product_width_cm:.0f} cm",
                      customer_type, shipping_speed, operation_speed,
                      actual_expectation, seller_level, f"{distance:,.0f} km"]
        })
        st.dataframe(summary, use_container_width=True, hide_index=True, height=600)

    with right:
        st.markdown("##### 🎯 Prediction Result")
        if predict_btn:
            if model is None:
                st.error("Model not loaded.")
            else:
                input_df = pd.DataFrame([{
                    "order status": order_status,
                    "order item id": order_item_id,
                    "price": price,
                    "freight value": freight_value,
                    "payment sequential": payment_sequential,
                    "payment type": payment_type,
                    "payment installments": payment_installments,
                    "payment value": payment_value,
                    "product weight g": product_weight_g,
                    "product height cm": product_height_cm,
                    "product width cm": product_width_cm,
                    "product category name english": product_category,
                    "customer type": customer_type,
                    "shipping speed": shipping_speed,
                    "operation speed": operation_speed,
                    "actuall expectation": actual_expectation,
                    "seller level": seller_level,
                    "distance between customer and seller": distance,
                    "order purchase month": order_purchase_month,
                    "order purchase year": order_purchase_year,
                }])
                try:
                    raw_pred   = model.predict(input_df)[0]
                    proba      = [float(p) for p in model.predict_proba(input_df)[0]]
                    classes    = [str(c) for c in model.classes_]
                    pred_label = str(raw_pred).strip().lower()
                    is_good    = "good" in pred_label

                    if is_good:
                        box_cls,color,emoji,label,meaning = (
                            "rbox-good","c-good","✅","Good Review","Customer is likely satisfied (score 4–5)")
                    else:
                        box_cls,color,emoji,label,meaning = (
                            "rbox-bad","c-bad","❌","Bad Review","Customer is likely unsatisfied (score 1–3)")

                    st.markdown(f"""
                    <div class="rbox {box_cls}">
                      <div class="big {color}">{emoji}</div>
                      <div class="lbl {color}">{label}</div>
                      <div class="sub">{meaning}</div>
                    </div>""", unsafe_allow_html=True)

                    st.markdown("<br>**Probability breakdown:**", unsafe_allow_html=True)

                    def _is_good(name):
                        n = str(name).strip().lower()
                        if any(x in n for x in ("good","1","positive")): return True
                        if any(x in n for x in ("bad","0","negative")):  return False
                        return None

                    flags = [_is_good(c) for c in classes]
                    if None in flags or len(set(flags)) != 2:
                        flags = [i > 0 for i in range(len(classes))]

                    for flag, prob in zip(flags, proba):
                        disp    = "✅ Good Review" if flag else "❌ Bad Review"
                        bar_cls = "prob-bar-good"  if flag else "prob-bar-bad"
                        pct     = round(prob * 100, 1)
                        st.markdown(f"""
                        <div class="prob-row">
                          <span class="prob-label">{disp}</span>
                          <div class="prob-bar-bg">
                            <div class="{bar_cls}" style="width:{int(pct)}%"></div>
                          </div>
                          <span class="prob-pct">{pct}%</span>
                        </div>""", unsafe_allow_html=True)

                    conf = round(max(proba)*100,1)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.metric("Model Confidence", f"{conf}%",
                              delta="High ▲" if conf>=70 else ("Medium" if conf>=50 else "Low ▼"))

                    if is_good:
                        st.markdown('<div class="tip">✅ <b>Happy customer!</b> Good candidate for re-marketing, loyalty program, and upsell campaigns.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="tip-bad">⚠️ <b>At-risk customer!</b> Send a proactive support message or compensation voucher before they churn.</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Prediction error: {e}")
        else:
            st.markdown('<div class="empty-state"><div style="font-size:2.8rem;margin-bottom:.7rem">🔮</div>Fill in the order details above<br>then click <b>Predict Review Outcome</b></div>', unsafe_allow_html=True)
            st.markdown('<div class="tip" style="margin-top:1rem">💡 Strongest predictors: <b>actual vs expectation</b>, <b>shipping speed</b>, and <b>seller level</b>.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🧠 Model Architecture")
    a1,a2,a3 = st.columns(3)
    with a1:
        st.markdown("""<div class="arch-card"><h4>⚙️ Preprocessing</h4><ul>
        <li>Cat NULLs → SimpleImputer + OHE</li><li>Num NULLs → KNNImputer</li>
        <li>Scaling → RobustScaler</li><li>Encoding → OneHotEncoder</li>
        <li>Remainder → passthrough</li></ul></div>""", unsafe_allow_html=True)
    with a2:
        st.markdown("""<div class="arch-card"><h4>🤖 XGBClassifier</h4><ul>
        <li>n_estimators = 700</li><li>learning_rate = 0.1</li>
        <li>max_depth = 7</li><li>reg_alpha = 1.5 | reg_lambda = 2.5</li>
        <li>Balancing: SMOTE</li><li>CV: 5-fold</li></ul></div>""", unsafe_allow_html=True)
    with a3:
        st.markdown("""<div class="arch-card"><h4>📈 Performance</h4><ul>
        <li>Train accuracy: 91.9%</li><li>Test accuracy: 87.4%</li>
        <li>Classes: Good Review / Bad Review</li>
        <li>Features: 20 engineered columns</li><li>Dataset: 115,037 rows</li></ul></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — BUSINESS ANALYSIS & PLOTS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    if df is None:
        st.info("📂 **To display live plots**, place your dataset CSV next to `app5.py` (name it `olist_analytical_dataset.csv`, `df.csv`, or `data.csv`) and restart the app.")
        st.markdown("The plots below will render automatically once the data file is detected.")
    else:
        month_order = ['January','February','March','April','May','June',
                       'July','August','September','October','November','December']

        def section(title):
            st.markdown(f'<div class="section-banner"><div class="section-banner-title">{title}</div></div>', unsafe_allow_html=True)

        def plot_card_start(num, title, badge, badge_cls):
            st.markdown(f"""
            <div class="plot-card">
              <div class="plot-header">
                <div class="plot-num">{num}</div>
                <div class="plot-title">{title}</div>
                <div class="plot-badge {badge_cls}">{badge}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        def meta(what, how, action):
            st.markdown(f"""
            <div class="meta-grid">
              <div class="meta-box"><div class="meta-lbl">📌 What it shows</div><div class="meta-txt">{what}</div></div>
              <div class="meta-box"><div class="meta-lbl">👁 How to read it</div><div class="meta-txt">{how}</div></div>
            </div>
            <div class="meta-box" style="margin-bottom:.6rem">
              <div class="meta-lbl">⚡ Business action</div><div class="meta-txt">{action}</div>
            </div>""", unsafe_allow_html=True)

        # ── SECTION 1: SELLER QUALITY ─────────────────────────────────────────
        section("🏪 Section 1 — Seller Quality")

        # Plot 1
        with st.container():
            st.markdown('<div class="plot-card">', unsafe_allow_html=True)
            st.markdown('<div class="plot-header"><div class="plot-num">1</div><div class="plot-title">Seller Level vs Review Type — The Core Paradox</div><div class="plot-badge badge-must">⭐ Must Have</div></div>', unsafe_allow_html=True)
            meta("Side-by-side bars: good vs bad review rate for bad sellers vs good sellers.",
                 "If bad sellers still have a tall green bar — a bad seller doesn't always mean a bad review. The customer judges the full experience.",
                 "Fix delivery perception first. A bad seller who ships on time may still satisfy customers.")
            ct1 = df.groupby(['seller level','review type']).size().reset_index(name='count')
            ct1['percentage'] = (ct1['count']/ct1.groupby('seller level')['count'].transform('sum')*100).round(1)
            fig1 = px.bar(ct1, x='seller level', y='percentage', color='review type', barmode='group',
                          text=ct1['percentage'].astype(str)+'%', color_discrete_map=color_map,
                          title='<b>Seller Level vs Review Type</b><br><sup>Does a bad seller always get a bad review?</sup>',
                          labels={'seller level':'Seller Level','percentage':'% of Orders','review type':'Review Type'})
            fig1.update_traces(textposition='outside', textfont_size=11)
            fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_family='Arial',
                               xaxis=dict(showgrid=False), yaxis=dict(showgrid=True,gridcolor='#F0F0F0',range=[0,85]))
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('<div class="rec-lbl">✍️ Your Recommendation</div>', unsafe_allow_html=True)
            st.text_area("", placeholder="Write your recommendation here...", height=90, key="rec1", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        # Plot 2
        with st.container():
            st.markdown('<div class="plot-card">', unsafe_allow_html=True)
            st.markdown('<div class="plot-header"><div class="plot-num">2</div><div class="plot-title">Seller Level × Actual Expectation → Bad Review % Heatmap</div><div class="plot-badge badge-must">⭐ Must Have</div></div>', unsafe_allow_html=True)
            meta("2×2 grid: each cell = % bad reviews for a seller level + expectation combination.",
                 "Darkest red cell = most dangerous combination. Bad seller + bad expectation is catastrophic.",
                 "Prioritize preventing the specific combination. Feature interaction matters more than any single factor.")
            bad_only = df[df['review type']=='bad review']
            total_combos = df.groupby(['seller level','actuall expectation']).size()
            bad_combos   = bad_only.groupby(['seller level','actuall expectation']).size()
            pct2 = (bad_combos/total_combos*100).round(1).reset_index(name='bad_review_pct')
            pivot2 = pct2.pivot(index='seller level', columns='actuall expectation', values='bad_review_pct')
            fig2 = go.Figure(data=go.Heatmap(
                z=pivot2.values, x=pivot2.columns.tolist(), y=pivot2.index.tolist(),
                colorscale=[[0,'#2ECC71'],[0.5,'#F39C12'],[1,'#E74C3C']],
                text=[[f'{v:.1f}%' for v in row] for row in pivot2.values],
                texttemplate='%{text}', textfont=dict(size=16,color='white'),
                colorbar=dict(title='Bad Review %',ticksuffix='%')))
            fig2.update_layout(title='<b>What Combination Most Likely Causes a Bad Review?</b>',
                               font_family='Arial', plot_bgcolor='white', paper_bgcolor='white',
                               xaxis_title='Actual Expectation', yaxis_title='Seller Level')
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('<div class="rec-lbl">✍️ Your Recommendation</div>', unsafe_allow_html=True)
            st.text_area("", placeholder="Write your recommendation here...", height=90, key="rec2", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        # Plot 3 — Faceted full picture
        with st.container():
            st.markdown('<div class="plot-card">', unsafe_allow_html=True)
            st.markdown('<div class="plot-header"><div class="plot-num">3</div><div class="plot-title">Full Picture — Seller Quality, Expectation & Review (Faceted)</div><div class="plot-badge badge-must">⭐ Must Have</div></div>', unsafe_allow_html=True)
            meta("Each panel = one seller type. X-axis = expectation met? Bars split by review type.",
                 "If bad seller + perfect expectation still yields mostly good reviews → the delivery buffer is masking bad sellers.",
                 "Evaluate sellers on operational metrics (seller_level), not just review scores.")
            ct4 = df.groupby(['seller level','actuall expectation','review type']).size().reset_index(name='count')
            ct4['percentage'] = (ct4['count']/ct4.groupby(['seller level','actuall expectation'])['count'].transform('sum')*100).round(1)
            fig4 = px.bar(ct4, x='actuall expectation', y='percentage', color='review type',
                          facet_col='seller level', barmode='group',
                          text=ct4['percentage'].astype(str)+'%', color_discrete_map=color_map,
                          title='<b>The Full Picture — Seller, Expectation, and Review Outcome</b>',
                          labels={'actuall expectation':'Actual Expectation','percentage':'% of Orders',
                                  'review type':'Review Type','seller level':'Seller Level'})
            fig4.update_traces(textposition='outside', textfont_size=10)
            fig4.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                               font_family='Arial', yaxis=dict(range=[0,95]))
            fig4.for_each_annotation(lambda a: a.update(text=a.text.replace('seller level=','')))
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown('<div class="rec-lbl">✍️ Your Recommendation</div>', unsafe_allow_html=True)
            st.text_area("", placeholder="Write your recommendation here...", height=90, key="rec3", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        # Plot 4 — Top 15 categories bad sellers
        with st.container():
            st.markdown('<div class="plot-card">', unsafe_allow_html=True)
            st.markdown('<div class="plot-header"><div class="plot-num">4</div><div class="plot-title">Top 15 Product Categories with Most Bad Sellers</div><div class="plot-badge badge-high">🔵 High Value</div></div>', unsafe_allow_html=True)
            meta("Top 15 categories with the highest count of bad-seller orders.",
                 "If concentrated in 2–3 categories → logistics issue specific to those products. Spread evenly → seller behavior problem.",
                 "Replace bad sellers in these categories with vetted alternatives. High concentration = logistics partner issue, not seller behavior.")
            q7 = (df[df['seller level']=='bad seller'].groupby('product category name english')
                    .agg(count=('order item id','count')).reset_index()
                    .sort_values('count',ascending=True).tail(15))
            fig7 = px.bar(q7, x='count', y='product category name english', orientation='h',
                          text='count', color='count', color_continuous_scale=['#F9E79F','#E74C3C'],
                          title='<b>Top 15 Categories with Most Bad Sellers</b>',
                          labels={'count':'Bad Seller Orders','product category name english':'Category'})
            fig7.update_traces(textposition='outside', textfont_size=11)
            fig7.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                               font_family='Arial', coloraxis_showscale=False,
                               xaxis=dict(showgrid=True,gridcolor='#F0F0F0'), yaxis=dict(showgrid=False))
            st.plotly_chart(fig7, use_container_width=True)
            st.markdown('<div class="rec-lbl">✍️ Your Recommendation</div>', unsafe_allow_html=True)
            st.text_area("", placeholder="Write your recommendation here...", height=90, key="rec4", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        # ── SECTION 2: CUSTOMER EXPERIENCE ───────────────────────────────────
        section("👥 Section 2 — Customer Experience")

        # Plot 5 — Shipping speed stacked
        with st.container():
            st.markdown('<div class="plot-card">', unsafe_allow_html=True)
            st.markdown('<div class="plot-header"><div class="plot-num">5</div><div class="plot-title">Shipping Speed → Review Type Distribution</div><div class="plot-badge badge-must">⭐ Must Have</div></div>', unsafe_allow_html=True)
            meta("Stacked bars: review type breakdown for each shipping speed category.",
                 "As shipping slows (left→right), red segment grows sharply. A sharp jump marks the threshold where customers stop tolerating delays.",
                 "Keep all orders in fast or regular shipping. Soo bad shipping produces bad reviews by ~75%+ — unrecoverable.")
            speed_order = ['fast shipping','regular shipping','bad shipping','soo bad shipping']
            ct3 = df.groupby(['shipping speed','review type']).size().reset_index(name='count')
            ct3['percentage'] = (ct3['count']/ct3.groupby('shipping speed')['count'].transform('sum')*100).round(1)
            ct3 = ct3[ct3['shipping speed'].isin(speed_order)].copy()
            ct3['shipping speed'] = pd.Categorical(ct3['shipping speed'],categories=speed_order,ordered=True)
            ct3 = ct3.sort_values('shipping speed')
            fig3 = px.bar(ct3, x='shipping speed', y='percentage', color='review type',
                          barmode='stack', text=ct3['percentage'].astype(str)+'%',
                          color_discrete_map=color_map,
                          title='<b>Shipping Speed is What the Customer Actually Judges</b>',
                          labels={'shipping speed':'Shipping Speed','percentage':'% of Orders','review type':'Review Type'})
            fig3.update_traces(textposition='inside', textfont_size=11)
            fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                               font_family='Arial', xaxis=dict(showgrid=False),
                               yaxis=dict(showgrid=True,gridcolor='#F0F0F0',range=[0,105]))
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown('<div class="rec-lbl">✍️ Your Recommendation</div>', unsafe_allow_html=True)
            st.text_area("", placeholder="Write your recommendation here...", height=90, key="rec5", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        # Plot 6 — New customers churn risk
        with st.container():
            st.markdown('<div class="plot-card">', unsafe_allow_html=True)
            st.markdown('<div class="plot-header"><div class="plot-num">6</div><div class="plot-title">New Customers: Bad Expectation → Churn Risk</div><div class="plot-badge badge-must">⭐ Must Have</div></div>', unsafe_allow_html=True)
            meta("New customers only: review type split by whether delivery promise was met.",
                 "Red bar on bad expectation side = new customers who almost certainly never return. Invisible churn — they never became regulars.",
                 "First Order Protection policy: assign best seller, add 1 day buffer, send proactive WhatsApp on dispatch. Low cost, high retention value.")
            q1 = (df[df['customer type']=='new'].groupby(['review type','actuall expectation'])
                    .agg(count=('order item id','count')).reset_index())
            q1['percentage'] = (q1['count']/q1.groupby('review type')['count'].transform('sum')*100).round(1)
            fig_q1 = px.bar(q1, x='review type', y='percentage', color='actuall expectation',
                            barmode='group', text=q1['percentage'].astype(str)+'%',
                            color_discrete_map={'perfect expectation':'#2ECC71','bad expectation':'#E74C3C'},
                            title='<b>New Customers: Review Type vs Delivery Expectation</b>',
                            labels={'review type':'Review Type','percentage':'% of New Customer Orders',
                                    'actuall expectation':'Expectation Met?'})
            fig_q1.update_traces(textposition='outside', textfont_size=12)
            fig_q1.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_family='Arial',
                                 yaxis=dict(range=[0,90],showgrid=True,gridcolor='#F0F0F0'),
                                 xaxis=dict(showgrid=False))
            st.plotly_chart(fig_q1, use_container_width=True)
            st.markdown('<div class="rec-lbl">✍️ Your Recommendation</div>', unsafe_allow_html=True)
            st.text_area("", placeholder="Write your recommendation here...", height=90, key="rec6", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        # Plot 7 — Operation speed failure chain heatmap
        with st.container():
            st.markdown('<div class="plot-card">', unsafe_allow_html=True)
            st.markdown('<div class="plot-header"><div class="plot-num">7</div><div class="plot-title">Operation Speed vs Shipping Speed — The Failure Chain</div><div class="plot-badge badge-must">⭐ Must Have</div></div>', unsafe_allow_html=True)
            meta("Heatmap: order counts for each operation speed × shipping speed combination.",
                 "Dark bottom-right corner = slow approval reliably leads to slow shipping. A compounded failure the customer cannot forgive.",
                 "If operation speed is already bad, escalate to priority shipping immediately. Preventing the second failure is more valuable than fixing either alone.")
            q3 = df.groupby(['operation speed','shipping speed']).agg(count=('order item id','count')).reset_index()
            op_order2  = ['perfect operation','regular operation','bad operation','soo bad']
            shp_order2 = ['fast shipping','regular shipping','bad shipping','soo bad shipping']
            pivot_q3 = (q3.pivot(index='operation speed',columns='shipping speed',values='count')
                          .reindex(index=op_order2,columns=shp_order2).fillna(0))
            fig_q3 = go.Figure(data=go.Heatmap(
                z=pivot_q3.values, x=pivot_q3.columns.tolist(), y=pivot_q3.index.tolist(),
                colorscale=[[0,'#2ECC71'],[0.5,'#F39C12'],[1,'#E74C3C']],
                text=[[str(int(v)) for v in row] for row in pivot_q3.values],
                texttemplate='%{text}', textfont=dict(size=13,color='white'),
                colorbar=dict(title='# Orders')))
            fig_q3.update_layout(title='<b>Operation Speed vs Shipping Speed — The Failure Chain</b>',
                                 xaxis_title='Shipping Speed', yaxis_title='Operation Speed',
                                 font_family='Arial', plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig_q3, use_container_width=True)
            st.markdown('<div class="rec-lbl">✍️ Your Recommendation</div>', unsafe_allow_html=True)
            st.text_area("", placeholder="Write your recommendation here...", height=90, key="rec7", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        # Plot 8 — Top high-risk combinations
        with st.container():
            st.markdown('<div class="plot-card">', unsafe_allow_html=True)
            st.markdown('<div class="plot-header"><div class="plot-num">8</div><div class="plot-title">Top High-Risk Combinations → Bad Review Rate</div><div class="plot-badge badge-must">⭐ Must Have</div></div>', unsafe_allow_html=True)
            meta("Top 15 combinations of expectation + shipping speed + seller level ranked by % bad reviews.",
                 "Leftmost bars = most dangerous. 100% bad review rate on bad shipping + bad expectation. Use these as your alert system trigger rules.",
                 "Top 5 combinations = auto-intervention rules. Any incoming order matching these patterns triggers an immediate action.")
            q4 = df.groupby(['actuall expectation','shipping speed','seller level','review type']).agg(count=('order item id','count')).reset_index()
            q4['percentage'] = (q4['count']/q4.groupby(['actuall expectation','shipping speed','seller level'])['count'].transform('sum')*100).round(1)
            q4['combo'] = q4['actuall expectation']+' | '+q4['shipping speed']+' | '+q4['seller level']
            bad_q4 = q4[q4['review type']=='bad review'].sort_values('percentage',ascending=False).head(15)
            fig_q4 = px.bar(bad_q4, x='combo', y='percentage', color='seller level',
                            text=bad_q4['percentage'].astype(str)+'%',
                            color_discrete_map={'bad seller':'#E74C3C','good seller':'#2ECC71'},
                            title='<b>Top High-Risk Combinations → Bad Review Rate</b>',
                            labels={'combo':'Feature Combination','percentage':'% Bad Reviews','seller level':'Seller Level'})
            fig_q4.update_traces(textposition='outside', textfont_size=10)
            fig_q4.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_family='Arial',
                                 xaxis=dict(tickangle=-35,showgrid=False),
                                 yaxis=dict(range=[0,110],showgrid=True,gridcolor='#F0F0F0'))
            st.plotly_chart(fig_q4, use_container_width=True)
            st.markdown('<div class="rec-lbl">✍️ Your Recommendation</div>', unsafe_allow_html=True)
            st.text_area("", placeholder="Write your recommendation here...", height=90, key="rec8", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        # Plot 9 — Categories missing delivery promise
        with st.container():
            st.markdown('<div class="plot-card">', unsafe_allow_html=True)
            st.markdown('<div class="plot-header"><div class="plot-num">9</div><div class="plot-title">Top 15 Categories That Most Frequently Miss the Delivery Promise</div><div class="plot-badge badge-high">🔵 High Value</div></div>', unsafe_allow_html=True)
            meta("Categories with highest count of orders where delivery was later than promised.",
                 "Longer bars = more broken promises. Concentrated in one category → logistics/product issue. Spread = seller issue.",
                 "Replace sellers in these categories with better alternatives. Add automatic delivery buffer for these categories.")
            q2 = (df[df['actuall expectation']=='bad expectation'].groupby('product category name english')
                    .agg(count=('order item id','count')).reset_index()
                    .sort_values('count',ascending=True).tail(15))
            fig_q2 = px.bar(q2, x='count', y='product category name english', orientation='h',
                            text='count', color='count', color_continuous_scale=['#F9E79F','#E74C3C'],
                            title='<b>Top 15 Categories That Most Frequently Miss the Delivery Promise</b>',
                            labels={'count':'Orders with Bad Expectation','product category name english':'Category'})
            fig_q2.update_traces(textposition='outside', textfont_size=11)
            fig_q2.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                                 font_family='Arial', coloraxis_showscale=False,
                                 xaxis=dict(showgrid=True,gridcolor='#F0F0F0'), yaxis=dict(showgrid=False))
            st.plotly_chart(fig_q2, use_container_width=True)
            st.markdown('<div class="rec-lbl">✍️ Your Recommendation</div>', unsafe_allow_html=True)
            st.text_area("", placeholder="Write your recommendation here...", height=90, key="rec9", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        # ── SECTION 3: SEASONAL ───────────────────────────────────────────────
        section("📅 Section 3 — Seasonal & Time Patterns")

        # Plot 10 — Monthly shipping heatmap
        with st.container():
            st.markdown('<div class="plot-card">', unsafe_allow_html=True)
            st.markdown('<div class="plot-header"><div class="plot-num">10</div><div class="plot-title">Monthly Shipping Speed Distribution — When Does Logistics Break?</div><div class="plot-badge badge-must">⭐ Must Have</div></div>', unsafe_allow_html=True)
            meta("% of orders in each shipping speed category per month.",
                 "Dark red rows = months where logistics is overwhelmed. Worst months: March, February, November, January, December.",
                 "60 days before peak months: pre-stock inventory, suspend new seller onboarding, add delivery buffer to customer-facing ETAs.")
            t2 = df.groupby(['order purchase month','shipping speed']).agg(count=('order item id','count')).reset_index()
            t2['pct'] = (t2['count']/t2.groupby('order purchase month')['count'].transform('sum')*100).round(1)
            pivot_t2 = (t2.pivot(index='order purchase month',columns='shipping speed',values='pct')
                          .reindex(index=month_order,columns=speed_order).fillna(0))
            fig_t2 = go.Figure(data=go.Heatmap(
                z=pivot_t2.values, x=pivot_t2.columns.tolist(), y=pivot_t2.index.tolist(),
                colorscale=[[0,'#2ECC71'],[0.5,'#F39C12'],[1,'#E74C3C']],
                text=[[f'{v:.0f}%' for v in row] for row in pivot_t2.values],
                texttemplate='%{text}', textfont=dict(size=11,color='white'),
                colorbar=dict(title='% Orders',ticksuffix='%')))
            fig_t2.update_layout(title='<b>Monthly Shipping Speed Distribution</b>',
                                 xaxis_title='Shipping Speed', yaxis_title='Month',
                                 font_family='Arial', plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig_t2, use_container_width=True)
            st.markdown('<div class="rec-lbl">✍️ Your Recommendation</div>', unsafe_allow_html=True)
            st.text_area("", placeholder="Write your recommendation here...", height=90, key="rec10", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        # Plot 11 — Volume vs bad review dual axis
        with st.container():
            st.markdown('<div class="plot-card">', unsafe_allow_html=True)
            st.markdown('<div class="plot-header"><div class="plot-num">11</div><div class="plot-title">Does High Order Volume Drive More Bad Reviews?</div><div class="plot-badge badge-must">⭐ Must Have</div></div>', unsafe_allow_html=True)
            meta("Monthly order volume (bars) vs bad review % (line) — do they peak together?",
                 "If the red line peaks when bars are tallest → volume overwhelms capacity. Most bad review months: March, Feb, Jan, Dec, May.",
                 "Set monthly volume caps per seller based on their historical on-time rate. Sellers who can't scale reliably get capped first.")
            t5_vol = df.groupby('order purchase month').agg(total=('order item id','count')).reset_index()
            t5_bad = (df[df['review type']=='bad review'].groupby('order purchase month')
                        .agg(bad_count=('order item id','count')).reset_index())
            t5 = t5_vol.merge(t5_bad, on='order purchase month')
            t5['bad_pct'] = (t5['bad_count']/t5['total']*100).round(1)
            t5['order purchase month'] = pd.Categorical(t5['order purchase month'],categories=month_order,ordered=True)
            t5 = t5.sort_values('order purchase month')
            fig_t5 = make_subplots(specs=[[{"secondary_y":True}]])
            fig_t5.add_trace(go.Bar(x=t5['order purchase month'],y=t5['total'],
                                    name='Total Orders',marker_color='#AED6F1',opacity=0.75), secondary_y=False)
            fig_t5.add_trace(go.Scatter(x=t5['order purchase month'],y=t5['bad_pct'],
                                        name='Bad Review %',mode='lines+markers+text',
                                        line=dict(color='#E74C3C',width=3),marker=dict(size=9,color='#E74C3C'),
                                        text=t5['bad_pct'].astype(str)+'%',
                                        textposition='top center',textfont=dict(size=10,color='#E74C3C')),
                             secondary_y=True)
            fig_t5.update_layout(title='<b>Does High Order Volume Drive More Bad Reviews?</b>',
                                 font_family='Arial', plot_bgcolor='white', paper_bgcolor='white',
                                 xaxis=dict(showgrid=False,tickangle=-30),legend=dict(orientation='h',y=-0.2))
            fig_t5.update_yaxes(title_text='Total Orders',secondary_y=False,showgrid=True,gridcolor='#F0F0F0')
            fig_t5.update_yaxes(title_text='Bad Review %',secondary_y=True,showgrid=False,range=[0,50])
            st.plotly_chart(fig_t5, use_container_width=True)
            st.markdown('<div class="rec-lbl">✍️ Your Recommendation</div>', unsafe_allow_html=True)
            st.text_area("", placeholder="Write your recommendation here...", height=90, key="rec11", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        # ── SECTION 4: LOGISTICS ──────────────────────────────────────────────
        section("🗺️ Section 4 — Logistics & Geography")

        # Plot 12 — Distance box plot
        with st.container():
            st.markdown('<div class="plot-card">', unsafe_allow_html=True)
            st.markdown('<div class="plot-header"><div class="plot-num">12</div><div class="plot-title">Distance vs Shipping Speed — Where Does Distance Break Promises?</div><div class="plot-badge badge-must">⭐ Must Have</div></div>', unsafe_allow_html=True)
            meta("Box plots: distance distribution for each shipping speed × expectation combination.",
                 "When red boxes (bad expectation) dominate at high distances → that range = warehouse coverage gap. Threshold found at ~1500km.",
                 "Orders above 1500km: auto-add buffer day to ETA, require seller to ship within 24h not 48h. Build regional warehouses in coverage gaps.")
            fig_q10 = px.box(df, x='shipping speed', y='distance between customer and seller',
                             color='actuall expectation',
                             color_discrete_map={'perfect expectation':'#2ECC71','bad expectation':'#E74C3C'},
                             category_orders={'shipping speed':['fast shipping','regular shipping','bad shipping','soo bad shipping']},
                             title='<b>Distance vs Shipping Speed — Where Does Distance Break Promises?</b>',
                             labels={'distance between customer and seller':'Distance (km)',
                                     'shipping speed':'Shipping Speed','actuall expectation':'Expectation Met?'})
            fig_q10.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_family='Arial',
                                  xaxis=dict(showgrid=False), yaxis=dict(showgrid=True,gridcolor='#F0F0F0'))
            st.plotly_chart(fig_q10, use_container_width=True)
            st.markdown('<div class="rec-lbl">✍️ Your Recommendation</div>', unsafe_allow_html=True)
            st.text_area("", placeholder="Write your recommendation here...", height=90, key="rec12", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — INSIGHTS & RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 💡 Business Insights & Recommendations")
    st.markdown("All insights derived from the Olist dataset analysis. Each one is grounded in a specific plot finding.")
    st.markdown("<br>", unsafe_allow_html=True)

    insights = [
        {
            "num":"#1","tag":"⭐ Critical","tag_color":"#C62828","bg":"#FFF5F5",
            "title":"Perfect System ≠ Good Review — The Hidden Quality Problem",
            "finding":"Row 53 reveals: even when operation, shipping, and expectation are all perfect, some orders still receive bad reviews. The product itself or carrier behavior (rudeness, damaged packaging) is the cause — factors outside your system.",
            "added":"This means your bad review rate is actually underestimated by your operational metrics. The real satisfaction gap is larger than the data shows.",
            "action":"Create a 'Mystery Bad Review' alert: flag orders where all metrics are perfect but review is bad. Customer service calls this segment first. Build a WhatsApp campaign to recover them — these customers are the most convertible to loyal because their experience was operationally fine.",
            "plot":"Plots 1, 3"
        },
        {
            "num":"#2","tag":"⭐ Critical","tag_color":"#C62828","bg":"#FFF5F5",
            "title":"Distance Above 1500km Breaks the Enterprise Deadline",
            "finding":"Sellers more than 1500km from the customer consistently break the shipping limit date. This isn't seller behavior — it's a geography problem the current logistics network cannot handle.",
            "added":"Build a delivery time prediction model using distance + seller category + month as inputs. This lets you show a realistic ETA to the customer before they order — reducing bad_expectation at the source.",
            "action":"Auto-add 1–2 buffer days to customer-facing ETA for orders >1500km. Require sellers in those corridors to ship within 24h not 48h. Identify the top 3–5 state pairs where this happens most and prioritize warehouse placement there.",
            "plot":"Plot 12"
        },
        {
            "num":"#3","tag":"⭐ Critical","tag_color":"#C62828","bg":"#FFF5F5",
            "title":"Call the Customers Who Left Bad Reviews Despite Perfect Operations",
            "finding":"A segment of customers left bad reviews when everything in the system was perfect. These customers had a problem with the product or carrier — not the platform.",
            "added":"These are the most valuable recovery targets: they had a good operational experience, meaning one personalized outreach can flip them to loyal. A loyal customer is worth 3–5x a new customer in lifetime value.",
            "action":"Customer service calls this segment within 48h of a bad review. Offer a personalized deal matching their product category. Follow up with a WhatsApp campaign. Priority: new customers first — a loyal customer who complained will likely return anyway; a new customer won't.",
            "plot":"Plots 1, 3, 6"
        },
        {
            "num":"#4","tag":"🔴 High","tag_color":"#E65100","bg":"#FFF8F0",
            "title":"Seasonal Risk Calendar — 5 High-Risk Months Identified",
            "finding":"Most bad shipping: March, February, November, January, December. Most bad reviews: March, February, January, December, May. The overlap proves causality — bad shipping directly causes bad reviews in those months.",
            "added":"May anomaly: bad reviews spike in May but shipping is relatively fine. This suggests a product quality or expectation issue specific to May — worth a separate category-level investigation.",
            "action":"Pre-season preparation 60 days before each peak month: (1) require bad sellers to pre-stock, (2) add delivery buffer to ETAs, (3) suspend new seller onboarding — only proven sellers handle peak volume. Present this as an annual risk calendar to leadership.",
            "plot":"Plots 10, 11"
        },
        {
            "num":"#5","tag":"🔴 High","tag_color":"#E65100","bg":"#FFF8F0",
            "title":"100% Bad Review Rate: Bad Shipping + Bad Expectation = Total Failure",
            "finding":"From Plot 8: when an order has both bad shipping AND bad expectation, the bad review rate reaches 100%. 50% of orders with bad expectation + regular shipping get bad reviews. 30% of orders with bad shipping + perfect expectation get bad reviews. Even when everything is bad (all features), bad review rate is 73–83%.",
            "added":"This gives you a clear risk scoring system without ML: assign points per feature, total score = intervention priority.",
            "action":"Build a simple rule engine: bad_expectation + bad_shipping → immediate intervention (compensation voucher + priority support). bad_expectation alone → proactive message on delivery day. Use Plot 8 percentages as the probability display in your monitoring system.",
            "plot":"Plot 8"
        },
        {
            "num":"#6","tag":"🔴 High","tag_color":"#E65100","bg":"#FFF8F0",
            "title":"Seller Warning System — 3-Stage Escalation",
            "finding":"Bad sellers (who ship after the limit date) cause cascading failures: late shipment → broken delivery promise → bad review. Some bad sellers are masked by the delivery buffer — they ship late but the ETA had enough buffer that the customer still received it on time.",
            "added":"A seller evaluated only on reviews will appear fine even when consistently shipping late. The buffer hides their operational failure from review metrics.",
            "action":"Stage 1 (Warning): 2+ late shipments in 30 days → automated warning email. Stage 2 (Restricted): 5+ late shipments → reduced visibility in search results. Stage 3 (Offboarded): late rate >30% for 2 consecutive months → account suspension. Show a 'Reliable Seller' badge for sellers with 0 late shipments in 90 days + >80% good reviews.",
            "plot":"Plots 1, 2, 3, 4"
        },
        {
            "num":"#7","tag":"🔵 Strategic","tag_color":"#1565C0","bg":"#F0F7FF",
            "title":"Build Regional Warehouses to Fix the Distance Problem",
            "finding":"Distance above 1500km systematically breaks delivery promises. This is not fixable by better sellers — it's a physical infrastructure gap.",
            "added":"Plot 12 shows the exact distance ranges where bad expectation becomes the norm. The top seller + category combinations with the most failures at long distances directly point to which state-pair corridors need coverage.",
            "action":"Identify the top 5 state pairs with the most bad_expectation orders above 1500km. Calculate the volume of orders that would be rescued by a warehouse in each location. Present ROI as: (bad review recovery rate × customer LTV) vs warehouse operational cost. This is a leadership-level infrastructure investment recommendation.",
            "plot":"Plot 12"
        },
        {
            "num":"#8","tag":"🔵 Strategic","tag_color":"#1565C0","bg":"#F0F7FF",
            "title":"New Customer Churn is the Platform's Most Expensive Invisible Problem",
            "finding":"New customers who experience bad_expectation + bad_review on their first order almost certainly never return. They are never counted in churn metrics because they never became regular customers — they simply disappear after one order.",
            "added":"This is invisible churn. Retention campaigns never reach them because they have no history. The acquisition cost is wasted entirely on a single bad experience.",
            "action":"First Order Protection: for every new customer's first order, (1) auto-assign the highest-rated seller available in that category, (2) add 1 day to the ETA shown to the customer, (3) send a WhatsApp dispatch notification. Measure: compare bad review rate on first orders before vs after policy. Even a 10% improvement in first-order satisfaction has compounding LTV impact.",
            "plot":"Plot 6"
        },
    ]

    for ins in insights:
        st.markdown(f"""
        <div style="background:{ins['bg']};border:1px solid #E0E0E0;border-left:4px solid {ins['tag_color']};
                    border-radius:10px;padding:1.1rem 1.3rem;margin-bottom:1rem;">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:.6rem;">
            <span style="background:{ins['tag_color']};color:white;font-size:.7rem;font-weight:700;
                         padding:2px 9px;border-radius:4px;">{ins['tag']}</span>
            <span style="font-size:.65rem;color:#999;font-weight:600;">Based on: {ins['plot']}</span>
            <span style="font-size:.95rem;font-weight:700;color:#111;">{ins['num']} — {ins['title']}</span>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:.7rem;">
            <div style="background:white;border-radius:7px;padding:8px 10px;">
              <div style="font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:#bbb;margin-bottom:3px;">📊 Finding from data</div>
              <div style="font-size:.77rem;color:#333;line-height:1.6;">{ins['finding']}</div>
            </div>
            <div style="background:white;border-radius:7px;padding:8px 10px;">
              <div style="font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:#bbb;margin-bottom:3px;">➕ Added value</div>
              <div style="font-size:.77rem;color:#333;line-height:1.6;">{ins['added']}</div>
            </div>
            <div style="background:white;border-radius:7px;padding:8px 10px;border-left:3px solid {ins['tag_color']};">
              <div style="font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:{ins['tag_color']};margin-bottom:3px;">⚡ Recommended action</div>
              <div style="font-size:.77rem;color:#333;line-height:1.6;">{ins['action']}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — PROJECT OVERVIEW & ENGINEERED COLUMNS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:

    # ── Project idea banner ───────────────────────────────────────────────────
    st.markdown("### 🧠 Project Overview")

    st.markdown(
        "<div style='background:linear-gradient(135deg,#1B5E20,#2E7D32,#43A047);"
        "border-radius:12px;padding:1.4rem 1.8rem;color:white;margin-bottom:1.2rem;'>"
        "<div style='font-size:1.1rem;font-weight:800;margin-bottom:.5rem;'>"
        "🚀 Customer Experience Intelligence System</div>"
        "<div style='font-size:.85rem;opacity:.9;line-height:1.7;'>"
        "An ML-powered system that predicts customer review outcomes <b>before delivery</b>, "
        "enabling proactive intervention to prevent bad experiences. "
        "Built on the Brazilian Olist E-Commerce dataset (115K orders, 28 engineered columns)."
        "</div></div>",
        unsafe_allow_html=True
    )

    # ── What it can become ────────────────────────────────────────────────────
    st.markdown("#### 🔭 What This System Can Evolve Into")
    ev1, ev2, ev3 = st.columns(3)
    with ev1:
        st.markdown(
            "<div style='background:white;border:1px solid #E8F5E9;border-radius:10px;"
            "padding:1rem 1.1rem;'>"
            "<div style='font-size:.85rem;font-weight:700;color:#1B5E20;margin-bottom:.5rem;'>"
            "📦 Product Problem Detector</div>"
            "<div style='font-size:.78rem;color:#555;line-height:1.6;'>"
            "Predict which products will generate complaints based on category, weight, "
            "seller history, and delivery distance — before the order ships.</div></div>",
            unsafe_allow_html=True
        )
    with ev2:
        st.markdown(
            "<div style='background:white;border:1px solid #E8F5E9;border-radius:10px;"
            "padding:1rem 1.1rem;'>"
            "<div style='font-size:.85rem;font-weight:700;color:#1B5E20;margin-bottom:.5rem;'>"
            "🚚 Shipping Risk Predictor</div>"
            "<div style='font-size:.78rem;color:#555;line-height:1.6;'>"
            "Flag high-risk shipments based on distance, seller level, and month. "
            "Automatically reroute through priority carriers for at-risk corridors.</div></div>",
            unsafe_allow_html=True
        )
    with ev3:
        st.markdown(
            "<div style='background:white;border:1px solid #E8F5E9;border-radius:10px;"
            "padding:1rem 1.1rem;'>"
            "<div style='font-size:.85rem;font-weight:700;color:#1B5E20;margin-bottom:.5rem;'>"
            "🏪 Seller Health Monitor</div>"
            "<div style='font-size:.78rem;color:#555;line-height:1.6;'>"
            "Real-time seller scoring with automated warning, restriction, and offboarding "
            "based on operational KPIs — not just review scores.</div></div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Engineered columns ────────────────────────────────────────────────────
    st.markdown("#### ⚙️ Engineered Feature Columns")
    st.markdown(
        "<div style='font-size:.8rem;color:#888;margin-bottom:.9rem;'>"
        "These 7 columns were manually built from raw timestamps, IDs, and coordinates "
        "in the original Olist dataset.</div>",
        unsafe_allow_html=True
    )

    # ── seller level ─────────────────────────────────────────────────────────
    st.markdown(
        "<div style='background:#E8F5E9;border-left:4px solid #2E7D32;border-radius:0 10px 10px 0;"
        "padding:1rem 1.2rem;margin-bottom:.8rem;'>"
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:.6rem;'>"
        "<span style='font-size:1.3rem;'>🏪</span>"
        "<span style='font-size:.92rem;font-weight:800;color:#1B5E20;font-family:monospace;'>seller level</span>"
        "<span style='background:#2E7D3222;color:#2E7D32;font-size:.7rem;font-weight:600;"
        "padding:2px 8px;border-radius:4px;margin-left:4px;'>good seller</span>"
        "<span style='background:#2E7D3222;color:#2E7D32;font-size:.7rem;font-weight:600;"
        "padding:2px 8px;border-radius:4px;'>bad seller</span>"
        "</div>"
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>"
        "<div style='background:white;border-radius:7px;padding:8px 10px;'>"
        "<div style='font-size:.62rem;font-weight:700;text-transform:uppercase;"
        "letter-spacing:.06em;color:#aaa;margin-bottom:3px;'>Formula</div>"
        "<div style='font-size:.78rem;font-family:monospace;color:#333;'>"
        "shipping_limit_date − order_delivered_customer_date</div></div>"
        "<div style='background:white;border-radius:7px;padding:8px 10px;'>"
        "<div style='font-size:.62rem;font-weight:700;text-transform:uppercase;"
        "letter-spacing:.06em;color:#aaa;margin-bottom:3px;'>Logic</div>"
        "<div style='font-size:.78rem;color:#333;line-height:1.6;'>"
        "Result &lt; 0 → <b>Bad Seller</b> (shipped after deadline)<br>"
        "Result ≥ 0 → <b>Good Seller</b></div></div>"
        "</div></div>",
        unsafe_allow_html=True
    )

    # ── shipping speed ────────────────────────────────────────────────────────
    st.markdown(
        "<div style='background:#E3F2FD;border-left:4px solid #1565C0;border-radius:0 10px 10px 0;"
        "padding:1rem 1.2rem;margin-bottom:.8rem;'>"
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:.6rem;'>"
        "<span style='font-size:1.3rem;'>🚚</span>"
        "<span style='font-size:.92rem;font-weight:800;color:#1565C0;font-family:monospace;'>shipping speed</span>"
        "<span style='background:#1565C022;color:#1565C0;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;margin-left:4px;'>fast</span>"
        "<span style='background:#1565C022;color:#1565C0;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;'>regular</span>"
        "<span style='background:#1565C022;color:#1565C0;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;'>bad</span>"
        "<span style='background:#1565C022;color:#1565C0;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;'>soo bad</span>"
        "</div>"
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>"
        "<div style='background:white;border-radius:7px;padding:8px 10px;'>"
        "<div style='font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#aaa;margin-bottom:3px;'>Formula</div>"
        "<div style='font-size:.78rem;font-family:monospace;color:#333;'>order_delivered_customer_date − order_purchase_timestamp (days)</div></div>"
        "<div style='background:white;border-radius:7px;padding:8px 10px;'>"
        "<div style='font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#aaa;margin-bottom:3px;'>Logic</div>"
        "<div style='font-size:.78rem;color:#333;line-height:1.6;'>"
        "0–10 days → <b>Fast Shipping</b><br>"
        "10–30 days → <b>Regular Shipping</b><br>"
        "30–60 days → <b>Bad Shipping</b><br>"
        "60+ days → <b>Soo Bad Shipping</b></div></div>"
        "</div></div>",
        unsafe_allow_html=True
    )

    # ── customer type ─────────────────────────────────────────────────────────
    st.markdown(
        "<div style='background:#FFF8E1;border-left:4px solid #E65100;border-radius:0 10px 10px 0;"
        "padding:1rem 1.2rem;margin-bottom:.8rem;'>"
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:.6rem;'>"
        "<span style='font-size:1.3rem;'>👥</span>"
        "<span style='font-size:.92rem;font-weight:800;color:#E65100;font-family:monospace;'>customer type</span>"
        "<span style='background:#E6510022;color:#E65100;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;margin-left:4px;'>new</span>"
        "<span style='background:#E6510022;color:#E65100;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;'>regular</span>"
        "<span style='background:#E6510022;color:#E65100;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;'>loyal</span>"
        "</div>"
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>"
        "<div style='background:white;border-radius:7px;padding:8px 10px;'>"
        "<div style='font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#aaa;margin-bottom:3px;'>Formula</div>"
        "<div style='font-size:.78rem;font-family:monospace;color:#333;'>COUNT(customer_unique_id) per customer</div></div>"
        "<div style='background:white;border-radius:7px;padding:8px 10px;'>"
        "<div style='font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#aaa;margin-bottom:3px;'>Logic</div>"
        "<div style='font-size:.78rem;color:#333;line-height:1.6;'>"
        "Count = 1 → <b>New Customer</b><br>"
        "Count = 2 → <b>Regular Customer</b><br>"
        "Count &gt; 3 → <b>Loyal Customer</b></div></div>"
        "</div></div>",
        unsafe_allow_html=True
    )

    # ── operation speed ───────────────────────────────────────────────────────
    st.markdown(
        "<div style='background:#F3E5F5;border-left:4px solid #6A1B9A;border-radius:0 10px 10px 0;"
        "padding:1rem 1.2rem;margin-bottom:.8rem;'>"
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:.6rem;'>"
        "<span style='font-size:1.3rem;'>⚙️</span>"
        "<span style='font-size:.92rem;font-weight:800;color:#6A1B9A;font-family:monospace;'>operation speed</span>"
        "<span style='background:#6A1B9A22;color:#6A1B9A;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;margin-left:4px;'>perfect</span>"
        "<span style='background:#6A1B9A22;color:#6A1B9A;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;'>regular</span>"
        "<span style='background:#6A1B9A22;color:#6A1B9A;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;'>bad</span>"
        "<span style='background:#6A1B9A22;color:#6A1B9A;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;'>soo bad</span>"
        "</div>"
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>"
        "<div style='background:white;border-radius:7px;padding:8px 10px;'>"
        "<div style='font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#aaa;margin-bottom:3px;'>Formula</div>"
        "<div style='font-size:.78rem;font-family:monospace;color:#333;'>order_approved_at − order_purchase_timestamp (days)</div></div>"
        "<div style='background:white;border-radius:7px;padding:8px 10px;'>"
        "<div style='font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#aaa;margin-bottom:3px;'>Logic</div>"
        "<div style='font-size:.78rem;color:#333;line-height:1.6;'>"
        "0–2 days → <b>Perfect Operation</b><br>"
        "3–5 days → <b>Regular Operation</b><br>"
        "6–10 days → <b>Bad Operation</b><br>"
        "10+ days → <b>Soo Bad Operation</b></div></div>"
        "</div></div>",
        unsafe_allow_html=True
    )

    # ── actual expectation ────────────────────────────────────────────────────
    st.markdown(
        "<div style='background:#FCE4EC;border-left:4px solid #C62828;border-radius:0 10px 10px 0;"
        "padding:1rem 1.2rem;margin-bottom:.8rem;'>"
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:.6rem;'>"
        "<span style='font-size:1.3rem;'>📅</span>"
        "<span style='font-size:.92rem;font-weight:800;color:#C62828;font-family:monospace;'>actuall expectation</span>"
        "<span style='background:#C6282822;color:#C62828;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;margin-left:4px;'>perfect expectation</span>"
        "<span style='background:#C6282822;color:#C62828;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;'>bad expectation</span>"
        "</div>"
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>"
        "<div style='background:white;border-radius:7px;padding:8px 10px;'>"
        "<div style='font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#aaa;margin-bottom:3px;'>Formula</div>"
        "<div style='font-size:.78rem;font-family:monospace;color:#333;'>order_estimated_delivery_date − order_delivered_customer_date (days)</div></div>"
        "<div style='background:white;border-radius:7px;padding:8px 10px;'>"
        "<div style='font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#aaa;margin-bottom:3px;'>Logic</div>"
        "<div style='font-size:.78rem;color:#333;line-height:1.6;'>"
        "Result ≥ 0 → <b>Perfect Expectation</b> (on time or early)<br>"
        "Result &lt; 0 → <b>Bad Expectation</b> (delivered late vs promise)</div></div>"
        "</div></div>",
        unsafe_allow_html=True
    )

    # ── distance ──────────────────────────────────────────────────────────────
    st.markdown(
        "<div style='background:#E0F2F1;border-left:4px solid #00695C;border-radius:0 10px 10px 0;"
        "padding:1rem 1.2rem;margin-bottom:.8rem;'>"
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:.6rem;'>"
        "<span style='font-size:1.3rem;'>🗺️</span>"
        "<span style='font-size:.92rem;font-weight:800;color:#00695C;font-family:monospace;'>distance between customer and seller</span>"
        "<span style='background:#00695C22;color:#00695C;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;margin-left:4px;'>Continuous (km)</span>"
        "</div>"
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>"
        "<div style='background:white;border-radius:7px;padding:8px 10px;'>"
        "<div style='font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#aaa;margin-bottom:3px;'>Formula</div>"
        "<div style='font-size:.78rem;font-family:monospace;color:#333;'>Haversine(seller lat/lng, customer lat/lng) in km</div></div>"
        "<div style='background:white;border-radius:7px;padding:8px 10px;'>"
        "<div style='font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#aaa;margin-bottom:3px;'>Logic</div>"
        "<div style='font-size:.78rem;color:#333;line-height:1.6;'>"
        "Higher distance → higher risk of delay and broken promise.<br>"
        "Key threshold found at <b>~1500 km</b>.</div></div>"
        "</div></div>",
        unsafe_allow_html=True
    )

    # ── review type ───────────────────────────────────────────────────────────
    st.markdown(
        "<div style='background:#FFF3E0;border-left:4px solid #BF360C;border-radius:0 10px 10px 0;"
        "padding:1rem 1.2rem;margin-bottom:.8rem;'>"
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:.6rem;'>"
        "<span style='font-size:1.3rem;'>⭐</span>"
        "<span style='font-size:.92rem;font-weight:800;color:#BF360C;font-family:monospace;'>review type</span>"
        "<span style='background:#BF360C22;color:#BF360C;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;margin-left:4px;'>good review</span>"
        "<span style='background:#BF360C22;color:#BF360C;font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:4px;'>bad review</span>"
        "<span style='background:#BF360C;color:white;font-size:.7rem;font-weight:700;padding:2px 8px;border-radius:4px;margin-left:6px;'>🎯 ML TARGET</span>"
        "</div>"
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;'>"
        "<div style='background:white;border-radius:7px;padding:8px 10px;'>"
        "<div style='font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#aaa;margin-bottom:3px;'>Formula</div>"
        "<div style='font-size:.78rem;font-family:monospace;color:#333;'>review_score (1–5 star rating from customer)</div></div>"
        "<div style='background:white;border-radius:7px;padding:8px 10px;'>"
        "<div style='font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#aaa;margin-bottom:3px;'>Logic</div>"
        "<div style='font-size:.78rem;color:#333;line-height:1.6;'>"
        "Score ≥ 3 → <b>Bad Review</b> (unsatisfied)<br>"
        "Score &lt; 3 → <b>Good Review</b> (satisfied)<br>"
        "This is the binary classification target for XGBoost.</div></div>"
        "</div></div>",
        unsafe_allow_html=True
    )

    # ── Dataset stats ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📊 Dataset Summary")
    d1, d2, d3, d4 = st.columns(4)
    for col, (v, l) in zip(
        [d1, d2, d3, d4],
        [("115,037","Total Orders"),("28","Engineered Columns"),
         ("7","New Feature Columns"),("2016–2018","Date Range")]
    ):
        col.markdown(
            f'<div class="kpi"><div class="v">{v}</div><div class="l">{l}</div></div>',
            unsafe_allow_html=True
        )

st.markdown(
    '<br><div style="text-align:center;color:#ccc;font-size:.75rem">'
    'Olist Brazilian E-Commerce · Intelligence Dashboard · Built with Streamlit & XGBoost'
    '</div>',
    unsafe_allow_html=True
)