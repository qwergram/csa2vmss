param(
 [Parameter(Mandatory=$True)]
 [string]
 $zipfilename,

 [Parameter(Mandatory=$True)]
 [string]
 $sourcedir
)


Compress-Archive -Path $sourcedir -DestinationPath $zipfilename