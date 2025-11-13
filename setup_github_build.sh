#!/bin/bash
# GitHub Actions를 사용한 APK 빌드 설정 스크립트

echo "=========================================="
echo "타로 카드 앱 - GitHub Actions 빌드 설정"
echo "=========================================="
echo ""

# Git 저장소 확인
if [ ! -d ".git" ]; then
    echo "Git 저장소를 초기화합니다..."
    git init
    git add .
    git commit -m "Initial commit: Tarot Card App"
    echo ""
    echo "✅ Git 저장소가 초기화되었습니다."
    echo ""
fi

echo "다음 단계를 따라주세요:"
echo ""
echo "1. GitHub에 새 저장소를 생성하세요:"
echo "   https://github.com/new"
echo ""
echo "2. 저장소 이름을 입력하세요 (예: tarot-card-app)"
echo ""
echo "3. 다음 명령어를 실행하세요:"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. GitHub 저장소의 Actions 탭으로 이동하세요"
echo ""
echo "5. 'Build Android APK' 워크플로우를 실행하세요"
echo ""
echo "6. 빌드가 완료되면 Artifacts에서 APK를 다운로드하세요"
echo ""
echo "=========================================="

