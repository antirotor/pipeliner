$current_dir = Get-Location
$script_dir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$root_dir = (Get-Item $script_dir).parent.FullName

function Install-Poetry() {
    Write-Host ">>> Installing Poetry ... "
    $python = "python"
    if (Get-Command "pyenv" -ErrorAction SilentlyContinue) {
        if (-not (Test-Path -PathType Leaf -Path "$($root_dir)\.python-version")) {
            $result = & pyenv global
            if ($result -eq "no global version configured") {
                Write-Host "!!! Using pyenv but having no local or global version of Python set."
                Exit-WithCode 1
            }
        }
        $python = & pyenv which python

    }

    $env:POETRY_HOME="$root_dir\.poetry"
    (Invoke-WebRequest -Uri https://install.python-poetry.org/ -UseBasicParsing).Content | & $($python) -
}


Write-Host ">>> Reading Poetry ... "
if (-not (Test-Path -PathType Container -Path "$($env:POETRY_HOME)\bin")) {
    Write-Host "  - Poetry not found, installing ... "
    Install-Poetry
}

if (-not (Test-Path -PathType Leaf -Path "$($root_dir)\poetry.lock")) {
    Write-Host ">>> Installing virtual environment and creating lock."
} else {
    Write-Host ">>> Installing virtual environment from lock."
}
$startTime = [int][double]::Parse((Get-Date -UFormat %s))
& "$env:POETRY_HOME\bin\poetry" install --no-root --ansi
if ($LASTEXITCODE -ne 0) {
    Write-Host "!!! Poetry command failed."
    Set-Location -Path $current_dir
    Exit-WithCode 1
}
$endTime = [int][double]::Parse((Get-Date -UFormat %s))
Write-Host "All done in $( $endTime - $startTime ) secs."
Set-Location -Path $current_dir
Write-Host ">>> Virtual environment created."
