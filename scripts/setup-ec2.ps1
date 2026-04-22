param(
    [Parameter(Mandatory = $true)]
    [string]$Ec2Host,

    [Parameter(Mandatory = $true)]
    [string]$KeyPath,

    [string]$User = "ubuntu",
    [string]$RepoUrl = "https://github.com/AbizerJesawada/solar-power-mlops.git",
    [string]$Branch = "main",
    [string]$RepoDir = "~/solar-power-mlops",
    [string]$ContainerName = "solar-app",
    [string]$ImageName = "solar-power-mlops",
    [int]$AppPort = 8501
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $KeyPath)) {
    throw "SSH private key not found at '$KeyPath'."
}

$resolvedKeyPath = (Resolve-Path -LiteralPath $KeyPath).Path
$remoteTarget = "$User@$Ec2Host"

$remoteScript = @"
set -e

sudo apt update
sudo apt install -y docker.io git
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $User || true

if [ ! -d "$RepoDir/.git" ]; then
  rm -rf "$RepoDir"
  git clone --branch "$Branch" "$RepoUrl" "$RepoDir"
fi

cd "$RepoDir"
git fetch origin "$Branch"
git checkout "$Branch"
git reset --hard "origin/$Branch"

sudo docker rm -f "$ContainerName" || true
sudo docker build -t "$ImageName" .
sudo docker run -d \
  --restart unless-stopped \
  -p ${AppPort}:8501 \
  --name "$ContainerName" \
  "$ImageName"

sudo docker container ls
"@

$remoteScript | ssh -i $resolvedKeyPath -o StrictHostKeyChecking=accept-new $remoteTarget "bash -s"
