import storage

if "{{ erase }}" == "yes":
    print("about to erase filesystem, including settings.toml")
    storage.erase_filesystem()
else:
    print("not erasing - run circremote DEVICE erase_fs yes to really erase")
    print("{{ erase }}")
