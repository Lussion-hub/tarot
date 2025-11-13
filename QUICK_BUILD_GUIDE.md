# 빠른 APK 빌드 가이드 (GitHub Actions)

## 🚀 3단계로 APK 빌드하기

### 1단계: GitHub 저장소 생성 및 코드 업로드

```bash
# 1. GitHub에 새 저장소 생성
# https://github.com/new 에서 새 저장소 만들기

# 2. 로컬에서 Git 초기화 (아직 안 했다면)
git init
git add .
git commit -m "Initial commit: Tarot Card App"

# 3. GitHub 저장소와 연결
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 2단계: GitHub Actions 실행

1. GitHub 저장소 페이지로 이동
2. 상단 메뉴에서 **"Actions"** 탭 클릭
3. 왼쪽 사이드바에서 **"Build Android APK"** 워크플로우 선택
4. 오른쪽 상단의 **"Run workflow"** 버튼 클릭
5. **"Run workflow"** 버튼 다시 클릭하여 실행

### 3단계: APK 다운로드

1. 워크플로우 실행이 시작되면 진행 상황을 볼 수 있습니다
2. 빌드는 약 **30-60분** 정도 소요됩니다
3. 빌드가 완료되면 (초록색 체크 표시):
   - **"tarot-app-apk"** Artifacts 섹션 클릭
   - APK 파일 다운로드

## 📱 APK 설치 방법

1. 다운로드한 APK 파일을 Android 기기로 전송
2. Android 기기에서:
   - 설정 > 보안 > 알 수 없는 소스 허용
   - APK 파일을 탭하여 설치

## ⚠️ 주의사항

- 첫 빌드는 시간이 오래 걸립니다 (의존성 다운로드 포함)
- 빌드 중에는 GitHub Actions 페이지를 열어두세요
- 빌드 실패 시 로그를 확인하세요

## 🔄 코드 수정 후 재빌드

코드를 수정한 후:

```bash
git add .
git commit -m "Update app"
git push
```

푸시하면 자동으로 빌드가 시작됩니다!

## 📝 빌드 상태 확인

- GitHub 저장소의 Actions 탭에서 모든 빌드 이력을 확인할 수 있습니다
- 빌드 실패 시 로그를 확인하여 문제를 해결하세요

