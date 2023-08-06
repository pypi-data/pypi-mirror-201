# Filerobot 

The Filerobot class provides all the functionality of the Filerobot and all of it's APIs. 
The idea of the filerobot class is to be used in every scrips filerobot
related providing the functionality of the Filerobot in an easier way.

![alt text](https://blog.scaleflex.com/content/images/2021/05/SCALEFLEX-LOGO-HORIZONTAL.png)
## Installation

```bash
pip install filerobot
```

## Usage

```python
from filerobot.filerobot import Filerobot

filerobot = Filerobot('<filerobot token>', '<filerobot key>')
# Check if filerobot credentials is right
filerobot.check_and_set_filerobot_credentials()
```
## Functionality
1. Folders
- Create folder
- Get folder details
- List & search folders
- Rename folder
- Move folder
- Delete folder
2. Files
- List files
- Get file details
- Rename file
- Move file
- Delete file
- HTTP upload file
- Multipart upload file
- Pool upload file
3. Metadata 
- Get metadata fields
- Get details about metadata field


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)