# 타로 카드 앱 - Android 버전

이 앱은 기존 Python Tkinter 타로 카드 선택 프로그램을 Android 모바일 앱으로 변환한 것입니다.

## 주요 기능

- 색도형카드 선택 및 순차 표시
- 타로 뒷면 플립
- 타로 앞면 순차 표시
- 이미지 흐림 효과
- 카드 선택 및 완료 화면

## 설치 및 빌드 방법

### 1. 필수 요구사항

- Python 3.8 이상
- Buildozer
- Android SDK 및 NDK
- Linux 또는 macOS (Windows에서는 WSL 또는 가상 머신 필요)

### 2. Buildozer 설치

```bash
pip install buildozer
```

### 3. Android SDK/NDK 설정

Android SDK와 NDK를 설치하고 환경 변수를 설정하세요.

### 4. 이미지 파일 준비

Android 기기의 `/sdcard/TarotProject/` 디렉토리에 다음 폴더 구조로 이미지 파일을 배치하세요:

```
/sdcard/TarotProject/
├── 도형_색카드/
│   └── *.webp (또는 *.png, *.jpg)
├── Rider_Waite/
│   └── compressed/
│       ├── AA_tarot/
│       │   └── *.webp
│       └── AB_tarot/
│           └── *.webp
├── 태극비디오/
│   └── GU_shcaled_4.mp4
└── 고속노출시배경/
    └── *.jpg (또는 *.png)
```

### 5. APK 빌드

```bash
buildozer android debug
```

또는 릴리즈 버전:

```bash
buildozer android release
```

빌드된 APK는 `bin/` 디렉토리에 생성됩니다.

## 사용 방법

1. 앱을 실행하면 메인 화면이 표시됩니다.
2. 이미지 경로를 설정하거나 기본 경로를 사용합니다.
3. 변수 설정(시간, 동시카드수, 흐림효과)을 조정합니다.
4. "색도형카드 선택" 버튼을 눌러 시작합니다.
5. 카드를 선택하고 순차적으로 진행합니다.
6. 타로 카드를 선택하고 완료 버튼을 눌러 결과를 확인합니다.

## 주의사항

- Android 5.0 (API 21) 이상 필요
- 외부 저장소 권한이 필요합니다
- 이미지 파일은 기기의 SD 카드에 저장되어 있어야 합니다
- 첫 실행 시 저장소 권한을 허용해야 합니다

## 문제 해결

### 이미지가 표시되지 않는 경우
- 이미지 파일 경로가 올바른지 확인하세요
- 파일 형식(.webp, .png, .jpg)을 확인하세요
- 저장소 권한이 허용되었는지 확인하세요

### 앱이 크래시되는 경우
- 로그를 확인하세요: `adb logcat | grep python`
- 이미지 파일이 손상되지 않았는지 확인하세요
- 메모리 부족일 수 있으니 다른 앱을 종료해보세요

## 개발자 정보

원본 프로그램: my_tarot_sim_v6_blur.py
Android 변환: Kivy 프레임워크 사용

