param(
  [Parameter(Mandatory=$True)]
  [string]
  $target,

  [Parameter(Mandatory=$True)]
  [string]
  $destination
)

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory($target, $destination)
