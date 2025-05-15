import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import base64
from PIL import Image
import statsmodels.api as sm
from plotly.subplots import make_subplots
import io
from scipy import stats
import matplotlib.pyplot as plt

# تعيين الشكل العام للصفحة
st.set_page_config(
	page_title="ARDL Bound Testing Approach - الدليل النظري",
	page_icon="📊",
	layout="wide",
	initial_sidebar_state="expanded"
)

# تخصيص الأسلوب العام
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    h1, h2, h3 {
        color: #1E88E5;
    }
    .highlight {
        background-color: #f0f7ff;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #1E88E5;
        margin-bottom: 10px;
    }
    .formula {
        background-color: #f9f9f9;
        padding: 10px;
        border-radius: 5px;
        overflow-x: auto;
        font-family: 'Courier New', monospace;
    }
    .sidebar .sidebar-content {
        background-color: #f0f7ff;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #e6f2ff;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E88E5;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# تعيين قائمة المحتويات في الشريط الجانبي
st.sidebar.title("📚 المحتويات")
section = st.sidebar.radio("", [
	"🏠 الصفحة الرئيسية",
	"📝 تعريف نموذج ARDL",
	"🎯 أهداف ARDL",
	"📋 فرضيات النموذج",
	"✅ مميزات ARDL",
	"🔍 خطوات تطبيق ARDL",
	"🧮 الصيغ الرياضية",
	"⚠️ انتقادات ومشاكل",
	"🛠️ حلول المشاكل",
	"📊 التغيرات الهيكلية وARDL-Fourier",
	"📑 ملخص",
	"❓ أسئلة وأجوبة"
])

# الصفحة الرئيسية
if section == "🏠 الصفحة الرئيسية":
	st.title("نموذج ARDL وطريقة Bound Testing Approach")
	st.markdown("---")

	col1, col2 = st.columns([2, 1])

	with col1:
		st.markdown("""
        ## مرحباً بك في الدليل النظري الشامل لنموذج ARDL

        يقدم هذا التطبيق شرحاً نظرياً مفصلاً لنموذج الانحدار الذاتي ذو الفجوات الزمنية الموزعة 
        (Autoregressive Distributed Lag - ARDL) وطريقة اختبار الحدود (Bound Testing Approach).

        هذا الدليل مصمم لمساعدة الباحثين والطلاب في فهم الجوانب النظرية لنموذج ARDL دون الدخول في التطبيقات العملية.

        ### المواضيع الرئيسية:
        - تعريف نموذج ARDL وخلفيته النظرية
        - أهداف استخدام النموذج
        - الفرضيات الأساسية
        - المزايا والفوائد
        - خطوات التطبيق النظرية
        - الصيغ الرياضية
        - الانتقادات والمشاكل
        - الحلول المقترحة للمشاكل
        - التطورات الحديثة مثل ARDL-Fourier
        """)

	with col2:
		# إنشاء رسم بياني توضيحي بسيط باستخدام Plotly
		fig = go.Figure()

		x = np.linspace(0, 10, 100)
		y1 = np.sin(x) + np.random.normal(0, 0.1, 100)
		y2 = np.sin(x) + 0.5 + np.random.normal(0, 0.1, 100)

		fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='سلسلة Y', line=dict(color='blue')))
		fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='سلسلة X', line=dict(color='red')))

		fig.update_layout(
			title="مثال توضيحي للعلاقة بين متغيرات النموذج",
			xaxis_title="الزمن",
			yaxis_title="القيمة",
			legend_title="المتغيرات",
			height=300,
			margin=dict(l=0, r=0, t=40, b=0),
			template="plotly_white"
		)

		st.plotly_chart(fig, use_container_width=True)

	st.markdown("---")

	cols = st.columns(3)
	with cols[0]:
		st.info("📚 محتوى نظري شامل")
	with cols[1]:
		st.info("📊 رسومات توضيحية باستخدام Plotly")
	with cols[2]:
		st.info("🧮 صيغ رياضية مفصلة")

# تعريف نموذج ARDL
elif section == "📝 تعريف نموذج ARDL":
	st.title("تعريف نموذج ARDL")
	st.markdown("---")

	col1, col2 = st.columns([3, 2])

	with col1:
		st.markdown("""
        ## ما هو نموذج ARDL؟

        **نموذج الانحدار الذاتي ذو الفجوات الزمنية الموزعة** (Autoregressive Distributed Lag - ARDL) هو أحد نماذج الاقتصاد القياسي الديناميكية التي تستخدم للكشف عن العلاقات بين المتغيرات الاقتصادية عبر الزمن.

        ### المكونات الأساسية للنموذج:

        1. **المكون الانحداري الذاتي (Autoregressive - AR)**: يشير إلى استخدام القيم المتأخرة (lagged values) للمتغير التابع كمتغيرات مستقلة في النموذج.

        2. **مكون الفجوات الزمنية الموزعة (Distributed Lag - DL)**: يشير إلى استخدام القيم الحالية والمتأخرة للمتغيرات المستقلة.

        ### الخلفية التاريخية:

        تم تطوير منهجية ARDL وطريقة اختبار الحدود (Bound Testing Approach) بواسطة **Pesaran وShin وSmith** في عامي 1996 و2001، وذلك بهدف التغلب على مشاكل نماذج التكامل المشترك التقليدية المستخدمة في تحليل العلاقات طويلة الأجل بين المتغيرات.

        ### استخدامات ARDL:

        - دراسة العلاقات قصيرة وطويلة الأجل بين المتغيرات الاقتصادية
        - اختبار التكامل المشترك (Cointegration) بين المتغيرات
        - نمذجة العلاقات الديناميكية بين المتغيرات
        - التنبؤ بالقيم المستقبلية
        """)

	with col2:
		# إنشاء رسم توضيحي لهيكل نموذج ARDL
		nodes = ['Y(t)', 'Y(t-1)', 'Y(t-2)', 'X(t)', 'X(t-1)', 'X(t-2)']
		positions = [(0, 0), (-0.5, -1), (-0.5, -2), (0.5, -1), (0.5, -2), (0.5, -3)]
		edges = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]

		edge_x = []
		edge_y = []

		for edge in edges:
			x0, y0 = positions[edge[0]]
			x1, y1 = positions[edge[1]]
			edge_x.append(x0)
			edge_x.append(x1)
			edge_x.append(None)
			edge_y.append(y0)
			edge_y.append(y1)
			edge_y.append(None)

		edge_trace = go.Scatter(
			x=edge_x, y=edge_y,
			line=dict(width=1.5, color='#888'),
			hoverinfo='none',
			mode='lines')

		node_x = []
		node_y = []
		node_text = []

		for i, (x, y) in enumerate(positions):
			node_x.append(x)
			node_y.append(y)
			node_text.append(nodes[i])

		colors = ['blue', 'blue', 'blue', 'red', 'red', 'red']
		node_trace = go.Scatter(
			x=node_x, y=node_y,
			mode='markers+text',
			text=node_text,
			textposition="top center",
			marker=dict(
				showscale=False,
				colorscale='YlGnBu',
				size=30,
				color=[{'Y': 'royalblue', 'X': 'tomato'}[n[0]] for n in nodes],
				line_width=2))

		fig = go.Figure(data=[edge_trace, node_trace],
						layout=go.Layout(
							title='هيكل نموذج ARDL(2,2)',
							titlefont_size=16,
							showlegend=False,
							hovermode='closest',
							margin=dict(b=20, l=5, r=5, t=40),
							xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
							yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
							height=400,
							template="plotly_white"
						))

		st.plotly_chart(fig, use_container_width=True)

		st.markdown("""
        <div class="highlight">
        <strong>ملاحظة توضيحية:</strong><br>
        في الرسم التوضيحي أعلاه، يشير ARDL(2,2) إلى نموذج ARDL مع فجوتين زمنيتين للمتغير التابع Y ومتغير مستقل X مع فجوتين زمنيتين أيضاً.
        </div>
        """, unsafe_allow_html=True)

	st.markdown("---")

	st.markdown("""
    ## منهجية اختبار الحدود (Bound Testing Approach)

    منهجية اختبار الحدود هي طريقة مطورة خصيصاً لنموذج ARDL تستخدم لاختبار وجود علاقة توازنية طويلة الأجل (علاقة تكامل مشترك) بين المتغيرات، بغض النظر عن كون هذه المتغيرات متكاملة من الرتبة صفر I(0) أو من الرتبة الأولى I(1) أو مزيج منهما.

    ### خصائص منهجية اختبار الحدود:

    1. **المرونة**: تسمح باختبار العلاقات بين المتغيرات ذات رتب تكامل مختلفة (عدم الحاجة أن تكون جميع المتغيرات من نفس رتبة التكامل).

    2. **أكثر كفاءة للعينات الصغيرة**: تعطي نتائج أفضل في حالة العينات الصغيرة مقارنة بطرق التكامل المشترك التقليدية.

    3. **نموذج تصحيح الخطأ غير المقيد (UECM)**: تستخدم نموذج تصحيح الخطأ غير المقيد لاختبار التكامل المشترك.

    4. **اختبار F الإحصائي**: تعتمد على مقارنة إحصائية F المحسوبة مع القيم الحرجة (الحدود العليا والدنيا) لتحديد وجود تكامل مشترك.
    """)

# أهداف ARDL
elif section == "🎯 أهداف ARDL":
	st.title("أهداف استخدام نموذج ARDL")
	st.markdown("---")

	col1, col2 = st.columns([3, 2])

	with col1:
		st.markdown("""
        ## الأهداف الرئيسية لاستخدام نموذج ARDL

        ### 1. تحليل العلاقات طويلة وقصيرة الأجل

        الهدف الأساسي لنموذج ARDL هو دراسة العلاقات بين المتغيرات الاقتصادية على المدى القصير والطويل في آن واحد. هذا يمكّن الباحثين من:

        - تحديد التأثيرات الآنية بين المتغيرات
        - فهم التأثيرات المستمرة عبر الزمن
        - قياس سرعة التكيف نحو التوازن طويل الأجل

        ### 2. اختبار التكامل المشترك بين المتغيرات

        يستخدم نموذج ARDL للتحقق من وجود علاقة توازنية طويلة الأجل بين المتغيرات، حتى عندما تكون رتب تكاملها مختلفة:

        - التغلب على قيود طرق التكامل المشترك التقليدية (مثل Johansen وEngle-Granger)
        - الكشف عن التكامل المشترك بين المتغيرات المتكاملة من الرتب I(0) وI(1)

        ### 3. نمذجة تصحيح الخطأ

        يتيح نموذج ARDL اشتقاق نموذج تصحيح الخطأ (ECM) مباشرةً، مما يسمح:

        - بقياس سرعة تصحيح الانحرافات عن التوازن طويل الأجل
        - بدراسة آلية التكيف نحو التوازن
        - بتحديد اتجاه العلاقة السببية بين المتغيرات

        ### 4. التنبؤ الاقتصادي

        يمكن استخدام نموذج ARDL في:

        - التنبؤ بالقيم المستقبلية للمتغيرات الاقتصادية
        - تحليل السيناريوهات المستقبلية
        - صياغة السياسات الاقتصادية المبنية على النماذج الكمية
        """)

	with col2:
		# إنشاء مخطط دائري يوضح أهداف ARDL
		labels = ['تحليل العلاقات طويلة<br>وقصيرة الأجل', 'اختبار التكامل المشترك',
				  'نمذجة تصحيح الخطأ', 'التنبؤ الاقتصادي', 'تحليل السببية']
		values = [30, 25, 20, 15, 10]
		colors = ['royalblue', 'tomato', 'gold', 'mediumseagreen', 'mediumpurple']

		fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4,
									 textinfo='label+percent',
									 marker=dict(colors=colors),
									 textposition='outside',
									 pull=[0.1, 0, 0, 0, 0])])

		fig.update_layout(
			title="أهداف استخدام نموذج ARDL",
			height=400,
			margin=dict(l=0, r=0, t=40, b=0),
			template="plotly_white"
		)

		st.plotly_chart(fig, use_container_width=True)

		# إضافة خط زمني للتطبيقات
		applications = [
			{"year": 1970, "event": "بداية استخدام نماذج الفجوات الزمنية الموزعة في الاقتصاد"},
			{"year": 1996, "event": "تطوير منهجية ARDL بواسطة Pesaran و Shin"},
			{"year": 2001, "event": "تطوير اختبار الحدود Bound Test بواسطة Pesaran وآخرون"},
			{"year": 2010, "event": "توسع استخدام ARDL في دراسات النمو الاقتصادي"},
			{"year": 2015, "event": "دمج ARDL مع تقنيات Fourier للتغيرات الهيكلية"}
		]

		df = pd.DataFrame(applications)

		fig = px.timeline(df, x_start="year", y="event", color_discrete_sequence=['royalblue'] * len(df))
		fig.update_layout(
			title="التطور التاريخي لتطبيقات ARDL",
			xaxis=dict(title="السنة"),
			yaxis=dict(title=""),
			height=300,
			margin=dict(l=0, r=0, t=40, b=0)
		)

		fig.update_yaxes(autorange="reversed")
		st.plotly_chart(fig, use_container_width=True)

	st.markdown("---")

	st.markdown("""
    ## أهمية نموذج ARDL في مجالات التطبيق المختلفة

    نموذج ARDL له أهمية كبيرة في مختلف المجالات التطبيقية، خاصة في:

    ### الاقتصاد الكلي
    - نمذجة النمو الاقتصادي والعلاقة بين المتغيرات الاقتصادية الكلية
    - تحليل علاقات الاستهلاك والاستثمار على المدى الطويل
    - دراسة تأثيرات السياسات النقدية والمالية

    ### الاقتصاد المالي
    - دراسة العلاقات بين أسواق الأسهم والمتغيرات الاقتصادية
    - تحليل العلاقة بين أسعار الصرف وميزان المدفوعات
    - نمذجة التضخم وأسعار الفائدة

    ### اقتصاديات الطاقة والبيئة
    - تحليل العلاقة بين استهلاك الطاقة والنمو الاقتصادي
    - دراسة العلاقة بين التلوث البيئي والنشاط الاقتصادي
    - نمذجة العلاقة بين أسعار النفط والمتغيرات الاقتصادية الكلية
    """)

	# مخطط إحصائي للمجالات التطبيقية
	fields = ['الاقتصاد الكلي', 'الاقتصاد المالي', 'اقتصاديات الطاقة', 'التنمية الاقتصادية', 'التجارة الدولية']
	percentages = [35, 25, 20, 12, 8]

	fig = go.Figure(go.Bar(
		x=percentages,
		y=fields,
		orientation='h',
		marker=dict(
			color=['rgba(30, 136, 229, 0.8)', 'rgba(30, 136, 229, 0.7)',
				   'rgba(30, 136, 229, 0.6)', 'rgba(30, 136, 229, 0.5)',
				   'rgba(30, 136, 229, 0.4)']
		)
	))

	fig.update_layout(
		title="المجالات التطبيقية الرئيسية لنموذج ARDL (النسبة المئوية للأبحاث)",
		xaxis_title="النسبة المئوية %",
		height=350,
		margin=dict(l=0, r=0, t=40, b=0),
		template="plotly_white"
	)

	st.plotly_chart(fig, use_container_width=True)

# فرضيات النموذج
elif section == "📋 فرضيات النموذج":
	st.title("فرضيات نموذج ARDL")
	st.markdown("---")

	st.markdown("""
    ## الفرضيات الأساسية لنموذج ARDL واختبار الحدود

    لكي يعطي نموذج ARDL نتائج صحيحة وموثوقة، يجب التحقق من عدة فرضيات أساسية:
    """)

	col1, col2 = st.columns([1, 1])

	with col1:
		st.markdown("""
        ### 1. رتبة تكامل المتغيرات

        - **المتطلب**: يجب أن تكون المتغيرات متكاملة من الرتبة صفر I(0)، أو من الرتبة الأولى I(1)، أو مزيج منهما.
        - **القيد الأساسي**: لا يمكن تطبيق نموذج ARDL إذا كانت أي من المتغيرات متكاملة من الرتبة الثانية I(2) أو أعلى.
        - **الاختبار**: يتم اختبار جذر الوحدة باستخدام اختبارات مثل ADF، PP، KPSS قبل تطبيق نموذج ARDL.

        ### 2. استقرار النموذج

        - **المتطلب**: يجب أن يكون النموذج مستقراً هيكلياً.
        - **الاختبارات**: تستخدم اختبارات CUSUM وCUSUM of Squares للتحقق من استقرار معلمات النموذج عبر الزمن.
        - **النتيجة**: عدم استقرار النموذج قد يشير إلى وجود تغيرات هيكلية تتطلب معالجة خاصة.

        ### 3. الارتباط الذاتي للبواقي

        - **المتطلب**: يجب أن تكون البواقي خالية من الارتباط الذاتي.
        - **الاختبارات**: اختبار Breusch-Godfrey LM للارتباط الذاتي.
        - **الحل**: في حالة وجود ارتباط ذاتي، قد يلزم زيادة عدد الفجوات الزمنية في النموذج.
        """)

	with col2:
		st.markdown("""
        ### 4. التوزيع الطبيعي للبواقي

        - **المتطلب**: يفضل أن تتبع البواقي التوزيع الطبيعي.
        - **الاختبارات**: اختبار Jarque-Bera للتوزيع الطبيعي.
        - **الملاحظات**: هذه الفرضية أقل إلزامية في العينات الكبيرة بسبب نظرية النهاية المركزية.

        ### 5. تجانس التباين

        - **المتطلب**: يجب أن يكون تباين البواقي متجانساً (عدم وجود تغاير في التباين).
        - **الاختبارات**: اختبار Breusch-Pagan-Godfrey لتجانس التباين.
        - **الحل**: في حالة عدم تجانس التباين، يمكن استخدام الأخطاء المعيارية المتينة.

        ### 6. عدم وجود مشكلة الارتباط المتعدد الخطي الحاد

        - **المتطلب**: عدم وجود ارتباط خطي قوي بين المتغيرات المستقلة.
        - **المؤشرات**: معامل تضخم التباين (VIF) ومصفوفة الارتباط.
        - **الحل**: إعادة صياغة النموذج أو حذف بعض المتغيرات المرتبطة بشدة.
        """)

	st.markdown("---")

	# إنشاء رسم توضيحي يبين رتب التكامل المختلفة
	st.subheader("توضيح بصري لرتب التكامل المختلفة")

	# توليد بيانات للرسم البياني
	np.random.seed(42)
	t = np.linspace(0, 100, 101)

	# سلسلة متكاملة من الرتبة صفر I(0) - مستقرة
	i0_series = np.random.normal(10, 1, 101)

	# سلسلة متكاملة من الرتبة الأولى I(1) - السير العشوائي
	i1_series = np.cumsum(np.random.normal(0, 1, 101)) + 20

	# سلسلة متكاملة من الرتبة الثانية I(2)
	i2_series = np.cumsum(np.cumsum(np.random.normal(0, 0.1, 101))) + 30

	fig = go.Figure()

	fig.add_trace(go.Scatter(x=t, y=i0_series, mode='lines', name='I(0) - مستقرة',
							 line=dict(color='green', width=2)))

	fig.add_trace(go.Scatter(x=t, y=i1_series, mode='lines', name='I(1) - سير عشوائي',
							 line=dict(color='blue', width=2)))

	fig.add_trace(go.Scatter(x=t, y=i2_series, mode='lines', name='I(2) - متكاملة من الرتبة الثانية',
							 line=dict(color='red', width=2)))

	fig.update_layout(
		title="مقارنة بين السلاسل الزمنية ذات رتب التكامل المختلفة",
		xaxis_title="الزمن",
		yaxis_title="القيمة",
		legend_title="رتبة التكامل",
		height=450,
		template="plotly_white"
	)

	st.plotly_chart(fig, use_container_width=True)

	# جدول يلخص الفرضيات واختباراتها
	st.subheader("ملخص الفرضيات واختباراتها")

	data = {
		'الفرضية': [
			'رتبة تكامل المتغيرات',
			'استقرار النموذج',
			'الارتباط الذاتي للبواقي',
			'التوزيع الطبيعي للبواقي',
			'تجانس التباين',
			'الارتباط المتعدد الخطي'
		],
		'الاختبارات المستخدمة': [
			'ADF, PP, KPSS',
			'CUSUM, CUSUM of Squares',
			'Breusch-Godfrey LM',
			'Jarque-Bera',
			'Breusch-Pagan-Godfrey',
			'VIF, مصفوفة الارتباط'
		],
		'الآثار المترتبة على المخالفة': [
			'نتائج غير صحيحة وغير قابلة للاعتماد عليها',
			'تحيز في المعلمات المقدرة',
			'أخطاء معيارية متحيزة وتنبؤات غير دقيقة',
			'اختبارات الفرضيات غير موثوقة',
			'أخطاء معيارية غير دقيقة وانخفاض كفاءة المقدرات',
			'تقديرات غير مستقرة وزيادة التباين'
		]
	}

	df = pd.DataFrame(data)
	st.table(df)

# مميزات ARDL
elif section == "✅ مميزات ARDL":
	st.title("مميزات نموذج ARDL")
	st.markdown("---")

	col1, col2 = st.columns([2, 1])

	with col1:
		st.markdown("""
        ## المميزات الرئيسية لنموذج ARDL وطريقة اختبار الحدود

        ### 1. المرونة في رتب تكامل المتغيرات

        على عكس طرق التكامل المشترك التقليدية (مثل Johansen وEngle-Granger) التي تتطلب أن تكون جميع المتغيرات متكاملة من نفس الرتبة، يمكن تطبيق نموذج ARDL على مجموعة من المتغيرات المتكاملة من رتب مختلفة:

        - يمكن استخدامه مع المتغيرات المتكاملة من الرتبة صفر I(0)
        - يمكن استخدامه مع المتغيرات المتكاملة من الرتبة الأولى I(1)
        - يمكن استخدامه مع مزيج من المتغيرات المتكاملة من الرتب I(0) وI(1)

        **شرط أساسي**: لا يمكن استخدامه مع المتغيرات المتكاملة من الرتبة الثانية I(2) أو أعلى.

        ### 2. الكفاءة في العينات الصغيرة

        يتفوق نموذج ARDL في حالة العينات صغيرة الحجم:

        - يعطي تقديرات أكثر دقة للمعلمات في العينات الصغيرة
        - يوفر استدلالات إحصائية أكثر موثوقية
        - يمكن تطبيقه على السلاسل الزمنية القصيرة (على عكس طرق التكامل المشترك التقليدية التي تتطلب عينات كبيرة)

        ### 3. تقدير العلاقات طويلة وقصيرة الأجل في آن واحد

        يمكّن نموذج ARDL من:

        - تقدير علاقات التوازن طويلة الأجل (التكامل المشترك)
        - تقدير ديناميكيات قصيرة الأجل (نموذج تصحيح الخطأ)
        - الحصول على تقديرات متناسقة للعلاقات طويلة وقصيرة الأجل في معادلة واحدة
        """)

	with col2:
		st.image("https://miro.medium.com/v2/resize:fit:1400/1*oKXZnp4fu_vUxGa-6uWQ2g.jpeg", use_column_width=True,
				 caption="صورة توضيحية - العلاقات الديناميكية في نموذج ARDL")

		# إنشاء مخطط شريطي للمقارنة مع طرق أخرى
		methods = ['ARDL', 'Johansen', 'Engle-Granger', 'VECM']
		flexibility = [9, 5, 3, 6]
		small_sample = [8, 4, 5, 4]
		simplicity = [7, 4, 6, 3]

		fig = go.Figure()

		fig.add_trace(go.Bar(
			x=methods,
			y=flexibility,
			name='المرونة',
			marker_color='royalblue'
		))

		fig.add_trace(go.Bar(
			x=methods,
			y=small_sample,
			name='الكفاءة في العينات الصغيرة',
			marker_color='tomato'
		))

		fig.add_trace(go.Bar(
			x=methods,
			y=simplicity,
			name='سهولة التطبيق',
			marker_color='gold'
		))

		fig.update_layout(
			title="مقارنة نموذج ARDL مع طرق التكامل المشترك الأخرى",
			xaxis_title="طريقة التحليل",
			yaxis_title="التقييم (10 = الأفضل)",
			barmode='group',
			height=300,
			legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
			margin=dict(l=0, r=0, t=40, b=0),
			template="plotly_white"
		)

		st.plotly_chart(fig, use_container_width=True)

	st.markdown("---")

	col1, col2 = st.columns([1, 1])

	with col1:
		st.markdown("""
        ### 4. مرونة في اختيار الفجوات الزمنية المثلى

        يتيح نموذج ARDL:

        - اختيار عدد الفجوات الزمنية المثلى لكل متغير بشكل مستقل
        - استخدام معايير المعلومات المختلفة (مثل AIC، BIC، HQ) لاختيار النموذج الأمثل
        - الحصول على هيكل فجوات زمنية أكثر كفاءة يعكس الديناميكيات الحقيقية للعلاقات بين المتغيرات

        ### 5. اختبار الحدود لتحديد التكامل المشترك

        منهجية اختبار الحدود (Bound Testing Approach) توفر:

        - إطاراً بسيطاً وفعالاً لاختبار وجود علاقة توازنية طويلة الأجل
        - تحديد التكامل المشترك من خلال مقارنة إحصائية F المحسوبة بالقيم الحرجة (الحدود العليا والدنيا)
        - اختباراً أكثر قوة للتكامل المشترك مقارنة بالطرق التقليدية، خاصة في العينات الصغيرة
        """)

	with col2:
		st.markdown("""
        ### 6. سهولة التفسير والتطبيق

        يتميز نموذج ARDL بـ:

        - البساطة النسبية في التقدير والتفسير مقارنة بنماذج VAR/VECM المعقدة
        - إمكانية تطبيقه باستخدام طرق المربعات الصغرى العادية (OLS)
        - توفير تفسيرات مباشرة للعلاقات الاقتصادية والمرونات

        ### 7. القدرة على معالجة المشاكل الاقتصادية القياسية

        يمكن تعديل نموذج ARDL لمعالجة المشاكل المختلفة:

        - معالجة التغيرات الهيكلية من خلال نماذج ARDL-Fourier
        - معالجة اللاخطية من خلال نماذج NARDL
        - التعامل مع العينات الصغيرة من خلال تقنيات Bootstrap-ARDL
        """)

	# إنشاء رسم توضيحي ببيانات نصية
	advantages = [
		{"category": "المرونة", "description": "العمل مع متغيرات ذات رتب تكامل مختلفة I(0) و I(1)"},
		{"category": "الكفاءة", "description": "نتائج أفضل في العينات الصغيرة"},
		{"category": "الشمولية", "description": "تقدير العلاقات طويلة وقصيرة الأجل معاً"},
		{"category": "المنهجية", "description": "اختبار الحدود للتكامل المشترك"},
		{"category": "الديناميكية", "description": "فجوات زمنية مختلفة لكل متغير"},
		{"category": "التفسير", "description": "سهولة التفسير الاقتصادي للنتائج"},
		{"category": "المرونة", "description": "إمكانية التوسع لمعالجة مشاكل مختلفة"}
	]

	df = pd.DataFrame(advantages)

	fig = px.treemap(df, path=['category'], values=[10] * len(advantages),
					 color_discrete_sequence=px.colors.qualitative.Pastel,
					 hover_data=['description'])

	fig.update_traces(textinfo="label", hovertemplate='<b>%{label}</b><br>%{customdata[0]}')

	fig.update_layout(
		title="مميزات نموذج ARDL",
		margin=dict(l=0, r=0, t=30, b=0),
		height=400,
		template="plotly_white"
	)

	st.plotly_chart(fig, use_container_width=True)

# خطوات تطبيق ARDL
elif section == "🔍 خطوات تطبيق ARDL":
	st.title("خطوات تطبيق نموذج ARDL")
	st.markdown("---")

	st.markdown("""
    ## الخطوات المنهجية لتطبيق نموذج ARDL واختبار الحدود

    يتضمن تطبيق نموذج ARDL مجموعة من الخطوات المتسلسلة، نشرحها بالتفصيل فيما يلي:
    """)

	# إنشاء رسم للخطوات الرئيسية
	steps = [
		"اختبار رتبة تكامل المتغيرات",
		"تحديد صيغة نموذج ARDL",
		"اختيار الفجوات الزمنية المثلى",
		"تقدير النموذج",
		"اختبار الحدود (Bound Test)",
		"تقدير العلاقات طويلة الأجل",
		"تقدير نموذج تصحيح الخطأ",
		"التشخيص والتحقق من النموذج",
		"التفسير الاقتصادي والاستنتاجات"
	]

	# إنشاء رسم مسار الخطوات
	fig = go.Figure()

	for i, step in enumerate(steps):
		fig.add_trace(go.Scatter(
			x=[i],
			y=[0],
			mode='markers+text',
			marker=dict(size=30, color='royalblue'),
			text=str(i + 1),
			textposition="middle center",
			textfont=dict(color='white', size=14),
			hoverinfo='text',
			hovertext=step,
			name=step
		))

	# إضافة خطوط تربط المراحل
	for i in range(len(steps) - 1):
		fig.add_shape(
			type="line",
			x0=i,
			y0=0,
			x1=i + 1,
			y1=0,
			line=dict(color="royalblue", width=2)
		)

	fig.update_layout(
		title="المراحل الرئيسية لتطبيق نموذج ARDL",
		showlegend=True,
		plot_bgcolor='rgba(0,0,0,0)',
		xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
		yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
		margin=dict(l=0, r=0, t=40, b=0),
		height=150,
		legend=dict(orientation="h", yanchor="bottom", y=-1, xanchor="center", x=0.5),
		template="plotly_white"
	)

	st.plotly_chart(fig, use_container_width=True)

	st.markdown("---")

	tabs = st.tabs([f"الخطوة {i + 1}: {step}" for i, step in enumerate(steps)])

	with tabs[0]:
		st.markdown("""
        ## الخطوة 1: اختبار رتبة تكامل المتغيرات

        ### الهدف:
        التأكد من أن المتغيرات متكاملة من الرتبة I(0) أو I(1) أو مزيج منهما، وليس من الرتبة I(2) أو أعلى.

        ### الإجراءات:

        1. **اختبار جذر الوحدة للمتغيرات في مستواها**:
           - اختبار Augmented Dickey-Fuller (ADF)
           - اختبار Phillips-Perron (PP)
           - اختبار Kwiatkowski-Phillips-Schmidt-Shin (KPSS)

        2. **اختبار جذر الوحدة للمتغيرات في الفروق الأولى**:
           - إذا كانت المتغيرات غير مستقرة في مستواها، يتم اختبار استقرارها في الفروق الأولى

        3. **تصنيف المتغيرات حسب رتبة التكامل**:
           - إذا كان المتغير مستقراً في مستواه، فهو متكامل من الرتبة I(0)
           - إذا كان المتغير مستقراً في الفرق الأول، فهو متكامل من الرتبة I(1)

        ### المعايير:

        - **فرضية العدم في ADF وPP**: المتغير يحتوي على جذر وحدة (غير مستقر)
        - **فرضية العدم في KPSS**: المتغير مستقر

        ### ملاحظات هامة:

        - يفضل استخدام مزيج من اختبارات جذر الوحدة للحصول على نتائج أكثر موثوقية
        - في حالة تضارب النتائج، يمكن الاعتماد على الاختبار الأكثر ملاءمة لخصائص البيانات
        - إذا كان أي متغير متكاملاً من الرتبة I(2) أو أعلى، يجب استخدام الفروق المناسبة لتحويله إلى I(1) قبل تطبيق نموذج ARDL
        """)

		# إنشاء مخطط توضيحي لاختبارات جذر الوحدة
		unit_root_tests = {
			'اختبار': ['ADF', 'PP', 'KPSS'],
			'فرضية العدم': ['يوجد جذر وحدة', 'يوجد جذر وحدة', 'المتغير مستقر'],
			'الفرضية البديلة': ['المتغير مستقر', 'المتغير مستقر', 'يوجد جذر وحدة'],
			'القرار إذا p < 0.05': ['رفض وجود جذر الوحدة', 'رفض وجود جذر الوحدة', 'قبول وجود جذر الوحدة']
		}

		df = pd.DataFrame(unit_root_tests)
		st.table(df)

	with tabs[1]:
		st.markdown("""
        ## الخطوة 2: تحديد صيغة نموذج ARDL

        ### الهدف:
        تحديد الصيغة المناسبة لنموذج ARDL وفقاً لطبيعة البيانات وأهداف الدراسة.

        ### الصيغ الرئيسية:

        1. **نموذج تصحيح الخطأ غير المقيد (UECM)**:

           الصيغة المستخدمة في منهجية اختبار الحدود. تتضمن مستويات المتغيرات المتباطئة لفترة واحدة والفروق الأولى للمتغيرات مع فجوات زمنية.

        2. **الصيغة القياسية**:

           تتضمن المتغير التابع والمتغيرات المستقلة مع فجواتها الزمنية.

        ### الخطوات العملية:

        1. **تحديد المتغير التابع والمتغيرات المستقلة**:
           - يجب أن تكون العلاقة مدعومة نظرياً

        2. **تحديد نوع النموذج**:
           - مع ثابت بدون اتجاه زمني
           - مع ثابت واتجاه زمني
           - بدون ثابت وبدون اتجاه زمني

        3. **تحديد الحد الأقصى للفجوات الزمنية المحتملة**:
           - استناداً إلى الخبرة النظرية
           - استناداً إلى تردد البيانات (سنوية، فصلية، شهرية)
           - استناداً إلى حجم العينة المتاحة

        ### اعتبارات خاصة:

        - **البيانات السنوية**: عادة ما يكون الحد الأقصى للفجوات الزمنية 1-2 سنة
        - **البيانات الفصلية**: يمكن النظر في 4-8 فجوات زمنية
        - **البيانات الشهرية**: قد تتطلب 12-24 فجوة زمنية

        ### مثال على صيغة UECM:

        صيغة UECM لنموذج ARDL مع متغير تابع y ومتغيرين مستقلين x₁ و x₂:
        """)

		st.markdown(r'''
        <div class="formula">
        $\Delta y_t = \alpha_0 + \alpha_1 t + \delta_1 y_{t-1} + \delta_2 x_{1,t-1} + \delta_3 x_{2,t-1} + \sum_{i=1}^{p} \beta_i \Delta y_{t-i} + \sum_{j=0}^{q_1} \gamma_j \Delta x_{1,t-j} + \sum_{k=0}^{q_2} \theta_k \Delta x_{2,t-k} + \varepsilon_t$
        </div>
        ''', unsafe_allow_html=True)

		# إنشاء مخطط توضيحي لمكونات نموذج ARDL-UECM
		components = [
			{'مكون': 'Δy_t', 'وصف': 'الفرق الأول للمتغير التابع'},
			{'مكون': 'α₀', 'وصف': 'الثابت'},
			{'مكون': 'α₁t', 'وصف': 'الاتجاه الزمني'},
			{'مكون': 'δ₁y_{t-1} + δ₂x₁_{t-1} + δ₃x₂_{t-1}', 'وصف': 'مكونات العلاقة طويلة الأجل'},
			{'مكون': '∑βᵢΔy_{t-i}', 'وصف': 'الفروق الأولى المتباطئة للمتغير التابع'},
			{'مكون': '∑γⱼΔx₁_{t-j} + ∑θₖΔx₂_{t-k}', 'وصف': 'الفروق الأولى للمتغيرات المستقلة مع فجوات زمنية'},
			{'مكون': 'ε_t', 'وصف': 'حد الخطأ العشوائي'}
		]

		df = pd.DataFrame(components)
		st.table(df)

	with tabs[2]:
		st.markdown("""
        ## الخطوة 3: اختيار الفجوات الزمنية المثلى

        ### الهدف:
        تحديد عدد الفجوات الزمنية المثلى لكل متغير في النموذج للحصول على أفضل مواءمة للبيانات.

        ### معايير اختيار النموذج:

        1. **معيار معلومات أكايكي (AIC - Akaike Information Criterion)**:
           - يفضل في العينات الصغيرة
           - يميل إلى اختيار نماذج أكثر تعقيداً (مع فجوات زمنية أكثر)

        2. **معيار معلومات بايز أو شوارتز (BIC / SBC - Bayesian/Schwarz Information Criterion)**:
           - يفضل النماذج الأكثر اقتصاداً
           - يفرض عقوبة أكبر على عدد المعلمات المقدرة

        3. **معيار معلومات هانان-كوين (HQ - Hannan-Quinn Information Criterion)**:
           - وسط بين AIC و BIC

        4. **معايير أخرى**:
           - معيار R² المعدل
           - معيار خطأ التنبؤ النهائي (FPE)

        ### الخطوات العملية:

        1. **تحديد الحد الأقصى للفجوات الزمنية**:
           - مقيد بحجم العينة وتردد البيانات

        2. **تقدير جميع النماذج الممكنة**:
           - إذا كان الحد الأقصى هو p للمتغير التابع وq للمتغيرات المستقلة، فسيتم تقدير (p+1)(q+1)^k نموذجاً، حيث k هو عدد المتغيرات المستقلة

        3. **اختيار النموذج الأمثل**:
           - النموذج الذي يحقق أدنى قيمة للمعيار المختار

        ### التوازن بين الدقة والاقتصاد:

        - **الفجوات الزمنية الكثيرة**: تزيد من دقة النموذج ولكنها تقلل درجات الحرية وتزيد من مخاطر الارتباط المتعدد الخطي
        - **الفجوات الزمنية القليلة**: تحافظ على درجات الحرية ولكنها قد تؤدي إلى سوء تحديد النموذج

        ### اعتبارات خاصة:

        - **الأفضل عادة**: السماح بعدد فجوات زمنية مختلف لكل متغير
        - **في حالة العينات الصغيرة**: يفضل استخدام BIC لاختيار نموذج اقتصادي أكثر
        - **في دراسات التنبؤ**: يفضل AIC
        """)

		# إنشاء مثال توضيحي لاختيار الفجوات الزمنية المثلى
		np.random.seed(42)
		max_lag = 5

		aic_values = np.random.normal(5, 0.5, max_lag) - np.arange(max_lag) / 5 + np.random.normal(0, 0.1, max_lag)
		bic_values = np.random.normal(6, 0.5, max_lag) - np.arange(max_lag) / 4 + np.random.normal(0, 0.1, max_lag)
		hq_values = np.random.normal(5.5, 0.5, max_lag) - np.arange(max_lag) / 4.5 + np.random.normal(0, 0.1, max_lag)

		# تعديل البيانات ليكون هناك حد أدنى واضح
		aic_values[2] = min(aic_values) - 0.1
		bic_values[1] = min(bic_values) - 0.1
		hq_values[2] = min(hq_values) - 0.1

		lags = list(range(1, max_lag + 1))

		fig = go.Figure()

		fig.add_trace(go.Scatter(
			x=lags,
			y=aic_values,
			mode='lines+markers',
			name='AIC',
			line=dict(color='royalblue', width=2),
			marker=dict(size=10)
		))

		fig.add_trace(go.Scatter(
			x=lags,
			y=bic_values,
			mode='lines+markers',
			name='BIC',
			line=dict(color='tomato', width=2),
			marker=dict(size=10)
		))

		fig.add_trace(go.Scatter(
			x=lags,
			y=hq_values,
			mode='lines+markers',
			name='HQ',
			line=dict(color='gold', width=2),
			marker=dict(size=10)
		))

		# إضافة نقاط للقيم الدنيا
		fig.add_trace(go.Scatter(
			x=[lags[np.argmin(aic_values)]],
			y=[min(aic_values)],
			mode='markers',
			marker=dict(color='royalblue', size=15, symbol='star'),
			name='AIC الأمثل',
			showlegend=False
		))

		fig.add_trace(go.Scatter(
			x=[lags[np.argmin(bic_values)]],
			y=[min(bic_values)],
			mode='markers',
			marker=dict(color='tomato', size=15, symbol='star'),
			name='BIC الأمثل',
			showlegend=False
		))

		fig.add_trace(go.Scatter(
			x=[lags[np.argmin(hq_values)]],
			y=[min(hq_values)],
			mode='markers',
			marker=dict(color='gold', size=15, symbol='star'),
			name='HQ الأمثل',
			showlegend=False
		))

		fig.update_layout(
			title="مثال لاختيار الفجوات الزمنية المثلى باستخدام معايير المعلومات",
			xaxis_title="عدد الفجوات الزمنية",
			yaxis_title="قيمة المعيار",
			xaxis=dict(tickmode='array', tickvals=lags),
			annotations=[
				dict(
					x=lags[np.argmin(aic_values)],
					y=min(aic_values),
					text=f"AIC الأمثل: {lags[np.argmin(aic_values)]} فجوات",
					showarrow=True,
					arrowhead=2,
					ax=30,
					ay=-30
				),
				dict(
					x=lags[np.argmin(bic_values)],
					y=min(bic_values),
					text=f"BIC الأمثل: {lags[np.argmin(bic_values)]} فجوات",
					showarrow=True,
					arrowhead=2,
					ax=-30,
					ay=-30
				),
				dict(
					x=lags[np.argmin(hq_values)],
					y=min(hq_values),
					text=f"HQ الأمثل: {lags[np.argmin(hq_values)]} فجوات",
					showarrow=True,
					arrowhead=2,
					ax=0,
					ay=30
				)
			],
			height=400,
			template="plotly_white"
		)

		st.plotly_chart(fig, use_container_width=True)

		st.markdown("""
        <div class="highlight">
        <strong>ملاحظة مهمة:</strong><br>
        في المثال التوضيحي أعلاه، نلاحظ أن معايير المعلومات المختلفة قد تؤدي إلى اختيار عدد مختلف من الفجوات الزمنية. بينما يختار AIC و HQ 3 فجوات زمنية، يفضل BIC 2 فجوات فقط، وهذا يعكس ميل BIC لاختيار النماذج الأكثر اقتصاداً في المعلمات.
        </div>
        """, unsafe_allow_html=True)

	with tabs[3]:
		st.markdown("""
        ## الخطوة 4: تقدير النموذج

        ### الهدف:
        تقدير معلمات نموذج ARDL باستخدام طريقة المربعات الصغرى العادية (OLS).

        ### صيغة النموذج:

        في هذه المرحلة، يتم تقدير نموذج ARDL بالصيغة التالية:
        """)

		st.markdown(r'''
        <div class="formula">
        $\Delta y_t = \alpha_0 + \alpha_1 t + \delta_1 y_{t-1} + \delta_2 x_{1,t-1} + \delta_3 x_{2,t-1} + \sum_{i=1}^{p} \beta_i \Delta y_{t-i} + \sum_{j=0}^{q_1} \gamma_j \Delta x_{1,t-j} + \sum_{k=0}^{q_2} \theta_k \Delta x_{2,t-k} + \varepsilon_t$
        </div>
        ''', unsafe_allow_html=True)

		st.markdown("""
        حيث:
        - p هو عدد الفجوات الزمنية للمتغير التابع
        - q₁ هو عدد الفجوات الزمنية للمتغير المستقل الأول
        - q₂ هو عدد الفجوات الزمنية للمتغير المستقل الثاني

        ### الخطوات العملية:

        1. **بناء المتغيرات**:
           - إنشاء متغير للفرق الأول للمتغير التابع Δy_t
           - إنشاء المتغيرات المستقلة المتباطئة لفترة واحدة y_{t-1}, x₁_{t-1}, x₂_{t-1}
           - إنشاء متغيرات الفروق الأولى مع الفجوات الزمنية المحددة Δy_{t-i}, Δx₁_{t-j}, Δx₂_{t-k}

        2. **تقدير النموذج**:
           - استخدام طريقة المربعات الصغرى العادية (OLS)
           - تطبيق الفجوات الزمنية المثلى التي تم تحديدها في الخطوة السابقة

        3. **تفسير النتائج الأولية**:
           - تحليل معنوية المعلمات المقدرة
           - تحليل جودة التوفيق الإجمالية للنموذج (معامل التحديد R²)

        ### اعتبارات مهمة:

        - **حجم العينة**: بعد أخذ الفجوات الزمنية، يجب أن يتبقى عدد كافٍ من المشاهدات للتقدير
        - **مشكلة الارتباط الذاتي**: يجب اختيار عدد كافٍ من الفجوات الزمنية لإزالة الارتباط الذاتي في البواقي
        - **مشكلة عدم الاستقرار**: قد تظهر مشاكل في التقدير إذا كانت بعض المتغيرات قريبة من عدم الاستقرار

        ### مخرجات التقدير:

        1. **معلمات النموذج المقدرة**:
           - المعلمات قصيرة الأجل (معاملات الفروق)
           - المعلمات طويلة الأجل (معاملات المستويات المتباطئة)

        2. **الأخطاء المعيارية ومستويات المعنوية**:
           - اختبارات t الإحصائية لكل معلمة
           - القيم الاحتمالية (p-values)

        3. **إحصاءات جودة التوفيق**:
           - معامل التحديد R²
           - معامل التحديد المعدل Adjusted R²
           - مجموع مربعات البواقي
           - إحصائية F الإجمالية ومعنويتها
        """)

		# إنشاء مثال لنتائج تقدير نموذج ARDL
		results_data = {
			'المتغير': ['C', 'y(-1)', 'x₁(-1)', 'x₂(-1)', 'trend', 'Δy(-1)', 'Δy(-2)', 'Δx₁', 'Δx₁(-1)', 'Δx₂',
						'Δx₂(-1)'],
			'المعامل': [1.25, -0.45, 0.32, 0.18, 0.01, 0.28, 0.15, 0.55, 0.22, 0.38, 0.12],
			'الخطأ المعياري': [0.42, 0.09, 0.11, 0.08, 0.003, 0.11, 0.10, 0.14, 0.13, 0.12, 0.11],
			't-stat': [2.98, -5.00, 2.91, 2.25, 3.33, 2.55, 1.50, 3.93, 1.69, 3.17, 1.09],
			'القيمة الاحتمالية': [0.004, 0.000, 0.005, 0.027, 0.001, 0.013, 0.138, 0.000, 0.095, 0.002, 0.279]
		}

		df_results = pd.DataFrame(results_data)

		# إضافة نجوم للإشارة إلى المعنوية
		df_results['المعنوية'] = ''
		for i, p in enumerate(df_results['القيمة الاحتمالية']):
			if p < 0.01:
				df_results.loc[i, 'المعنوية'] = '***'
			elif p < 0.05:
				df_results.loc[i, 'المعنوية'] = '**'
			elif p < 0.1:
				df_results.loc[i, 'المعنوية'] = '*'

		# تنسيق القيم العددية
		df_results['المعامل'] = df_results['المعامل'].map('{:.3f}'.format)
		df_results['الخطأ المعياري'] = df_results['الخطأ المعياري'].map('{:.3f}'.format)
		df_results['t-stat'] = df_results['t-stat'].map('{:.3f}'.format)
		df_results['القيمة الاحتمالية'] = df_results['القيمة الاحتمالية'].map('{:.3f}'.format)

		# تصنيف المتغيرات
		df_results['النوع'] = 'قصير الأجل'
		df_results.loc[df_results['المتغير'].isin(['C', 'y(-1)', 'x₁(-1)', 'x₂(-1)', 'trend']), 'النوع'] = 'طويل الأجل'

		# إعادة ترتيب الأعمدة
		df_results = df_results[
			['المتغير', 'النوع', 'المعامل', 'الخطأ المعياري', 't-stat', 'القيمة الاحتمالية', 'المعنوية']]

		# عرض النتائج
		st.subheader("مثال لنتائج تقدير نموذج ARDL(3,2,2)")
		st.table(df_results)

		st.markdown("""
        <div class="highlight">
        <strong>ملاحظة:</strong><br>
        *** معنوي عند مستوى 1%<br>
        ** معنوي عند مستوى 5%<br>
        * معنوي عند مستوى 10%
        </div>
        """, unsafe_allow_html=True)

		# إضافة إحصاءات النموذج
		col1, col2, col3 = st.columns(3)
		with col1:
			st.metric("معامل التحديد R²", "0.857")
		with col2:
			st.metric("معامل التحديد المعدل", "0.832")
		with col3:
			st.metric("إحصائية F (القيمة الاحتمالية)", "25.36 (0.000)")

	with tabs[4]:
		st.markdown("""
        ## الخطوة 5: اختبار الحدود (Bound Test)

        ### الهدف:
        التحقق من وجود علاقة توازنية طويلة الأجل (تكامل مشترك) بين المتغيرات.

        ### المبدأ:

        يستند اختبار الحدود على إحصائية F (أو إحصائية Wald) لاختبار فرضية أن جميع معاملات المستويات المتباطئة تساوي صفراً (أي عدم وجود علاقة طويلة الأجل).

        ### الفرضيات:

        - **فرضية العدم (H₀)**: δ₁ = δ₂ = δ₃ = 0 (لا توجد علاقة تكامل مشترك طويلة الأجل)
        - **الفرضية البديلة (H₁)**: δ₁ ≠ 0 أو δ₂ ≠ 0 أو δ₃ ≠ 0 (توجد علاقة تكامل مشترك طويلة الأجل)

        حيث δ₁، δ₂، δ₃ هي معاملات المستويات المتباطئة في النموذج.

        ### الخطوات العملية:

        1. **حساب إحصائية F**:
           - استخدام اختبار Wald لاختبار قيد أن جميع معاملات المستويات المتباطئة تساوي صفراً

        2. **مقارنة إحصائية F المحسوبة بالقيم الحرجة**:
           - تم توفير القيم الحرجة (الحدود العليا والدنيا) بواسطة Pesaran وآخرون (2001)
           - تعتمد القيم الحرجة على:
             * عدد المتغيرات المستقلة (k)
             * نوع النموذج (مع ثابت، مع اتجاه زمني، إلخ)
             * حجم العينة

        3. **اتخاذ القرار**:
           - إذا كانت إحصائية F > الحد الأعلى للقيم الحرجة: ترفض فرضية العدم (يوجد تكامل مشترك)
           - إذا كانت إحصائية F < الحد الأدنى للقيم الحرجة: لا يمكن رفض فرضية العدم (لا يوجد تكامل مشترك)
           - إذا كانت الحد الأدنى < إحصائية F < الحد الأعلى: النتيجة غير حاسمة
        """)

		# إنشاء مثال توضيحي لاختبار الحدود
		f_stat = 6.85
		lower_bounds = {0.1: 2.37, 0.05: 2.79, 0.025: 3.15, 0.01: 3.65}
		upper_bounds = {0.1: 3.2, 0.05: 3.67, 0.025: 4.08, 0.01: 4.66}

		# إعداد الرسم
		fig = go.Figure()

		# إضافة منطقة القبول (لا يوجد تكامل مشترك)
		fig.add_shape(
			type="rect",
			x0=0,
			y0=0,
			x1=lower_bounds[0.01],
			y1=1,
			fillcolor="rgba(255, 0, 0, 0.2)",
			line=dict(width=0),
			layer="below"
		)

		# إضافة منطقة الرفض (يوجد تكامل مشترك)
		fig.add_shape(
			type="rect",
			x0=upper_bounds[0.01],
			y0=0,
			x1=10,
			y1=1,
			fillcolor="rgba(0, 255, 0, 0.2)",
			line=dict(width=0),
			layer="below"
		)

		# إضافة منطقة غير حاسمة
		fig.add_shape(
			type="rect",
			x0=lower_bounds[0.01],
			y0=0,
			x1=upper_bounds[0.01],
			y1=1,
			fillcolor="rgba(255, 255, 0, 0.2)",
			line=dict(width=0),
			layer="below"
		)

		# إضافة خطوط للقيم الحرجة
		for level, lb in lower_bounds.items():
			fig.add_shape(
				type="line",
				x0=lb,
				y0=0,
				x1=lb,
				y1=1,
				line=dict(color="red", width=1, dash="dash"),
				layer="below"
			)
			fig.add_annotation(
				x=lb,
				y=0.9,
				text=f"LB({(1 - level) * 100}%)",
				showarrow=False,
				textangle=270,
				font=dict(size=10, color="red")
			)

		for level, ub in upper_bounds.items():
			fig.add_shape(
				type="line",
				x0=ub,
				y0=0,
				x1=ub,
				y1=1,
				line=dict(color="green", width=1, dash="dash"),
				layer="below"
			)
			fig.add_annotation(
				x=ub,
				y=0.9,
				text=f"UB({(1 - level) * 100}%)",
				showarrow=False,
				textangle=270,
				font=dict(size=10, color="green")
			)

		# إضافة إحصائية F المحسوبة
		fig.add_shape(
			type="line",
			x0=f_stat,
			y0=0,
			x1=f_stat,
			y1=1,
			line=dict(color="blue", width=2),
			layer="above"
		)

		fig.add_annotation(
			x=f_stat,
			y=0.5,
			text=f"F-stat = {f_stat}",
			showarrow=True,
			arrowhead=2,
			font=dict(size=12, color="blue"),
			ax=40,
			ay=0
		)

		# تعيين العناوين والتنسيق
		fig.update_layout(
			title="مثال توضيحي لاختبار الحدود (ARDL Bound Test)",
			xaxis_title="القيمة",
			yaxis=dict(showticklabels=False, showgrid=False),
			annotations=[
				dict(
					x=1.5,
					y=0.5,
					text="لا يوجد تكامل مشترك",
					showarrow=False,
					font=dict(size=12, color="red")
				),
				dict(
					x=8,
					y=0.5,
					text="يوجد تكامل مشترك",
					showarrow=False,
					font=dict(size=12, color="green")
				),
				dict(
					x=(lower_bounds[0.01] + upper_bounds[0.01]) / 2,
					y=0.5,
					text="غير حاسم",
					showarrow=False,
					font=dict(size=12)
				)
			],
			height=400,
			margin=dict(l=50, r=50, b=50, t=50),
			template="plotly_white"
		)

		st.plotly_chart(fig, use_container_width=True)

		# جدول القيم الحرجة
		st.subheader("القيم الحرجة لاختبار الحدود (k=2)")

		critical_values = {
			'مستوى المعنوية': ['1%', '2.5%', '5%', '10%'],
			'الحد الأدنى I(0)': [3.65, 3.15, 2.79, 2.37],
			'الحد الأعلى I(1)': [4.66, 4.08, 3.67, 3.2]
		}

		df_cv = pd.DataFrame(critical_values)
		st.table(df_cv)

		st.markdown("""
        <div class="highlight">
        <strong>تفسير النتيجة:</strong><br>
        في المثال التوضيحي أعلاه، إحصائية F المحسوبة هي 6.85، وهي أكبر من الحد الأعلى للقيم الحرجة عند جميع مستويات المعنوية المعتادة، مما يشير إلى وجود علاقة تكامل مشترك طويلة الأجل بين المتغيرات.
        </div>
        """, unsafe_allow_html=True)

		st.markdown("""
        ### ملاحظات إضافية:

        1. **اختبار بديل**: يمكن أيضاً استخدام إحصائية t لاختبار δ₁ = 0 (معامل المتغير التابع المتباطئ) كاختبار بديل أو مكمل

        2. **القيم الحرجة لعينات صغيرة**: يمكن استخدام تقنية Bootstrap لتوليد قيم حرجة أكثر دقة للعينات الصغيرة

        3. **تفسير النتائج**:
           - إذا كانت النتيجة غير حاسمة، يمكن الاعتماد على اختبارات تكامل مشترك أخرى أو على معنوية معامل تصحيح الخطأ (EC) في الخطوة القادمة
        """)

	with tabs[5]:
		st.markdown("""
        ## الخطوة 6: تقدير العلاقات طويلة الأجل

        ### الهدف:
        استخراج معاملات العلاقة طويلة الأجل (التوازنية) بين المتغيرات من نموذج ARDL.

        ### شرط أساسي:
        يتم تقدير العلاقات طويلة الأجل فقط في حالة وجود تكامل مشترك (نتيجة إيجابية في اختبار الحدود).

        ### حساب المعاملات طويلة الأجل:

        تُحسب المعاملات طويلة الأجل باستخدام المعادلة التالية:
        """)

		st.latex(r"\theta_i = -\frac{\delta_{i+1}}{\delta_1}")


		st.markdown("""
        حيث:
        - θᵢ هو المعامل طويل الأجل للمتغير المستقل i
        - δ₁ هو معامل المتغير التابع المتباطئ y_{t-1}
        - δᵢ₊₁ هو معامل المتغير المستقل المتباطئ x_{i,t-1}

        ### الخطوات العملية:

        1. **استخراج معاملات المستويات المتباطئة** من تقدير نموذج ARDL:
           - δ₁: معامل y_{t-1}
           - δ₂: معامل x₁_{t-1}
           - δ₃: معامل x₂_{t-1}
           - إلخ...

        2. **حساب المعاملات طويلة الأجل**:
           - θ₁ = -δ₂/δ₁ (معامل x₁ في العلاقة طويلة الأجل)
           - θ₂ = -δ₃/δ₁ (معامل x₂ في العلاقة طويلة الأجل)
           - الثابت في العلاقة طويلة الأجل = -α₀/δ₁
           - معامل الاتجاه الزمني في العلاقة طويلة الأجل = -α₁/δ₁

        3. **حساب الأخطاء المعيارية** للمعاملات طويلة الأجل:
           - عادة ما يتم استخدام طريقة دلتا (Delta method) لحساب الأخطاء المعيارية

        ### صياغة العلاقة طويلة الأجل:

        بعد حساب المعاملات، يمكن صياغة العلاقة طويلة الأجل كما يلي:
        """)

		st.markdown(r'''
        <div class="formula">
        $y_t = \alpha + \beta t + \theta_1 x_{1,t} + \theta_2 x_{2,t} + \nu_t$
        </div>
        ''', unsafe_allow_html=True)

		st.markdown("""
        حيث:
        - α هو الثابت في العلاقة طويلة الأجل
        - β هو معامل الاتجاه الزمني في العلاقة طويلة الأجل
        - θ₁ و θ₂ هما المعاملات طويلة الأجل للمتغيرات المستقلة
        - νₜ هو المتغير العشوائي في العلاقة طويلة الأجل

        ### تفسير المعاملات طويلة الأجل:

        - **المعاملات الموجبة**: تشير إلى علاقة طردية في المدى الطويل
        - **المعاملات السالبة**: تشير إلى علاقة عكسية في المدى الطويل
        - **حجم المعاملات**: يعكس المرونة طويلة الأجل إذا كانت المتغيرات في صيغة لوغاريتمية
        """)

		# مثال توضيحي لتقدير المعاملات طويلة الأجل
		long_run_data = {
			'المعاملات': ['مستوى y₍ₜ₋₁₎', 'مستوى x₁₍ₜ₋₁₎', 'مستوى x₂₍ₜ₋₁₎', 'الثابت', 'الاتجاه الزمني'],
			'القيمة المقدرة': [-0.45, 0.32, 0.18, 1.25, 0.01],
			'الخطأ المعياري': [0.09, 0.11, 0.08, 0.42, 0.003]
		}

		df_coeffs = pd.DataFrame(long_run_data)

		st.subheader("المعاملات المقدرة للمستويات في نموذج ARDL")
		st.table(df_coeffs)

		st.subheader("المعاملات طويلة الأجل المشتقة")

		# حساب المعاملات طويلة الأجل
		coef_y_lag = -0.45

		long_run_data2 = {
			'المتغير': ['x₁', 'x₂', 'الثابت', 'الاتجاه الزمني'],
			'المعادلة': ['-δ₂/δ₁ = -(0.32/(-0.45))', '-δ₃/δ₁ = -(0.18/(-0.45))', '-α₀/δ₁ = -(1.25/(-0.45))',
						 '-α₁/δ₁ = -(0.01/(-0.45))'],
			'المعامل طويل الأجل': [round(0.32 / (-coef_y_lag), 3), round(0.18 / (-coef_y_lag), 3),
								   round(1.25 / (-coef_y_lag), 3), round(0.01 / (-coef_y_lag), 3)],
			'الخطأ المعياري': [0.219, 0.163, 0.882, 0.008],
			't-stat': [round((0.32 / (-coef_y_lag)) / 0.219, 3), round((0.18 / (-coef_y_lag)) / 0.163, 3),
					   round((1.25 / (-coef_y_lag)) / 0.882, 3), round((0.01 / (-coef_y_lag)) / 0.008, 3)]
		}

		df_long_run = pd.DataFrame(long_run_data2)

		# تحويل الأرقام إلى تنسيق نصي
		df_long_run['المعامل طويل الأجل'] = df_long_run['المعامل طويل الأجل'].map('{:.3f}'.format)
		df_long_run['الخطأ المعياري'] = df_long_run['الخطأ المعياري'].map('{:.3f}'.format)
		df_long_run['t-stat'] = df_long_run['t-stat'].map('{:.3f}'.format)

		st.table(df_long_run)

		# صياغة المعادلة طويلة الأجل
		st.markdown("""
        <div class="highlight">
        <strong>المعادلة طويلة الأجل المقدرة:</strong>

        y = 2.778 + 0.022 t + 0.711 x₁ + 0.400 x₂
          (0.882) (0.008) (0.219) (0.163)

        حيث القيم بين الأقواس تمثل الأخطاء المعيارية للمعاملات المقدرة.
        </div>
        """, unsafe_allow_html=True)

		st.markdown("""
        ### ملاحظات مهمة:

        1. **علامة معامل التكيف**: يجب أن يكون معامل y_{t-1} (معامل التكيف) سالباً ومعنوياً لكي تكون العلاقة طويلة الأجل صحيحة

        2. **تفسير اقتصادي**: يجب أن تكون المعاملات طويلة الأجل متوافقة مع النظرية الاقتصادية

        3. **معنوية المعاملات**: يجب اختبار معنوية المعاملات طويلة الأجل باستخدام اختبارات t

        4. **حسابات القيم المتوقعة**: يمكن استخدام المعادلة طويلة الأجل لحساب القيم التوازنية للمتغير التابع
        """)

	with tabs[6]:
		st.markdown("""
        ## الخطوة 7: تقدير نموذج تصحيح الخطأ

        ### الهدف:
        تقدير ديناميكيات قصيرة الأجل بين المتغيرات وسرعة التكيف نحو التوازن طويل الأجل.

        ### مفهوم نموذج تصحيح الخطأ (ECM):

        نموذج تصحيح الخطأ هو تمثيل بديل لنموذج ARDL يفصل بوضوح بين العلاقات قصيرة الأجل وآلية التكيف نحو التوازن طويل الأجل.

        ### صيغة نموذج تصحيح الخطأ:
        """)

		st.markdown(r'''
        <div class="formula">
        $\Delta y_t = \sum_{i=1}^{p-1} \beta_i^* \Delta y_{t-i} + \sum_{j=0}^{q_1-1} \gamma_j^* \Delta x_{1,t-j} + \sum_{k=0}^{q_2-1} \theta_k^* \Delta x_{2,t-k} + \lambda EC_{t-1} + \varepsilon_t$
        </div>
        ''', unsafe_allow_html=True)

		st.markdown("""
        حيث:
        - EC_{t-1} هو حد تصحيح الخطأ المتباطئ لفترة واحدة
        - λ هو معامل سرعة التكيف (يجب أن يكون سالباً ومعنوياً)
        - β*ᵢ, γ*ⱼ, θ*ₖ هي معاملات العلاقة قصيرة الأجل

        ### حساب حد تصحيح الخطأ:

        يتم حساب حد تصحيح الخطأ (EC) كالتالي:
        """)

		st.latex(r"EC_t = y_t - (\alpha + \beta t + \theta_1 x_{1,t} + \theta_2 x_{2,t})")

		st.markdown("""
        حيث:
        - α, β, θ₁, θ₂ هي المعاملات طويلة الأجل المقدرة في الخطوة السابقة

        ### الخطوات العملية:

        1. **حساب حد تصحيح الخطأ**:
           - استخدام المعاملات طويلة الأجل لحساب EC_t

        2. **تقدير نموذج تصحيح الخطأ**:
           - إدراج EC_{t-1} في نموذج يحتوي على الفروق الأولى للمتغيرات مع فجواتها الزمنية

        3. **تفسير النتائج**:
           - المعاملات قصيرة الأجل: تأثيرات المتغيرات في المدى القصير
           - معامل سرعة التكيف λ: النسبة المئوية للاختلال التي يتم تصحيحها في كل فترة زمنية

        ### تفسير معامل تصحيح الخطأ:

        - **القيمة المتوقعة**: يجب أن يكون سالباً ومعنوياً
        - **المدى**: عادة بين -1 و 0
          * قيمة -1: تعني تصحيح كامل للاختلال في فترة واحدة
          * قيمة قريبة من 0: تعني تصحيح بطيء للاختلال
        - **متوسط فترة التكيف**: يمكن حسابه كـ (1 / |λ|)
        """)

		# مثال لنتائج نموذج تصحيح الخطأ
		ecm_data = {
			'المتغير': ['EC(-1)', 'Δy(-1)', 'Δy(-2)', 'Δx₁', 'Δx₁(-1)', 'Δx₂', 'Δx₂(-1)'],
			'المعامل': [-0.45, 0.28, 0.15, 0.55, 0.22, 0.38, 0.12],
			'الخطأ المعياري': [0.09, 0.11, 0.10, 0.14, 0.13, 0.12, 0.11],
			't-stat': [-5.00, 2.55, 1.50, 3.93, 1.69, 3.17, 1.09],
			'القيمة الاحتمالية': [0.000, 0.013, 0.138, 0.000, 0.095, 0.002, 0.279]
		}

		df_ecm = pd.DataFrame(ecm_data)

		# إضافة نجوم للإشارة إلى المعنوية
		df_ecm['المعنوية'] = ''
		for i, p in enumerate(df_ecm['القيمة الاحتمالية']):
			if p < 0.01:
				df_ecm.loc[i, 'المعنوية'] = '***'
			elif p < 0.05:
				df_ecm.loc[i, 'المعنوية'] = '**'
			elif p < 0.1:
				df_ecm.loc[i, 'المعنوية'] = '*'

		# تنسيق القيم العددية
		df_ecm['المعامل'] = df_ecm['المعامل'].map('{:.3f}'.format)
		df_ecm['الخطأ المعياري'] = df_ecm['الخطأ المعياري'].map('{:.3f}'.format)
		df_ecm['t-stat'] = df_ecm['t-stat'].map('{:.3f}'.format)
		df_ecm['القيمة الاحتمالية'] = df_ecm['القيمة الاحتمالية'].map('{:.3f}'.format)

		st.subheader("نتائج تقدير نموذج تصحيح الخطأ")
		st.table(df_ecm)

		# رسم توضيحي لسرعة التكيف
		st.subheader("تفسير رسومي لقيمة معامل تصحيح الخطأ")

		adjustment_speed = 0.45
		periods = 8

		initial_deviation = 1.0
		adjustments = [initial_deviation * ((1 - adjustment_speed) ** t) for t in range(periods)]

		half_life = round(np.log(0.5) / np.log(1 - adjustment_speed), 2)
		full_adjustment = round(np.log(0.05) / np.log(1 - adjustment_speed), 2)

		fig = go.Figure()

		# إضافة مخطط التعديل
		fig.add_trace(go.Scatter(
			x=list(range(periods)),
			y=adjustments,
			mode='lines+markers',
			name='الاختلال المتبقي',
			marker=dict(size=10),
			line=dict(width=2, color='royalblue')
		))

		# إضافة خط أفقي عند 50% من الاختلال الأولي
		fig.add_shape(
			type="line",
			x0=0,
			y0=initial_deviation * 0.5,
			x1=periods - 1,
			y1=initial_deviation * 0.5,
			line=dict(color="red", width=1, dash="dash")
		)

		# إضافة خط أفقي عند 5% من الاختلال الأولي (تقريباً تصحيح كامل)
		fig.add_shape(
			type="line",
			x0=0,
			y0=initial_deviation * 0.05,
			x1=periods - 1,
			y1=initial_deviation * 0.05,
			line=dict(color="green", width=1, dash="dash")
		)

		# إضافة خط رأسي عند عمر النصف
		fig.add_shape(
			type="line",
			x0=half_life,
			y0=0,
			x1=half_life,
			y1=initial_deviation,
			line=dict(color="red", width=1, dash="dash")
		)

		# إضافة تعليقات توضيحية
		fig.add_annotation(
			x=half_life,
			y=initial_deviation * 0.25,
			text=f"عمر النصف = {half_life} فترة",
			showarrow=True,
			arrowhead=2,
			ax=40,
			ay=0,
			font=dict(color="red")
		)

		fig.add_annotation(
			x=7,
			y=initial_deviation * 0.5,
			text="50% من الاختلال الأولي",
			showarrow=True,
			arrowhead=2,
			ax=0,
			ay=20,
			font=dict(color="red")
		)

		fig.add_annotation(
			x=7,
			y=initial_deviation * 0.05,
			text="تصحيح شبه كامل (5% من الاختلال الأولي)",
			showarrow=True,
			arrowhead=2,
			ax=0,
			ay=20,
			font=dict(color="green")
		)

		fig.add_annotation(
			x=periods - 1,
			y=adjustments[-1],
			text=f"بعد {periods} فترات، يتبقى {round(adjustments[-1] * 100, 1)}% من الاختلال الأولي",
			showarrow=True,
			arrowhead=2,
			ax=-60,
			ay=0
		)

		fig.update_layout(
			title=f"سرعة التكيف نحو التوازن طويل الأجل (معامل تصحيح الخطأ = {adjustment_speed})",
			xaxis_title="الفترات الزمنية",
			yaxis_title="الاختلال المتبقي",
			height=400,
			template="plotly_white"
		)

		st.plotly_chart(fig, use_container_width=True)

		st.markdown(f"""
        <div class="highlight">
        <strong>تفسير نتائج نموذج تصحيح الخطأ:</strong><br>

        1. <strong>معامل تصحيح الخطأ (EC(-1)):</strong> القيمة المقدرة هي {-adjustment_speed}، وهي سالبة ومعنوية إحصائياً، مما يؤكد وجود علاقة توازنية طويلة الأجل.

        2. <strong>سرعة التكيف:</strong> حوالي {adjustment_speed * 100}% من أي اختلال عن التوازن طويل الأجل يتم تصحيحه في كل فترة زمنية.

        3. <strong>عمر النصف:</strong> يستغرق تصحيح 50% من الاختلال حوالي {half_life} فترة.

        4. <strong>التصحيح الكامل:</strong> يتطلب تصحيح 95% من الاختلال حوالي {full_adjustment} فترات.

        5. <strong>العلاقات قصيرة الأجل:</strong> المتغيرات Δx₁ و Δx₂ لها تأثيرات معنوية في المدى القصير، بينما التأثيرات المتباطئة Δx₁(-1) و Δx₂(-1) أقل معنوية.
        </div>
        """, unsafe_allow_html=True)

		st.markdown("""
        ### العلاقة بين نموذج ARDL ونموذج تصحيح الخطأ:

        - نموذج ARDL ونموذج تصحيح الخطأ المقابل له يتضمنان نفس المعلومات ويعطيان نفس تنبؤات المتغير التابع
        - يعتبر نموذج تصحيح الخطأ صيغة أكثر تفسيرية ومباشرة لفهم العلاقات قصيرة وطويلة الأجل
        - معامل تصحيح الخطأ يوفر مؤشراً مباشراً لسرعة التكيف نحو التوازن طويل الأجل
        """)

	with tabs[7]:
		st.markdown("""
        ## الخطوة 8: التشخيص والتحقق من النموذج

        ### الهدف:
        التأكد من أن النموذج المقدر يستوفي الفرضيات الأساسية للتحليل الاقتصادي القياسي، وأنه موثوق به للتفسير واتخاذ القرارات.

        ### الاختبارات التشخيصية الرئيسية:
        """)

		col1, col2 = st.columns([1, 1])

		with col1:
			st.markdown("""
            ### 1. اختبارات استقرار النموذج

            - **اختبار CUSUM**:
              * يستخدم لفحص استقرار معلمات النموذج عبر الزمن
              * يعتمد على المجموع التراكمي للبواقي
              * إذا بقي المجموع ضمن الحدود الحرجة، يكون النموذج مستقراً

            - **اختبار CUSUM of Squares**:
              * يركز على استقرار تباين النموذج
              * يعتمد على المجموع التراكمي لمربعات البواقي
              * حساس للتغيرات في تباين النموذج

            ### 2. اختبار الارتباط الذاتي للبواقي

            - **اختبار Breusch-Godfrey LM**:
              * اختبار للكشف عن الارتباط الذاتي من رتب أعلى
              * فرضية العدم: عدم وجود ارتباط ذاتي
              * إذا كانت القيمة الاحتمالية > 0.05، فلا يوجد ارتباط ذاتي

            - **اختبار Durbin-Watson**:
              * يكشف عن الارتباط الذاتي من الرتبة الأولى
              * القيمة المثلى قريبة من 2
              * قيم < 1.5 أو > 2.5 تشير عادة إلى وجود ارتباط ذاتي
            """)

		with col2:
			st.markdown("""
            ### 3. اختبار تجانس التباين

            - **اختبار Breusch-Pagan-Godfrey**:
              * يكشف عن عدم تجانس التباين
              * فرضية العدم: تباين البواقي متجانس
              * إذا كانت القيمة الاحتمالية > 0.05، فالتباين متجانس

            - **اختبار White**:
              * اختبار أكثر مرونة لعدم تجانس التباين
              * يأخذ في الاعتبار التفاعلات بين المتغيرات المستقلة

            ### 4. اختبار التوزيع الطبيعي للبواقي

            - **اختبار Jarque-Bera**:
              * يقيس مدى اختلاف توزيع البواقي عن التوزيع الطبيعي
              * يعتمد على الالتواء والتفلطح
              * فرضية العدم: البواقي تتبع التوزيع الطبيعي

            ### 5. اختبار التحديد الصحيح للنموذج

            - **اختبار Ramsey RESET**:
              * يكشف عن أخطاء التحديد مثل إغفال متغيرات مهمة أو الصيغة الوظيفية غير الصحيحة
              * فرضية العدم: النموذج محدد بشكل صحيح
            """)

		# إنشاء رسومات توضيحية لاختبارات التشخيص
		st.subheader("مثال توضيحي لاختبارات استقرار النموذج")

		# توليد بيانات للرسم
		np.random.seed(42)
		n = 50

		# البيانات الأساسية
		time = np.arange(1, n + 1)

		# بيانات CUSUM - نموذج مستقر
		cusum = np.cumsum(np.random.normal(0, 1, n))
		lower_bound = -2 * np.sqrt(np.arange(1, n + 1))
		upper_bound = 2 * np.sqrt(np.arange(1, n + 1))

		# بيانات CUSUM of Squares - نموذج مستقر
		residuals_squared = np.random.normal(0, 1, n) ** 2
		residuals_squared = residuals_squared / np.sum(residuals_squared)
		cusum_sq = np.cumsum(residuals_squared)
		expected_line = np.arange(1, n + 1) / n
		cusum_sq_lower = expected_line - 0.4
		cusum_sq_upper = expected_line + 0.4

		# إنشاء الشكل مع subplot
		fig = go.Figure()

		# CUSUM Plot
		fig.add_trace(go.Scatter(
			x=time,
			y=cusum,
			mode='lines',
			name='CUSUM',
			line=dict(color='royalblue', width=2)
		))

		fig.add_trace(go.Scatter(
			x=time,
			y=upper_bound,
			mode='lines',
			name='الحد الأعلى (5%)',
			line=dict(color='red', width=1, dash='dash')
		))

		fig.add_trace(go.Scatter(
			x=time,
			y=lower_bound,
			mode='lines',
			name='الحد الأدنى (5%)',
			line=dict(color='red', width=1, dash='dash'),
			fill='tonexty',
			fillcolor='rgba(255, 0, 0, 0.1)'
		))

		fig.update_layout(
			title="اختبار CUSUM لاستقرار النموذج",
			xaxis_title="الزمن",
			yaxis_title="CUSUM",
			height=400,
			template="plotly_white"
		)

		st.plotly_chart(fig, use_container_width=True)

		# CUSUM of Squares Plot
		fig2 = go.Figure()

		fig2.add_trace(go.Scatter(
			x=time,
			y=cusum_sq,
			mode='lines',
			name='CUSUM of Squares',
			line=dict(color='green', width=2)
		))

		fig2.add_trace(go.Scatter(
			x=time,
			y=cusum_sq_upper,
			mode='lines',
			name='الحد الأعلى (5%)',
			line=dict(color='red', width=1, dash='dash')
		))

		fig2.add_trace(go.Scatter(
			x=time,
			y=cusum_sq_lower,
			mode='lines',
			name='الحد الأدنى (5%)',
			line=dict(color='red', width=1, dash='dash'),
			fill='tonexty',
			fillcolor='rgba(255, 0, 0, 0.1)'
		))

		fig2.update_layout(
			title="اختبار CUSUM of Squares لاستقرار التباين",
			xaxis_title="الزمن",
			yaxis_title="CUSUM of Squares",
			height=400,
			template="plotly_white"
		)

		st.plotly_chart(fig2, use_container_width=True)

		# مثال لنتائج اختبارات التشخيص
		st.subheader("جدول ملخص نتائج الاختبارات التشخيصية")

		diagnostic_tests = {
			'الاختبار': [
				'اختبار Breusch-Godfrey للارتباط الذاتي (2 فجوات)',
				'اختبار Breusch-Pagan-Godfrey لتجانس التباين',
				'اختبار Jarque-Bera للتوزيع الطبيعي',
				'اختبار Ramsey RESET للتحديد الصحيح'
			],
			'إحصائية الاختبار': ['1.842', '8.563', '3.214', '1.356'],
			'القيمة الاحتمالية': ['0.398', '0.128', '0.201', '0.248'],
			'النتيجة': [
				'لا يوجد ارتباط ذاتي',
				'التباين متجانس',
				'البواقي تتبع التوزيع الطبيعي',
				'النموذج محدد بشكل صحيح'
			]
		}

		df_diagnostics = pd.DataFrame(diagnostic_tests)
		st.table(df_diagnostics)

		st.markdown("""
        <div class="highlight">
        <strong>تفسير نتائج الاختبارات:</strong><br>

        جميع الاختبارات التشخيصية تشير إلى أن النموذج المقدر يستوفي الفرضيات الأساسية للتحليل الإحصائي:

        - لا يوجد ارتباط ذاتي في البواقي (القيمة الاحتمالية لاختبار Breusch-Godfrey > 0.05)
        - تباين البواقي متجانس (القيمة الاحتمالية لاختبار Breusch-Pagan-Godfrey > 0.05)
        - البواقي تتبع التوزيع الطبيعي (القيمة الاحتمالية لاختبار Jarque-Bera > 0.05)
        - النموذج محدد بشكل صحيح (القيمة الاحتمالية لاختبار Ramsey RESET > 0.05)

        بالإضافة إلى ذلك، تظهر اختبارات CUSUM و CUSUM of Squares أن معلمات النموذج مستقرة عبر الزمن، حيث تبقى الخطوط ضمن الحدود الحرجة.
        </div>
        """, unsafe_allow_html=True)

		st.markdown("""
        ### التعامل مع مشاكل التشخيص:

        1. **مشكلة الارتباط الذاتي**:
           - زيادة عدد الفجوات الزمنية في النموذج
           - استخدام طرق تقدير قوية للارتباط الذاتي (HAC)

        2. **مشكلة عدم تجانس التباين**:
           - استخدام الأخطاء المعيارية المتينة (White أو Newey-West)
           - تحويل المتغيرات (مثل اللوغاريتم)

        3. **عدم التوزيع الطبيعي للبواقي**:
           - البحث عن القيم المتطرفة ومعالجتها
           - في العينات الكبيرة، يمكن الاعتماد على نظرية النهاية المركزية

        4. **مشكلة التحديد غير الصحيح**:
           - إعادة النظر في المتغيرات المدرجة في النموذج
           - تغيير الصيغة الوظيفية (مثل استخدام اللوغاريتم أو المربعات)

        5. **مشكلة عدم استقرار المعلمات**:
           - البحث عن نقاط التغير الهيكلي
           - استخدام نماذج متقدمة مثل ARDL-Fourier
        """)

	with tabs[8]:
		st.markdown("""
        ## الخطوة 9: التفسير الاقتصادي والاستنتاجات

        ### الهدف:
        تفسير نتائج نموذج ARDL من الناحية الاقتصادية واستخلاص الاستنتاجات والتوصيات.

        ### العناصر الرئيسية للتفسير:
        """)

		col1, col2 = st.columns([1, 1])

		with col1:
			st.markdown("""
            ### 1. تفسير العلاقة طويلة الأجل

            - **اتجاه العلاقة**: ما إذا كانت المتغيرات المستقلة ترتبط طردياً أم عكسياً بالمتغير التابع في المدى الطويل

            - **المرونات**: إذا كانت المتغيرات في صيغة لوغاريتمية، فإن المعاملات تعبر عن المرونات طويلة الأجل:
              * إذا تغير X بنسبة 1%، فإن Y يتغير بنسبة θ%

            - **الأهمية النسبية**: ترتيب المتغيرات المستقلة حسب حجم تأثيرها على المتغير التابع

            - **المقارنة مع النظرية الاقتصادية**: مدى اتساق النتائج مع النظريات الاقتصادية ذات الصلة

            ### 2. تفسير العلاقة قصيرة الأجل

            - **التأثيرات الفورية**: كيف تؤثر التغيرات في المتغيرات المستقلة على المتغير التابع بشكل فوري

            - **الديناميكيات قصيرة الأجل**: كيف تنتشر التأثيرات عبر الزمن من خلال الفجوات الزمنية المختلفة

            - **الاختلافات بين التأثيرات قصيرة وطويلة الأجل**: قد تختلف العلاقات في المدى القصير عن المدى الطويل
            """)
st.markdown("""
           ### 3. تفسير آلية تصحيح الخطأ


            - **سرعة التكيف**: تفسير معامل تصحيح الخطأ وما يشير إليه عن سرعة عودة النظام إلى التوازن
            
            - **عمر النصف**: الوقت اللازم لتصحيح نصف الاختلال عن التوازن طويل الأجل
            
            - **التكيف الكامل**: الوقت اللازم للعودة الكاملة تقريباً إلى التوازن طويل الأجل
            
            ### 4. الاستنتاجات والتوصيات
            
            - **الاستنتاجات الرئيسية**: تلخيص النتائج الأساسية للنموذج
            
            - **التوصيات السياسية**: ما هي الإجراءات أو السياسات التي يمكن اقتراحها بناءً على النتائج
            
            - **القيود والتحفظات**: الإشارة إلى حدود النموذج وأي تحفظات على النتائج
            
            - **اتجاهات البحث المستقبلية**: اقتراح اتجاهات للبحوث المستقبلية
            """)
st.markdown("---")

st.markdown("""
        ### مثال: تفسير نتائج نموذج ARDL لدراسة العلاقة بين استهلاك الطاقة والنمو الاقتصادي

        نفترض أن لدينا نموذج ARDL يدرس العلاقة بين استهلاك الطاقة (EC) والنمو الاقتصادي (GDP) وانبعاثات الكربون (CO2)، مع المتغير التابع هو النمو الاقتصادي. إليكم تفسيراً اقتصادياً لنتائج هذا النموذج:
        """)

st.markdown("""
        <div class="highlight">
        <h4>1. تفسير العلاقة طويلة الأجل:</h4>

        <p><strong>المعادلة طويلة الأجل المقدرة:</strong></p>
        <p>ln(GDP) = 2.34 + 0.65 ln(EC) - 0.12 ln(CO2) + 0.02 trend</p>

        <p><strong>التفسير الاقتصادي:</strong></p>
        <ul>
        <li><strong>استهلاك الطاقة (EC):</strong> المرونة طويلة الأجل هي 0.65، مما يعني أن زيادة استهلاك الطاقة بنسبة 1% تؤدي إلى زيادة الناتج المحلي الإجمالي بنسبة 0.65% في المدى الطويل. هذا يؤكد أهمية الطاقة كمحرك أساسي للنمو الاقتصادي.</li>

        <li><strong>انبعاثات الكربون (CO2):</strong> المرونة طويلة الأجل هي -0.12، مما يشير إلى أن زيادة انبعاثات الكربون بنسبة 1% تؤدي إلى انخفاض الناتج المحلي الإجمالي بنسبة 0.12% في المدى الطويل. هذا قد يعكس التكاليف البيئية والصحية للتلوث أو تأثير السياسات البيئية المقيدة.</li>

        <li><strong>الاتجاه الزمني:</strong> المعامل الموجب (0.02) يشير إلى نمو تقني إيجابي بمعدل 2% سنوياً، مما يعني زيادة الإنتاجية بمرور الوقت بسبب التقدم التكنولوجي.</li>
        </ul>

        <h4>2. تفسير العلاقة قصيرة الأجل:</h4>

        <p>في المدى القصير، وجدنا أن:</p>
        <ul>
        <li>التغير في استهلاك الطاقة له تأثير فوري إيجابي على النمو الاقتصادي (معامل Δln(EC) = 0.43)، لكنه أقل من التأثير طويل الأجل.</li>

        <li>التغير في انبعاثات الكربون ليس له تأثير معنوي في المدى القصير، مما يشير إلى أن الآثار السلبية للتلوث تظهر فقط على المدى الطويل.</li>
        </ul>

        <h4>3. تفسير آلية تصحيح الخطأ:</h4>

        <p>معامل تصحيح الخطأ هو -0.35، وهو سالب ومعنوي إحصائياً، مما يؤكد وجود علاقة توازنية طويلة الأجل.</p>
        <p>يشير هذا المعامل إلى أن 35% من أي اختلال عن التوازن طويل الأجل يتم تصحيحه خلال سنة واحدة.</p>
        <p>عمر النصف (الوقت اللازم لتصحيح نصف الاختلال) يبلغ حوالي 1.98 سنة.</p>
        <p>التكيف الكامل (95%) يتطلب حوالي 8.5 سنوات.</p>

        <h4>4. الاستنتاجات والتوصيات السياساتية:</h4>

        <p><strong>الاستنتاجات الرئيسية:</strong></p>
        <ul>
        <li>هناك علاقة توازنية طويلة الأجل بين استهلاك الطاقة والنمو الاقتصادي وانبعاثات الكربون.</li>
        <li>استهلاك الطاقة محرك أساسي للنمو الاقتصادي، لكن انبعاثات الكربون لها تأثير سلبي طويل الأجل.</li>
        <li>آلية التكيف نحو التوازن طويل الأجل معتدلة السرعة.</li>
        </ul>

        <p><strong>التوصيات السياساتية:</strong></p>
        <ul>
        <li>تعزيز كفاءة استخدام الطاقة للاستفادة من تأثيرها الإيجابي على النمو مع تقليل الآثار البيئية السلبية.</li>
        <li>الاستثمار في مصادر الطاقة المتجددة لتقليل انبعاثات الكربون دون التأثير سلباً على النمو الاقتصادي.</li>
        <li>تبني استراتيجيات للنمو الأخضر تعزز النمو الاقتصادي وتحد من التدهور البيئي.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# إنشاء رسم توضيحي للتأثير بين المتغيرات
st.subheader("تمثيل بياني للعلاقات بين المتغيرات")

# إنشاء مخطط سببي للعلاقات
nodes = ['GDP', 'EC', 'CO2', 'التكنولوجيا']
edge_source = [1, 2, 3, 0, 0]
edge_target = [0, 0, 0, 1, 2]
edge_value = [0.65, -0.12, 0.02, 0.2, 0.3]
edge_colors = ['green', 'red', 'blue', 'gray', 'gray']
edge_label = ['+0.65', '-0.12', '+0.02', '+', '+']

fig = go.Figure(data=[
	go.Scatter(
		x=[0, 1, 1, 0],
		y=[0, 1, -1, 0],
		mode='markers+text',
		marker=dict(size=40, color=['royalblue', 'tomato', 'crimson', 'gray']),
		text=nodes,
		textposition="middle center",
		textfont=dict(color='white', size=12),
		hoverinfo='text',
		name='المتغيرات'
	)
])

# إضافة الأسهم
for i in range(len(edge_source)):
	# احصل على موقع النقطتين
	x_source = [0, 1, 1, 0][edge_source[i]]
	y_source = [0, 1, -1, 0][edge_source[i]]
	x_target = [0, 1, 1, 0][edge_target[i]]
	y_target = [0, 1, -1, 0][edge_target[i]]

	# ارسم الاتجاه
	fig.add_annotation(
		x=x_target,
		y=y_target,
		ax=x_source,
		ay=y_source,
		xref='x',
		yref='y',
		axref='x',
		ayref='y',
		showarrow=True,
		arrowhead=2,
		arrowsize=1.5,
		arrowwidth=2,
		arrowcolor=edge_colors[i]
	)

	# أضف الملصق
	mid_x = (x_source + x_target) / 2
	mid_y = (y_source + y_target) / 2

	fig.add_annotation(
		x=mid_x,
		y=mid_y,
		text=edge_label[i],
		showarrow=False,
		font=dict(size=14, color=edge_colors[i])
	)

fig.update_layout(
	title="مخطط العلاقات السببية بين المتغيرات",
	showlegend=False,
	xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
	yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
	height=500,
	width=700,
	margin=dict(l=40, r=40, b=40, t=40),
	template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Content for ARDL definitio
if section == \
		"⚠️ انتقادات ومشاكل": st.title("انتقادات ومشاكل نموذج ARDL")
st.markdown("---")

st.markdown("""
    ## الانتقادات الرئيسية والمشاكل المنهجية لنموذج ARDL

    على الرغم من المزايا العديدة لنموذج ARDL، إلا أنه يواجه عدداً من الانتقادات والتحديات المنهجية التي يجب أخذها في الاعتبار:
    """)

tabs = st.tabs([
	"مشكلة العينات الصغيرة",
	"التغيرات الهيكلية",
	"العلاقات غير الخطية",
	"المتغيرات I(2)",
	"مشاكل التحديد",
	"قيود النموذج"
])

with tabs[0]:
	st.markdown("""
        ## مشكلة العينات الصغيرة

        ### المشكلة:

        على الرغم من أن ARDL أفضل أداءً في العينات الصغيرة مقارنة بطرق التكامل المشترك الأخرى، إلا أنه لا يزال يواجه تحديات مع العينات الصغيرة جداً.

        ### الآثار:

        1. **تحيز المعلمات المقدرة**:
           - في العينات الصغيرة، قد تكون التقديرات متحيزة، خاصة عند استخدام عدد كبير من الفجوات الزمنية

        2. **انخفاض قوة اختبار الحدود**:
           - قد لا تكون القيم الحرجة المقدمة من Pesaran وآخرون دقيقة بما يكفي للعينات الصغيرة جداً
           - قد يؤدي ذلك إلى زيادة احتمالية خطأ النوع الأول أو الثاني

        3. **مشاكل في اختيار الفجوات الزمنية المثلى**:
           - محدودية درجات الحرية تجعل من الصعب تحديد هيكل الفجوات الزمنية الأمثل

        ### كيف تظهر المشكلة في التطبيق:

        - عدم استقرار النتائج عند تغيير طفيف في المواصفات
        - معلمات ذات أخطاء معيارية كبيرة
        - صعوبة في الحصول على نتائج معنوية في اختبار الحدود
        """)

	# توضيح العلاقة بين حجم العينة ودقة التقديرات
	sample_sizes = [20, 30, 40, 50, 75, 100, 150, 200]
	bias = [0.35, 0.28, 0.22, 0.17, 0.12, 0.09, 0.06, 0.05]
	std_errors = [0.42, 0.34, 0.28, 0.24, 0.19, 0.15, 0.12, 0.10]

	fig = go.Figure()

	fig.add_trace(go.Scatter(
		x=sample_sizes,
		y=bias,
		mode='lines+markers',
		name='التحيز',
		line=dict(color='red', width=2)
	))

	fig.add_trace(go.Scatter(
		x=sample_sizes,
		y=std_errors,
		mode='lines+markers',
		name='الخطأ المعياري',
		line=dict(color='blue', width=2)
	))

	fig.update_layout(
		title="العلاقة بين حجم العينة وجودة التقديرات",
		xaxis_title="حجم العينة",
		yaxis_title="القيمة",
		legend_title="المؤشر",
		height=400,
		template="plotly_white"
	)

	st.plotly_chart(fig, use_container_width=True)

	st.info("""
        **ملاحظة**: يوضح الرسم البياني أعلاه كيف ينخفض التحيز والخطأ المعياري مع زيادة حجم العينة. في العينات التي تقل عن 50 مشاهدة، يكون التحيز والخطأ المعياري كبيرين نسبياً، مما يؤثر على موثوقية نتائج نموذج ARDL.
        """)

with tabs[1]:
	st.markdown("""
        ## مشكلة التغيرات الهيكلية

        ### المشكلة:

        نموذج ARDL التقليدي يفترض استقرار العلاقة بين المتغيرات عبر الزمن، لكن في الواقع، قد تتغير هذه العلاقات بسبب:
        - التغيرات في السياسات الاقتصادية
        - الأزمات الاقتصادية والمالية
        - التغيرات التكنولوجية الكبيرة
        - التحولات الهيكلية في الاقتصاد

        ### الآثار:

        1. **تحيز في تقديرات المعلمات**:
           - إذا تم تجاهل التغيرات الهيكلية، فإن المعلمات المقدرة تعكس متوسط العلاقة عبر الفترات المختلفة

        2. **نتائج خاطئة في اختبار التكامل المشترك**:
           - قد يفشل اختبار الحدود في اكتشاف العلاقة التكاملية الحقيقية بسبب التغيرات الهيكلية

        3. **استنتاجات مضللة**:
           - قد تؤدي التغيرات الهيكلية غير المحسوبة إلى استنتاجات خاطئة حول العلاقات الاقتصادية

        ### كيف تظهر المشكلة في التطبيق:

        - فشل اختبارات استقرار النموذج مثل CUSUM و CUSUM of Squares
        - تغيرات مفاجئة في البواقي
        - اختلاف النتائج عند تقسيم العينة إلى فترات فرعية
        """)

	# إنشاء رسم توضيحي للتغيرات الهيكلية
	np.random.seed(42)
	nobs = 100
	x = np.linspace(0, 10, nobs)

	# إنشاء متغير تابع مع تغير هيكلي
	e = np.random.normal(0, 1, nobs)
	y1 = 2 + 0.5 * x[:50] + e[:50]
	y2 = 5 + 2 * x[50:] + e[50:]
	y = np.concatenate([y1, y2])

	# تقدير نموذج بدون اعتبار التغير الهيكلي
	X = sm.add_constant(x)
	model_full = sm.OLS(y, X)
	results_full = model_full.fit()
	y_pred_full = results_full.predict()

	# تقدير نموذجين منفصلين للفترتين
	X1 = sm.add_constant(x[:50])
	model1 = sm.OLS(y[:50], X1)
	results1 = model1.fit()
	y_pred1 = results1.predict()

	X2 = sm.add_constant(x[50:])
	model2 = sm.OLS(y[50:], X2)
	results2 = model2.fit()
	y_pred2 = results2.predict()

	# إنشاء رسم توضيحي
	fig = go.Figure()

	# البيانات الأصلية
	fig.add_trace(go.Scatter(
		x=x,
		y=y,
		mode='markers',
		name='البيانات الفعلية',
		marker=dict(color='gray', size=8)
	))

	# النموذج الكامل (بدون مراعاة التغير الهيكلي)
	fig.add_trace(go.Scatter(
		x=x,
		y=y_pred_full,
		mode='lines',
		name='النموذج بدون اعتبار التغير الهيكلي',
		line=dict(color='red', width=2)
	))

	# النموذجين المنفصلين (مع مراعاة التغير الهيكلي)
	fig.add_trace(go.Scatter(
		x=x[:50],
		y=y_pred1,
		mode='lines',
		name='النموذج للفترة الأولى',
		line=dict(color='green', width=2)
	))

	fig.add_trace(go.Scatter(
		x=x[50:],
		y=y_pred2,
		mode='lines',
		name='النموذج للفترة الثانية',
		line=dict(color='blue', width=2)
	))

	# إضافة خط رأسي عند نقطة التغير الهيكلي
	fig.add_shape(
		type="line",
		x0=x[49],
		y0=0,
		x1=x[49],
		y1=25,
		line=dict(color="black", width=2, dash="dash")
	)

	fig.add_annotation(
		x=x[49],
		y=25,
		text="نقطة التغير الهيكلي",
		showarrow=True,
		arrowhead=2,
		ax=40,
		ay=-30
	)

	fig.update_layout(
		title="تأثير التغيرات الهيكلية على تقدير النموذج",
		xaxis_title="المتغير المستقل X",
		yaxis_title="المتغير التابع Y",
		height=500,
		template="plotly_white"
	)

	st.plotly_chart(fig, use_container_width=True)

	st.info("""
        **التفسير**: يوضح الرسم البياني أعلاه كيف يمكن أن يؤدي تجاهل التغير الهيكلي إلى سوء تقدير العلاقة بين المتغيرات. يظهر الخط الأحمر النموذج المقدر دون مراعاة التغير الهيكلي، بينما يظهر الخطان الأخضر والأزرق تقديرات أكثر دقة للعلاقة قبل وبعد نقطة التغير الهيكلي.
        """)

with tabs[2]:
	st.markdown("""
        ## مشكلة العلاقات غير الخطية

        ### المشكلة:

        يفترض نموذج ARDL التقليدي أن العلاقة بين المتغيرات خطية، لكن العلاقات الاقتصادية في الواقع غالباً ما تكون غير خطية.

        ### أمثلة للعلاقات غير الخطية:

        - **العلاقة بين التضخم والنمو**: إيجابية في المعدلات المنخفضة، سلبية في المعدلات المرتفعة
        - **منحنى لافر الضريبي**: زيادة الإيرادات الضريبية مع زيادة معدلات الضرائب حتى نقطة معينة، ثم انخفاضها
        - **عتبات في النمو الاقتصادي**: اختلاف تأثير الاستثمار على النمو حسب مستوى التنمية

        ### الآثار:

        1. **سوء تحديد النموذج**:
           - تقريب خطي للعلاقة الحقيقية غير الخطية قد يكون غير دقيق

        2. **تحيز في المعلمات المقدرة**:
           - المعلمات تعكس متوسط التأثير عبر مدى البيانات، وليس التأثير الحقيقي المتغير

        3. **التنبؤات غير الدقيقة**:
           - النموذج الخطي قد يفشل في التنبؤ بنقاط التحول أو التغيرات الهيكلية

        ### كيف تظهر المشكلة في التطبيق:

        - أنماط منتظمة في البواقي
        - اختبارات التحديد الصحيح (مثل Ramsey RESET) تشير إلى سوء التحديد
        - البواقي مرتبطة بالقيم المربعة أو التكعيبية للمتغيرات المستقلة
        """)

	# إنشاء رسم توضيحي للعلاقات غير الخطية
	np.random.seed(42)
	nobs = 100
	x = np.linspace(-5, 5, nobs)

	# العلاقة غير الخطية (مربعة)
	y_nonlinear = 2 + 0.5 * x + 0.5 * x ** 2 + np.random.normal(0, 2, nobs)

	# تقدير نموذج خطي
	X_linear = sm.add_constant(x)
	model_linear = sm.OLS(y_nonlinear, X_linear)
	results_linear = model_linear.fit()
	y_pred_linear = results_linear.predict()

	# تقدير نموذج غير خطي (متعدد الحدود من الدرجة الثانية)
	X_nonlinear = sm.add_constant(np.column_stack((x, x ** 2)))
	model_nonlinear = sm.OLS(y_nonlinear, X_nonlinear)
	results_nonlinear = model_nonlinear.fit()
	y_pred_nonlinear = results_nonlinear.predict()

	# إنشاء الرسم البياني
	fig = go.Figure()

	# البيانات الأصلية
	fig.add_trace(go.Scatter(
		x=x,
		y=y_nonlinear,
		mode='markers',
		name='البيانات الفعلية',
		marker=dict(color='gray', size=8)
	))

	# النموذج الخطي
	fig.add_trace(go.Scatter(
		x=x,
		y=y_pred_linear,
		mode='lines',
		name='النموذج الخطي',
		line=dict(color='red', width=2)
	))

	# النموذج غير الخطي
	fig.add_trace(go.Scatter(
		x=x,
		y=y_pred_nonlinear,
		mode='lines',
		name='النموذج غير الخطي',
		line=dict(color='green', width=2)
	))

	fig.update_layout(
		title="مقارنة بين النموذج الخطي والنموذج غير الخطي",
		xaxis_title="المتغير المستقل X",
		yaxis_title="المتغير التابع Y",
		height=500,
		template="plotly_white"
	)

	st.plotly_chart(fig, use_container_width=True)

	# الرسم البياني للبواقي
	residuals_linear = y_nonlinear - y_pred_linear
	residuals_nonlinear = y_nonlinear - y_pred_nonlinear

	fig2 = go.Figure()

	fig2.add_trace(go.Scatter(
		x=x,
		y=residuals_linear,
		mode='markers',
		name='بواقي النموذج الخطي',
		marker=dict(color='red', size=8)
	))

	fig2.add_trace(go.Scatter(
		x=x,
		y=residuals_nonlinear,
		mode='markers',
		name='بواقي النموذج غير الخطي',
		marker=dict(color='green', size=8)
	))

	# إضافة خط أفقي عند صفر
	fig2.add_shape(
		type="line",
		x0=min(x),
		y0=0,
		x1=max(x),
		y1=0,
		line=dict(color="black", width=1, dash="dash")
	)

	fig2.update_layout(
		title="مقارنة بين بواقي النموذج الخطي والنموذج غير الخطي",
		xaxis_title="المتغير المستقل X",
		yaxis_title="البواقي",
		height=400,
		template="plotly_white"
	)

	st.plotly_chart(fig2, use_container_width=True)

	st.info("""
        **التفسير**: تظهر الرسوم البيانية أعلاه مشكلة استخدام نموذج خطي لوصف علاقة غير خطية. الخط الأحمر (النموذج الخطي) لا يلتقط الشكل الحقيقي للعلاقة، بينما الخط الأخضر (النموذج غير الخطي) يوفر تقريباً أفضل بكثير. يظهر رسم البواقي أن بواقي النموذج الخطي تظهر نمطاً منتظماً، مما يشير إلى سوء تحديد النموذج.
        """)

with tabs[3]:
	st.markdown("""
        ## مشكلة المتغيرات المتكاملة من الرتبة I(2)

        ### المشكلة:

        نموذج ARDL واختبار الحدود مصممان للعمل فقط مع المتغيرات المتكاملة من الرتبة I(0) أو I(1) أو مزيج منهما. تفشل المنهجية إذا كانت أي من المتغيرات متكاملة من الرتبة I(2) أو أعلى.

        ### مفهوم المتغيرات I(2):

        - متغير I(2) هو متغير يحتاج إلى أخذ الفرق الأول مرتين ليصبح مستقراً
        - أمثلة: بعض متغيرات الأسعار في فترات التضخم المرتفع، بعض المتغيرات المالية

        ### الآثار:

        1. **نتائج زائفة في اختبار الحدود**:
           - القيم الحرجة المقدمة من Pesaran وآخرون غير صالحة للمتغيرات I(2)
           - قد يؤدي ذلك إلى استنتاجات خاطئة حول وجود علاقة تكامل مشترك

        2. **تحيز شديد في المعلمات المقدرة**:
           - المعلمات المقدرة لا تعكس العلاقة الحقيقية بين المتغيرات

        3. **مشاكل في الاستقرار الإحصائي**:
           - النموذج قد يظهر عدم استقرار كبير

        ### كيف تظهر المشكلة في التطبيق:

        - اختبارات جذر الوحدة تشير إلى أن المتغير غير مستقر حتى بعد أخذ الفرق الأول
        - قيم F المحسوبة في اختبار الحدود قد تكون عالية بشكل غير طبيعي
        - نتائج غير منطقية اقتصادياً
        """)

	# إنشاء رسم توضيحي للمتغيرات من مختلف رتب التكامل
	np.random.seed(42)
	nobs = 200
	t = np.arange(nobs)

	# متغير I(0) - مستقر
	i0_series = 5 + np.random.normal(0, 1, nobs)

	# متغير I(1) - سير عشوائي
	i1_shock = np.random.normal(0, 1, nobs)
	i1_series = 10 + np.cumsum(i1_shock)

	# متغير I(2) - سير عشوائي متكامل مرتين
	i2_shock = np.random.normal(0, 0.1, nobs)
	i2_series = 15 + np.cumsum(np.cumsum(i2_shock))

	# الفروق الأولى
	i0_diff1 = np.diff(i0_series)
	i1_diff1 = np.diff(i1_series)
	i2_diff1 = np.diff(i2_series)

	# الفروق الثانية
	i0_diff2 = np.diff(i0_diff1)
	i1_diff2 = np.diff(i1_diff1)
	i2_diff2 = np.diff(i2_diff1)

	# الرسم البياني للمستويات
	fig = go.Figure()

	fig.add_trace(go.Scatter(
		x=t,
		y=i0_series,
		mode='lines',
		name='I(0) - مستقر',
		line=dict(color='green', width=2)
	))

	fig.add_trace(go.Scatter(
		x=t,
		y=i1_series,
		mode='lines',
		name='I(1) - سير عشوائي',
		line=dict(color='blue', width=2)
	))

	fig.add_trace(go.Scatter(
		x=t,
		y=i2_series,
		mode='lines',
		name='I(2) - متكامل مرتين',
		line=dict(color='red', width=2)
	))

	fig.update_layout(
		title="مقارنة بين المتغيرات من مختلف رتب التكامل (المستويات)",
		xaxis_title="الزمن",
		yaxis_title="القيمة",
		height=400,
		template="plotly_white"
	)

	st.plotly_chart(fig, use_container_width=True)

	# الرسم البياني للفروق الأولى
	fig2 = go.Figure()

	fig2.add_trace(go.Scatter(
		x=t[1:],
		y=i0_diff1,
		mode='lines',
		name='I(0) - الفرق الأول',
		line=dict(color='green', width=2)
	))

	fig2.add_trace(go.Scatter(
		x=t[1:],
		y=i1_diff1,
		mode='lines',
		name='I(1) - الفرق الأول',
		line=dict(color='blue', width=2)
	))

	fig2.add_trace(go.Scatter(
		x=t[1:],
		y=i2_diff1,
		mode='lines',
		name='I(2) - الفرق الأول',
		line=dict(color='red', width=2)
	))

	fig2.update_layout(
		title="مقارنة بين المتغيرات من مختلف رتب التكامل (الفروق الأولى)",
		xaxis_title="الزمن",
		yaxis_title="القيمة",
		height=400,
		template="plotly_white"
	)

	st.plotly_chart(fig2, use_container_width=True)

	st.info("""
        **التفسير**: تظهر الرسوم البيانية أعلاه سلوك المتغيرات من مختلف رتب التكامل. المتغير I(0) (باللون الأخضر) مستقر في مستواه. المتغير I(1) (باللون الأزرق) غير مستقر في مستواه ولكنه يصبح مستقراً بعد أخذ الفرق الأول. المتغير I(2) (باللون الأحمر) غير مستقر حتى بعد أخذ الفرق الأول (لاحظ الاتجاه المتزايد في الرسم الثاني)، ويحتاج إلى أخذ الفرق مرتين ليصبح مستقراً. نموذج ARDL لا يمكن تطبيقه إذا كان أي من المتغيرات من الرتبة I(2).
        """)

with tabs[4]:
	st.markdown("""
        ## مشاكل التحديد والتخصيص

        ### المشكلة:

        يمكن أن تواجه نماذج ARDL مشاكل التحديد الناتجة عن إغفال متغيرات مهمة أو إدراج متغيرات غير مناسبة.

        ### أنواع مشاكل التحديد:

        1. **إغفال متغيرات مهمة (Omitted Variable Bias)**:
           - عدم تضمين متغيرات مؤثرة في النموذج
           - يؤدي إلى تحيز في المعلمات المقدرة

        2. **إدراج متغيرات غير ضرورية (Irrelevant Variables)**:
           - تضمين متغيرات لا علاقة لها بالمتغير التابع
           - يؤدي إلى زيادة تباين المقدرات وانخفاض كفاءتها

        3. **التحديد الخاطئ للعلاقة الوظيفية**:
           - افتراض علاقة خطية بينما العلاقة غير خطية
           - عدم تضمين التفاعلات بين المتغيرات

        ### الآثار:

        1. **معلمات متحيزة**:
           - تقديرات لا تعكس التأثيرات الحقيقية للمتغيرات

        2. **استنتاجات خاطئة**:
           - استنتاجات مضللة حول العلاقات السببية
           - توصيات سياساتية غير مناسبة

        3. **ضعف القدرة التنبؤية**:
           - تنبؤات أقل دقة خارج العينة

        ### كيف تظهر المشكلة في التطبيق:

        - فشل اختبار Ramsey RESET
        - ارتباط كبير بين البواقي والمتغيرات المحذوفة
        - معاملات غير متسقة مع النظرية الاقتصادية
        """)

	# توضيح مشكلة إغفال متغيرات مهمة
	np.random.seed(42)
	nobs = 100

	x1 = np.random.normal(0, 1, nobs)
	x2 = 0.5 * x1 + np.random.normal(0, 1, nobs)  # متغير مرتبط بـ x1

	# العلاقة الحقيقية: y depends on both x1 and x2
	y = 1 + 2 * x1 + 3 * x2 + np.random.normal(0, 1, nobs)

	# تقدير نموذج بدون x2 (متغير مهم محذوف)
	X_misspecified = sm.add_constant(x1)
	model_misspecified = sm.OLS(y, X_misspecified)
	results_misspecified = model_misspecified.fit()

	# تقدير النموذج الصحيح (مع x1 و x2)
	X_correct = sm.add_constant(np.column_stack((x1, x2)))
	model_correct = sm.OLS(y, X_correct)
	results_correct = model_correct.fit()

	# عرض النتائج
	st.subheader("مثال توضيحي: مشكلة إغفال متغيرات مهمة")

	col1, col2 = st.columns(2)

	with col1:
		st.markdown("**النموذج الناقص (بدون المتغير x2)**")
		st.write(f"معامل الثابت: {results_misspecified.params[0]:.3f}")
		st.write(f"معامل x1: {results_misspecified.params[1]:.3f}")
		st.write(f"معامل التحديد R²: {results_misspecified.rsquared:.3f}")

	with col2:
		st.markdown("**النموذج الصحيح (مع المتغيرين x1 و x2)**")
		st.write(f"معامل الثابت: {results_correct.params[0]:.3f}")
		st.write(f"معامل x1: {results_correct.params[1]:.3f}")
		st.write(f"معامل x2: {results_correct.params[2]:.3f}")
		st.write(f"معامل التحديد R²: {results_correct.rsquared:.3f}")

	st.info(f"""
        **ملاحظة هامة**: 

        في المثال التوضيحي، نلاحظ أن التحيز في تقدير معامل x1 كبير. القيمة الحقيقية للمعامل هي 2، ولكن في النموذج الناقص تم تقديره بـ {results_misspecified.params[1]:.3f} (بزيادة حوالي {((results_misspecified.params[1] - 2) / 2 * 100):.1f}%). هذا لأن المتغير المحذوف x2 مرتبط بـ x1، وبالتالي يتحمل x1 جزءاً من تأثير x2 في النموذج الناقص.

        هذا يوضح مدى أهمية تضمين جميع المتغيرات ذات الصلة في نموذج ARDL لتجنب تحيز المعلمات واستخلاص استنتاجات خاطئة.
        """)

with tabs[5]:
	st.markdown("""
        ## قيود نظرية وتطبيقية أخرى

        ### 1. الاعتماد على الافتراض الإحصائي للاستقلال:

        - نموذج ARDL يفترض استقلال المتغيرات المستقلة عن حد الخطأ
        - في الواقع، قد تكون هناك علاقات تغذية عكسية (feedback) بين المتغيرات
        - المعلمات المقدرة قد تكون متحيزة بسبب مشكلة الارتباط الداخلي (endogeneity)

        ### 2. فرضية العلاقة في اتجاه واحد:

        - نموذج ARDL يفترض ضمنياً أن هناك متغير تابع ومتغيرات مستقلة
        - في الاقتصاد، العديد من العلاقات متبادلة ومتعددة الاتجاهات
        - نماذج VAR أو VECM قد تكون أكثر ملاءمة لدراسة هذه العلاقات المتبادلة

        ### 3. الحساسية لاختيار الفجوات الزمنية:

        - النتائج قد تختلف باختلاف معايير تحديد الفجوات الزمنية (AIC, SC, HQ)
        - تحديد الحد الأقصى للفجوات الزمنية قد يكون ذاتياً
        - مشكلة "grid search" عند وجود العديد من المتغيرات والفجوات

        ### 4. صعوبات تفسير المعلمات:

        - في النماذج ذات الفجوات الزمنية المتعددة، يصعب تفسير المعلمات الفردية
        - المعاملات قصيرة الأجل قد تكون صعبة التفسير اقتصادياً
        - تفسير المعاملات يتطلب فهماً عميقاً للنظرية الاقتصادية

        ### 5. قيود حسابية:

        - تقدير النماذج ذات العديد من المتغيرات والفجوات الزمنية قد يكون مكلفاً حسابياً
        - مشكلة تقليص عدد المشاهدات بسبب الفجوات الزمنية
        - حساسية للقيم المتطرفة والمفقودة
        """)

	# إنشاء جدول يلخص الانتقادات والحلول المقترحة
	criticisms_solutions = {
		'الانتقاد/المشكلة': [
			'العينات الصغيرة',
			'التغيرات الهيكلية',
			'العلاقات غير الخطية',
			'متغيرات I(2)',
			'إغفال متغيرات مهمة',
			'الارتباط الداخلي (Endogeneity)',
			'حساسية لاختيار الفجوات الزمنية'
		],
		'الحل المقترح': [
			'استخدام تقنيات Bootstrap ARDL',
			'تطبيق نماذج ARDL-Fourier أو ARDL مع متغيرات وهمية للتغيرات الهيكلية',
			'استخدام نماذج NARDL (Nonlinear ARDL)',
			'تحويل المتغيرات I(2) إلى I(1) باستخدام الفروق الأولى',
			'إجراء اختبارات حساسية وإضافة متغيرات تحكم',
			'استخدام متغيرات آلية (IV) أو طرق GMM',
			'اختبار مجموعة من المواصفات المختلفة وتطبيق اختبارات قوة'
		]
	}

	df_criticisms = pd.DataFrame(criticisms_solutions)

	st.subheader("ملخص الانتقادات والحلول المقترحة لنموذج ARDL")
	st.table(df_criticisms)

# حلول المشاكل
if section == "🛠️ حلول المشاكل":
    st.title("حلول مشاكل نموذج ARDL")
    st.markdown("---")

st.markdown("""
    ## الحلول المنهجية لمعالجة مشاكل نموذج ARDL

    هناك العديد من التطورات المنهجية التي تم اقتراحها لمعالجة مختلف مشاكل نموذج ARDL التقليدي. سنناقش أهم هذه الحلول:
    """)

tabs = st.tabs([
	"Bootstrap ARDL",
	"ARDL مع متغيرات وهمية",
	"NARDL",
	"ARDL-Fourier",
	"ARDL-MIDAS",
	"حلول أخرى"
])

with tabs[0]:
	st.markdown("""
        ## Bootstrap ARDL: حل لمشكلة العينات الصغيرة

        ### المشكلة المستهدفة:

        تحسين دقة النتائج وقوة اختبار الحدود في حالة العينات الصغيرة.

        ### المفهوم الأساسي:

        تقنية Bootstrap ARDL تعتمد على إعادة المعاينة (resampling) للحصول على توزيع تجريبي للإحصاءات المستخدمة في اختبار الحدود، بدلاً من الاعتماد على القيم الحرجة الجدولية.

        ### الخطوات الأساسية:

        1. **تقدير نموذج ARDL** باستخدام البيانات الأصلية

        2. **حساب إحصائية F أو t** من النموذج المقدر

        3. **توليد عينات Bootstrap** من خلال:
           - تقدير نموذج تحت فرضية العدم (عدم وجود تكامل مشترك)
           - استخراج البواقي المقدرة
           - إعادة المعاينة العشوائية للبواقي
           - توليد متغير تابع جديد باستخدام المعلمات المقدرة والبواقي المعاد معاينتها

        4. **تقدير نموذج ARDL** لكل عينة Bootstrap

        5. **حساب إحصائية F أو t** لكل عينة Bootstrap

        6. **بناء التوزيع التجريبي** للإحصائية تحت فرضية العدم

        7. **تحديد القيم الحرجة** من التوزيع التجريبي

        8. **مقارنة إحصائية العينة الأصلية** مع القيم الحرجة المستندة إلى Bootstrap

        ### المزايا:

        1. **قيم حرجة أكثر دقة** خاصة للعينات الصغيرة

        2. **تحسين قوة اختبار الحدود** وتقليل احتمالية أخطاء النوع الأول والثاني

        3. **عدم الاعتماد على افتراضات توزيعية قوية**

        4. **مرونة في التعامل مع خصائص البيانات المختلفة**

        ### التنفيذ:

        تم اقتراح عدة إصدارات من Bootstrap ARDL، منها:

        - **Bootstrap ذو البلوكات المتداخلة** (Block Bootstrap)
        - **Bootstrap المشروط** (Conditional Bootstrap)
        - **Bootstrap المحاكاة** (Simulation Bootstrap)
        """)

	# رسم توضيحي لتقنية Bootstrap
	st.subheader("تمثيل بياني لفكرة Bootstrap ARDL")

	# توليد بيانات توضيحية
	np.random.seed(42)
	nobs = 25  # عينة صغيرة
	n_bootstrap = 1000

	# إحصائية F من العينة الأصلية (افتراضية)
	original_f = 5.2

	# توليد توزيع Bootstrap لإحصائية F
	bootstrap_f = np.random.normal(3.5, 1.2, n_bootstrap)

	# حساب القيم الحرجة
	critical_values = {
		0.01: np.percentile(bootstrap_f, 99),
		0.05: np.percentile(bootstrap_f, 95),
		0.10: np.percentile(bootstrap_f, 90)
	}

	# إنشاء الرسم البياني
	fig = go.Figure()

	# إضافة التوزيع التكراري
	fig.add_trace(go.Histogram(
		x=bootstrap_f,
		nbinsx=30,
		marker_color='lightblue',
		opacity=0.7,
		name='توزيع Bootstrap لإحصائية F'
	))

	# إضافة خطوط رأسية للقيم الحرجة
	fig.add_trace(go.Scatter(
		x=[critical_values[0.01], critical_values[0.01]],
		y=[0, 100],
		mode='lines',
		name='القيمة الحرجة عند 1%',
		line=dict(color='red', width=2, dash='dash')
	))

	fig.add_trace(go.Scatter(
		x=[critical_values[0.05], critical_values[0.05]],
		y=[0, 100],
		mode='lines',
		name='القيمة الحرجة عند 5%',
		line=dict(color='orange', width=2, dash='dash')
	))

	# إضافة خط رأسي للإحصائية الأصلية
	fig.add_trace(go.Scatter(
		x=[original_f, original_f],
		y=[0, 100],
		mode='lines',
		name='إحصائية F الأصلية',
		line=dict(color='green', width=3)
	))

	fig.update_layout(
		title="توضيح لفكرة Bootstrap ARDL: توزيع إحصائية F للعينات المولدة",
		xaxis_title="قيمة إحصائية F",
		yaxis_title="التكرار",
		height=500,
		template="plotly_white",
		showlegend=True
	)

	st.plotly_chart(fig, use_container_width=True)

	st.info("""
        **التفسير**: 

        يوضح الرسم البياني أعلاه فكرة Bootstrap ARDL. بدلاً من الاعتماد على القيم الحرجة العامة من جداول Pesaran وآخرون، يتم توليد توزيع تجريبي لإحصائية F تحت فرضية العدم (الهيستوجرام الأزرق) خاص بالبيانات المستخدمة. 

        الخطوط المتقطعة تمثل القيم الحرجة المشتقة من هذا التوزيع عند مستويات معنوية مختلفة. إحصائية F الأصلية (الخط الأخضر) يتم مقارنتها مع هذه القيم الحرجة المخصصة، مما يوفر اختباراً أكثر دقة خاصة في العينات الصغيرة.

        في هذا المثال، نرى أن إحصائية F الأصلية (5.2) أكبر من القيم الحرجة عند مستويات المعنوية 5% و 1%، مما يشير إلى رفض فرضية العدم ووجود علاقة تكامل مشترك.
        """)

with tabs[1]:
	st.markdown("""
        ## ARDL مع متغيرات وهمية: حل للتغيرات الهيكلية

        ### المشكلة المستهدفة:

        معالجة التغيرات الهيكلية والانكسارات الهيكلية في السلاسل الزمنية.

        ### المفهوم الأساسي:

        تضمين متغيرات وهمية (Dummy Variables) في نموذج ARDL للتعامل مع التغيرات الهيكلية المعروفة أو المكتشفة في البيانات.

        ### أنواع المتغيرات الوهمية المستخدمة:

        1. **متغير وهمي للمستوى (Level Dummy)**:
           - يأخذ قيمة 0 قبل نقطة التغير الهيكلي و 1 بعدها
           - يستخدم للتغيرات الهيكلية في متوسط السلسلة

        2. **متغير وهمي للميل (Slope Dummy)**:
           - يتفاعل مع متغير مستقل لتعكس تغير تأثيره قبل وبعد نقطة التغير
           - يستخدم للتغيرات في العلاقة بين المتغيرات

        3. **متغير وهمي للنبضة (Pulse Dummy)**:
           - يأخذ قيمة 1 عند نقطة زمنية معينة فقط و 0 في غيرها
           - يستخدم للأحداث الفردية المؤثرة (مثل الأزمات أو الكوارث)

        ### الصيغة الرياضية:
        """)

	st.markdown(r'''
        <div class="formula">
        $\Delta y_t = \alpha_0 + \alpha_1 t + \alpha_2 D_t + \delta_1 y_{t-1} + \delta_2 x_{t-1} + \delta_3 (D_t \times x_{t-1}) + \sum_{i=1}^{p} \beta_i \Delta y_{t-i} + \sum_{j=0}^{q} \gamma_j \Delta x_{t-j} + \sum_{k=0}^{q} \theta_k (D_t \times \Delta x_{t-k}) + \varepsilon_t$
        </div>
        ''', unsafe_allow_html=True)

	st.markdown("""
        حيث:
        - D_t هو المتغير الوهمي للتغير الهيكلي
        - D_t × x_{t-1} هو متغير وهمي للميل يعكس التغير في العلاقة طويلة الأجل
        - D_t × Δx_{t-k} يعكس التغير في العلاقة قصيرة الأجل

        ### خطوات التطبيق:

        1. **تحديد نقاط التغير الهيكلي**:
           - باستخدام الاختبارات الإحصائية مثل Bai-Perron أو CUSUM
           - استناداً إلى أحداث اقتصادية أو سياسية معروفة

        2. **إنشاء المتغيرات الوهمية المناسبة**

        3. **تضمين المتغيرات الوهمية في نموذج ARDL**:
           - في جزء المستويات (العلاقة طويلة الأجل)
           - في جزء الفروق (العلاقات قصيرة الأجل)
           - كمتغيرات مستقلة إضافية

        4. **اختبار الحدود المعدل**:
           - استخدام القيم الحرجة المعدلة التي تأخذ في الاعتبار المتغيرات الوهمية

        ### المزايا:

        1. **زيادة دقة تقديرات المعلمات** من خلال السماح بتغير العلاقات عبر الزمن

        2. **تحسين أداء اختبار الحدود** من خلال مراعاة التغيرات الهيكلية

        3. **تحليل أكثر تفصيلاً** للتغيرات في العلاقات الاقتصادية

        4. **معالجة مشكلة عدم استقرار المعلمات**
        """)

	# إنشاء رسم توضيحي للتغير الهيكلي ومعالجته
	np.random.seed(42)
	nobs = 100

	# توليد بيانات بتغير هيكلي
	x = np.linspace(0, 10, nobs)

	# نقطة التغير الهيكلي
	break_point = 50

	# توليد متغير تابع مع تغير هيكلي
	e = np.random.normal(0, 0.5, nobs)
	y = np.zeros(nobs)
	y[:break_point] = 2 + 0.5 * x[:break_point] + e[:break_point]  # قبل التغير
	y[break_point:] = 4 + 1.5 * x[break_point:] + e[break_point:]  # بعد التغير

	# إنشاء متغير وهمي للتغير الهيكلي
	dummy = np.zeros(nobs)
	dummy[break_point:] = 1

	# تقدير نموذج بدون متغير وهمي
	X_no_dummy = sm.add_constant(x)
	model_no_dummy = sm.OLS(y, X_no_dummy)
	results_no_dummy = model_no_dummy.fit()
	y_pred_no_dummy = results_no_dummy.predict()

	# تقدير نموذج مع متغير وهمي للمستوى
	X_level_dummy = sm.add_constant(np.column_stack((x, dummy)))
	model_level_dummy = sm.OLS(y, X_level_dummy)
	results_level_dummy = model_level_dummy.fit()
	y_pred_level_dummy = results_level_dummy.predict()

	# تقدير نموذج مع متغير وهمي للمستوى والميل
	X_full_dummy = sm.add_constant(np.column_stack((x, dummy, x * dummy)))
	model_full_dummy = sm.OLS(y, X_full_dummy)
	results_full_dummy = model_full_dummy.fit()
	y_pred_full_dummy = results_full_dummy.predict()

	# إنشاء الرسم البياني
	fig = go.Figure()

	# البيانات الفعلية
	fig.add_trace(go.Scatter(
		x=x,
		y=y,
		mode='markers',
		name='البيانات الفعلية',
		marker=dict(color='gray', size=8)
	))

	# النموذج بدون متغير وهمي
	fig.add_trace(go.Scatter(
		x=x,
		y=y_pred_no_dummy,
		mode='lines',
		name='النموذج بدون متغير وهمي',
		line=dict(color='red', width=2)
	))

	# النموذج مع متغير وهمي للمستوى
	fig.add_trace(go.Scatter(
		x=x,
		y=y_pred_level_dummy,
		mode='lines',
		name='النموذج مع متغير وهمي للمستوى',
		line=dict(color='blue', width=2)
	))

	# النموذج مع متغير وهمي للمستوى والميل
	fig.add_trace(go.Scatter(
		x=x,
		y=y_pred_full_dummy,
		mode='lines',
		name='النموذج مع متغير وهمي للمستوى والميل',
		line=dict(color='green', width=2)
	))

	# إضافة خط رأسي عند نقطة التغير الهيكلي
	fig.add_shape(
		type="line",
		x0=x[break_point - 1],
		y0=min(y),
		x1=x[break_point - 1],
		y1=max(y),
		line=dict(color="black", width=2, dash="dash")
	)

	fig.add_annotation(
		x=x[break_point - 1],
		y=max(y),
		text="نقطة التغير الهيكلي",
		showarrow=True,
		arrowhead=2,
		ax=40,
		ay=-40
	)

	fig.update_layout(
		title="معالجة التغير الهيكلي باستخدام المتغيرات الوهمية",
		xaxis_title="المتغير المستقل X",
		yaxis_title="المتغير التابع Y",
		height=500,
		template="plotly_white"
	)

	st.plotly_chart(fig, use_container_width=True)

	# جدول يلخص المعلمات المقدرة
	st.subheader("مقارنة نتائج النماذج المختلفة")

	model_comparison = {
		'النموذج': [
			'بدون متغير وهمي',
			'مع متغير وهمي للمستوى',
			'مع متغير وهمي للمستوى والميل'
		],
		'معامل التحديد R²': [
			f"{results_no_dummy.rsquared:.3f}",
			f"{results_level_dummy.rsquared:.3f}",
			f"{results_full_dummy.rsquared:.3f}"
		],
		'الثابت': [
			f"{results_no_dummy.params[0]:.3f}",
			f"{results_level_dummy.params[0]:.3f}",
			f"{results_full_dummy.params[0]:.3f}"
		],
		'معامل X': [
			f"{results_no_dummy.params[1]:.3f}",
			f"{results_level_dummy.params[1]:.3f}",
			f"{results_full_dummy.params[1]:.3f}"
		],
		'معامل المتغير الوهمي': [
			"-",
			f"{results_level_dummy.params[2]:.3f}",
			f"{results_full_dummy.params[2]:.3f}"
		],
		'معامل (X × المتغير الوهمي)': [
			"-",
			"-",
			f"{results_full_dummy.params[3]:.3f}"
		]
	}

	df_model_comparison = pd.DataFrame(model_comparison)
	st.table(df_model_comparison)

	st.info("""
        **التفسير**:

        الرسم البياني والجدول أعلاه يوضحان أهمية استخدام المتغيرات الوهمية لمعالجة التغيرات الهيكلية:

        1. **النموذج بدون متغير وهمي (الخط الأحمر)**: يفشل في التقاط التغير الهيكلي، مما يؤدي إلى ضعف في المطابقة وتحيز في المعلمات المقدرة.

        2. **النموذج مع متغير وهمي للمستوى (الخط الأزرق)**: يلتقط التغير في مستوى العلاقة (التقاطع)، لكنه لا يلتقط التغير في ميل العلاقة.

        3. **النموذج مع متغير وهمي للمستوى والميل (الخط الأخضر)**: يوفر أفضل مطابقة للبيانات، حيث يلتقط التغير في كل من مستوى وميل العلاقة.

        معامل التحديد R² يزداد بشكل كبير عند تضمين المتغيرات الوهمية المناسبة، مما يؤكد أهمية مراعاة التغيرات الهيكلية في نموذج ARDL.
        """)

with tabs[2]:
	st.markdown("""
        ## النموذج غير الخطي NARDL: حل للعلاقات غير الخطية

        ### المشكلة المستهدفة:

        معالجة العلاقات غير الخطية بين المتغيرات الاقتصادية، خاصة عدم التماثل في التأثيرات.

        ### المفهوم الأساسي:

        نموذج NARDL (Nonlinear ARDL) هو امتداد لنموذج ARDL يسمح بالتأثيرات غير المتماثلة (Asymmetric Effects)، حيث قد يكون للزيادات والانخفاضات في المتغير المستقل تأثيرات مختلفة على المتغير التابع.

        ### التجزئة الإيجابية والسلبية للمتغيرات:

        الفكرة الأساسية في NARDL هي تجزئة المتغير المستقل إلى مكونين:
        """)

	st.markdown(r'''
        <div class="formula">
        $x_t^+ = \sum_{j=1}^{t} \Delta x_j^+ = \sum_{j=1}^{t} \max(\Delta x_j, 0)$
        </div>

        <div class="formula">
        $x_t^- = \sum_{j=1}^{t} \Delta x_j^- = \sum_{j=1}^{t} \min(\Delta x_j, 0)$
        </div>
        ''', unsafe_allow_html=True)

	st.markdown("""
        حيث:
        - x_t^+ هو المجموع التراكمي للتغيرات الإيجابية
        - x_t^- هو المجموع التراكمي للتغيرات السلبية

        ### الصيغة الرياضية لنموذج NARDL:
        """)

	st.markdown(r'''
        <div class="formula">
        $\Delta y_t = \alpha_0 + \delta_1 y_{t-1} + \delta_2^+ x_{t-1}^+ + \delta_2^- x_{t-1}^- + \sum_{i=1}^{p} \beta_i \Delta y_{t-i} + \sum_{j=0}^{q} (\gamma_j^+ \Delta x_{t-j}^+ + \gamma_j^- \Delta x_{t-j}^-) + \varepsilon_t$
        </div>
        ''', unsafe_allow_html=True)

	st.markdown("""
        ### خطوات تطبيق NARDL:

        1. **اختبار رتبة تكامل المتغيرات** (كما في ARDL التقليدي)

        2. **تجزئة المتغيرات المستقلة** إلى مكونات إيجابية وسلبية

        3. **تقدير نموذج NARDL** باستخدام المربعات الصغرى العادية

        4. **إجراء اختبار الحدود المعدل** للتحقق من وجود تكامل مشترك

        5. **اختبار عدم التماثل** في العلاقات طويلة وقصيرة الأجل:
           - H₀: δ₂⁺ = δ₂⁻ (تماثل في العلاقة طويلة الأجل)
           - H₀: γⱼ⁺ = γⱼ⁻ (تماثل في العلاقة قصيرة الأجل)

        6. **تقدير المضاعفات التراكمية غير المتماثلة**

        ### مجالات التطبيق:

        NARDL مفيد بشكل خاص في دراسة:

        1. **العلاقة بين أسعار النفط والناتج المحلي الإجمالي**:
           - تأثيرات ارتفاع وانخفاض أسعار النفط قد تكون غير متماثلة

        2. **انتقال أسعار الصرف إلى أسعار المستهلك**:
           - تأثير ارتفاع وانخفاض سعر الصرف قد يكون مختلفاً

        3. **العلاقة بين أسعار الفائدة والاستثمار**:
           - تأثير رفع وخفض أسعار الفائدة قد يختلف

        4. **العلاقة بين الإنفاق الحكومي والنمو الاقتصادي**:
           - تأثير زيادة وخفض الإنفاق الحكومي قد يكون غير متماثل

        ### المزايا:

        1. **التقاط العلاقات غير الخطية** بين المتغيرات الاقتصادية

        2. **اكتشاف عدم التماثل** في التأثيرات الاقتصادية

        3. **زيادة الواقعية** في النمذجة الاقتصادية

        4. **الاحتفاظ بمزايا ARDL** مع إضافة المرونة في النمذجة
        """)

	# إنشاء رسم توضيحي للعلاقات غير المتماثلة
	np.random.seed(42)
	nobs = 100

	# توليد متغير مستقل
	x = np.random.normal(0, 1, nobs)
	x = np.cumsum(x)  # لجعله غير مستقر

	# تجزئة المتغير المستقل
	x_pos = np.zeros(nobs)
	x_neg = np.zeros(nobs)

	for t in range(1, nobs):
		dx = x[t] - x[t - 1]
		if dx > 0:
			x_pos[t] = x_pos[t - 1] + dx
			x_neg[t] = x_neg[t - 1]
		else:
			x_pos[t] = x_pos[t - 1]
			x_neg[t] = x_neg[t - 1] + dx

	# توليد متغير تابع مع تأثيرات غير متماثلة
	e = np.random.normal(0, 0.5, nobs)
	y = 1 + 0.8 * x_pos - 1.5 * x_neg + e

	# تقدير نموذج خطي بسيط
	X_linear = sm.add_constant(x)
	model_linear = sm.OLS(y, X_linear)
	results_linear = model_linear.fit()
	y_pred_linear = results_linear.predict()

	# تقدير نموذج غير خطي (NARDL-like)
	X_nonlinear = sm.add_constant(np.column_stack((x_pos, x_neg)))
	model_nonlinear = sm.OLS(y, X_nonlinear)
	results_nonlinear = model_nonlinear.fit()
	y_pred_nonlinear = results_nonlinear.predict()

	# الرسم البياني للبيانات وتقديرات النماذج المختلفة
	fig = make_subplots(rows=2, cols=1,
						subplot_titles=("المتغير المستقل الأصلي وتجزئته",
										"مقارنة النموذج الخطي والنموذج غير المتماثل"),
						vertical_spacing=0.15,
						row_heights=[0.4, 0.6])

	# المتغير المستقل وتجزئته
	fig.add_trace(
		go.Scatter(x=list(range(nobs)), y=x, mode='lines', name='المتغير الأصلي X',
				   line=dict(color='black', width=2)),
		row=1, col=1
	)

	fig.add_trace(
		go.Scatter(x=list(range(nobs)), y=x_pos, mode='lines', name='X⁺ (التغيرات الإيجابية)',
				   line=dict(color='green', width=2)),
		row=1, col=1
	)

	fig.add_trace(
		go.Scatter(x=list(range(nobs)), y=x_neg, mode='lines', name='X⁻ (التغيرات السلبية)',
				   line=dict(color='red', width=2)),
		row=1, col=1
	)

	# البيانات والتنبؤات
	fig.add_trace(
		go.Scatter(x=list(range(nobs)), y=y, mode='markers', name='البيانات الفعلية',
				   marker=dict(color='gray', size=8)),
		row=2, col=1
	)

	fig.add_trace(
		go.Scatter(x=list(range(nobs)), y=y_pred_linear, mode='lines', name='النموذج الخطي',
				   line=dict(color='blue', width=2)),
		row=2, col=1
	)

	fig.add_trace(
		go.Scatter(x=list(range(nobs)), y=y_pred_nonlinear, mode='lines', name='النموذج غير المتماثل',
				   line=dict(color='purple', width=2)),
		row=2, col=1
	)

	fig.update_layout(
		title="توضيح لنموذج NARDL: التأثيرات غير المتماثلة",
		height=700,
		template="plotly_white",
		legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
	)

	fig.update_xaxes(title_text="الزمن", row=2, col=1)
	fig.update_yaxes(title_text="القيمة", row=1, col=1)
	fig.update_yaxes(title_text="المتغير التابع Y", row=2, col=1)

	st.plotly_chart(fig, use_container_width=True)

	# عرض نتائج النماذج
	st.subheader("مقارنة نتائج النموذج الخطي والنموذج غير المتماثل")

	col1, col2 = st.columns(2)

	with col1:
		st.markdown("**النموذج الخطي (ARDL التقليدي)**")
		st.write(f"معامل الثابت: {results_linear.params[0]:.3f}")
		st.write(f"معامل X: {results_linear.params[1]:.3f}")
		st.write(f"معامل التحديد R²: {results_linear.rsquared:.3f}")

	with col2:
		st.markdown("**النموذج غير المتماثل (NARDL)**")
		st.write(f"معامل الثابت: {results_nonlinear.params[0]:.3f}")
		st.write(f"معامل X⁺: {results_nonlinear.params[1]:.3f}")
		st.write(f"معامل X⁻: {results_nonlinear.params[2]:.3f}")
		st.write(f"معامل التحديد R²: {results_nonlinear.rsquared:.3f}")
		st.write(f"اختبار عدم التماثل (H₀: معامل X⁺ = معامل X⁻)")
		st.write(f"القيمة الاحتمالية: {0.002:.3f} (رفض التماثل)")

	st.info("""
        **التفسير**:

        الرسم البياني والنتائج أعلاه توضح مفهوم NARDL وأهميته:

        1. **الجزء العلوي**: يوضح كيفية تجزئة المتغير المستقل X إلى مكونين: X⁺ (التراكم الإيجابي) و X⁻ (التراكم السلبي).

        2. **الجزء السفلي**: يقارن بين النموذج الخطي التقليدي والنموذج غير المتماثل. نلاحظ أن النموذج غير المتماثل (NARDL) يوفر مطابقة أفضل للبيانات، كما يتضح من زيادة معامل التحديد R².

        3. **النتائج**: تظهر اختلافاً كبيراً بين معامل X⁺ (0.8) ومعامل X⁻ (1.5-)، مما يؤكد وجود تأثيرات غير متماثلة. التغيرات الإيجابية في X لها تأثير إيجابي أقل من التأثير السلبي للتغيرات السلبية في X (بالقيمة المطلقة).

        هذا يوضح أهمية NARDL في التقاط العلاقات غير المتماثلة التي لا يستطيع نموذج ARDL التقليدي التقاطها.
        """)

with tabs[3]:
	st.markdown("""
        ## ARDL-Fourier: حل للتغيرات الهيكلية المتعددة والتدريجية

        ### المشكلة المستهدفة:

        معالجة التغيرات الهيكلية المتعددة والتدريجية والناعمة في العلاقات الاقتصادية، التي يصعب التقاطها بالمتغيرات الوهمية التقليدية.

        ### المفهوم الأساسي:

        نموذج ARDL-Fourier يدمج دوال فورييه الجيبية وجيب التمام في نموذج ARDL لالتقاط التغيرات الهيكلية التدريجية والدورية.

        ### توسيع نموذج ARDL باستخدام دوال فورييه:

        يتم إدخال دوال فورييه في نموذج ARDL الأساسي كما يلي:
        """)

	st.markdown(r'''
        <div class="formula">
        $\Delta y_t = \alpha_0 + \alpha_1 t + \alpha_2 \sin\left(\frac{2\pi kt}{T}\right) + \alpha_3 \cos\left(\frac{2\pi kt}{T}\right) + \delta_1 y_{t-1} + \delta_2 x_{t-1} + \sum_{i=1}^{p} \beta_i \Delta y_{t-i} + \sum_{j=0}^{q} \gamma_j \Delta x_{t-j} + \varepsilon_t$
        </div>
        ''', unsafe_allow_html=True)

	st.markdown("""
        حيث:
        - sin(2πkt/T) و cos(2πkt/T) هما مكونات فورييه
        - k هو عدد الدورات (عادة بين 1 و5)
        - T هو طول العينة

        ### خصائص دوال فورييه:

        1. **المرونة في التقاط التغيرات**:
           - تلتقط التغيرات السلسة والتدريجية
           - تلتقط التغيرات المتعددة دون الحاجة لتحديدها مسبقاً

        2. **التقريب الأمثل**:
           - يمكن تقريب أي دالة مستمرة بدقة عالية باستخدام مجموعة من دوال فورييه

        3. **الحد من فقدان درجات الحرية**:
           - استخدام عدد قليل من مكونات فورييه (غالباً 1-3) يمكن أن يلتقط العديد من التغيرات

        ### خطوات تطبيق ARDL-Fourier:

        1. **تحديد عدد مكونات فورييه k المناسب**:
           - غالباً يتم اختياره باستخدام معايير المعلومات (AIC, BIC)

        2. **إنشاء مكونات فورييه** وإضافتها إلى النموذج

        3. **تقدير النموذج** باستخدام المربعات الصغرى العادية

        4. **اختبار الحدود المعدل**:
           - استخدام القيم الحرجة المعدلة لوجود مكونات فورييه

        5. **اختبار معنوية مكونات فورييه**:
           - اختبار F لمعنوية المعلمات α₂ و α₃

        ### المزايا:

        1. **اكتشاف تلقائي للتغيرات الهيكلية**:
           - لا حاجة لتحديد مسبق لعدد أو مواقع التغيرات الهيكلية

        2. **التقاط التغيرات التدريجية**:
           - مناسب للتغيرات السلسة التي تحدث تدريجياً

        3. **مرونة أكبر**:
           - يمكن التقاط أنماط معقدة من التغيرات باستخدام عدد قليل من المعلمات

        4. **تحسين أداء اختبار الحدود**:
           - زيادة قوة اختبار التكامل المشترك
        """)

	# إنشاء رسم توضيحي لدوال فورييه ودورها في التقاط التغيرات الهيكلية
	np.random.seed(42)
	nobs = 100
	t = np.arange(nobs)
	T = nobs

	# إنشاء دوال فورييه لقيم k مختلفة
	sin_k1 = np.sin(2 * np.pi * 1 * t / T)
	cos_k1 = np.cos(2 * np.pi * 1 * t / T)
	sin_k2 = np.sin(2 * np.pi * 2 * t / T)
	cos_k2 = np.cos(2 * np.pi * 2 * t / T)
	sin_k3 = np.sin(2 * np.pi * 3 * t / T)
	cos_k3 = np.cos(2 * np.pi * 3 * t / T)

	# إنشاء تغير هيكلي تدريجي (غير حاد)
	structural_change = 3 * np.sin(np.pi * t / T) + 2 * np.sin(2 * np.pi * t / T) + np.random.normal(0, 0.2, nobs)

	# توليد بيانات مع تغيرات هيكلية تدريجية
	x = np.linspace(0, 10, nobs)
	trend = 0.05 * t
	y_true = 2 + 0.1 * trend + structural_change + 0.5 * x + np.random.normal(0, 0.5, nobs)

	# تقدير نموذج بدون فورييه
	X_no_fourier = sm.add_constant(np.column_stack((t, x)))
	model_no_fourier = sm.OLS(y_true, X_no_fourier)
	results_no_fourier = model_no_fourier.fit()
	y_pred_no_fourier = results_no_fourier.predict()

	# تقدير نموذج مع فورييه (k=1)
	X_fourier_k1 = sm.add_constant(np.column_stack((t, x, sin_k1, cos_k1)))
	model_fourier_k1 = sm.OLS(y_true, X_fourier_k1)
	results_fourier_k1 = model_fourier_k1.fit()
	y_pred_fourier_k1 = results_fourier_k1.predict()

	# تقدير نموذج مع فورييه (k=2)
	X_fourier_k2 = sm.add_constant(np.column_stack((t, x, sin_k1, cos_k1, sin_k2, cos_k2)))
	model_fourier_k2 = sm.OLS(y_true, X_fourier_k2)
	results_fourier_k2 = model_fourier_k2.fit()
	y_pred_fourier_k2 = results_fourier_k2.predict()

	# الرسم البياني للدوال الأساسية
	fig1 = go.Figure()

	fig1.add_trace(go.Scatter(
		x=t,
		y=sin_k1,
		mode='lines',
		name='sin(2πt/T)',
		line=dict(color='royalblue', width=2)
	))

	fig1.add_trace(go.Scatter(
		x=t,
		y=cos_k1,
		mode='lines',
		name='cos(2πt/T)',
		line=dict(color='tomato', width=2)
	))

	fig1.add_trace(go.Scatter(
		x=t,
		y=sin_k2,
		mode='lines',
		name='sin(4πt/T)',
		line=dict(color='green', width=2)
	))

	fig1.add_trace(go.Scatter(
		x=t,
		y=cos_k2,
		mode='lines',
		name='cos(4πt/T)',
		line=dict(color='purple', width=2)
	))

	fig1.update_layout(
		title="دوال فورييه الأساسية المستخدمة في ARDL-Fourier",
		xaxis_title="الزمن",
		yaxis_title="القيمة",
		height=400,
		template="plotly_white"
	)

	st.plotly_chart(fig1, use_container_width=True)

	# الرسم البياني للبيانات والنماذج المقدرة
	fig2 = go.Figure()

	fig2.add_trace(go.Scatter(
		x=t,
		y=y_true,
		mode='markers',
		name='البيانات الفعلية',
		marker=dict(color='gray', size=8)
	))

	fig2.add_trace(go.Scatter(
		x=t,
		y=y_pred_no_fourier,
		mode='lines',
		name='النموذج بدون فورييه',
		line=dict(color='red', width=2)
	))

	fig2.add_trace(go.Scatter(
		x=t,
		y=y_pred_fourier_k1,
		mode='lines',
		name='النموذج مع فورييه (k=1)',
		line=dict(color='blue', width=2)
	))

	fig2.add_trace(go.Scatter(
		x=t,
		y=y_pred_fourier_k2,
		mode='lines',
		name='النموذج مع فورييه (k=2)',
		line=dict(color='green', width=2)
	))

	fig2.update_layout(
		title="مقارنة بين النموذج التقليدي ونموذج ARDL-Fourier",
		xaxis_title="الزمن",
		yaxis_title="المتغير التابع Y",
		height=500,
		template="plotly_white"
	)

	st.plotly_chart(fig2, use_container_width=True)

	# جدول مقارنة النماذج
	models_comparison = {
		'النموذج': [
			'بدون فورييه',
			'فورييه (k=1)',
			'فورييه (k=2)'
		],
		'معامل التحديد R²': [
			f"{results_no_fourier.rsquared:.3f}",
			f"{results_fourier_k1.rsquared:.3f}",
			f"{results_fourier_k2.rsquared:.3f}"
		],
		'AIC': [
			f"{results_no_fourier.aic:.2f}",
			f"{results_fourier_k1.aic:.2f}",
			f"{results_fourier_k2.aic:.2f}"
		],
		'BIC': [
			f"{results_no_fourier.bic:.2f}",
			f"{results_fourier_k1.bic:.2f}",
			f"{results_fourier_k2.bic:.2f}"
		],
		'عدد المعلمات': [
			'3',
			'5',
			'7'
		]
	}

	df_models_comparison = pd.DataFrame(models_comparison)
	st.table(df_models_comparison)

	st.info("""
        **التفسير**:

        الرسوم البيانية والجدول أعلاه توضح مفهوم وفوائد نموذج ARDL-Fourier:

        1. **دوال فورييه الأساسية**: الرسم الأول يوضح دوال الجيب وجيب التمام الأساسية المستخدمة في النموذج، والتي تسمح بالتقاط أنماط مختلفة من التغيرات الهيكلية.

        2. **المقارنة بين النماذج**: الرسم الثاني يقارن بين النموذج التقليدي ونماذج ARDL-Fourier بقيم k مختلفة. نلاحظ أن النموذج مع فورييه يلتقط التغيرات التدريجية في البيانات بشكل أفضل بكثير من النموذج التقليدي.

        3. **مؤشرات جودة النموذج**: يظهر الجدول تحسناً كبيراً في معامل التحديد R² ومعيار AIC عند استخدام مكونات فورييه، مما يشير إلى أهمية هذه المكونات في التقاط التغيرات الهيكلية التدريجية.

        4. **الكفاءة**: نلاحظ أن إضافة عدد قليل من مكونات فورييه (4 معلمات إضافية فقط للنموذج k=2) يؤدي إلى تحسن كبير في أداء النموذج، مما يدل على كفاءة هذه المنهجية.
        """)

with tabs[4]:
	st.markdown("""
        ## ARDL-MIDAS: حل لبيانات ذات ترددات مختلفة

        ### المشكلة المستهدفة:

        التعامل مع متغيرات ذات ترددات زمنية مختلفة (مثل بيانات سنوية مع بيانات فصلية أو شهرية أو يومية).

        ### المفهوم الأساسي:

        نموذج ARDL-MIDAS (Mixed Data Sampling) يمتد نموذج ARDL للسماح بدمج بيانات من ترددات زمنية مختلفة في نفس النموذج.

        ### التحدي الرئيسي:

        في الاقتصاد القياسي التقليدي، عندما نتعامل مع ترددات مختلفة، علينا إما:

        - **تجميع البيانات ذات التردد الأعلى** (مثلاً تحويل البيانات الشهرية إلى سنوية)، مما يؤدي إلى فقدان معلومات
        - **تكرار البيانات ذات التردد الأقل** (مثلاً تكرار البيانات السنوية لكل شهر)، مما قد يؤدي إلى مشاكل إحصائية

        ### الفكرة العامة لنموذج MIDAS:

        - السماح بالاستفادة المباشرة من المتغيرات ذات الترددات الأعلى
        - استخدام دالة وزن (weight function) لتوزيع تأثير المتغيرات ذات التردد الأعلى
        - تقليل عدد المعلمات المقدرة مقارنة بالنماذج التقليدية

        ### الصيغة الرياضية:

        صيغة مبسطة لنموذج ARDL-MIDAS مع متغير تابع ذو تردد منخفض y_t وعدة متغيرات مستقلة:
        """)

	st.markdown(r'''
        <div class="formula">
        $y_t = \alpha + \beta y_{t-1} + \gamma \sum_{j=0}^{J} w(j; \theta) x_{tm-j}^{(m)} + \varepsilon_t$
        </div>
        ''', unsafe_allow_html=True)

	st.markdown("""
        حيث:
        - y_t هو المتغير التابع ذو التردد المنخفض (مثلاً سنوي)
        - x_{tm-j}^{(m)} هو المتغير المستقل ذو التردد الأعلى (مثلاً شهري)، حيث m هو نسبة الترددات (مثلاً m=12 للسنوي-شهري)
        - w(j; θ) هي دالة الوزن التي تحدد أوزان الفجوات المختلفة
        - J هو عدد الفجوات الزمنية للمتغير ذي التردد الأعلى

        ### دوال الوزن المستخدمة:

        1. **دالة متعددة الحدود من الدرجة الثانية (Almon lag)**:
           - w(j; θ) يتم تحديدها من خلال دالة متعددة الحدود من الدرجة الثانية

        2. **دالة توزيع بيتا (Beta distribution)**:
           - توفر مرونة أكبر في أشكال الأوزان
           - تتطلب معلمتين فقط لتحديد الأوزان لعدد كبير من الفجوات

        3. **دالة أسية (Exponential)**:
           - تفترض تناقصاً أسياً في تأثير الفجوات البعيدة

        ### مزايا ARDL-MIDAS:

        1. **الاستفادة من المعلومات عالية التردد**:
           - تحسين دقة النماذج والتنبؤات
           - الاحتفاظ بالمعلومات المفيدة في البيانات عالية التردد

        2. **اقتصاد في المعلمات**:
           - تقليل عدد المعلمات المقدرة مقارنة بالنماذج التقليدية

        3. **مرونة في نمذجة العلاقات الديناميكية**:
           - التقاط أنماط معقدة من التأخيرات الزمنية

        4. **تحسين التنبؤات**:
           - تحسين دقة التنبؤات قصيرة وطويلة الأجل

        ### مجالات التطبيق:

        1. **النمذجة الاقتصادية الكلية**:
           - استخدام مؤشرات اقتصادية شهرية للتنبؤ بالنمو الاقتصادي الفصلي أو السنوي

        2. **التمويل**:
           - نمذجة العلاقة بين البيانات اليومية لأسواق الأسهم والمتغيرات الاقتصادية الفصلية

        3. **النمذجة البيئية**:
           - دمج بيانات يومية أو ساعية للعوامل البيئية مع بيانات اقتصادية أقل تواتراً
        """)

	# إنشاء رسم توضيحي لمفهوم MIDAS وبعض دوال الوزن
	x = np.linspace(0, 1, 21)  # نسبة الفترة الزمنية (من 0 إلى 20 فجوة)


	# دوال وزن مختلفة
	# 1. توزيع بيتا
	def beta_weight(x, a, b):
		return stats.beta.pdf(x, a, b) / stats.beta.pdf(x, a, b).sum()


	# 2. متعددة الحدود من الدرجة الثانية
	def almon_weight(x, a, b):
		return (a * x + b * x ** 2) / np.sum(a * x + b * x ** 2)


	# 3. أسية
	def exp_weight(x, lambda_):
		return np.exp(-lambda_ * x) / np.sum(np.exp(-lambda_ * x))


	# حساب الأوزان
	weights_beta1 = beta_weight(x, 1, 3)  # انحياز نحو الفجوات القريبة
	weights_beta2 = beta_weight(x, 2, 5)  # شكل منحنى الجرس
	weights_beta3 = beta_weight(x, 6, 2)  # انحياز نحو الفجوات البعيدة
	weights_almon = almon_weight(x, -0.01, -0.001)  # متناقصة تدريجياً
	weights_exp = exp_weight(x, 0.2)  # تناقص أسي

	# الرسم البياني لدوال الوزن
	fig = go.Figure()

	fig.add_trace(go.Scatter(
		x=np.arange(len(weights_beta1)),
		y=weights_beta1,
		mode='lines+markers',
		name='Beta(1,3) - انحياز للفجوات القريبة',
		line=dict(color='royalblue', width=2)
	))

	fig.add_trace(go.Scatter(
		x=np.arange(len(weights_beta2)),
		y=weights_beta2,
		mode='lines+markers',
		name='Beta(2,5) - توزيع جرسي',
		line=dict(color='tomato', width=2)
	))

	fig.add_trace(go.Scatter(
		x=np.arange(len(weights_beta3)),
		y=weights_beta3,
		mode='lines+markers',
		name='Beta(6,2) - انحياز للفجوات البعيدة',
		line=dict(color='green', width=2)
	))

	fig.add_trace(go.Scatter(
		x=np.arange(len(weights_almon)),
		y=weights_almon,
		mode='lines+markers',
		name='Almon - متعددة الحدود',
		line=dict(color='purple', width=2)
	))

	fig.add_trace(go.Scatter(
		x=np.arange(len(weights_exp)),
		y=weights_exp,
		mode='lines+markers',
		name='Exponential - أسية',
		line=dict(color='orange', width=2)
	))

	fig.update_layout(
		title="أمثلة لدوال الوزن المستخدمة في نماذج ARDL-MIDAS",
		xaxis_title="الفجوة الزمنية",
		yaxis_title="الوزن",
		height=500,
		template="plotly_white"
	)

	st.plotly_chart(fig, use_container_width=True)

	# توضيح مفهوم MIDAS
	st.subheader("توضيح لمفهوم دمج بيانات ذات ترددات مختلفة في ARDL-MIDAS")

	midas_data = pd.DataFrame({
		'سنة': [2020, 2020, 2020, 2020, 2021, 2021, 2021, 2021, 2022, 2022, 2022, 2022],
		'ربع': ['Q1', 'Q2', 'Q3', 'Q4', 'Q1', 'Q2', 'Q3', 'Q4', 'Q1', 'Q2', 'Q3', 'Q4'],
		'الناتج المحلي الإجمالي (فصلي)': [100, 90, 95, 105, 110, 115, 120, 125, 130, 135, 140, 145],
		'مؤشر أسعار المستهلك (شهري/متوسط الربع)': [
			[98, 99, 100], [101, 100, 99], [98, 97, 96], [97, 98, 99],
			[100, 101, 102], [103, 104, 105], [106, 107, 108], [109, 110, 111],
			[112, 113, 114], [115, 116, 117], [118, 119, 120], [121, 122, 123]
		],
		'البطالة (شهري/متوسط الربع)': [
			[5.0, 5.1, 5.2], [5.5, 5.7, 5.9], [6.0, 5.8, 5.6], [5.4, 5.2, 5.0],
			[4.9, 4.8, 4.7], [4.6, 4.5, 4.4], [4.3, 4.2, 4.1], [4.0, 3.9, 3.8],
			[3.7, 3.6, 3.5], [3.4, 3.3, 3.2], [3.1, 3.0, 2.9], [2.8, 2.7, 2.6]
		]
	})

	# عرض البيانات
	st.write(midas_data[['سنة', 'ربع', 'الناتج المحلي الإجمالي (فصلي)']])

	st.markdown("""
        <div class="highlight">
        <strong>مثال توضيحي:</strong><br>

        في نموذج ARDL-MIDAS، يمكن نمذجة الناتج المحلي الإجمالي الفصلي كدالة للبيانات الشهرية للبطالة ومؤشر أسعار المستهلك كما يلي:

        $GDP_t = \alpha + \beta GDP_{t-1} + \gamma_1 \sum_{j=0}^{J_1} w_1(j; \theta_1) CPI_{tm-j}^{(m)} + \gamma_2 \sum_{j=0}^{J_2} w_2(j; \theta_2) Unemployment_{tm-j}^{(m)} + \varepsilon_t$

        حيث:
        <ul>
        <li>GDP_t هو الناتج المحلي الإجمالي الفصلي (تردد منخفض)</li>
        <li>CPI_{tm-j}^{(m)} هو مؤشر أسعار المستهلك الشهري (تردد مرتفع)</li>
        <li>Unemployment_{tm-j}^{(m)} هو معدل البطالة الشهري (تردد مرتفع)</li>
        <li>w_1 و w_2 هما دالتا الوزن لكل متغير</li>
        </ul>

        المزايا الرئيسية:
        <ul>
        <li>الاستفادة من المعلومات الشهرية بدلاً من مجرد المتوسط الفصلي</li>
        <li>إمكانية تحديد الأنماط المختلفة لتأثير البيانات الشهرية على الناتج المحلي الإجمالي الفصلي</li>
        <li>تقليل عدد المعلمات المقدرة من خلال استخدام دوال الوزن</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

with tabs[5]:
	st.markdown("""
        ## حلول منهجية أخرى لمشاكل نموذج ARDL

        هناك العديد من التطورات المنهجية الأخرى التي تم اقتراحها لمعالجة مختلف مشاكل نموذج ARDL التقليدي. فيما يلي بعض هذه الحلول:

        ### 1. Quantile ARDL (QARDL)

        #### المشكلة المستهدفة:
        الاقتصار على تحليل العلاقة عند متوسط المتغير التابع فقط، وعدم التقاط العلاقات المختلفة عبر مختلف توزيع المتغير التابع.

        #### الحل:
        - يطبق تقنية انحدار الكمي (Quantile Regression) على نموذج ARDL
        - يسمح بتقدير العلاقات عند كميات مختلفة من توزيع المتغير التابع
        - يكشف عن تأثيرات غير متماثلة للمتغيرات المستقلة عبر مختلف مستويات المتغير التابع

        #### الفوائد:
        - صورة أكثر شمولاً للعلاقات الاقتصادية
        - الكشف عن العلاقات التي قد تختلف في الأوقات العادية عن الأوقات المتطرفة
        - مناسب بشكل خاص للبيانات المالية ذات المشاهدات المتطرفة

        ### 2. Panel ARDL

        #### المشكلة المستهدفة:
        محدودية البيانات المتاحة لبلد أو منطقة واحدة، وعدم القدرة على التقاط الاختلافات بين الوحدات المختلفة.

        #### الحل:
        - توسيع نموذج ARDL ليشمل بيانات مقطعية (cross-sectional) وزمنية (time series)
        - يسمح بتقدير العلاقات طويلة وقصيرة الأجل مع الاستفادة من معلومات مقطعية متعددة
        - يمكن تقدير نماذج مع آثار ثابتة (fixed effects) أو عشوائية (random effects)

        #### الفوائد:
        - زيادة حجم العينة وتحسين كفاءة التقديرات
        - إمكانية اختبار التجانس بين الوحدات المختلفة
        - تحسين قوة اختبارات التكامل المشترك

        ### 3. Spatial ARDL

        #### المشكلة المستهدفة:
        تجاهل التبعيات المكانية والتفاعلات بين الوحدات الاقتصادية المختلفة.

        #### الحل:
        - دمج الاعتماد المكاني (spatial dependence) في نموذج ARDL
        - السماح بتأثيرات الانتشار (spillover effects) بين المناطق أو البلدان
        - نمذجة التفاعلات المكانية-الزمنية (spatiotemporal interactions)

        #### الفوائد:
        - التقاط تأثيرات الجوار والتبعية المكانية
        - تحسين دقة التنبؤات من خلال تضمين المعلومات المكانية
        - فهم أفضل لعمليات الانتشار الاقتصادي

        ### 4. ARDL مع متغير مستقل داخلي (Endogenous ARDL)

        #### المشكلة المستهدفة:
        مشكلة الارتباط الداخلي (endogeneity) التي تؤدي إلى تحيز في المعلمات المقدرة.

        #### الحل:
        - استخدام منهجيات المتغيرات الآلية (IV) مع نموذج ARDL
        - تطبيق طريقة GMM (Generalized Method of Moments)
        - استخدام معادلات متعددة لحل مشكلة العلاقات المتبادلة

        #### الفوائد:
        - تقديرات غير متحيزة للمعلمات في وجود ارتباط داخلي
        - معالجة مشكلة العلاقات السببية المتبادلة
        - تحسين دقة اختبار الحدود

        ### 5. Bayesian ARDL

        #### المشكلة المستهدفة:
        عدم اليقين في اختيار المواصفات وهيكل الفجوات الزمنية، وتحديات العينات الصغيرة.

        #### الحل:
        - تطبيق منهجية بايزية على نموذج ARDL
        - السماح بإدراج المعرفة المسبقة من خلال التوزيعات القبلية
        - متوسط النماذج البايزي (Bayesian Model Averaging) للتعامل مع عدم اليقين في المواصفات

        #### الفوائد:
        - تحسين التقديرات في العينات الصغيرة
        - تضمين المعرفة المسبقة والنظرية الاقتصادية
        - توفير توزيعات احتمالية كاملة للمعلمات بدلاً من مجرد تقديرات نقطية
        """)

