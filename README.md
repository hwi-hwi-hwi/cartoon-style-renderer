# 🎨 Cartoon Style Renderer

A Python image processing tool that converts photos into cartoon-style images using OpenCV.

## ✅ 주요 OpenCV 함수 설명

**1. `cv2.bilateralFilter()`**
```python
cv2.bilateralFilter(color, d=9, sigmaColor=300, sigmaSpace=300)
```
- 경계(Edge)는 뚜렷하게 유지하면서 내부 색상을 부드럽게 블러링하는 고급 필터입니다.

- 본 프로젝트에서는 이를 7번 반복 적용하여, 사진의 복잡한 색상을 만화처럼 단순하고 평탄한 색 영역(Flat Color)으로 압축시켰습니다.

**2. `cv2.cvtColor()`**
```python
cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```
- 이미지를 BGR 컬러에서 그레이스케일로 변환합니다.

- 카툰 렌더링에서는 펜선(윤곽선)을 명확하게 검출하기 위해 컬러 대신 밝기만 남기는 흑백 이미지가 필요합니다.

**3. `cv2.medianBlur()`**
```python
cv2.medianBlur(gray, 5)
```
- 중간값 필터를 적용하여 이미지의 노이즈를 제거합니다.

- 특히 윤곽선을 흐릿하게 만들지 않으면서 점처럼 생긴 잡음(Salt-and-pepper noise)을 제거하는 데 탁월합니다.

**4. `cv2.adaptiveThreshold()`**
```python
cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
```
- 전체 이미지가 아닌 국소 영역의 밝기값에 따라 자동으로 임계값을 계산하여 윤곽선을 검출합니다.

- 조명 변화가 있거나 그림자가 진 이미지에서도 만화책의 펜선 같은 경계를 아주 잘 잡아냅니다.

**5. `cv2.bitwise_and()`**
```python
cv2.bitwise_and(color, color, mask=edges)
```
- 검출된 윤곽선 마스크(Mask)와 색상 단순화 이미지를 결합합니다.

- 엣지가 있는 부분만 검은색 선으로 칠해주는 만화 테두리 효과를 구현하는 핵심 단계입니다.

## 🧠 전체 흐름 요약
1. 원본 이미지 불러오기

2. Bilateral Filter 반복 적용으로 색상 단순화 (수채화/만화 채색 효과)

3. BGR → Grayscale로 변환

4. Median Blur로 노이즈 제거

5. Adaptive Threshold로 뚜렷한 스케치 윤곽선(Edge) 추출

6. Bitwise AND 연산으로 단순화된 색상과 윤곽선을 합성하여 카툰 효과 완성

## 🖼️ 필터 결과 비교 (성공 vs 실패)
아래 이미지들은 본 알고리즘을 적용한 카툰 필터 결과입니다. 피사체의 특성에 따른 결과물의 차이를 통해 필터의 한계를 확인할 수 있습니다.
(왼쪽: 원본 / 오른쪽: Rendering 후)
### 🌟 1. 성공 데모: 주술회전 피규어 (고죠 사토루 / 게토 스구루)
![고죠_cartoon_result](https://github.com/user-attachments/assets/aa61bf24-1562-4b90-a572-4cf4e847107e)

![게토_cartoon_result](https://github.com/user-attachments/assets/e5356924-2de4-4ad8-8cc2-e9b4c089ed73)


- 결과: 엣지가 뚜렷하고 색상 대비가 명확해 만화 스타일이 아주 잘 표현되었습니다.

- 이유: 애니메이션 피규어 특성상 표면이 매끄럽고 단색 위주로 구성되어 있어, Bilateral Filter의 색상 평탄화와 Adaptive Threshold의 펜선 추출이 아주 효과적으로 작동했습니다.

### ❌ 2. 실패 데모: 쿼카 & 원숭이 인형
![cartoon_result](https://github.com/user-attachments/assets/0e93df35-09eb-4ce1-81b4-a27d636811cd)


- 결과: 만화 특유의 깔끔함이 완전히 사라지고, 불필요한 노이즈가 낀 것처럼 지저분하게 렌더링 되었습니다.

- 이유: 솜인형 특유의 미세한 '털 질감(Texture)' 때문에 노이즈가 낀 것처럼 지저분하게 렌더링 됐습니다. 엣지 검출기가 형태를 구분하는 외곽선뿐만 아니라 털 사이사이의 미세한 명암까지 모두 윤곽선으로 인식해버렸기 때문에 결과가 아쉬웠습니다.

## 📌 알고리즘의 한계
- 입력 이미지의 조명, 표면 질감, 색상 대비에 따라 결과가 크게 달라집니다.

- adaptiveThreshold()는 배경이나 피사체에 미세한 텍스처(예: 털, 거친 바위 등)가 많을 경우 이를 모두 윤곽선으로 검출해 이미지를 지저분하게 만듭니다.

- 강하고 불규칙한 그림자가 있는 경우 경계가 무분별하게 추출되어, bilateralFilter가 수행하는 본연의 색상 평탄화(Flat Color) 작업을 크게 방해합니다.

- 조명이나 해상도가 크게 다른 사진의 경우 bilateralFilter 파라미터나 반복 횟수를 범용적으로 적용하기 어려워 수동 튜닝이 필요합니다.
