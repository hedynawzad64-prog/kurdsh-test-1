import streamlit as st
import plotly.express as px
import pandas as pd
import random

# إعداد واجهة الويب والأسلوب العسكري المستقبلي للعبة
st.set_page_config(page_title="حرب الروبوتات 2099", layout="wide")
st.title("🤖 جبهة الروبوتات 2099 - حرب المستقبل التكتيكية")
st.caption("مرحباً بك أيها القائد الذكائي. قد جيوشك الآلية واحتل مراكز الطاقة العالمية مع أصدقائك.")

# إنشاء قاعدة بيانات افتراضية لمدن المستقبل والموارد والجيوش الآلية داخل الجلسة (Session State)
if 'map_data' not in st.session_state:
    st.session_state.map_data = pd.DataFrame({
        'Sector': ['Neo-Cairo Sector', 'Cyber-Riyadh Hub', 'Quantum-Baghdad', 'Neo-Tokyo Core', 'Matrix-Berlin', 'Silicon-Valley Base'],
        'Region': ['Africa Prime', 'Arabia Grid', 'Mesopotamia', 'Asia Core', 'Europa Grid', 'Americas Grid'],
        'Lat': [30.0444, 24.7136, 33.3152, 35.6762, 52.5200, 37.4419],
        'Lon': [31.2357, 46.6753, 44.3661, 139.6503, 13.4050, -122.1430],
        'Overlord': ['🤖 نظام الذكاء الخامل', '🤖 نظام الذكاء الخامل', '🤖 نظام الذكاء الخامل', '🤖 نظام الذكاء الخامل', '🤖 نظام الذكاء الخامل', '🤖 نظام الذكاء الخامل'],
        'Mecha_Armies':, # عدد روبوتات الميكا في القطاع
        'Plasma_Cores': [100, 150, 120, 200, 180, 250] # إنتاج خلايا البلازما (الموارد)
    })

if 'factions' not in st.session_state:
    st.session_state.factions = {}

# --- نظام تسجيل قادة الفصائل الآلية ---
st.sidebar.header("🕹️ تسجيل فصيلتك السيبرانية")
commander_name = st.sidebar.text_input("اسم القائد السيبراني:")
starting_sector = st.sidebar.selectbox("اختر قطاع البداية للسيطرة عليه:", st.session_state.map_data['Sector'])

if st.sidebar.button("📡 تفعيل الاتصال والسيطرة"):
    if commander_name:
        # تحديث الحاكم للقطاع المختار ليكون اللاعب الجديد
        idx = st.session_state.map_data[st.session_state.map_data['Sector'] == starting_sector].index
        st.session_state.map_data.at[idx, 'Overlord'] = commander_name
        st.session_state.map_data.at[idx, 'Mecha_Armies'] = 40 # دعم ميكا إضافي للاعب البادئ
        st.session_state.factions[commander_name] = {'Credits': 500}
        st.sidebar.success(f"تم ربط القائد {commander_name} بالقطاع {starting_sector}!")
    else:
        st.sidebar.error("الرجاء إدخال اسم القائد لتشغيل النظام.")

# --- لوحة التحكم في الهجوم وتحريك الجيوش الروبوتية ---
st.sidebar.header("⚔️ مصفوفة الهجوم العسكري")
attacker = st.sidebar.selectbox("القائد المهاجم المصرّح له:", list(st.session_state.factions.keys()))

if attacker:
    # فلترة القطاعات التي يملكها المهاجم للاختيار منها
    my_sectors = st.session_state.map_data[st.session_state.map_data['Overlord'] == attacker]['Sector'].tolist()
    if my_sectors:
        from_sector = st.sidebar.selectbox("إطلاق الميكا من قطاع:", my_sectors)
        target_sector = st.sidebar.selectbox("القطاع المستهدف بالاختراق والتدمير:", st.session_state.map_data['Sector'].tolist())
        
        max_attackers = int(st.session_state.map_data[st.session_state.map_data['Sector'] == from_sector]['Mecha_Armies'].values) - 1
        if max_attackers > 1:
            mecha_to_send = st.sidebar.slider("عدد روبوتات الـ Mecha المرسلة:", 1, max_attackers, 1)

            if st.sidebar.button("🚀 إطلاق جحافل الروبوتات (Launch Attack)"):
                idx_from = st.session_state.map_data[st.session_state.map_data['Sector'] == from_sector].index
                idx_target = st.session_state.map_data[st.session_state.map_data['Sector'] == target_sector].index
                
                # خصم القوات الآلية من القطاع المهاجم
                st.session_state.map_data.at[idx_from, 'Mecha_Armies'] -= mecha_to_send
                
                # حساب نتيجة المعركة الإلكترونية/الميكانيكية
                defender_force = st.session_state.map_data.at[idx_target, 'Mecha_Armies']
                defender_name = st.session_state.map_data.at[idx_target, 'Overlord']
                
                # حساب النتيجة (محاكاة اشتباك ليزري)
                battle_result = mecha_to_send - defender_force
                
                if battle_result > 0:
                    # انتصار المهاجم واحتلال القطاع المستقبلي
                    st.session_state.map_data.at[idx_target, 'Overlord'] = attacker
                    st.session_state.map_data.at[idx_target, 'Mecha_Armies'] = battle_result
                    st.balloons()
                    st.success(f"💥 تم اختراق النظم! القائد {attacker} يسيطر بالكامل على {target_sector} ودمر ميكا {defender_name}!")
                else:
                    # هزيمة المهاجم وصمود خطوط الدفاع
                    st.session_state.map_data.at[idx_target, 'Mecha_Armies'] = abs(battle_result)
                    st.error(f"💀 فشل الهجوم! صمدت دفاعات {target_sector}. المتبقي للعدو {defender_name}: {abs(battle_result)} روبوت ميكا.")
        else:
            st.sidebar.warning("لا توجد ميكا كافية للهجوم من هذا القطاع (اترك روبوت واحد على الأقل للدفاع).")
    else:
        st.sidebar.warning("يجب أن تسيطر على قطاع طاقة واحد على الأقل للبدء.")

# --- عرض الخريطة الرقمية وتقارير الاستخبارات السيبرانية ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🌐 الرادار العالمي وتوزيع القوات الروبوتية")
    # رسم الخريطة التفاعلية بأسلوب داكن ومستقبلي
    fig = px.scatter_mapbox(
        st.session_state.map_data, 
        lat="Lat", lon="Lon", 
        text="Sector", 
        color="Overlord", 
        size="Mecha_Armies",
        size_max=35, 
        zoom=1, 
        mapbox_style="carto-darkmatter" # الخلفية السوداء العسكرية الملائمة للمستقبل
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 مصفوفة البيانات والسيطرة")
    st.dataframe(
        st.session_state.map_data[['Sector', 'Overlord', 'Mecha_Armies', 'Plasma_Cores']], 
        hide_index=True,
        use_container_width=True
    )
