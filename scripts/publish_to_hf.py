"""Upload TokenAtlas Space and Dataset to Hugging Face."""

from pathlib import Path
from huggingface_hub import HfApi, whoami


def main():
    api = HfApi()
    user_info = whoami()
    username = user_info["name"]
    print(f"Authenticated as Hugging Face user: {username} ({user_info.get('fullname')})")

    root = Path(__file__).resolve().parent.parent

    # 1. Publish Space
    space_id = f"{username}/token-atlas"
    space_dir = root / "hf_space"
    print(f"\n[1/2] Creating and uploading Space: {space_id}...")
    api.create_repo(
        repo_id=space_id,
        repo_type="space",
        space_sdk="static",
        exist_ok=True,
    )
    api.upload_folder(
        folder_path=str(space_dir),
        repo_id=space_id,
        repo_type="space",
        commit_message="feat: publish TokenAtlas interactive web atlas v0.2.0",
    )
    print(f"✓ Space uploaded: https://huggingface.co/spaces/{space_id}")

    # 2. Publish Dataset
    dataset_id = f"{username}/token-atlas-benchmark"
    dataset_dir = root / "hf_dataset"
    print(f"\n[2/2] Creating and uploading Dataset: {dataset_id}...")
    api.create_repo(
        repo_id=dataset_id,
        repo_type="dataset",
        exist_ok=True,
    )
    api.upload_folder(
        folder_path=str(dataset_dir),
        repo_id=dataset_id,
        repo_type="dataset",
        commit_message="feat: upload TokenAtlas 52-language x 6-tokenizer FLORES-200 benchmark dataset",
    )
    print(f"✓ Dataset uploaded: https://huggingface.co/datasets/{dataset_id}")

    print("\n🎉 TokenAtlas successfully published to Hugging Face!")


if __name__ == "__main__":
    main()
