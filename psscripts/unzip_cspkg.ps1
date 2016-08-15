param(
  [Parameter(Mandatory=$True)]
  [string]
  $file,

  [Parameter(Mandatory=$True)]
  [string]
  $destination
)

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory($file, $destination)

