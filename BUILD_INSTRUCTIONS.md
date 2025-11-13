# Android APK 빌드 가이드

## ⚠️ 중요: Windows 환경 제한사항

Buildozer는 **Linux 또는 macOS 환경**에서만 작동합니다. Windows에서는 다음 방법 중 하나를 사용해야 합니다:

## 방법 1: WSL (Windows Subsystem for Linux) 사용 (권장)

### 1. WSL 설치
```powershell
wsl --install
```

### 2. Ubuntu 설치 후 WSL 실행
```bash
# Ubuntu에서 실행
sudo apt update
sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

### 3. Buildozer 설치
```bash
pip3 install --user buildozer
export PATH=$PATH:~/.local/bin
```

### 4. Android SDK/NDK 설정
```bash
# Android SDK 설치
mkdir -p ~/.buildozer/android/platform
cd ~/.buildozer/android/platform
# Android SDK Command Line Tools 다운로드 및 설치 필요
```

### 5. APK 빌드
```bash
cd /mnt/c/Users/김진찬/Desktop/AI/cursor
buildozer android debug
```

## 방법 2: Docker 사용

### 1. Docker Desktop 설치

### 2. Docker 이미지 사용
```bash
docker run --rm -v %cd%:/app kivy/buildozer buildozer android debug
```

## 방법 3: 클라우드 빌드 서비스

- **GitHub Actions** 사용
- **GitLab CI/CD** 사용
- **CircleCI** 사용

## 방법 4: Linux 가상 머신 사용

VirtualBox나 VMware에 Ubuntu를 설치하고 위의 WSL 방법과 동일하게 진행

## 빠른 테스트: 로컬 Python 실행

APK 빌드 전에 데스크톱에서 앱이 정상 작동하는지 확인:

```bash
pip install kivy pillow opencv-python-headless numpy
python main.py
```

## 빌드 성공 시

빌드가 성공하면 `bin/` 폴더에 APK 파일이 생성됩니다:
- `bin/tarotapp-0.1-arm64-v8a-debug.apk`
- `bin/tarotapp-0.1-armeabi-v7a-debug.apk`

## 문제 해결

### 빌드 오류 발생 시
1. `buildozer.spec` 파일 확인
2. Android SDK/NDK 경로 확인
3. 로그 파일 확인: `.buildozer/` 폴더

### 권한 문제
```bash
chmod +x ~/.buildozer/android/platform/android-sdk/tools/bin/*
```

## 참고 사항

- 첫 빌드는 시간이 오래 걸릴 수 있습니다 (30분~1시간)
- 인터넷 연결이 필요합니다
- 최소 10GB 이상의 여유 공간이 필요합니다

