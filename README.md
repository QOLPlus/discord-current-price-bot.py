# Price Bot (Status Mode)

### 사용법

```bash
#!/usr/bin/zsh                                                                                                             
set -e                                                                                                                     
sudo docker run --rm \                                                                                                     
    -e INTERVAL=30 \                                                                                                       
    -e DISCORD_BOT_TOKEN="$PRICE_BOT_TOKEN_KAKAOPAY" \                                                                     
    -e SHORT_CODE=A377300 \                                                                                                
    -d \                                                                                                                   
    -it ghcr.io/qolplus/discord-current-price-bot.py:2021.12.11-3
```
