@echo off
chcp 65001 >nul
title OHZDIS v4.3.0

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║     OHZDIS v4.3.0  -  ONE HEALTH        ║
echo  ║     Zoonotic Disease Intelligence        ║
echo  ╚══════════════════════════════════════════╝
echo.

echo  [1/3] 리포트 생성 중...
python generate_report.py
echo.

echo  [2/3] 서버 시작 중...
start "" python server.py
timeout /t 4 /nobreak >nul

echo  [3/3] 브라우저 실행 중...
start "" http://localhost:5000
start "" ohzdis_report.html

echo.
echo  ✅ 완료!
echo.
echo  대시보드:  http://localhost:5000
echo  리포트:    ohzdis_report.html
echo  현장입력:  http://localhost:5000/field
echo.
echo  (이 창은 닫아도 됩니다)
pause
