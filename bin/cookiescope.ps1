# Copyright (C) 2023, Steven Cooper
#
# This file is part of Cookiescope.
#
# Cookiescope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cookiescope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cookiescope.  If not, see <https://www.gnu.org/licenses/>.

function Invoke-Cookiescope
{
    param(
        [string[]]$CommandLineArguments
    )

    Set-Location (Get-Item $PSScriptRoot).parent.FullName

    if (-not (Test-Path venv -PathType Container))
    {
        Write-Output "The virtual environment folder 'venv' does not exist."
        $response = Read-Host "Is it okay to create a new virtual environment in 'venv'?"
        if ($response -ne 'y')
        {
            Exit
        }
        Write-Output "Creating virtual environment 'venv' ..."
        python -m venv venv --system-site-packages
        venv\Scripts\python.exe -m pip install --upgrade pip
        venv\Scripts\python.exe -m pip install .
    }

    $env:PYTHONPATH="."
    venv\Scripts\python cookiescope\main.py @CommandLineArguments
}

Invoke-Cookiescope $args
