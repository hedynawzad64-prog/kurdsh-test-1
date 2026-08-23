import streamlit as st
import plotly.express as px
import pandas as pd
import random

# إعداد واجهة الويب والأسلوب العسكري المستقبلي للعبة
st.set_page_config(page_title="حرب الروبوتات 2099", layout="wide")
st.title("🤖 جبهة الروبوتات 2099 - حرب المستقبل التكتيكية")
st.caption("مرحباً بك أيها القائد الذكائي. قد جيوشك الآلية واحتل مراكز الطاقة العالمية مع أصدقائك.")

# إنشاء قاعدة بيانات مبسطة لمدن المستقبل والجيوش الآلية داخل الجلسة (Session State)
if 'map_data' not in st.session_state:
    st.session_state.map_data = pd.DataFrame({
        'Sector': ['Neo-Cairo Sector', 'Cyber-Riyadh Hub', 'Quantum-Baghdad', 'Neo-Tokyo Core', 'Matrix-Berlin', 'Silicon-Valley Base'],
        'Region': ['Africa Prime', 'Arabia Grid', 'Mesopotamia', 'Asia Core', 'Europa Grid', 'Americas Grid'],
        'Lat': [30.0444, 24.7136, 33.3152, 35.6762, 52.5200, 37.4419],
        'Lon': [31.2357, 46.6753, 44.3661, 139.6503, 13.4050, -122.1430],
        'Overlord': ['🤖 نظام الذكاء الخامل'] * 6,
        'Mecha_Armies': [20, 20, 20, 20, 20, 20], # عدد روبوتات الميكا للكمبيوتر
        'Plasma_Cores': [10, 15, 12, 25, 18, 30]   # إنتاج خلايا البلازما
    })

if 'factions' not in st.session_state:
    st.session_state.factions = {}

# تحويل البيانات إلى قاموس لتسهيل القراءة البرمجية وتجنب أخطاء الفهارس المعقدة
df = st.session_state.map_data

# --- نظام تسجيل قادة الفصائل الآلية ---
st.sidebar.header("🕹️ تسجيل فصيلتك السيبرانية")
commander_name = st.sidebar.text_input("اسم القائد السيبراني:")
starting_sector = st.sidebar.selectbox("اختر قطاع البداية للسيطرة عليه:", df['Sector'].tolist())

if st.sidebar.button("📡 تفعيل الاتصال والسيطرة"):
    if commander_name:
        # تحديث الحاكم للقطاع المختار بطريقة مباشرة ومضمونة
        df.loc[df['Sector'] == starting_sector, 'Overlord'] = commander_name
        df.loc[df['Sector'] == starting_sector, 'Mecha_Armies'] = 40 # دعم ميكا إضافي للاعب
        st.session_state.factions[commander_name] = {'Credits': 500}
        st.session_state.map_data = df
        st.sidebar.success(f"تم ربط القائد {commander_name} بالقطاع {starting_sector}!")
        st.rerun()
    else:
        st.sidebar.error("الرجاء إدخال اسم القائد لتشغيل النظام.")

# --- لوحة التحكم في الهجوم وتحريك الجيوش الروبوتية ---
st.sidebar.header("⚔️ مصفوفة الهجوم العسكري")
attacker = st.sidebar.selectbox("القائد المهاجم المصرّح له:", list(st.session_state.factions.keys()))

if attacker:
    # فلترة القطاعات التي يملكها المهاجم للاختيار منها
    my_sectors = df[df['Overlord'] == attacker]['Sector'].tolist()
    if my_sectors:
        from_sector = st.sidebar.selectbox("إطلاق الميكا من قطاع:", my_sectors)
        target_sector = st.sidebar.selectbox("القطاع المستهدف بالاختراق والتدمير:", df['Sector'].tolist())
        
        # جلب القوات الحالية للقطاع المهاجم بشكل رقمي صريح
        current_garrison = int(df[df['Sector'] == from_sector]['Mecha_Armies'].values[0])
        max_attackers = current_garrison - 1
        
        if max_attackers >= 1:
            mecha_to_send = st.sidebar.slider("عدد روبوتات الـ Mecha المرسلة:", 1, max_attackers, 1)

            if st.sidebar.button("🚀 إطلاق جحافل الروبوتات (Launch Attack)"):
                # حساب معركة غزو القطاعات المستقبلية
                defender_force = int(df[df['Sector'] == target_sector]['Mecha_Armies'].values[0])
                defender_name = str(df[df['Sector'] == target_sector]['Overlord'].values[0])
                
                # خصم القوات الآلية من القطاع المهاجم أولاً
                df.loc[df['Sector'] == from_sector, 'Mecha_Armies'] = current_garrison - mecha_to_send
                
                battle_result = mecha_to_send - defender_force
                
                if battle_result > 0:
                    # انتصار المهاجم واحتلال القطاع المستقبلي بالكامل
                    df.loc[df['Sector'] == target_sector, 'Overlord'] = attacker
                    df.loc[df['Sector'] == target_sector, 'Mecha_Armies'] = battle_result
                    st.session_state.map_data = df
                    st.balloons()
                    st.success(f"💥 تم اختراق النظم! القائد {attacker} يسيطر بالكامل على {target_sector} ودمر ميكا {defender_name}!")
                    st.rerun()
                else:
                    # هزيمة المهاجم وصمود خطوط الدفاع للعدو
                    df.loc[df['Sector'] == target_sector, 'Mecha_Armies'] = abs(battle_result)
                    st.session_state.map_data = df
                    st.error(f"💀 فشل الهجوم! صمدت دفاعات {target_sector}. المتبقي للعدو {defender_name}: {abs(battle_result)} ميكا.")
                    st.rerun()
        else:
            st.sidebar.warning("لا توجد ميكا كافية للهجوم من هذا القطاع (اترك روبوت واحد على الأقل للدفاع).")
    else:
        st.sidebar.warning("يجب أن تسيطر على قطاع طاقة واحد على الأقل للبدء.")

# --- عرض الخريطة الرقمية وتقارير الاستخبارات السيبرانية ---
col1, col2 = st.columns()

with col1:
    st.subheader("🌐 الرادار العالمي وتوزيع القوات الروبوتية")
    # رسم الخريطة التفاعلية بأسلوب داكن ومستقبلي مناسب لحرب الروبوتات
    fig = px.scatter_mapbox(
        st.session_state.map_data, 
        lat="Lat", lon="Lon", 
        text="Sector", 
        color="Overlord", 
        size="Mecha_Armies",
        size_max=35, 
        zoom=1, 
        mapbox_style="carto-darkmatter"
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

 
 
 
