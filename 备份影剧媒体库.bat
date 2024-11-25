@echo off
:: 检查是否以管理员身份运行
echo 正在检查管理员权限...
openfiles >nul 2>nul
if %errorlevel% neq 0 (
    echo 当前脚本未以管理员权限运行，正在请求管理员权限...
    powershell -Command "Start-Process cmd -ArgumentList '/c', '%~s0' -Verb runAs"
    exit /b
)

echo starting backup movie data ....

:: 设置源目录和目标目录
echo 设置源目录和目标目录...

set dest_dir=C:\emby-as-115\backup

set tv_source_dir=C:\emby-as-115\TV
set movie_source_dir=C:\emby-as-115\MOVIE

set tv_archive_name=TV.rar
set movie_archive_name=MOVIE.rar

:: 根据实际安装路径修改
set rar_path="C:\Program Files\WinRAR\rar.exe"

:: 检查 WinRAR 是否存在
echo 检查 WinRAR 是否已安装...
if not exist %rar_path% (
    echo WinRAR 未安装或路径不正确，请检查 WinRAR 安装目录。
    exit /b
)


:: 显示待压缩的文件夹和保存路径
echo 将要压缩的文件夹: %tv_source_dir% , %movie_source_dir%
echo 压缩包将保存至: %dest_dir%

:: 执行压缩命令
echo 开始压缩文件夹...

echo starting backup tv data ..
%rar_path% a -r -m0  -ol "%dest_dir%\%tv_archive_name%" "%tv_source_dir%\*"

:: 检查压缩是否成功
if %errorlevel% equ 0 (
    echo 压缩完成！压缩包已保存至 %dest_dir%\%tv_archive_name%.
) else (
    echo 压缩过程中发生错误，请检查日志。
)

echo starting backup movie data ....
%rar_path% a -r -m0  -ol "%dest_dir%\%movie_archive_name%" "%movie_source_dir%\*"

:: 检查压缩是否成功
if %errorlevel% equ 0 (
    echo 压缩完成！压缩包已保存至 %dest_dir%\%movie_archive_name%.
) else (
    echo 压缩过程中发生错误，请检查日志。
)

:: 检查压缩是否成功
if %errorlevel% equ 0 (
    echo 压缩完成！压缩包已保存至 %dest_dir%\%archive_name%.
) else (
    echo 压缩过程中发生错误，请检查日志。
)

:: 完成提示
echo 脚本执行完毕！
pause