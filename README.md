# ELA photo check
Telegram bot for analysis any picture with Error Level Analysis (ELA) algorithm

# How it works
Error Level Analysis (ELA) permits identifying areas within an image that are at different compression levels. With JPEG images, the entire picture should be at roughly the same level. If a section of the image is at a significantly different error level, then it likely indicates a digital modification.

⚠ Note: send to bot picture as an uncompressed file for best results.
___
## Technologies and used frameworks
* Python
* aiogram - framework for Telegram Bot API


## Tasks for the project
- [X] Develop base working bot version
- [X] Implement commands for interact with bot (/help, /start, etc)
- [ ] Develop function to compress the final image
- [ ] Implement a mechanism for deleting temporary files after the analysis is completed and the file is sent to the user