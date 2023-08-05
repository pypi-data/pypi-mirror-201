@echo off

echo ***********************
echo * Confirm to continue *
echo ***********************
pause

rmdir /s /q build dist pybw.egg-info

python setup.py sdist bdist_wheel 

twine upload dist/* 

pause
