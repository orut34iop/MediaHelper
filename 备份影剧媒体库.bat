@echo off
:: ��ȡ��ǰϵͳ����
setlocal enabledelayedexpansion

:: ����Ƿ��Թ���Ա�������
echo ���ڼ�����ԱȨ��...
openfiles >nul 2>nul
if %errorlevel% neq 0 (
    echo ��ǰ�ű�δ�Թ���ԱȨ�����У������������ԱȨ��...
    powershell -Command "Start-Process cmd -ArgumentList '/c', '%~s0' -Verb runAs"
    exit /b
)

:: ����ԴĿ¼��Ŀ��Ŀ¼
echo ����ԴĿ¼��Ŀ��Ŀ¼...

set dest_dir=C:\emby-as-115\backup

set tv_source_dir=C:\emby-as-115\TV
set movie_source_dir=C:\emby-as-115\MOVIE
set embyserver_programdata_dir=C:\Users\wiz\AppData\Roaming\Emby-Server\programdata

set tv_archive_name=TV.rar
set movie_archive_name=MOVIE.rar
set embyserver_programdata_archive_name=programdata.rar


:: ����ʵ�ʰ�װ·���޸�
set rar_path="C:\Program Files\WinRAR\rar.exe"

:: ��� WinRAR �Ƿ����
echo ��� WinRAR �Ƿ��Ѱ�װ...
if not exist %rar_path% (
    echo WinRAR δ��װ��·������ȷ������ WinRAR ��װĿ¼��
    exit /b
)

echo ��ǰ����·����: %CD%

:: ���Emby Server�Ƿ�������
set "program_name=EmbyServer.exe"
tasklist /FI "IMAGENAME eq %program_name%" | findstr /I /C:"%program_name%" > nul
if !errorlevel! equ 0 (
    echo Emby Server �������У�׼��ǿ���˳�...
    taskkill /IM %program_name% /F
    echo Emby Server ���˳���
) else (
    echo Emby Server û�������С�
)



set "program_name=embytray.exe"
tasklist /FI "IMAGENAME eq %program_name%" | findstr /I /C:"%program_name%" > nul
if !errorlevel! equ 0 (
    echo Emby Tray �������У�׼��ǿ���˳�...
    taskkill /IM %program_name% /F
    echo Emby Tray ���˳���
) else (
    echo Emby Tray û�������С�
)

 
:: ��ȡ��ǰ����
for /F "tokens=1-3 delims=/ " %%a in ('date /t') do (
    set year=%%a
    set month=%%b
    set day=%%c
)
 
:: ��ʽ��ΪYYYY-MM-DD
set datefolder=%year%-%month%-%day%
 
echo �������ݵ�Ŀ¼���ƣ�   %datefolder%


:: �����Ե�ǰ���������ı����ļ���
if not exist "%dest_dir%" mkdir "%dest_dir%"
set "backupdir=%dest_dir%\%datefolder%"
if not exist "%backupdir%" mkdir "%backupdir%"


:: ѹ���ļ���
echo ����ѹ�� EmbyServer App data �ļ��� %embyserver_programdata_dir% ...
"C:\Program Files\WinRAR\WinRAR.exe" a -r -m0 "%backupdir%\%embyserver_programdata_archive_name%" "%embyserver_programdata_dir%\*"

:: ���ѹ���Ƿ�ɹ�
if !errorlevel! equ 0 (
    echo �ļ���ѹ���ɹ���ѹ���������� "%backupdir%\%embyserver_programdata_archive_name%"��
) else (
    echo �ļ���ѹ��ʧ�ܡ�
)

echo starting backup movie data ....





:: ��ʾ��ѹ�����ļ��кͱ���·��
echo ��Ҫѹ�����ļ���: %tv_source_dir% , %movie_source_dir%
echo ѹ������������: %backupdir%

:: ִ��ѹ������
echo ��ʼѹ���ļ���...

echo starting backup tv data ..
%rar_path% a -r -m0  -ol "%backupdir%\%tv_archive_name%" "%tv_source_dir%\*"

:: ���ѹ���Ƿ�ɹ�
if %errorlevel% equ 0 (
    echo ѹ����ɣ�ѹ�����ѱ����� %backupdir%\%tv_archive_name%.
) else (
    echo ѹ�������з�������������־��
)

echo starting backup movie data ....
%rar_path% a -r -m0  -ol "%backupdir%\%movie_archive_name%" "%movie_source_dir%\*"

:: ���ѹ���Ƿ�ɹ�
if %errorlevel% equ 0 (
    echo ѹ����ɣ�ѹ�����ѱ����� %backupdir%\%movie_archive_name%.
) else (
    echo ѹ�������з�������������־��
)

echo �������ݵ�Ŀ¼��   %backupdir%

:: �����ʾ
echo �ű�ִ����ϣ�
pause