# 五人空间 - 一键启动
$port = 5678
$dir = "D:\workspace\五人协作"
$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.*" -and $_.IPAddress -notlike "127.*"} | Select -First 1).IPAddress

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  五人空间 - 启动中..." -ForegroundColor White
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Start server
$j = Start-Job -ScriptBlock { param($p,$d) python.exe -m http.server $p -d $d } -ArgumentList $port,$dir
Start-Sleep 1

Write-Host "  ✅ 服务器已启动!" -ForegroundColor Green
Write-Host ""
Write-Host "  💻 本机:     http://localhost:$port/" -ForegroundColor Green
Write-Host "  📱 局域网:   http://$($ip):$port/" -ForegroundColor Yellow
Write-Host ""
Write-Host "  PWA: 用Chrome打开 → 地址栏安装应用" -ForegroundColor White
Write-Host ""
Write-Host "  按 Ctrl+C 停止服务器" -ForegroundColor DarkGray
Write-Host "==================================" -ForegroundColor Cyan

Start-Process "http://localhost:$port/"
