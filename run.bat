:loop
git pull
cd src
call gen.bat
cd ..
git diff --stat
git add *
git commit -m "update content"
git push
timeout /t 300
goto :loop