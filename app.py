import streamlit as st
import pandas as pd
import math

# 🚨 [모바일 최적화 CSS - 헤더 삭제 및 버튼 크기 콤팩트화]
st.markdown("""
<style>
/* 상단 헤더(빈 공간) 완전 삭제 -> 찌꺼기 텍스트 원천 차단 */
header[data-testid="stHeader"] {
    display: none !important;
}
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 1.5rem !important;
}
/* 모바일용 버튼/입력칸 크기 축소 (스크롤 최적화) */
[data-testid="stButton"] button {
    min-height: 36px !important;
    height: 36px !important;
    padding: 0px 4px !important;
    font-size: 14px !important;
    line-height: 1 !important;
}
[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input {
    min-height: 36px !important;
    height: 36px !important;
    padding: 0px 8px !important;
    font-size: 14px !important;
}
div[data-testid="column"] {
    padding-left: 0.2rem !important;
    padding-right: 0.2rem !important;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="고호계산기 (모바일용)", page_icon="📱", layout="centered")

# ==========================================
# 전역 변수 및 유틸리티 함수
# ==========================================
def parse_int(val):
    try: return int(str(val).replace(",", "").replace("원", "").replace("만", "").strip())
    except: return 0

def format_input(key):
    val = str(st.session_state[key]).replace(",", "").replace("원", "").replace("만", "").strip()
    if val.isdigit(): st.session_state[key] = f"{int(val):,}"

def click_00(key):
    val = str(st.session_state[key]).replace(",", "").replace("원", "").replace("만", "").strip()
    if val.isdigit() and int(val) > 0: st.session_state[key] = f"{int(val) * 100:,}"

def click_man(key):
    val = str(st.session_state[key]).replace(",", "").replace("원", "").replace("만", "").strip()
    if val.isdigit() and int(val) > 0: st.session_state[key] = f"{int(val) * 10000:,}"

def format_manwon(val):
    if val <= 0: return "0만원"
    return f"{int(val // 10000):,}만원"

def calculate_pmt(principal, rate, months):
    if principal <= 0: return 0
    r = (rate / 100) / 12
    if r == 0: return principal / months
    return math.floor((principal * r * ((1 + r) ** months)) / (((1 + r) ** months) - 1))

# Session State 초기화
input_keys = ['a_sal_25', 'a_sal_26', 'a_sal_est', 'a_debt_total', 'a_card_total', 'a_final_req', 'a_card_year', 'a_all_sim', 'a_na_sim', 'c_calc_amt']
for k in input_keys:
    if k not in st.session_state: st.session_state[k] = "0" if k not in ['a_card_year', 'a_all_sim', 'a_na_sim'] else ""

if 'a_bank_pct' not in st.session_state: st.session_state.a_bank_pct = 73.0
if 'c_calc_rate' not in st.session_state: st.session_state.c_calc_rate = None
if 'c_calc_months' not in st.session_state: st.session_state.c_calc_months = 0
if 'quick_month' not in st.session_state: st.session_state.quick_month = "직접 입력"
if 'calc_table_df' not in st.session_state: st.session_state.calc_table_df = pd.DataFrame()
if 'content_text' not in st.session_state: st.session_state.content_text = "분석 탭에서 [보고서 생성]을 눌러주세요."
if 'briefing_text' not in st.session_state: st.session_state.briefing_text = "분석 탭에서 [보고서 생성]을 눌러주세요."

def reset_calc():
    st.session_state.c_calc_amt = "0"
    st.session_state.c_calc_rate = None
    st.session_state.c_calc_months = 0
    st.session_state.quick_month = "직접 입력"
    st.toast("계산기가 초기화되었습니다!", icon="🔄")

def set_months():
    val = st.session_state.quick_month
    if val != "직접 입력":
        st.session_state.c_calc_months = int(val)

# ==========================================
# 화면 레이아웃 시작
# ==========================================
st.title("📱 빠른 고호계산기")
tab_calc, tab_analysis, tab_content, tab_briefing = st.tabs(["🧮 론계산기", "📊 분석", "📝 내용", "📢 브리핑"])

# ==========================================
# 탭 1: 론 계산기 
# ==========================================
with tab_calc:
    c_hdr1, c_hdr2 = st.columns([3, 1])
    with c_hdr1: st.header("🧮 대출 이자 계산")
    with c_hdr2: st.markdown("<br>", unsafe_allow_html=True); st.button("🔄 초기화", use_container_width=True, on_click=reset_calc, key="btn_reset_calc")
    
    lc1, lc2, lc3 = st.columns([5, 1.5, 1.5], vertical_alignment="bottom")
    with lc1: st.text_input("대출 금액 (원)", key="c_calc_amt", on_change=format_input, args=("c_calc_amt",))
    with lc2: st.button("00", key="z_calc_amt", on_click=click_00, args=("c_calc_amt",), use_container_width=True)
    with lc3: st.button("만", key="m_calc_amt", on_click=click_man, args=("c_calc_amt",), use_container_width=True)
        
    m_col, r_col = st.columns(2)
    method_1 = m_col.selectbox("상환 방법", ["원리금균등", "원금균등", "만기일시"])
    rate_1 = r_col.number_input("금리 (%)", min_value=0.0, max_value=24.0, step=0.1, key="c_calc_rate")
    
    mon_col, quick_col = st.columns(2, vertical_alignment="bottom")
    with mon_col: months_1 = st.number_input("기간 (개월)", min_value=0, max_value=360, step=1, key="c_calc_months")
    with quick_col: st.selectbox("📅 빠른 선택", ["직접 입력", "36", "48", "60", "72", "84", "120"], key="quick_month", on_change=set_months)

    if st.button("계산하기", type="primary", use_container_width=True):
        principal = parse_int(st.session_state.c_calc_amt)
        calc_rate = rate_1 if rate_1 is not None else 0.0
        monthly_rate = (calc_rate / 100) / 12
        tot_int = 0; bal = principal; sch = []
        first_month_pay = 0
        
        if principal > 0 and months_1 > 0:
            if "원리금" in method_1:
                pmt = calculate_pmt(principal, calc_rate, months_1)
                first_month_pay = pmt
                for i in range(1, months_1 + 1):
                    inte = math.floor(bal * monthly_rate)
                    prin = pmt - inte
                    bal -= prin
                    if i == months_1: prin += bal; pmt += bal; bal = 0
                    tot_int += inte
                    sch.append({"회차": i, "납입금": pmt, "잔액": bal})
            elif "원금" in method_1:
                m_prin = math.floor(principal / months_1)
                for i in range(1, months_1 + 1):
                    inte = math.floor(bal * monthly_rate)
                    pay = m_prin + inte
                    if i == 1: first_month_pay = pay
                    bal -= m_prin
                    if i == months_1: pay += bal; bal = 0
                    tot_int += inte
                    sch.append({"회차": i, "납입금": pay, "잔액": bal})
            else:
                m_int = math.floor(principal * monthly_rate)
                first_month_pay = m_int
                for i in range(1, months_1 + 1):
                    pay = m_int
                    if i == months_1: pay += principal; bal = 0
                    tot_int += m_int
                    sch.append({"회차": i, "납입금": pay, "잔액": bal})
            
            cc1, cc2, cc3 = st.columns(3)
            pay_label = "월 납입금" if "원리금" in method_1 or "만기" in method_1 else "월 납입금(1회차)"
            cc1.metric(pay_label, f"{first_month_pay:,} 원")
            cc2.metric("총 대출이자", f"{tot_int:,} 원")
            cc3.metric("총 상환금액", f"{principal + tot_int:,} 원")
            
            st.dataframe(pd.DataFrame(sch), use_container_width=True, hide_index=True)
        else:
            st.warning("대출 금액과 기간을 0보다 큰 숫자로 올바르게 입력해주세요.")

# ==========================================
# 탭 2: 분석 (Av 한도/보고서 산출 로직)
# ==========================================
with tab_analysis:
    st.header("📊 연봉 및 한도 분석")
    st.info("숫자 입력 후 빈 화면을 터치하면 콤마가 찍힙니다. (단위: 만원)")

    st.subheader("1. 연봉 입력")
    c1, c2, c3 = st.columns(3)
    with c1: st.text_input("25년 (만원)", key="a_sal_25", on_change=format_input, args=("a_sal_25",))
    with c2: st.text_input("26년 (만원)", key="a_sal_26", on_change=format_input, args=("a_sal_26",))
    with c3: st.text_input("추정연봉 (만원)", key="a_sal_est", on_change=format_input, args=("a_sal_est",))

    st.subheader("2. 대출/내용 기초정보 (보고서용)")
    c4, c5 = st.columns(2)
    with c4: st.text_input("현재 기대출 총액 (만원)", key="a_debt_total", on_change=format_input, args=("a_debt_total",))
    with c5: st.text_input("현재 카드잔액 합계 (만원)", key="a_card_total", on_change=format_input, args=("a_card_total",))
    
    c6, c7, c8 = st.columns(3)
    with c6: st.text_input("카드개설년도", key="a_card_year")
    with c7: st.text_input("올시뮬", key="a_all_sim")
    with c8: st.text_input("나시뮬", key="a_na_sim")

    st.subheader("3. 목표 설계 설정")
    c9, c10 = st.columns(2)
    with c9: st.text_input("최종 필요금액 (만원)", key="a_final_req", on_change=format_input, args=("a_final_req",))
    with c10: st.number_input("은행 한도 비율 (%)", min_value=0.0, max_value=200.0, step=1.0, key="a_bank_pct")

    # 계산 버튼
    if st.button("🚀 한도 산출 및 보고서 생성", type="primary", use_container_width=True):
        # 파싱
        s25 = parse_int(st.session_state.a_sal_25)
        s26 = parse_int(st.session_state.a_sal_26)
        s_est = parse_int(st.session_state.a_sal_est)
        debt = parse_int(st.session_state.a_debt_total)
        card = parse_int(st.session_state.a_card_total)
        final_req_man = parse_int(st.session_state.a_final_req)
        bank_pct = st.session_state.a_bank_pct

        final_amt = final_req_man * 10000
        sal_won = s_est * 10000

        # 은행 한도 산출
        bank_amt = round((sal_won * (bank_pct / 100)) / 500000) * 500000

        # 햇살론 산출 (Av 로직 그대로)
        base_sun = 7000000 if 20000000 <= sal_won <= 29999999 else 10000000 if 30000000 <= sal_won <= 44600000 else 0
        sun_amt = min(max(0, final_amt - bank_amt), base_sun) if base_sun > 0 else 0
        
        if sun_amt > 0:
            raw_sun_m = calculate_pmt(sun_amt, 11.0, 84)
            sun_m = round(raw_sun_m / 10000) * 10000
        else:
            sun_m = 0

        # 2금융권 산출 (최종금액 - 은행 - 햇살론)
        sec2_amt = max(0, final_amt - bank_amt - sun_amt)
        
        # 월 납입금 계산
        bp5 = calculate_pmt(bank_amt, 9.0, 60)
        bp7 = calculate_pmt(bank_amt, 9.0, 84)
        bp10 = calculate_pmt(bank_amt, 9.0, 120)
        p_sec2 = calculate_pmt(sec2_amt, 15.0, 72)

        # UI 출력용
        st.markdown("---")
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("최종 필요금액", format_manwon(final_amt))
        r2.metric(f"은행 ({bank_pct}%)", format_manwon(bank_amt))
        r3.metric("햇살론", format_manwon(sun_amt))
        r4.metric("2금융", format_manwon(sec2_amt))

        st.markdown(f"<div style='background-color:#e3f2fd; padding:10px; border-radius:5px; margin-bottom:10px;'><span style='color:#1565c0; font-weight:bold;'>2금융 월납입(6년): {format_manwon(p_sec2)}</span></div>", unsafe_allow_html=True)

        stxt = format_manwon(sun_m) if sun_m > 0 else "•"
        table_data = [
            ["5년", format_manwon(bp5), stxt, format_manwon(p_sec2), format_manwon(bp5 + sun_m + p_sec2)],
            ["7년", format_manwon(bp7), stxt, format_manwon(p_sec2), format_manwon(bp7 + sun_m + p_sec2)],
            ["10년", format_manwon(bp10), stxt, format_manwon(p_sec2), format_manwon(bp10 + sun_m + p_sec2)]
        ]
        df_calc = pd.DataFrame(table_data, columns=["기간", "은행", "햇살론", "2금융", "합계"])
        st.dataframe(df_calc, use_container_width=True, hide_index=True)

        # ----------------------------------------------------
        # 보고서 (내용/브리핑) 텍스트 자동 생성
        # ----------------------------------------------------
        cy = st.session_state.a_card_year
        als = st.session_state.a_all_sim
        ns = st.session_state.a_na_sim
        
        ratio_str = ""
        if s25 == 0 and s26 == 0 and s_est > 0:
            sal_block = f"추정연봉 {format_manwon(sal_won)}"
            ratio_str = f"({int((final_amt / sal_won) * 100)}%)" if sal_won > 0 else ""
        else:
            sal_block = f"25납부 {s25}만원\n26납부 {s26}만원"
            r_list = []
            if s25 > 0: r_list.append(f"({int((final_amt / (s25*10000)) * 100)}%)")
            if s26 > 0: r_list.append(f"({int((final_amt / (s26*10000)) * 100)}%)")
            ratio_str = "".join(r_list)

        cd = f"카드 {card}만, " if card > 0 else ""
        
        def line_text(p, b):
            parts = [format_manwon(b)] + ([format_manwon(sun_m)] if sun_m > 0 else []) + ([format_manwon(p_sec2)] if p_sec2 > 0 else [])
            return f"[{p}] {'+'.join(parts)} = {format_manwon(b + sun_m + p_sec2)}"

        # [내용] 텍스트 구성
        content = f"{sal_block}\n카드개설 {cy}년\n{cd}올시뮬 {als}, 나시뮬 {ns}\n{format_manwon(debt*10000)} 상환후 12%포함 약 {format_manwon(final_amt)} {ratio_str}\n\n"
        content += f"은행 {format_manwon(bank_amt)}\n5년 {format_manwon(bp5)}\n7년 {format_manwon(bp7)}\n10년 {format_manwon(bp10)}\n\n"
        if sun_m > 0: content += f"햇살론 {format_manwon(sun_m)}\n{format_manwon(sun_amt)}\n\n"
        if sec2_amt > 0: content += f"2금융 {format_manwon(sec2_amt)}\n{format_manwon(p_sec2)}\n\n"
        content += f"{line_text('5년', bp5)}\n{line_text('7년', bp7)}\n{line_text('10년', bp10)}"

        # [브리핑] 텍스트 구성
        brief = f"고객은 가능하며\n{format_manwon(debt*10000)} 상환후 12%포함 약 {format_manwon(final_amt)}\n\n"
        brief += f"은행 {format_manwon(bank_amt)}(평균9%대)"
        if sun_m > 0: brief += f"\n햇살론 {format_manwon(sun_amt)}(평균11%대)"
        if sec2_amt > 0: brief += f"\n2금 {format_manwon(sec2_amt)}(평균15%대)(6년)"
        if card > 0: brief += f"\n(카드금액 {format_manwon(card*10000)} 포함)"
        brief += f"\n\n{line_text('5년', bp5)}\n{line_text('7년', bp7)}\n{line_text('10년', bp10)}\n\n"
        brief += "예상합니다.\n(요즘 은행이 잘안나오기에 은행금액을 75%로 계산했으나\n고객 인지시 연봉대비 65%~85%  말씀해주시면 됩니다.)\n수수료 인지 및 은행 5년 월불입액 동의 후 담당자분 성함, 수수료, \n고객 연락처 주시면 제가 전화 드리도록 하겠습니다!"

        # Session State에 저장하여 탭 이동 시 출력
        st.session_state.content_text = content.strip()
        st.session_state.briefing_text = brief.strip()
        st.toast("보고서 생성이 완료되었습니다! 탭을 이동하여 확인하세요.", icon="✅")

# ==========================================
# 탭 3: 내용 
# ==========================================
with tab_content:
    st.header("📝 고객 내용")
    st.info("👇 박스 우측 상단의 겹친 네모 아이콘(📋)을 누르면 모바일에서도 즉시 복사됩니다.")
    st.code(st.session_state.content_text, language="text")

# ==========================================
# 탭 4: 브리핑
# ==========================================
with tab_briefing:
    st.header("📢 브리핑 멘트")
    st.info("👇 박스 우측 상단의 겹친 네모 아이콘(📋)을 누르면 모바일에서도 즉시 복사됩니다.")
    st.code(st.session_state.briefing_text, language="text")
