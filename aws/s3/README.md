# Delete Old S3 Objects Script

This script deletes S3 objects older than or equal to a specified date based on their `LastModified` timestamp.

## Features

- ✅ Delete objects older than or equal to a specific date
- ✅ Support for bucket prefixes (folders)
- ✅ Dry-run mode to preview deletions
- ✅ Batch deletion (up to 1000 objects per batch)
- ✅ Progress tracking and error handling
- ✅ Size calculation and summary
- ✅ Confirmation prompt before deletion

## Requirements

```bash
pip install boto3
```

## Usage

### Basic Usage

Delete all objects in a bucket older than or equal to January 1, 2024:

```bash
python delete_old_s3_objects.py --bucket my-bucket --date 2024-01-01
```

### With Prefix (Folder)

Delete objects in a specific folder:

```bash
python delete_old_s3_objects.py --bucket my-bucket --prefix folder/subfolder/ --date 2024-06-15
```

### Dry Run (Preview)

Preview what would be deleted without actually deleting:

```bash
python delete_old_s3_objects.py --bucket my-bucket --date 2024-01-01 --dry-run
```

### With Custom AWS Profile

```bash
python delete_old_s3_objects.py --bucket my-bucket --date 2024-01-01 --profile my-aws-profile
```

### With Custom Region

```bash
python delete_old_s3_objects.py --bucket my-bucket --date 2024-01-01 --region us-west-2
```

## Command Line Arguments

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `--bucket` | Yes | S3 bucket name | - |
| `--date` | Yes | Cutoff date in YYYY-MM-DD format | - |
| `--prefix` | No | S3 prefix/folder path | Empty string |
| `--dry-run` | No | Preview mode (no actual deletion) | False |
| `--region` | No | AWS region | us-east-1 |
| `--profile` | No | AWS profile name | Default profile |
| `--batch-size` | No | Objects per batch (max 1000) | 1000 |

## How It Works

1. **Scan**: The script scans the specified S3 bucket and prefix for all objects
2. **Filter**: Compares each object's `LastModified` timestamp with the cutoff date
3. **Preview**: Shows the total count and size of objects to be deleted
4. **Confirm**: Asks for confirmation (unless in dry-run mode)
5. **Delete**: Deletes objects in batches of up to 1000 objects per API call

## Important Notes

- Objects with `LastModified` date **older than OR equal to** the specified date will be deleted
- The script uses the object's `LastModified` timestamp, not the object key or creation date
- Deletions are permanent and cannot be undone (unless versioning is enabled on the bucket)
- Always run with `--dry-run` first to preview what will be deleted
- Requires appropriate AWS credentials and IAM permissions

## Required AWS Permissions

The AWS user/role running this script needs the following S3 permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::your-bucket-name",
        "arn:aws:s3:::your-bucket-name/*"
      ]
    }
  ]
}
```

## Examples

### Example 1: Delete logs older than 90 days

```bash
# Calculate date 90 days ago and delete
python delete_old_s3_objects.py --bucket my-logs-bucket --prefix logs/ --date 2024-09-18
```

### Example 2: Clean up old backups

```bash
# First, preview
python delete_old_s3_objects.py --bucket backups --prefix daily/ --date 2024-01-01 --dry-run

# Then delete
python delete_old_s3_objects.py --bucket backups --prefix daily/ --date 2024-01-01
```

### Example 3: Delete all objects in a bucket older than a year

```bash
python delete_old_s3_objects.py --bucket archive-bucket --date 2023-12-18
```

## Error Handling

The script includes comprehensive error handling:
- Invalid date format validation
- Batch deletion error tracking
- Graceful handling of pagination issues
- Clear error messages for debugging

## Output Example

```
Cutoff date: 2024-01-01
Objects with LastModified <= 2024-01-01 will be deleted.

Scanning bucket 'my-bucket' with prefix 'logs/'...
Total objects scanned: 5000
Objects older than or equal to 2024-01-01: 1200

============================================================
Total objects to delete: 1200
Total size: 2.45 GB
============================================================

Are you sure you want to delete 1200 objects? (yes/no): yes
Deleted 1000 objects (Progress: 1000/1200)
Deleted 200 objects (Progress: 1200/1200)

Deletion complete. Total objects deleted: 1200/1200
```
