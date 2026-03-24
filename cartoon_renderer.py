import cv2 as cv
import numpy as np


def cartoonize_image(img):  # 입력 이미지를 Cartoon(만화) 스타일로 변환하는 함수
    # Cartoon 스타일의 두 가지 핵심
    # 1. 색감 단순화 (Flat Color) -> Bilateral Filter 반복 적용
    # 2. 뚜렷한 외곽선 (Bold Edge) -> Adaptive Thresholding

    # STEP 1) 색감 단순화 -> Bilateral Filter (양방향 필터): 경계선은 유지하면서 색을 단순하게
    color = img.copy()
    for _ in range(7):
        color = cv.bilateralFilter(
            color,
            d = 9,              # Kernel 크기
            sigmaColor = 300,   # 색상 범위 (클수록 색이 더 단순해짐)
            sigmaSpace = 300    # 공간 범위 (클수록 넓은 영역 참조)
        )

    # STEP 2) Edge 추출
    # 2-1) Grayscale 변환, Edge Detection을 위해 흑백 이미지로 변환
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # 2-2) Median Blur: 노이즈 제거
    # Gaussian보다 Salt-and-Pepper 노이즈 제거에 효과적 + 동시에 Edge(경계선)는 잘 보존됨
    gray_blur = cv.medianBlur(gray, 5)

    # 2-3) Adaptive Thresholding: 외곽선 추출
    #  전체 이미지에 동일한 기준이 아닌 지역마다 다른 기준 적용 -> 조명이 고르지 않아도 깔끔한 외곽선 추출 가능
    edges = cv.adaptiveThreshold(
        gray_blur,                  # 입력 이미지
        255,                        # 최대값 (흰색)
        cv.ADAPTIVE_THRESH_MEAN_C,  # 주변 픽셀 평균 기반 Threshold
        cv.THRESH_BINARY,           # Binary 방식
        9,                          # Block Size: 지역 영역 크기 (홀수여야 함)
        9                           # C값: 평균에서 빼는 보정값
    )
    # 결과: 외곽선만 흰색으로 남은 흑백 이미지

    # STEP 3) 색감 + Edge 합성
    # bitwise_and: edges가 흰색(255)인 곳만 color 이미지를 보여줌 -> 외곽선이 있는 부분만 색상 표시 = Cartoon 스타일 완성
    cartoon = cv.bitwise_and(color, color, mask=edges)

    return cartoon


def main():
    # 이미지 불러오기
    img_path = 'image.jpg'
    output_path = 'cartoon_result.jpg'

    img = cv.imread(img_path)

    # 이미지 정상 로드 확인
    if img is None:
        print(f"이미지를 불러올 수 없습니다. {img_path}")
        print("파일 경로와 파일명을 확인해주세요")
        return

    # cartoon 변환 실행
    cartoon = cartoonize_image(img)

    # 원본 이미지와 결과 이미지를 가로로 나란히 이어 붙이기
    combined_image = np.hstack((img, cartoon))

    # 결과 출력: 원본 vs Cartoon 비교 (하나의 창에 병합된 이미지가 뜹니다)
    cv.imshow('Original vs Cartoon', combined_image)

    print("아무 키를 눌러 종료하세요.")
    cv.waitKey(0)
    cv.destroyAllWindows()

    # 결과 저장
    cv.imwrite(output_path, combined_image)
    print(f"저장 완료: {output_path}")


if __name__ == "__main__":
    main()