# UserLex

UserLex is a simple parser of human generated content. 
It is designed to be used in a variety of applications, including but not limited to:

* Chatbots
* Natural Language Processing
* Machine Learning
* Data Mining
* Data Analysis
* Data Visualization
* Data Collection

## Installation

Installation with `pip` is easiest:

```bash
pip install userlex
```

## Usage

```python
from userlex.social_media import SocialMedia
message = "Hey, my instagram is @userlex, and my twitter is @userlex_"
social_media = SocialMedia(message)
social_media.parse()
print(social_media.instagram)
print(social_media.twitter)
```
