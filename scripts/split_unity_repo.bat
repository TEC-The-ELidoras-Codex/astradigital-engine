@echo off
echo Creating directory for clean Unity project...
mkdir TEC_AI_ENGINE_CLEAN
echo Copying essential Unity files...
xcopy /E /I TEC_AI_ENGINE\Assets TEC_AI_ENGINE_CLEAN\Assets
xcopy /E /I TEC_AI_ENGINE\ProjectSettings TEC_AI_ENGINE_CLEAN\ProjectSettings
xcopy /E /I TEC_AI_ENGINE\Packages TEC_AI_ENGINE_CLEAN\Packages
echo Initializing new git repository for clean Unity project...
cd TEC_AI_ENGINE_CLEAN
git init
copy ..\.gitattributes .
copy ..\.gitignore .
echo # TEC AI ENGINE > README.md
git add .
git commit -m "Initial Unity project files (clean version)"
echo Done! TEC_AI_ENGINE_CLEAN is ready to be pushed to GitHub
