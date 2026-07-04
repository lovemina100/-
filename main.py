import streamlit as st
import pandas as pd

# 1. 웹 브라우저 설정
st.set_page_config(page_title="K-POP 아이돌 아카이브", page_icon="💿", layout="centered")

# 2. 초호화 아이돌 데이터베이스 (예시 데이터입니다. 원하는 대로 확장해 보세요!)
idol_data = [
    {
        "성별": "여자아이돌", 
        "소속사": "에스엠 (SM)", 
        "그룹명": "에스파", 
        "로고": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500", # 예시 이미지 (실제 로고 URL로 교체 가능)
        "데뷔일": "2020년 11월 17일",
        "멤버": ["카리나", "지젤", "윈터", "닝닝"], 
        "유명한 노래": "Next Level, Supernova", 
        "추천 수록곡": "Lucid Dream, Thirsty",
        "레전드 무대": "https://www.youtube.com/results?search_query=에스파+레전드+무대",
        "역대 앨범": ["Black Mamba (정식)", "Next Level", "Savage", "Girls", "MY WORLD", "Drama", "Armageddon"],
        "평균키": 164.5, 
        "남팬비율": 40, "여팬비율": 60
    },
    {
        "성별": "남자아이돌", 
        "소속사": "하이브 (HYBE)", 
        "그룹명": "라이즈", 
        "로고": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=500", 
        "데뷔일": "2023년 9월 4일",
        "멤버": ["쇼타로", "은석", "성찬", "원빈", "소희", "앤톤"], 
        "유명한 노래": "Get A Guitar, Boom Boom Bass", 
        "추천 수록곡": "Honestly, Memories",
        "레전드 무대": "https://www.youtube.com/results?search_query=라이즈+레전드+무대",
        "역대 앨범": ["Get A Guitar", "Talk Saxy", "Love 119", "RIIZING"],
        "평균키": 179.0, 
        "남팬비율": 25, "여팬비율": 75
    }
]

# 데이터프레임 변환
df = pd.DataFrame(idol_data)

# 3. 메인 타이틀
st.title("💿 K-POP 아이돌 올인원 아카이브")
st.write("소속사별 필터링부터 데뷔일, 앨범 역사, 팬 비율, 레전드 무대까지 한눈에 확인하세요!")
st.markdown("---")

# 4. 사이드바 검색 및 필터 설정
st.sidebar.header("🔍 아카이브 필터")
gender_option = st.sidebar.radio("1. 성별 선택", options=["전체", "남자아이돌", "여자아이돌"])
companies = ["전체"] + sorted(list(df["소속사"].unique()))
company_option = st.sidebar.selectbox("2. 소속사 선택", options=companies)

# 데이터 필터링 규칙 적용
filtered_df = df.copy()
if gender_option != "전체":
    filtered_df = filtered_df[filtered_df["성별"] == gender_option]
if company_option != "전체":
    filtered_df = filtered_df[filtered_df["소속사"] == company_option]

# 5. 검색된 기본 목록 출력
st.subheader(f"📊 등록된 아이돌 목록 ({len(filtered_df)}팀)")
if not filtered_df.empty:
    # 화면 표에는 가독성을 위해 리스트 데이터를 문자열로 변환해서 보여줌
    display_df = filtered_df.copy()
    display_df["멤버"] = display_df["멤버"].apply(lambda x: ", ".join(x))
    st.dataframe(display_df[["성별", "소속사", "그룹명", "데뷔일", "멤버"]], use_container_width=True)
else:
    st.warning("조건에 맞는 아이돌이 없습니다. 필터를 변경해 보세요!")

st.markdown("---")

# 6. 대망의 상세 분석 구역 (사용자가 특정 그룹을 선택했을 때 작동)
if not filtered_df.empty:
    st.subheader("🔍 선택한 아이돌 상세 프로필")
    selected_group = st.selectbox("자세히 분석할 그룹을 골라보세요 👇", options=filtered_df["그룹명"].tolist())
    
    # 선택된 그룹의 상세 데이터 한 줄 추출
    group_info = filtered_df[filtered_df["그룹명"] == selected_group].iloc[0]
    
    # 레이아웃 나누기 (왼쪽: 로고 이미지 / 오른쪽: 그룹 기본 정보)
    col_img, col_info = st.columns([1, 2])
    
    with col_img:
        # 로고 이미지 출력 (width로 크기 조절 가능)
        st.image(group_info["로고"], caption=f"{selected_group} 공식 로고/이미지", use_container_width=True)
        
    with col_info:
        st.markdown(f"### 👑 {selected_group}")
        st.write(f"📅 **데뷔일:** {group_info['데뷔일']}")
        st.write(f"🏢 **소속사:** {group_info['소속사']}")
        st.write(f"📏 **평균 키:** {group_info['평균키']} cm")
        # 레전드 무대 유튜브 검색 링크 버튼 생성
        st.link_button("📺 레전드 무대 보러가기 (YouTube)", group_info["레전드 무대"])

    # 탭 기능으로 상세 정보 나누기
    tab1, tab2, tab3 = st.tabs(["👤 멤버 & 앨범 역사", "🎵 명곡 아카이브", "📊 팬덤 데이터 분석"])
    
    with tab1:
        st.write("### 👥 멤버 구성 (개인)")
        # 멤버 리스트를 보기 좋게 불릿 포인트로 출력
        for member in group_info["멤버"]:
            st.write(f"- ✨ **{member}**")
            
        st.write("### 🗂️ 역대 발매 앨범 목록")
        # 앨범 리스트 순서대로 나열
        for i, album in enumerate(group_info["역대 앨범"], 1):
            st.write(f"{i}. 💿 {album}")
        
    with tab2:
        st.write("### 🌟 타이틀곡 & 추천 수록곡")
        st.success(f"🎤 **가장 유명한 노래 (타이틀):** {group_info['유명한 노래']}")
        st.info(f"🎧 **팬들이 추천하는 숨은 명곡 (수록곡):** {group_info['추천 수록곡']}")
            
    with tab3:
        st.write("### 📈 남녀 팬 비율 그래프")
        # 가로 바 차트로 시각화
        fan_data = pd.DataFrame({
            "성별 비율 (%)": [group_info["남팬비율"], group_info["여팬비율"]]
        }, index=["남팬 (Male)", "여팬 (Female)"])
        st.bar_chart(fan_data)
        
        # 숫자로도 보여주기
        c1, c2 = st.columns(2)
        c1.metric("🙋‍♂️ 남팬 비율", f"{group_info['남팬비율']}%")
        c2.metric("🙋‍♀️ 여팬 비율", f"{group_info['여팬비율']}%")
