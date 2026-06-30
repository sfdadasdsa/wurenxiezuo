# GitHub Pages 自动部署脚本
# 注册完成后运行此脚本

$user = "xingyuan456"
$repo = "wuren-space"
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${user}:xuhao123"))
$headers = @{ Authorization = "Basic $auth" }

# 1. 创建仓库
Write-Host "正在创建仓库..."
$body = @{name=$repo; description="五人协作空间"; auto_init=$true} | ConvertTo-Json
try {
    $r = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Headers $headers -Method Post -Body $body -ContentType "application/json"
    Write-Host "仓库创建成功!" -ForegroundColor Green
} catch {
    Write-Host "仓库可能已存在: $_" -ForegroundColor Yellow
}

# 2. 上传所有文件
Write-Host "正在上传文件..."
$files = @("index.html","m1.html","m2.html","m3.html","m4.html","m5.html","manifest.json","sw.js","icon.svg","samoyed.mp4","启动.cmd","部署说明.txt")
$dir = "D:\workspace\五人协作"

foreach ($file in $files) {
    $path = Join-Path $dir $file
    if (Test-Path $path) {
        $content = [Convert]::ToBase64String([IO.File]::ReadAllBytes($path))
        $putBody = @{
            message = "上传 $file"
            content = $content
            branch = "main"
        } | ConvertTo-Json
        
        try {
            $r = Invoke-RestMethod -Uri "https://api.github.com/repos/${user}/${repo}/contents/$file" -Headers $headers -Method Put -Body $putBody -ContentType "application/json"
            Write-Host "  ✅ $file" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ $file : $_" -ForegroundColor Red
        }
    }
}

# 3. 开启 GitHub Pages
Write-Host "正在开启 GitHub Pages..."
$pagesBody = @{source = @{branch = "main"; path = "/"}} | ConvertTo-Json
try {
    $r = Invoke-RestMethod -Uri "https://api.github.com/repos/${user}/${repo}/pages" -Headers $headers -Method Post -Body $pagesBody -ContentType "application/json"
    Write-Host "Pages 已开启!" -ForegroundColor Green
} catch {
    Write-Host "Pages 开启失败: $_" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================"
Write-Host "  部署完成!"
Write-Host "  等2分钟后访问:"
Write-Host "  https://${user}.github.io/${repo}/"
Write-Host "================================"
