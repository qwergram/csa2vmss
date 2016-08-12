import sys
import io

script = """
Write-Host "Downloading Zip file"
Invoke-WebRequest -Uri {} -OutFile contents.zip
"""


if __name__ == "__main__":
    url = sys.argv[1]
    with io.open("autogen.savezip.ps1", 'w') as handle:
        handle.write(script.format(url))
