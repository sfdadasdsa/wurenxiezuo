# 五人协作共享空间 - 本地启动器
$port = 5678
$root = Split-Path $MyInvocation.MyCommand.Path

# 用 .NET HTTP Listener (无需 Python)
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")
$listener.Prefixes.Add("http://127.0.0.1:$port/")
$listener.Start()

Write-Host "===================================" -ForegroundColor Cyan
Write-Host "  五人协作共享空间" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  本地地址: http://localhost:$port" -ForegroundColor Green
Write-Host ""

# 显示局域网地址
$ips = [System.Net.Dns]::GetHostAddresses([System.Net.Dns]::GetHostName()) | Where-Object { $_.AddressFamily -eq 'InterNetwork' -and $_.Address -ne '127.0.0.1' }
foreach ($ip in $ips) {
    Write-Host "  局域网: http://$($ip.IPAddressToString):$port" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "  按 Ctrl+C 停止服务器" -ForegroundColor DarkGray
Write-Host "===================================" -ForegroundColor Cyan

# 打开浏览器
Start-Process "http://localhost:$port/"

while ($listener.IsListening) {
    $context = $listener.GetContext()
    $req = $context.Request
    $res = $context.Response

    $path = $req.Url.LocalPath.TrimStart('/')
    if ([string]::IsNullOrEmpty($path)) { $path = "index.html" }
    $file = Join-Path $root $path

    if (Test-Path $file -PathType Leaf) {
        $content = [System.IO.File]::ReadAllBytes($file)
        $ext = [System.IO.Path]::GetExtension($file)
        $mime = @{
            '.html'='text/html; charset=utf-8'
            '.css'='text/css'
            '.js'='application/javascript'
            '.png'='image/png'
            '.jpg'='image/jpeg'
            '.svg'='image/svg+xml'
        }
        $res.ContentType = if ($mime.ContainsKey($ext)) { $mime[$ext] } else { 'application/octet-stream' }
        $res.OutputStream.Write($content, 0, $content.Length)
    } else {
        $res.StatusCode = 404
        $data = [System.Text.Encoding]::UTF8.GetBytes("<h1>404 - 文件未找到</h1>")
        $res.OutputStream.Write($data, 0, $data.Length)
    }
    $res.OutputStream.Close()
}
