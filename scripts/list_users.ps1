# Ensure the script is run with administrative privileges
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script must be run as an administrator"
    exit 1
}

# Retrieve the list of local users
$users = Get-LocalUser | Select-Object Name, Enabled

# Create a hashtable to store the JSON data
$jsonObject = @{}

# Populate the hashtable with user data
foreach ($user in $users) {
    $jsonObject[$user.Name] = $user.Enabled
}

# Convert the hashtable to a JSON-formatted string
$json = $jsonObject | ConvertTo-Json -Depth 2 -Compress

# Output the JSON string
Write-Output $json
