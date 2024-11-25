@echo off
:: 获取当前系统日期
setlocal enabledelayedexpansion

:: 检查是否以管理员身份运行
echo 正在检查管理员权限...
openfiles >nul 2>nul
if %errorlevel% neq 0 (
    echo 当前脚本未以管理员权限运行，正在请求管理员权限...
    powershell -Command "Start-Process cmd -ArgumentList '/c', '%~s0' -Verb runAs"
    exit /b
)

:: 设置源目录和目标目录
echo 设置源目录和目标目录...

set dest_dir=C:\emby-as-115\backup

set tv_source_dir=C:\emby-as-115\TV
set movie_source_dir=C:\emby-as-115\MOVIE
set embyserver_programdata_dir=C:\Users\wiz\AppData\Roaming\Emby-Server\programdata

set tv_archive_name=TV.rar
set movie_archive_name=MOVIE.rar
set embyserver_programdata_archive_name=programdata.rar


:: 根据实际安装路径修改
set rar_path="C:\Program Files\WinRAR\rar.exe"

:: 检查 WinRAR 是否存在
echo 检查 WinRAR 是否已安装...
if not exist %rar_path% (
    echo WinRAR 未安装或路径不正确，请检查 WinRAR 安装目录。
    exit /b
)

echo 当前运行路径是: %CD%

:: 检测Emby Server是否在运行
set "program_name=EmbyServer.exe"
tasklist /FI "IMAGENAME eq %program_name%" | findstr /I /C:"%program_name%" > nul
if !errorlevel! equ 0 (
    echo Emby Server 正在运行，准备强制退出...
    taskkill /IM %program_name% /F
    echo Emby Server 已退出。
) else (
    echo Emby Server 没有在运行。
)



set "program_name=embytray.exe"
tasklist /FI "IMAGENAME eq %program_name%" | findstr /I /C:"%program_name%" > nul
if !errorlevel! equ 0 (
    echo Emby Tray 正在运行，准备强制退出...
    taskkill /IM %program_name% /F
    echo Emby Tray 已退出。
) else (
    echo Emby Tray 没有在运行。
)

 
:: 获取当前日期
for /F "tokens=1-3 delims=/ " %%a in ('date /t') do (
    set year=%%a
    set month=%%b
    set day=%%c
)
 
:: 格式化为YYYY-MM-DD
set datefolder=%year%-%month%-%day%
 
echo 保存数据的目录名称：   %datefolder%


:: 创建以当前日期命名的备份文件夹
if not exist "%dest_dir%" mkdir "%dest_dir%"
set "backupdir=%dest_dir%\%datefolder%"
if not exist "%backupdir%" mkdir "%backupdir%"


:: 压缩文件夹
echo 正在压缩 EmbyServer App data 文件夹 %embyserver_programdata_dir% ...
"C:\Program Files\WinRAR\WinRAR.exe" a -r -m0 "%backupdir%\%embyserver_programdata_archive_name%" "%embyserver_programdata_dir%\*"

:: 检查压缩是否成功
if !errorlevel! equ 0 (
    echo 文件夹压缩成功，压缩包保存在 "%backupdir%\%embyserver_programdata_archive_name%"。
) else (
    echo 文件夹压缩失败。
)

echo starting backup movie data ....





:: 显示待压缩的文件夹和保存路径
echo 将要压缩的文件夹: %tv_source_dir% , %movie_source_dir%
echo 压缩包将保存至: %backupdir%

:: 执行压缩命令
echo 开始压缩文件夹...

echo starting backup tv data ..
%rar_path% a -r -m0  -ol "%backupdir%\%tv_archive_name%" "%tv_source_dir%\*"

:: 检查压缩是否成功
if %errorlevel% equ 0 (
    echo 压缩完成！压缩包已保存至 %backupdir%\%tv_archive_name%.
) else (
    echo 压缩过程中发生错误，请检查日志。
)

echo starting backup movie data ....
%rar_path% a -r -m0  -ol "%backupdir%\%movie_archive_name%" "%movie_source_dir%\*"

:: 检查压缩是否成功
if %errorlevel% equ 0 (
    echo 压缩完成！压缩包已保存至 %backupdir%\%movie_archive_name%.
) else (
    echo 压缩过程中发生错误，请检查日志。
)

echo 备份数据的目录：   %backupdir%

:: 完成提示
echo 脚本执行完毕！
pause