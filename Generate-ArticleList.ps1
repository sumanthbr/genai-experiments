# Define a feed URL
$feedUrl = "https://thenewstack.io/feed/" # replace with your RSS feed URL

# Get feed and parse it into an XML document
$rss = Invoke-WebRequest -Uri $feedUrl
$feed = [xml]$rss.Content

# Get the current date and time
$currentTime = Get-Date

# Loop through all items in the feed
foreach ($item in $feed.rss.channel.item) {
    # Parse the publication date of the item
    $pubDate = Get-Date $item.pubDate
    
    # Check if the item was published within the last day
    if ($pubDate -ge $currentTime.AddDays(-1)) {
        # Output the item title
        Write-Host $item.title
        Write-Host $item.link
    }
}

# Define the connection string and container name for your Azure Blob Storage
$connectionString = "DefaultEndpointsProtocol=https;AccountName=<your-account-name>;AccountKey=<your-account-key>;EndpointSuffix=core.windows.net"
$containerName = "<your-container-name>"

# Define the local file path of the file you want to upload
$localFilePath = "C:\Path\To\Your\File.txt"

# Create a blob client using the connection string
$blobClient = [Microsoft.Azure.Storage.Blob.CloudBlobClient]::new($connectionString)

# Get a reference to the container
$container = $blobClient.GetContainerReference($containerName)

# Create a blob reference for the file
$blobName = [System.IO.Path]::GetFileName($localFilePath)
$blob = $container.GetBlockBlobReference($blobName)

# Upload the file to blob storage
$blob.UploadFromFile($localFilePath)

# Output the URL of the uploaded file
$blob.Uri.AbsoluteUri
