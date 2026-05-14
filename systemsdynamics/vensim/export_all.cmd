@echo off
REM Run this from the folder containing your M-01.mdl ... M-19.mdl files
REM Adjust the path to Vensim's vensimdp.exe to match your installation

set VENSIM="C:\Program Files\Vensim\vensimdp.exe"

for %%i in (M-01 M-02 M-03 M-04 M-05 M-06 M-07 M-08 M-09 M-10 M-11 M-12 M-13 M-14 M-15 M-16 M-17 M-18 M-19) do (
    echo Running %%i...
    %VENSIM% %%i.mdl
)
echo Done. Now export each .vdfx to CSV manually in Vensim GUI,
echo or use the Python script below if you have pysd installed.
pause