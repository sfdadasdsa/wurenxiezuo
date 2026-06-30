@echo off
chcp 65001 >nul
echo ========================================
echo   五人拼图空间 - 一键部署到 Gitee
echo ========================================
echo.
echo 第一步：请先在浏览器登录 https://gitee.com
echo 第二步：访问 https://gitee.com/personal_access_tokens
echo         创建一个新令牌，权限选：projects, files
echo 第三步：将令牌粘贴到下方
echo.
set /p TOKEN=请输入 Gitee 个人访问令牌: 
if "%TOKEN%"=="" goto error

echo.
echo 正在部署到 Gitee...
python deploy_to_gitee.py %TOKEN%
if %ERRORLEVEL% NEQ 0 goto error

echo.
echo ✅ 部署成功！
echo 你的网页地址: https://xingyuan456.gitee.io/wuren-kongjian
echo.
pause
exit /b 0

:error
echo ❌ 部署失败，请检查令牌是否正确
pause
