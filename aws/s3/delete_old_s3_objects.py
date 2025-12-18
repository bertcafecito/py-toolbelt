"""
Script to delete S3 objects older than a specific date.

This script scans an S3 bucket (and optional prefix) and deletes objects
whose LastModified date is older than or equal to the specified cutoff date.

Usage:
    python delete_old_s3_objects.py --bucket my-bucket --date 2024-01-01
    python delete_old_s3_objects.py --bucket my-bucket --prefix folder/ --date 2024-06-15 --dry-run
"""

import argparse
import boto3
from datetime import datetime
from typing import List, Dict
import sys


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Delete S3 objects older than a specific date"
    )
    parser.add_argument("--bucket", required=True, help="S3 bucket name")
    parser.add_argument("--prefix", default="", help="S3 prefix/folder path (optional)")
    parser.add_argument(
        "--date",
        required=True,
        help="Cutoff date in YYYY-MM-DD format. Objects older than or equal to this date will be deleted.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be deleted without actually deleting",
    )
    parser.add_argument(
        "--region", default="us-east-1", help="AWS region (default: us-east-1)"
    )
    parser.add_argument("--profile", default=None, help="AWS profile name (optional)")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Number of objects to delete per batch (default: 1000, max: 1000)",
    )

    return parser.parse_args()


def parse_cutoff_date(date_string: str) -> datetime:
    """
    Parse the cutoff date string into a datetime object.

    Args:
        date_string: Date in YYYY-MM-DD format

    Returns:
        datetime object (timezone-aware UTC)
    """
    try:
        cutoff_date = datetime.strptime(date_string, "%Y-%m-%d")
        # Make it timezone-aware (UTC) for comparison with S3 LastModified
        return cutoff_date.replace(tzinfo=datetime.now().astimezone().tzinfo)
    except ValueError:
        raise ValueError(f"Invalid date format: {date_string}. Use YYYY-MM-DD format.")


def list_old_objects(
    s3_client, bucket: str, prefix: str, cutoff_date: datetime
) -> List[Dict]:
    """
    List all objects in the bucket/prefix that are older than the cutoff date.

    Args:
        s3_client: Boto3 S3 client
        bucket: S3 bucket name
        prefix: S3 prefix/folder path
        cutoff_date: Cutoff date (timezone-aware)

    Returns:
        List of objects to delete
    """
    objects_to_delete = []
    paginator = s3_client.get_paginator("list_objects_v2")

    print(f"Scanning bucket '{bucket}' with prefix '{prefix}'...")

    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)

    total_objects = 0
    for page in page_iterator:
        if "Contents" not in page:
            continue

        for obj in page["Contents"]:
            total_objects += 1
            last_modified = obj["LastModified"]

            # Compare dates (objects older than OR equal to cutoff date)
            if last_modified <= cutoff_date:
                objects_to_delete.append(
                    {
                        "Key": obj["Key"],
                        "LastModified": last_modified,
                        "Size": obj["Size"],
                    }
                )

    print(f"Total objects scanned: {total_objects}")
    print(
        f"Objects older than or equal to {cutoff_date.strftime('%Y-%m-%d')}: {len(objects_to_delete)}"
    )

    return objects_to_delete


def delete_objects(
    s3_client,
    bucket: str,
    objects: List[Dict],
    batch_size: int = 1000,
    dry_run: bool = False,
):
    """
    Delete objects from S3 in batches.

    Args:
        s3_client: Boto3 S3 client
        bucket: S3 bucket name
        objects: List of objects to delete
        batch_size: Number of objects to delete per batch (max 1000)
        dry_run: If True, only preview without deleting
    """
    if not objects:
        print("No objects to delete.")
        return

    # Calculate total size
    total_size_bytes = sum(obj["Size"] for obj in objects)
    total_size_mb = total_size_bytes / (1024 * 1024)
    total_size_gb = total_size_bytes / (1024 * 1024 * 1024)

    print(f"\n{'=' * 60}")
    print(f"Total objects to delete: {len(objects)}")
    if total_size_gb >= 1:
        print(f"Total size: {total_size_gb:.2f} GB")
    else:
        print(f"Total size: {total_size_mb:.2f} MB")
    print(f"{'=' * 60}\n")

    if dry_run:
        print("DRY RUN MODE - No objects will be deleted\n")
        print("Sample of objects that would be deleted (first 10):")
        for obj in objects[:10]:
            size_kb = obj["Size"] / 1024
            print(
                f"  - {obj['Key']} (Modified: {obj['LastModified']}, Size: {size_kb:.2f} KB)"
            )
        if len(objects) > 10:
            print(f"  ... and {len(objects) - 10} more objects")
        return

    # Confirm deletion
    confirmation = input(
        f"\nAre you sure you want to delete {len(objects)} objects? (yes/no): "
    )
    if confirmation.lower() != "yes":
        print("Deletion cancelled.")
        return

    # Delete in batches
    deleted_count = 0
    batch_size = min(batch_size, 1000)  # AWS limit is 1000 objects per delete request

    for i in range(0, len(objects), batch_size):
        batch = objects[i : i + batch_size]
        delete_keys = [{"Key": obj["Key"]} for obj in batch]

        try:
            response = s3_client.delete_objects(
                Bucket=bucket, Delete={"Objects": delete_keys}
            )

            deleted = len(response.get("Deleted", []))
            deleted_count += deleted

            print(
                f"Deleted {deleted} objects (Progress: {deleted_count}/{len(objects)})"
            )

            # Check for errors
            if "Errors" in response and response["Errors"]:
                print(f"Errors encountered in batch {i // batch_size + 1}:")
                for error in response["Errors"]:
                    print(f"  - {error['Key']}: {error['Message']}")

        except Exception as e:
            print(f"Error deleting batch {i // batch_size + 1}: {str(e)}")
            continue

    print(f"\nDeletion complete. Total objects deleted: {deleted_count}/{len(objects)}")


def main():
    """Main execution function."""
    args = parse_arguments()

    try:
        # Parse cutoff date
        cutoff_date = parse_cutoff_date(args.date)
        print(f"Cutoff date: {cutoff_date.strftime('%Y-%m-%d')}")
        print(
            f"Objects with LastModified <= {cutoff_date.strftime('%Y-%m-%d')} will be deleted.\n"
        )

        # Initialize S3 client
        session_kwargs = {"region_name": args.region}
        if args.profile:
            session_kwargs["profile_name"] = args.profile

        session = boto3.Session(**session_kwargs)
        s3_client = session.client("s3")

        # List old objects
        objects_to_delete = list_old_objects(
            s3_client, args.bucket, args.prefix, cutoff_date
        )

        # Delete objects
        delete_objects(
            s3_client, args.bucket, objects_to_delete, args.batch_size, args.dry_run
        )

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
