# Get a list of local users
$users = Get-LocalUser | Select-Object Name, Enabled, LastLogon

# Convert the list of users to JSON
$json = $users | ConvertTo-Json -Depth 2

# Output the JSON
$json
