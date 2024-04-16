@echo off

REM Vérification de la présence de Python
where python > nul 2>nul
if %errorlevel% neq 0 (
    echo Python n'est pas installé sur ce système.
    pause
    exit /b
)

REM Installation des modules nécessaires
python -m pip install matplotlib pandas numpy openpyxl

REM Vérification de la réussite de l'installation
if %errorlevel% neq 0 (
    echo Erreur lors de l'installation des modules.
    exit /b
)

REM Demande du nom de la feuille de calcul à l'utilisateur
echo Entrez le nom de la feuille voulue dans le fichier excel, ou "all" si vous les voulez toutes" :
set /p fileName=

REM Exécution du script Python avec le nom de la feuille de calcul en argument
python main.py "%fileName%"

REM Optionnel : Attendre une action de l'utilisateur pour fermer la fenêtre
pause
