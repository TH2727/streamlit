import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
file_path = '서울특별시 서초구_어린이보호구역_20240603.csv'  # 실제 파일 경로
data = pd.read_csv(file_path, encoding='cp949')

# Streamlit 제목
st.title("서울특별시 서초구 어린이 보호구역 지도 및 데이터 분석")

# 사이드바 설정
st.sidebar.header("필터 설정")
facility_type = st.sidebar.multiselect(
    "시설 종류 선택", data['시설종류'].unique(), default=data['시설종류'].unique()
)
cctv_installed = st.sidebar.selectbox(
    "CCTV 설치 여부", ['전체', '설치', '미설치']
)

# 데이터 필터링
filtered_data = data[data['시설종류'].isin(facility_type)]
if cctv_installed != '전체':
    filtered_data = filtered_data[filtered_data['CCTV설치여부'] == cctv_installed]

# 지도 생성
st.subheader("어린이 보호구역 위치 지도")
fig = px.scatter_mapbox(
    filtered_data,
    lat='위도',
    lon='경도',
    color='시설종류',
    hover_name='대상시설명',
    hover_data=['소재지도로명주소', 'CCTV설치여부'],
    title="서초구 어린이 보호구역 지도",
    mapbox_style="open-street-map",
    zoom=12
)
st.plotly_chart(fig)

# 시각화 추가: 시설 종류별 분포
st.subheader("시설 종류별 분포")
facility_distribution = filtered_data['시설종류'].value_counts().reset_index()
facility_distribution.columns = ['시설종류', 'count']
distribution_fig = px.bar(
    facility_distribution,
    x='시설종류',
    y='count',
    labels={'시설종류': '시설 종류', 'count': '개수'},
    title="시설 종류별 개수 분포",
    color='시설종류',
    text_auto=True
)
st.plotly_chart(distribution_fig)

# 데이터 테이블
st.subheader("필터링된 데이터 테이블")
st.dataframe(filtered_data)
