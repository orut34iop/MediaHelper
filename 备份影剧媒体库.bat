@echo off
:: ����Ƿ��Թ���Ա�������
echo ���ڼ�����ԱȨ��...
openfiles >nul 2>nul
if %errorlevel% neq 0 (
    echo ��ǰ�ű�δ�Թ���ԱȨ�����У������������ԱȨ��...
    powershell -Command "Start-Process cmd -ArgumentList '/c', '%~s0' -Verb runAs"
    exit /b
)

echo starting backup movie data ....

:: ����ԴĿ¼��Ŀ��Ŀ¼
echo ����ԴĿ¼��Ŀ��Ŀ¼...

set dest_dir=C:\emby-as-115\backup

set tv_source_dir=C:\emby-as-115\TV
set movie_source_dir=C:\emby-as-115\MOVIE

set tv_archive_name=TV.rar
set movie_archive_name=MOVIE.rar

:: ����ʵ�ʰ�װ·���޸�
set rar_path="C:\Program Files\WinRAR\rar.exe"

:: ��� WinRAR �Ƿ����
echo ��� WinRAR �Ƿ��Ѱ�װ...
if not exist %rar_path% (
    echo WinRAR δ��װ��·������ȷ������ WinRAR ��װĿ¼��
    exit /b
)


:: ��ʾ��ѹ�����ļ��кͱ���·��
echo ��Ҫѹ�����ļ���: %tv_source_dir% , %movie_source_dir%
echo ѹ������������: %dest_dir%

:: ִ��ѹ������
echo ��ʼѹ���ļ���...

echo starting backup tv data ..
%rar_path% a -r -m0  -ol "%dest_dir%\%tv_archive_name%" "%tv_source_dir%\*"

:: ���ѹ���Ƿ�ɹ�
if %errorlevel% equ 0 (
    echo ѹ����ɣ�ѹ�����ѱ����� %dest_dir%\%tv_archive_name%.
) else (
    echo ѹ�������з�������������־��
)

echo starting backup movie data ....
%rar_path% a -r -m0  -ol "%dest_dir%\%movie_archive_name%" "%movie_source_dir%\*"

:: ���ѹ���Ƿ�ɹ�
if %errorlevel% equ 0 (
    echo ѹ����ɣ�ѹ�����ѱ����� %dest_dir%\%movie_archive_name%.
) else (
    echo ѹ�������з�������������־��
)

:: ���ѹ���Ƿ�ɹ�
if %errorlevel% equ 0 (
    echo ѹ����ɣ�ѹ�����ѱ����� %dest_dir%\%archive_name%.
) else (
    echo ѹ�������з�������������־��
)

:: �����ʾ
echo �ű�ִ����ϣ�
pause